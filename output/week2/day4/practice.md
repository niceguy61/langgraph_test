# Week 2 Day 4 실습 가이드

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
- [ ] S3 버킷 생성 및 기본 설정 완료
- [ ] 버킷 정책을 통해 접근 제어 설정
- [ ] SSE-KMS 암호화 및 버전 관리 활성화

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분
- Step 1: 약 10분
- Step 2: 약 15분
- Step 3: 약 10분
- 리소스 정리: 약 5분

---

## 📝 실습 단계

### Step 1: S3 버킷 생성 및 기본 설정 (약 10분)

#### 1.1 S3 버킷 생성
```bash
# AWS CLI로 S3 버킷 생성
aws s3api create-bucket --bucket my-secure-bucket --region ap-northeast-2
```

**예상 출력:**
```
{
    "Location": "http://my-secure-bucket.s3.ap-northeast-2.amazonaws.com/"
}
```

> **💡 설명:** `create-bucket` 명령어는 지정된 리전에 버킷을 생성합니다. `my-secure-bucket`이라는 이름의 버킷이 생성되며, 리전은 `ap-northeast-2`로 설정됩니다. 버킷 이름은 전역적으로 유일해야 하므로, 중복 시 오류 발생합니다.

#### 1.2 AWS 콘솔에서 버킷 확인
1. AWS 관리 콘솔 접속 → **S3 서비스**로 이동  
2. **버킷 목록**에서 `my-secure-bucket`이 생성되었는지 확인  
3. 버킷 이름 클릭 후 **버킷 정책** 탭에서 기본 설정 확인

> **📸 화면 확인:** 버킷 목록에 `my-secure-bucket`이 정상적으로 생성되었는지 확인

#### ✅ Step 1 완료 확인
- [ ] `my-secure-bucket` 버킷 생성 완료
- [ ] 버킷 정책 탭에서 기본 설정 확인 가능

---

### Step 2: 버킷 정책 및 암호화 설정 (약 15분)

#### 2.1 버킷 정책 설정 (Bucket Policy)
```bash
# 버킷 정책 생성 (JSON 파일로 저장)
cat <<EOF > bucket-policy.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-secure-bucket/*"
        }
    ]
}
EOF
```

```bash
# 버킷 정책 적용
aws s3api put-bucket-policy --bucket my-secure-bucket --policy file://bucket-policy.json
```

> **💡 설명:** 이 정책은 `my-secure-bucket` 내 모든 객체를 공개 읽기 권한으로 설정합니다. 실무에서는 IP 제한이나 특정 IAM 사용자만 허용하는 정책이 필요하나, 초보자용으로는 기본적인 공개 접근을 시연합니다.

#### 2.2 SSE-KMS 암호화 설정
```bash
# SSE-KMS 암호화 활성화
aws s3api put-bucket-encryption --bucket my-secure-bucket --server-side-encryption-configuration '{
  "Rules": [
    {
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "aws:kms"
      }
    }
  ]
}'
```

> **💡 설명:** `aws:kms` 알고리즘은 AWS KMS 키를 사용해 데이터를 암호화합니다. 이 설정은 버킷 내 모든 새 객체에 자동 적용됩니다.

#### 2.3 버전 관리 활성화
```bash
# 버전 관리 설정
aws s3api put-bucket-versioning --bucket my-secure-bucket --versioning-configuration Status=Enabled
```

> **💡 설명:** 버전 관리는 동일한 파일명으로 덮어쓰기 시 이전 버전을 유지합니다. 파일 복구 및 버전별 차이 분석에 유용합니다.

#### ✅ Step 2 완료 확인
- [ ] 버킷 정책이 성공적으로 적용됨
- [ ] SSE-KMS 암호화 활성화 확인
- [ ] 버전 관리 설정 완료

---

### Step 3: MFA Delete 및 Object Lock 설정 (약 10분)

#### 3.1 MFA Delete 활성화
```bash
# MFA Delete 설정
aws s3api put-bucket-versioning --bucket my-secure-bucket --versioning-configuration '{
  "Status": "Enabled",
  "MFADelete": "Enabled"
}'
```

> **💡 설명:** MFA Delete는 버전 관리 시 AWS MFA 장치를 사용해 삭제를 인증해야 합니다. 이 기능은 데이터 유출 방지에 효과적입니다.

#### 3.2 Object Lock 설정
```bash
# Object Lock 정책 활성화
aws s3api put-bucket-object-lock --bucket my-secure-bucket --object-lock-configuration '{
  "ObjectLockEnabled": true,
  "Rule": {
    "DefaultRetention": {
      "Mode": "Governance",
      "Days": 30
    }
  }
}'
```

> **💡 설명:** Object Lock은 객체를 영구히 보존하는 기능입니다. `Governance` 모드는 관리자 권한이 필요하며, 30일간 보존 후 자동 삭제됩니다.

#### ✅ Step 3 완료 확인
- [ ] MFA Delete 활성화 완료
- [ ] Object Lock 정책 적용됨

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] 버킷 정책이 정상적으로 적용됨
- [ ] SSE-KMS 암호화 활성화됨
- [ ] 버전 관리 및 MFA Delete 설정 완료

### 예상 최종 결과
```bash
# 버킷 상태 확인
aws s3api get-bucket-encryption --bucket my-secure-bucket
aws s3api get-bucket-versioning --bucket my-secure-bucket
aws s3api get-bucket-object-lock --bucket my-secure-bucket
```

**예상 출력:**
```
{
    "ServerSideEncryptionConfiguration": {
        "Rules": [
            {
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "aws:kms"
                }
            }
        ]
    }
}
```

---

## 🔧 트러블슈팅

### 문제 1: `InvalidArgument` 오류
**증상:** `The bucket name must be unique` 오류 발생

**원인:** 동일한 버킷 이름이 이미 존재하거나 올바른 형식이 아님

**해결 방법:**
1. 버킷 이름을 `my-secure-bucket-<random>` 형식으로 변경
2. `aws s3api create-bucket` 명령어 재실행

### 문제 2: `AccessDenied` 오류
**증상:** `Access denied` 또는 `UnauthorizedAccess` 오류

**해결 방법:**
1. IAM 사용자 권한 확인
2. `s3:PutObject`, `s3:GetObject` 권한이 있는지 확인
3. `aws iam get-user` 명령어로 사용자 권한 확인

### 문제 3: 버전 관리 설정 실패
**증상:** `InvalidArgument` 또는 `MalformedXML` 오류

**해결 방법:**
1. JSON 형식을 `jq` 또는 온라인 JSON 검증기로 확인
2. `aws s3api put-bucket-versioning` 명령어 재실행

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] `my-secure-bucket` 버킷 삭제
- [ ] 관련 정책 및 설정 삭제

### 리소스 정리 명령어
```bash
# 1. 버킷 삭제 (MFA Delete 활성화 시 MFA 입력 필요)
aws s3api delete-bucket --bucket my-secure-bucket

# 2. 버킷 정책 삭제 (필요 시)
aws s3api delete-bucket-policy --bucket my-secure-bucket

# 3. 삭제 확인
aws s3api get-bucket-location --bucket my-secure-bucket
```

### 정리 완료 확인
```bash
# 리소스가 모두 삭제되었는지 확인
aws s3api list-buckets
```

---

## 📚 추가 학습 자료
- [AWS S3 버킷 정책 문서](https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-policies.html)
- [SSE-KMS 암호화 가이드](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingServerSideEncryption.html)
- [버전 관리 및 Object Lock 튜토리얼](https://aws.amazon.com/ko/blogs/storage/using-aws-s3-object-lock-to-prevent-data-deletion/)