# Week 4 Day 5 실습 가이드

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
- [ ] **CloudFormation 스택 생성** (기본 리소스 생성)
- [ ] **CDK를 활용한 인프라 정의** (TypeScript로 스택 정의)
- [ ] **Systems Manager 사용법 익히기** (State Manager 설정)

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분
- Step 1: 약 10분
- Step 2: 약 15분
- Step 3: 약 10분
- 리소스 정리: 약 5분

---

## 📝 실습 단계

### Step 1: CloudFormation 스택 생성 (약 10분)

#### 1.1 CloudFormation 스택 생성
```bash
# EC2 인스턴스 생성용 템플릿 생성
aws cloudformation create-stack --stack-name my-first-stack \
--template-body file://cloudformation.yaml \
--capabilities CAPABILITY_IAM
```

**예상 출력:**
```
{
  "StackId": "arn:aws:cloudformation:region:account-id:stack/my-first-stack/uuid"
}
```

> **💡 설명:** `cloudformation.yaml` 파일을 통해 EC2 인스턴스와 보안 그룹을 생성합니다. `CAPABILITY_IAM` 권한이 필요합니다.

#### 1.2 AWS 콘솔에서 스택 확인
1. [AWS Management Console](https://console.aws.amazon.com/cloudformation/) 접속
2. "my-first-stack" 검색
3. "CREATE_COMPLETE" 상태 확인

> **📸 화면 확인:** EC2 인스턴스가 생성된 리소스 목록이 보이면 정상입니다.

#### ✅ Step 1 완료 확인
- [ ] CloudFormation 스택 생성 완료
- [ ] EC2 인스턴스 생성 완료

---

### Step 2: CDK로 인프라 정의 (약 15분)

#### 2.1 CDK 환경 설정
```bash
# CDK 설치
npm install -g aws-cdk

# 프로젝트 생성
mkdir cdk-demo && cd cdk-demo
cdk init --language typescript
```

#### 2.2 TypeScript로 스택 정의
```typescript
// lib/cdk-demo-stack.ts
import * as cdk from 'aws-cdk-lib';
import { Vpc, Instance, InstanceType, MachineImage } from 'aws-cdk-lib';

export class CdkDemoStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new Vpc(this, 'MyVpc', {
      maxAzs: 2,
      vpnGateway: false
    });

    new Instance(this, 'MyInstance', {
      vpc,
      instanceType: InstanceType.of(InstanceType.TYPE_T2_MICRO),
      machineImage: MachineImage.latestAmazonLinux()
    });
  }
}
```

#### 2.3 스택 배포
```bash
# 스택 배포
cdk deploy
```

> **💡 설명:** CDK는 자동으로 AWS 리소스를 생성하고, 변경 사항을 추적합니다. `cdk destroy`로 리소스를 삭제할 수 있습니다.

#### ✅ Step 2 완료 확인
- [ ] CDK 프로젝트 생성 완료
- [ ] EC2 인스턴스 생성 완료

---

### Step 3: Systems Manager 사용 (약 10분)

#### 3.1 State Manager 문서 생성
```bash
# State Manager 문서 생성
aws ssm create-document --name "MyCustomDocument" \
--content file://state-manager.json
```

**state-manager.json 예시:**
```json
{
  "schemaVersion": "2.2",
  "description": "Sample State Manager document",
  "formatVersion": "2.2",
  "parameters": {
    "InstanceId": {
      "type": "String"
    }
  },
  "mainSteps": [
    {
      "action": "runCommand",
      "name": "RunCommand",
      "inputs": {
        "commands": ["echo 'Hello from State Manager!'"],
        "target": [{"key": "InstanceIds", "value": ["${InstanceId}"]}]
      }
    }
  ]
}
```

#### 3.2 인스턴스 관리
```bash
# 인스턴스 ID 확인
aws ec2 describe-instances --query "Reservations[].Instances[].InstanceId"
```

#### 3.3 명령 실행
```bash
# State Manager 명령 실행
aws ssm send-command --document-name "MyCustomDocument" \
--parameters '{"InstanceId": ["i-1234567890abcdef0"]}'
```

> **📸 화면 확인:** SSM Command Center에서 명령 실행 결과를 확인할 수 있습니다.

#### ✅ Step 3 완료 확인
- [ ] State Manager 문서 생성 완료
- [ ] 인스턴스에 명령 실행 완료

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] CloudFormation 스택 생성 완료
- [ ] CDK로 인프라 정의 완료
- [ ] Systems Manager 사용 완료

### 예상 최종 결과
```bash
# 리소스 확인
aws ec2 describe-instances
aws cloudformation list-stacks
aws ssm list-commands
```

**예상 출력:**
```
{
  "Stacks": [
    {
      "StackId": "arn:aws:cloudformation:region:account-id:stack/my-first-stack/uuid"
    }
  ]
}
```

---

## 🔧 트러블슈팅

### 문제 1: `ValidationError: Template error: the length of the template is 0`
**증상:** 템플릿 파일이 누락된 경우  
**원인:** `cloudformation.yaml` 파일이 존재하지 않음  
**해결 방법:**
```bash
# 템플릿 파일 생성
echo "AWSTemplateFormatVersion: '2010-09-09'
Resources:
  MyEC2:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t2.micro
      ImageId: ami-0c55b159cbfafe1f0
      SecurityGroupIds:
        - !Ref MySecurityGroup" > cloudformation.yaml
```

### 문제 2: 권한 오류 (AccessDenied)
**증상:** `AccessDenied` 오류 발생  
**해결 방법:**
1. IAM 사용자 권한 확인
2. `AmazonEC2FullAccess` 및 `CloudFormationFullAccess` 정책 추가
```bash
# 권한 확인
aws iam get-user
```

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] CloudFormation 스택 (`my-first-stack`)
- [ ] CDK 배포된 인스턴스
- [ ] SSM 문서 및 명령

### 리소스 정리 명령어
```bash
# 1. CloudFormation 스택 삭제
aws cloudformation delete-stack --stack-name my-first-stack

# 2. CDK 리소스 삭제
cdk destroy

# 3. SSM 문서 삭제
aws ssm delete-document --document-name "MyCustomDocument"
```

### 정리 완료 확인
```bash
# 리소스 삭제 확인
aws cloudformation list-stacks
aws ssm list-documents
```

---

## 📚 추가 학습 자료
- [AWS CloudFormation 공식 문서](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
- [AWS CDK 튜토리얼](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
- [Systems Manager 사용 가이드](https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-ssm.html)
- [Well-Architected Framework 가이드](https://aws.amazon.com/architecture/well-architected/)