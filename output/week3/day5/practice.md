# Week 3 Day 5 실습 가이드

## ⚠️ 필수 사전 준비

> **🚨 중요:** 실습을 시작하기 전에 반드시 아래 가이드를 먼저 완료하세요!

### 📚 필수 선행 문서
실습을 시작하기 전에 다음 문서들을 **반드시** 먼저 읽고 완료하세요:

| 문서 | 설명 | 필수 여부 |
|-----|------|----------|
| [AWS 계정 생성 가이드](../prerequisites/aws-account-setup.md) | AWS 계정이 없다면 이 가이드를 따라 계정을 생성하세요 | ✅ 필수 |
| [AWS CLI 설치 가이드](../prerequisites/aws-cli-setup.md) | AWS CLI 설치 및 설정 방법 | ✅ 필수 |
| [IAM 사용자 생성 가이드](../prerequisites/iam-user-setup.md) | 실습용 IAM 사용자 생성 방법 | ✅ 필수 |
| [VS Code 설정 가이드](../prerequisites/vscode-setup.md) | 개발 환경 설정 (선택) | 선택 |

### ✅ 사전 체크리스트
실습을 시작하기 전 아래 항목들을 모두 확인하세요:

- [ ] AWS 계정이 있고 로그인할 수 있다
- [ ] AWS CLI가 설치되어 있다 (`aws --version` 으로 확인)
- [ ] AWS CLI 자격 증명이 설정되어 있다 (`aws sts get-caller-identity` 로 확인)
- [ ] 실습에 필요한 IAM 권한이 있다
- [ ] 결제 알림이 설정되어 있다 (예상치 못한 비용 방지)

```bash
# 사전 준비 확인 명령어
aws --version
aws sts get-caller-identity
```

> **⚠️ 주의:** 위 체크리스트가 모두 완료되지 않았다면 실습을 진행하지 마세요!
> 문제 발생 시 해결이 어려울 수 있습니다.

---

## 🎯 실습 목표
이 실습을 완료하면 다음을 할 수 있습니다:
- [ ] Step Functions 상태 머신을 생성하고 테스트할 수 있다
- [ ] EventBridge 규칙을 생성하여 이벤트를 처리할 수 있다
- [ ] SQS 표준/FIFO 큐를 생성하고 메시지 전달을 테스트할 수 있다
- [ ] SNS 토픽을 생성하고 구독자를 추가할 수 있다
- [ ] Kinesis Data Streams를 생성하고 데이터 인그레션을 테스트할 수 있다

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분
- Step 1: 약 10분
- Step 2: 약 15분
- Step 3: 약 10분
- 리소스 정리: 약 5분

---

## 📝 실습 단계

### Step 1: Step Functions 상태 머신 생성 (약 10분)

#### 1.1 Step Functions 상태 머신 정의 파일 생성
```json
{
  "Comment": "A simple state machine that processes an input",
  "StartAt": "Hello",
  "States": {
    "Hello": {
      "Type": "Succeed",
      "End": true
    }
  }
}
```

**예상 출력:**
```
{"Comment": "A simple state machine that processes an input", "StartAt": "Hello", "States": {"Hello": {"Type": "Succeed", "End": true}}}
```

> **💡 설명:** 이 JSON 파일은 상태 머신의 기본 구조를 정의합니다. `Succeed` 상태는 작업이 성공적으로 완료되었음을 나타냅니다.

#### 1.2 Step Functions 상태 머신 생성 (CLI)
```bash
aws stepfunctions create-state-machine \
  --name "MyFirstStateMachine" \
  --definition file://state-machine.json \
  --role-arn "arn:aws:iam::<ACCOUNT_ID>:role/lambda-role"
```

**예상 출력:**
```
{
  "stateMachineArn": "arn:aws:states:us-east-1:<ACCOUNT_ID>:stateMachine:MyFirstStateMachine"
}
```

> **💡 설명:** `--role-arn`은 Lambda 실행 역할을 지정합니다. IAM 역할이 없는 경우, 먼저 Lambda 역할을 생성해야 합니다.

#### 1.3 상태 머신 테스트 (CLI)
```bash
aws stepfunctions start-execution \
  --state-machine-arn "arn:aws:states:us-east-1:<ACCOUNT_ID>:stateMachine:MyFirstStateMachine" \
  --input "{}"
```

**예상 출력:**
```
{
  "executionArn": "arn:aws:states:us-east-1:<ACCOUNT_ID>:execution:MyFirstStateMachine:1",
  "startDate": "2023-10-01T12:00:00.000Z"
}
```

> **📸 화면 확인:** AWS 콘솔에서 **Step Functions** 서비스 > **State machines** 탭에서 생성된 상태 머신이 표시되는지 확인하세요.

#### ✅ Step 1 완료 확인
- [ ] 상태 머신이 성공적으로 생성되었다
- [ ] 실행이 성공적으로 완료되었다

---

### Step 2: EventBridge 이벤트 처리 (약 15분)

#### 2.1 EventBridge 규칙 생성 (CLI)
```bash
aws events put-rule \
  --name "MyFirstRule" \
  --schedule-expression "rate(5 minutes)"
```

**예상 출력:**
```
{
  "RuleArn": "arn:aws:events:us-east-1:<ACCOUNT_ID>:rule/MyFirstRule"
}
```

> **💡 설명:** `rate(5 minutes)`는 매 5분마다 이벤트를 발생시킵니다.

#### 2.2 EventBridge 규칙에 Step Functions 연결 (CLI)
```bash
aws events put-targets \
  --rule "MyFirstRule" \
  --targets "Id":"1","Arn":"arn:aws:states:us-east-1:<ACCOUNT_ID>:stateMachine:MyFirstStateMachine"
```

**예상 출력:**
```
{
  "FailedEntries": [],
  "SuccessfulEntries": [
    {
      "Id": "1",
      "TargetArn": "arn:aws:states:us-east-1:<ACCOUNT_ID>:stateMachine:MyFirstStateMachine"
    }
  ]
}
```

> **📸 화면 확인:** AWS 콘솔에서 **EventBridge** 서비스 > **Rules** 탭에서 생성된 규칙이 표시되는지 확인하세요.

#### 2.3 이벤트 발생 확인 (CLI)
```bash
aws events list-rules
```

**예상 출력:**
```
{
  "Rules": [
    {
      "Arn": "arn:aws:events:us-east-1:<ACCOUNT_ID>:rule/MyFirstRule",
      "Name": "MyFirstRule",
      "ScheduleExpression": "rate(5 minutes)"
    }
  ]
}
```

#### ✅ Step 2 완료 확인
- [ ] EventBridge 규칙이 생성되었다
- [ ] Step Functions가 규칙에 연결되었다

---

### Step 3: SQS/SNS 통합 (약 10분)

#### 3.1 SQS 표준 큐 생성 (CLI)
```bash
aws sqs create-queue \
  --queue-name "MyStandardQueue" \
  --region us-east-1
```

**예상 출력:**
```
{
  "QueueUrl": "https://sqs.us-east-1.amazonaws.com/<ACCOUNT_ID>/MyStandardQueue"
}
```

> **💡 설명:** 표준 큐는 메시지 순서 보장이 없으며, 메시지 중복이 발생할 수 있습니다.

#### 3.2 SNS 토픽 생성 및 SQS 구독 설정 (CLI)
```bash
aws sns create-topic --name "MySnsTopic"
aws sns subscribe --topic-arn "arn:aws:sns:us-east-1:<ACCOUNT_ID>:MySnsTopic" --protocol sqs --queue-arn "https://sqs.us-east-1.amazonaws.com/<ACCOUNT_ID>/MyStandardQueue"
```

**예상 출력:**
```
{
  "SubscriptionArn": "arn:aws:sns:us-east-1:<ACCOUNT_ID>:MySnsTopic:1234567890abcdef"
}
```

#### 3.3 메시지 전송 테스트 (CLI)
```bash
aws sns publish --topic-arn "arn:aws:sns:us-east-1:<ACCOUNT_ID>:MySnsTopic" --message "Hello SQS!"
```

**예상 출력:**
```
{
  "MessageId": "12345678-1234-1234-1234-123456789012"
}
```

> **📸 화면 확인:** AWS 콘솔에서 **SQS** 서비스 > **Queues** 탭에서 메시지가 수신되는지 확인하세요.

#### ✅ Step 3 완료 확인
- [ ] SQS 표준 큐가 생성되었다
- [ ] SNS 토픽과 SQS의 연결이 완료되었다

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] Step Functions 상태 머신이 생성되었다
- [ ] EventBridge 규칙이 생성되고 Step Functions에 연결되었다
- [ ] SQS 표준 큐와 SNS 토픽이 연결되었다
- [ ] 메시지 전송이 성공적으로 이루어졌다

### 예상 최종 결과
```bash
# 상태 머신 실행 확인
aws stepfunctions list-state-machines
```

**예상 출력:**
```
{
  "stateMachines": [
    {
      "name": "MyFirstStateMachine",
      "stateMachineArn": "arn:aws:states:us-east-1:<ACCOUNT_ID>:stateMachine:MyFirstStateMachine"
    }
  ]
}
```

---

## 🔧 트러블슈팅

### 문제 1: `AccessDenied` 오류
**증상:** `AccessDenied` 오류 발생
**원인:** IAM 사용자에게 필요한 권한이 부족합니다.
**해결 방법:**
1. IAM 사용자에게 `AWSStepFunctionsFullAccess` 정책 추가
2. `aws sts get-caller-identity`로 사용자 확인

### 문제 2: CLI 명령어 문법 오류
**증상:** `InvalidParameter` 오류 발생
**원인:** JSON 파일 또는 CLI 파라미터 오류
**해결 방법:**
1. JSON 파일의 문법을 다시 확인하세요
2. `--input` 파라미터를 올바르게 입력하세요

### 문제 3: 리소스 생성 실패
**증상:** `ResourceAlreadyExists` 오류
**원인:** 동일한 이름의 리소스가 이미 존재합니다.
**해결 방법:**
1. 다른 이름을 사용하여 리소스를 생성하세요
2. `aws <service> list-<resource>`로 기존 리소스 확인

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] Step Functions 상태 머신
- [ ] EventBridge 규칙
- [ ] SQS 표준 큐
- [ ] SNS 토픽

### 리소스 정리 명령어
```bash
# 1. Step Functions 상태 머신 삭제
aws stepfunctions delete-state-machine --state-machine-arn "arn:aws:states:us-east-1:<ACCOUNT_ID>:stateMachine:MyFirstStateMachine"

# 2. EventBridge 규칙 삭제
aws events delete-rule --name "MyFirstRule"

# 3. SQS 큐 삭제
aws sqs delete-queue --queue-url "https://sqs.us-east-1.amazonaws.com/<ACCOUNT_ID>/MyStandardQueue"

# 4. SNS 토픽 삭제
aws sns delete-topic --topic-arn "arn:aws:sns:us-east-1:<ACCOUNT_ID>:MySnsTopic"
```

### 정리 완료 확인
```bash
# 리소스가 모두 삭제되었는지 확인
aws stepfunctions list-state-machines
aws events list-rules
aws sqs list-queues
aws sns list-topics
```

---

## 📚 추가 학습 자료
- [AWS Step Functions 공식 문서](https://docs.aws.amazon.com/step-functions/)
- [EventBridge 이벤트 패턴 가이드](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-patterns.html)
- [SQS FIFO 큐 설정 가이드](https://docs.aws.amazon.com/sqs/latest/developerguide/fifo-queues.html)
- [Kinesis Data Streams 시작 가이드](https://docs.aws.amazon.com/streams/latest/dev/what-is-stream-processing.html)