# Week 4 Day 2 실습 가이드

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
- [ ] KMS CMK 생성 및 암호화 키 관리
- [ ] 봉투 암호화(Envelope Encryption) 구현
- [ ] Secrets Manager 자동 교체 정책 설정

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분
- Step 1: 약 10분
- Step 2: 약 15분
- Step 3: 약 10분
- 리소스 정리: 약 5분

---

## 📝 실습 단계

### Step 1: KMS CMK 생성 및 관리 (약 10분)

#### 1.1 KMS CMK 생성
**AWS CLI 명령어:**
```bash
aws kms create-key --description "My CMK for encryption"
```

**예상 출력:**
```
{
    "keyMetadata": {
        "arn": "arn:aws:kms:region:account-id:key/key-id",
        "creationDate": 1625092800,
        "description": "My CMK for encryption",
        "enabled": true,
        "keyId": "key-id",
        "keyManager": "AWS",
        "keyState": "Enabled",
        "primaryKey": true,
        "tags": [],
        "validTo": 1656628800
    }
}
```

> **💡 설명:** `create-key` 명령어는 AWS KMS에 CMK를 생성합니다. 생성된 CMK의 ARN은 암호화 작업에 필요합니다.  
> **⚠️ 주의:** 생성된 CMK는 자동으로 활성화됩니다. 비활성화 시 암호화 작업이 실패합니다.

**AWS 콘솔에서:**
1. 서비스 검색창에서 "KMS" 입력 후 클릭
2. "Keys" 탭에서 생성된 CMK 확인
3. "Key details" 섹션에서 ARN과 상태 확인

> **📸 화면 확인:** 생성된 CMK의 "Enabled" 상태와 설명이 "My CMK for encryption"로 설정되었는지 확인

#### 1.2 CMK 권한 설정
**AWS CLI 명령어:**
```bash
aws kms put-key-policy --key-id arn:aws:kms:region:account-id:key/key-id --policy-permissions "['{ \"Effect\": \"Allow\", \"Principal\": { \"AWS\": \"arn:aws:iam::account-id:root\" }, \"Action\": \"kms:Encrypt\" }']"
```

**예상 출력:**
```
{
    "keyPolicy": {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "Allow use of the key",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::account-id:root"
                },
                "Action": [
                    "kms:Encrypt",
                    "kms:Decrypt",
                    "kms:DescribeKey"
                ]
            }
        ]
    }
}
```

> **💡 설명:** `put-key-policy` 명령어는 CMK의 사용 권한을 설정합니다. 이 권한은 암호화/복호화 작업에 필요합니다.  
> **⚠️ 주의:** 권한을 잘못 설정하면 암호화 작업이 실패할 수 있습니다.

#### ✅ Step 1 완료 확인
다음이 보이면 Step 1이 완료된 것입니다:
- [ ] KMS CMK 생성 완료 (콘솔에서 확인)
- [ ] CMK 권한 설정 완료 (콘솔에서 확인)

---

### Step 2: 봉투 암호화(Envelope Encryption) 구현 (약 15분)

#### 2.1 데이터 키 생성 및 암호화
**AWS CLI 명령어:**
```bash
aws kms generate-data-key --key-id arn:aws:kms:region:account-id:key/key-id --number-of-bytes 128
```

**예상 출력:**
```
{
    "KeyId": "arn:aws:kms:region:account-id:key/key-id",
    "Plaintext": "base64-encoded-data-key",
    "CiphertextBlob": "base64-encoded-encrypted-data-key"
}
```

> **💡 설명:** `generate-data-key` 명령어는 데이터 키를 생성하고, KMS를 사용해 암호화합니다.  
> **⚠️ 주의:** `Plaintext`는 암호화된 데이터 키, `CiphertextBlob`는 암호화된 데이터 키의 암호문입니다.

#### 2.2 데이터 암호화
**AWS CLI 명령어:**
```bash
aws kinesis put-record --stream-name my-stream --partition-key 1 --data "encrypted-data"
```

**예상 출력:**
```
{
    "ShardId": "shardId-000000000000",
    "SequenceNumber": "12345678901234567890"
}
```

> **💡 설명:** `put-record` 명령어는 Kinesis 스트림에 암호화된 데이터를 전송합니다.  
> **⚠️ 주의:** 이 예제는 Kinesis를 사용하지만, S3, RDS 등 다른 서비스에서도 봉투 암호화를 적용할 수 있습니다.

**AWS 콘솔에서:**
1. 서비스 검색창에서 "Kinesis" 입력 후 클릭
2. "Streams" 탭에서 생성된 스트림 확인
3. "Stream details" 섹션에서 데이터 전송 확인

> **📸 화면 확인:** 생성된 스트림의 "Stream name"이 "my-stream"로 설정되었는지 확인

#### ✅ Step 2 완료 확인
다음이 보이면 Step 2가 완료된 것입니다:
- [ ] 데이터 키 생성 및 암호화 완료 (콘솔에서 확인)
- [ ] 암호화된 데이터 전송 완료 (콘솔에서 확인)

---

### Step 3: Secrets Manager 자동 교체 정책 설정 (약 10분)

#### 3.1 Secret 생성
**AWS CLI 명령어:**
```bash
aws secretsmanager create-secret --name "MySecret" --description "Secret for database password" --secret-string "{\"username\":\"admin\",\"password\":\"securepassword123\"}"
```

**예상 출력:**
```
{
    "ARN": "arn:aws:secretsmanager:region:account-id:secret:MySecret-098765",
    "Name": "MySecret",
    "VersionId": "1"
}
```

> **💡 설명:** `create-secret` 명령어는 Secrets Manager에 secret을 생성합니다. 이 secret은 DB 패스워드 등 민감 정보를 보호하는 데 사용됩니다.  
> **⚠️ 주의:** secret의 값은 JSON 형식으로 전달해야 합니다.

#### 3.2 자동 교체 정책 설정
**AWS CLI 명령어:**
```bash
aws secretsmanager put-secret-value --secret-id arn:aws:secretsmanager:region:account-id:secret:MySecret-098765 --secret-string "{\"username\":\"admin\",\"password\":\"newsecurepassword456\"}"
```

**예상 출력:**
```
{
    "SecretId": "arn:aws:secretsmanager:region:account-id:secret:MySecret-098765",
    "SecretString": "{\"username\":\"admin\",\"password\":\"newsecurepassword456\"}",
    "VersionId": "2"
}
```

> **💡 설명:** `put-secret-value` 명령어는 secret의 값을 업데이트합니다. 자동 교체는 AWS Lambda와 같은 서비스와 연동해 자동으로 secret을 갱신할 수 있습니다.  
> **⚠️ 주의:** 자동 교체를 위해 Lambda 함수를 설정해야 합니다.

**AWS 콘솔에서:**
1. 서비스 검색창에서 "Secrets Manager" 입력 후 클릭
2. "Secrets" 탭에서 생성된 secret 확인
3. "Secret details" 섹션에서 version history 확인

> **📸 화면 확인:** secret의 "Version"이 2로 업데이트되었는지 확인

#### ✅ Step 3 완료 확인
다음이 보이면 Step 3가 완료된 것입니다:
- [ ] Secret 생성 완료 (콘솔에서 확인)
- [ ] Secret 값 업데이트 완료 (콘솔에서 확인)

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] KMS CMK 생성 및 권한 설정 완료
- [ ] 봉투 암호화 작업 성공
- [ ] Secrets Manager secret 생성 및 갱신 완료

### 예상 최종 결과
```bash
# 결과 확인 명령어
aws kms describe-key --key-id arn:aws:kms:region:account-id:key/key-id
aws secretsmanager get-secret-value --secret-id arn:aws:secretsmanager:region:account-id:secret:MySecret-098765
```

**예상 출력:**
```
{
    "KeyMetadata": {
        "arn": "arn:aws:kms:region:account-id:key/key-id",
        "description": "My CMK for encryption",
        "enabled": true
    }
}
{
    "SecretString": "{\"username\":\"admin\",\"password\":\"newsecurepassword456\"}",
    "VersionId": "2"
}
```

---

## 🔧 트러블슈팅

### 문제 1: `AccessDenied` 오류
**증상:** `AccessDenied` 또는 `UnauthorizedAccess` 오류 발생

**원인:** IAM 사용자 권한이 부족하거나, KMS/Secrets Manager 정책이 제한됨

**해결 방법:**
1. IAM 사용자 권한 확인
2. 필요한 정책 연결
```bash
# 현재 사용자 권한 확인
aws sts get-caller-identity
```

### 문제 2: CMK 생성 실패
**증상:** `InvalidParameterException` 또는 `ResourceNotFoundException` 오류

**원인:** 잘못된 지역 또는 계정 ID 입력

**해결 방법:**
1. `aws configure` 명령어로 정확한 지역 및 계정 ID 설정
2. `aws kms list-keys` 명령어로 기존 CMK 확인

### 문제 3: Secret 업데이트 실패
**증상:** `InvalidRequestException` 오류

**원인:** Secret ID가 잘못 입력되었거나, JSON 형식 오류

**해결 방법:**
1. `aws secretsmanager describe-secrets` 명령어로 Secret ARN 확인
2. JSON 값의 형식을 다시 확인

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!  
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] KMS CMK (ARN: arn:aws:kms:region:account-id:key/key-id)
- [ ] Secrets Manager Secret (ARN: arn:aws:secretsmanager:region:account-id:secret:MySecret-098765)
- [ ] Kinesis Stream (이름: my-stream)

### 리소스 정리 명령어
```bash
# 1. KMS CMK 삭제
aws kms delete-key --key-id arn:aws:kms:region:account-id:key/key-id

# 2. Secrets Manager Secret 삭제
aws secretsmanager delete-secret --secret-id arn:aws:secretsmanager:region:account-id:secret:MySecret-098765

# 3. Kinesis Stream 삭제
aws kinesis delete-stream --stream-name my-stream
```

### 정리 완료 확인
```bash
# 리소스가 모두 삭제되었는지 확인
aws kms list-keys
aws secretsmanager list-secrets
aws kinesis list-streams
```

---

## 📚 추가 학습 자료
- [AWS KMS 공식 문서](https://docs.aws.amazon.com/kms/latest/developerguide/)
- [Secrets Manager 사용 가이드](https://docs.aws.amazon.com/secretsmanager/latest/userguide/introduction.html)
- [Envelope Encryption 개념](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#envelope-encryption)