# Week 1 Day 1 실습 가이드

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
- [ ] AWS 리전/Availability Zone(AZ) 및 Edge Location 구성
- [ ] IAM 사용자, 그룹, 역할 생성 및 정책 적용
- [ ] MFA 및 AWS Organizations 설정

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분
- Step 1: 약 10분
- Step 2: 약 15분
- Step 3: 약 10분
- 리소스 정리: 약 5분

---

## 📝 실습 단계

### Step 1: AWS 글로벌 인프라스트럭처 구성 (약 10분)

#### 1.1 리전 및 AZ 확인
**AWS CLI 명령어:**
```bash
# 현재 리전 목록 확인
aws ec2 describe-regions --output table
```

**예상 출력:**
```
| RegionName      | RegionARN                                  |
|-----------------|--------------------------------------------|
| us-east-1       | arn:aws:ec2:us-east-1:123456789012:region  |
| eu-west-1       | arn:aws:ec2:eu-west-1:123456789012:region  |
```

> **💡 설명:** `describe-regions` 명령어는 AWS에서 제공하는 모든 리전을 목록화합니다.  
> `--output table` 옵션으로 테이블 형식으로 결과를 확인할 수 있습니다.

#### 1.2 리전 내 AZ 확인
**AWS CLI 명령어:**
```bash
# 특정 리전의 AZ 목록 확인 (예: us-east-1)
aws ec2 describe-availability-zones --region us-east-1 --output table
```

**예상 출력:**
```
| AvailabilityZoneId | RegionName | ZoneState | 
|--------------------|------------|----------|
| us-east-1a         | us-east-1  | available |
| us-east-1b         | us-east-1  | available |
```

> **📸 화면 확인:** AWS 콘솔에서 [리전 선택] → [AZ 목록] 항목을 확인하면 동일한 결과를 볼 수 있습니다.

#### ✅ Step 1 완료 확인
다음이 보이면 Step 1이 완료된 것입니다:
- [ ] CLI로 리전 목록 확인 성공
- [ ] CLI로 특정 리전의 AZ 목록 확인 성공

---

### Step 2: IAM 사용자/역할/정책 설정 (약 15분)

#### 2.1 IAM 사용자 생성
**AWS CLI 명령어:**
```bash
# 사용자 생성
aws iam create-user --user-name DevOpsUser
```

**예상 출력:**
```
{
    "User": {
        "UserName": "DevOpsUser",
        "UserId": "AIDAIQZ4J23J5Z6789012",
        "Arn": "arn:aws:iam::123456789012:user/DevOpsUser"
    }
}
```

> **💡 설명:** `create-user` 명령어로 IAM 사용자를 생성합니다.  
> 생성된 사용자의 ARN은 권한 설정 시 필요합니다.

#### 2.2 IAM 그룹 생성 및 사용자 추가
**AWS CLI 명령어:**
```bash
# 그룹 생성
aws iam create-group --group-name DevOpsGroup

# 사용자 그룹에 추가
aws iam add-user-to-group --user-name DevOpsUser --group-name DevOpsGroup
```

> **📸 화면 확인:** AWS 콘솔에서 [IAM] → [그룹] → [DevOpsGroup] → [사용자 추가]를 통해 확인할 수 있습니다.

#### 2.3 IAM 역할 생성
**AWS CLI 명령어:**
```bash
# 역할 생성 (EC2 권한 부여)
aws iam create-role --role-name EC2InstanceRole --assume-role-policy-document file://trust-policy.json
```

**trust-policy.json 파일 예시:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "ec2.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

> **💡 설명:** 역할은 EC2 인스턴스가 AWS 서비스를 호출할 수 있도록 권한을 부여합니다.

#### ✅ Step 2 완료 확인
다음이 보이면 Step 2가 완료된 것입니다:
- [ ] 사용자 생성 및 그룹 추가 성공
- [ ] 역할 생성 및 Trust Policy 설정 성공

---

### Step 3: IAM 정책 및 MFA 설정 (약 10분)

#### 3.1 IAM 정책 생성
**AWS CLI 명령어:**
```bash
# 정책 생성 (S3 접근 권한)
aws iam create-policy --policy-name S3AccessPolicy --policy-document file://s3-policy.json
```

**s3-policy.json 파일 예시:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "*"
    }
  ]
}
```

> **💡 설명:** 정책은 특정 서비스에 대한 접근 권한을 정의합니다.  
> `Inline Policy`와 `Managed Policy` 두 가지 유형이 있습니다.

#### 3.2 정책 연결 및 MFA 설정
**AWS CLI 명령어:**
```bash
# 사용자에게 정책 연결
aws iam attach-user-policy --user-name DevOpsUser --policy-arn arn:aws:iam::123456789012:policy/S3AccessPolicy

# MFA 설정 (예: Google Authenticator)
aws iam enable-mfa --user-name DevOpsUser --serial-number arn:aws:iam::123456789012:mfa/DevOpsUser --authentication-code-1 123456 --authentication-code-2 654321
```

> **📸 화면 확인:** AWS 콘솔에서 [IAM] → [사용자] → [DevOpsUser] → [MFA 설정]을 확인합니다.

#### ✅ Step 3 완료 확인
다음이 보이면 Step 3가 완료된 것입니다:
- [ ] 정책 생성 및 연결 성공
- [ ] MFA 설정 성공

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] AWS 리전/AVZ 목록 확인
- [ ] IAM 사용자/그룹/역할 생성
- [ ] IAM 정책 및 MFA 설정

### 예상 최종 결과
```bash
# 최종 상태 확인
aws iam get-user
aws ec2 describe-regions
```

**예상 출력:**
```
{
    "User": {
        "UserName": "DevOpsUser",
        "UserId": "AIDAIQZ4J23J5Z6789012",
        "Arn": "arn:aws:iam::123456789012:user/DevOpsUser"
    }
}
```

---

## 🔧 트러블슈팅

### 문제 1: `AccessDenied` 오류
**증상:** `AccessDenied` 또는 `UnauthorizedAccess` 오류 발생

**원인:** IAM 사용자 권한 부족 또는 정책 연결 누락

**해결 방법:**
1. IAM 사용자 권한 확인
2. 필요한 정책 연결
```bash
# 현재 사용자 권한 확인
aws sts get-caller-identity
```

### 문제 2: CLI 명령어 오류
**증상:** `InvalidParameter` 오류 발생

**원인:** JSON 파일 경로 오류 또는 형식 불일치

**해결 방법:**
- JSON 파일 경로를 정확히 지정
- `file://` 프로토콜 사용

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!  
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] IAM 사용자 (DevOpsUser)
- [ ] IAM 그룹 (DevOpsGroup)
- [ ] IAM 역할 (EC2InstanceRole)
- [ ] IAM 정책 (S3AccessPolicy)

### 리소스 정리 명령어
```bash
# 1. 사용자 삭제
aws iam delete-user --user-name DevOpsUser

# 2. 정책 삭제
aws iam delete-policy --policy-arn arn:aws:iam::123456789012:policy/S3AccessPolicy

# 3. 정리 확인
aws iam list-users
aws iam list-policies
```

### 정리 완료 확인
```bash
# 리소스가 모두 삭제되었는지 확인
aws iam list-users
aws iam list-policies
```

---

## 📚 추가 학습 자료
- [AWS Global Infrastructure 문서](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html)
- [IAM 사용자 가이드](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html)
- [AWS Organizations 소개](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html)