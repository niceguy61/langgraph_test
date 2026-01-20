# Week 3 Day 4 실습 가이드

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
- [ ] Lambda 함수를 AWS SAM을 사용해 생성하고 실행
- [ ] API Gateway를 통해 Lambda 함수를 호출하는 REST API를 배포
- [ ] Lambda 계층을 사용해 공통 라이브러리를 관리

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분
- Step 1: 약 10분
- Step 2: 약 15분
- Step 3: 약 10분
- 리소스 정리: 약 5분

---

## 📝 실습 단계

### Step 1: Lambda 함수 생성 (약 10분)

#### 1.1 AWS SAM CLI로 Lambda 함수 생성
**AWS CLI 명령어:**
```bash
sam init --runtime python3.10 --template AWS_Serverless_Application_Model
```

**예상 출력:**
```
Initialized project in directory my-sam-app
```

> **💡 설명:** `sam init` 명령어는 기본 템플릿을 기반으로 Lambda 함수 프로젝트를 생성합니다. Python 3.10 런타임을 선택했으며, 이는 AWS Lambda에서 지원하는 최신 런타임입니다.

#### 1.2 Lambda 함수 코드 수정
**VS Code에서 `lambda_function.py` 파일 열기:**
```python
import json

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello from Lambda!"})
    }
```

**AWS 콘솔에서:**
1. 서비스 검색창에 `Lambda` 입력
2. Lambda 서비스 클릭
3. "Functions" 탭에서 생성된 함수 이름 확인
4. "Test" 버튼 클릭 후 기본 테스트 이벤트 실행

> **📸 화면 확인:** Lambda 함수의 "Test" 탭에서 "Hello from Lambda!" 메시지가 반환되면 정상입니다.

#### ✅ Step 1 완료 확인
- [ ] AWS SAM CLI로 프로젝트 생성 완료
- [ ] Lambda 함수 코드 수정 및 테스트 성공

---

### Step 2: API Gateway 연동 및 배포 (약 15분)

#### 2.1 API Gateway 생성 및 Lambda 연결
**AWS CLI 명령어:**
```bash
sam deploy --guided
```

**예상 출력:**
```
INFO: Waiting for changes to propagate...
INFO: Deployment successful!
```

> **💡 설명:** `sam deploy` 명령어는 AWS SAM의 정의 파일(`template.yaml`)을 기반으로 리소스를 배포합니다. 이 과정에서 Lambda 함수가 API Gateway REST API로 배포됩니다.

#### 2.2 API Gateway URL 확인
**AWS 콘솔에서:**
1. 서비스 검색창에 `API Gateway` 입력
2. API Gateway 서비스 클릭
3. "Create API" 탭에서 생성된 API 이름 확인
4. "Stages" 탭에서 "Prod" 스테이지 URL 복사

> **📸 화면 확인:** "Invoke URL"이 표시되면 정상입니다. 이 URL은 HTTP 요청을 Lambda 함수로 전달합니다.

#### 2.3 REST API 테스트
**curl 명령어:**
```bash
curl -X GET https://<API_GATEWAY_URL>/prod/anything
```

**예상 출력:**
```
{"statusCode":200,"body":"{\"message\": \"Hello from Lambda!\"}"}
```

> **💡 설명:** `curl` 명령어로 API Gateway를 호출하면 Lambda 함수가 실행되고, JSON 형식의 응답을 반환합니다.

#### ✅ Step 2 완료 확인
- [ ] API Gateway 배포 성공
- [ ] REST API 테스트 성공

---

### Step 3: Lambda 계층 적용 (약 10분)

#### 3.1 Lambda 계층 생성
**AWS CLI 명령어:**
```bash
aws lambda publish-layer-version --layer-name my-python-layer --description "Custom Python library" --content S3Bucket=my-bucket,S3Key=my-layer.zip
```

**예상 출력:**
```
{
    "layerVersionArn": "arn:aws:lambda:region:account:layer:my-python-layer:1"
}
```

> **💡 설명:** `publish-layer-version` 명령어는 S3 버킷에서 ZIP 파일을 가져와 Lambda 계층을 생성합니다. 이 계층은 Lambda 함수에 공통 라이브러리를 공유할 수 있습니다.

#### 3.2 Lambda 함수에 계층 연결
**AWS 콘솔에서:**
1. Lambda 서비스 이동
2. 생성된 함수 클릭
3. "Configuration" 탭에서 "Layers" 선택
4. "Add layer" 버튼 클릭
5. 생성된 계층 선택 후 저장

> **📸 화면 확인:** "Layers" 탭에서 생성된 계층이 표시되면 정상입니다.

#### ✅ Step 3 완료 확인
- [ ] Lambda 계층 생성 및 연결 성공

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] Lambda 함수가 정상적으로 실행됨
- [ ] API Gateway를 통해 Lambda 호출 성공
- [ ] Lambda 계층이 성공적으로 연결됨

### 예상 최종 결과
```bash
# Lambda 함수 실행 결과
aws lambda invoke --function-name my-function --payload '{"key": "value"}' response.json
```

**예상 출력:**
```
{"statusCode":200,"body":"{\"key\": \"value\"}"}
```

---

## 🔧 트러블슈팅

### 문제 1: "No such function" 오류
**증상:** `aws lambda invoke` 명령어 실행 시 "No such function" 오류 발생

**원인:** Lambda 함수 이름 또는 버전이 잘못 입력되었거나, 함수가 배포되지 않았습니다.

**해결 방법:**
1. `sam deploy --guided` 명령어로 다시 배포
2. `aws lambda list-functions` 명령어로 함수 목록 확인

### 문제 2: "AccessDenied" 오류
**증상:** `aws lambda invoke` 명령어 실행 시 "AccessDenied" 오류 발생

**해결 방법:**
1. IAM 사용자 권한 확인
2. `AWSLambdaBasicExecutionRole` 정책 연결

```bash
# 현재 사용자 권한 확인
aws sts get-caller-identity
```

### 문제 3: API Gateway URL 오류
**증상:** "Invalid endpoint" 또는 "404 Not Found" 오류 발생

**해결 방법:**
1. API Gateway 서비스 이동
2. "Stages" 탭에서 "Prod" 스테이지 URL 확인
3. `curl` 명령어로 URL 재검증

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] Lambda 함수
- [ ] API Gateway
- [ ] Lambda 계층

### 리소스 정리 명령어
```bash
# 1. Lambda 함수 삭제
aws lambda delete-function --function-name my-function

# 2. API Gateway 삭제
aws apigateway delete-rest-api --rest-api-id <API_ID>

# 3. Lambda 계층 삭제
aws lambda delete-layer-version --layer-name my-python-layer --version 1
```

### 정리 완료 확인
```bash
# 리소스가 모두 삭제되었는지 확인
aws lambda list-functions
aws apigateway get-rest-apis
```

---

## 📚 추가 학습 자료
- [AWS Lambda 개발자 가이드](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [API Gateway REST API 문서](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-what-is-api-gateway.html)
- [AWS SAM 사용 가이드](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)