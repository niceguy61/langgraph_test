# Week 4 Day 3 실습 가이드

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
- [ ] **GuardDuty 기본 구성** 완료 (AWS 콘솔 및 CLI로 설정)
- [ ] **Security Hub 통합 설정** 완료 (보안 데이터 통합)
- [ ] **CloudTrail 로깅 활성화** 완료 (API 요청 로그 수집)
- [ ] **Trusted Advisor 정책 설정** 완료 (성능/보안 최적화)

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분  
- Step 1: 약 10분  
- Step 2: 약 15분  
- Step 3: 약 10분  
- 리소스 정리: 약 5분  

---

## 📝 실습 단계

### Step 1: GuardDuty 구성 (약 10분)

#### 1.1 GuardDuty 생성 및 기본 설정
**AWS 콘솔에서:**
1. 서비스 검색창에서 "GuardDuty" 입력 후 클릭  
2. **"Create detector"** 버튼 클릭  
3. **Detector Name** 입력 (예: `MySecurityDetector`)  
4. **"Enable all default findings"** 선택  
5. **"Create"** 버튼 클릭  

> **📸 화면 확인:** "Detector ARN"이 생성된 상태로 "Findings" 탭이 표시되면 정상입니다.

**CLI 명령어:**
```bash
# GuardDuty Detector 생성
aws guardduty create-detector --name "MySecurityDetector"
```

**예상 출력:**
```json
{
    "DetectorId": "123456789012",
    "DetectorArn": "arn:aws:guardduty:us-east-1:123456789012:detector/123456789012"
}
```

> **💡 설명:** Detector는 GuardDuty의 핵심 리소스로, 보안 위협 탐지를 시작하는 첫 단계입니다.  
> **비용 주의:** 기본 설정 시 AWS 서비스에 대한 모니터링이 자동 활성화됩니다.

#### 1.2 GuardDuty 정책 설정
**AWS 콘솔에서:**
1. **"Rules"** 탭에서 **"Create rule"** 클릭  
2. **Rule Name** 입력 (예: `MalwareDetectionRule`)  
3. **"Rule type"**에서 **"Finding"** 선택  
4. **"Finding types"**에서 **"MALWARE"** 선택  
5. **"Actions"**에서 **"Publish finding"** 활성화  
6. **"Create"** 클릭  

> **📸 화면 확인:** "Rule ARN"이 생성된 상태로 "Actions"가 활성화된 상태 확인.

**CLI 명령어:**
```bash
# GuardDuty Rule 생성
aws guardduty create-rule --detector-id "123456789012" \
--name "MalwareDetectionRule" \
--finding-ids "MALWARE" \
--action "publishFinding"
```

**예상 출력:**
```json
{
    "RuleId": "abcdef1234567890",
    "RuleArn": "arn:aws:guardduty:us-east-1:123456789012:rule/123456789012/abcdef1234567890"
}
```

#### ✅ Step 1 완료 확인
- [ ] GuardDuty Detector 생성 완료  
- [ ] Rule 생성 및 활성화 완료  
- [ ] AWS 콘솔에서 "Findings" 탭이 표시됨

---

### Step 2: Security Hub 통합 설정 (약 15분)

#### 2.1 Security Hub 활성화
**AWS 콘솔에서:**
1. 서비스 검색창에서 "Security Hub" 입력 후 클릭  
2. **"Enable Security Hub"** 버튼 클릭  
3. **"Enable all default standards"** 선택  
4. **"Enable"** 클릭  

> **📸 화면 확인:** "Standards" 탭에서 "AWS Foundational Security Best Practices"가 활성화된 상태 확인.

**CLI 명령어:**
```bash
# Security Hub 활성화
aws securityhub enable-security-hub
```

**예상 출력:**
```json
{
    "SecurityHub": {
        "Status": "ENABLED"
    }
}
```

#### 2.2 Security Hub 통합 설정
**AWS 콘솔에서:**
1. **"Standards"** 탭에서 **"Create standard"** 클릭  
2. **Standard Name** 입력 (예: `CustomSecurityStandard`)  
3. **"Custom standard"** 선택  
4. **"Add standard"** 클릭  
5. **"Add controls"**에서 **"AWS CloudTrail"** 및 **"AWS GuardDuty"** 추가  
6. **"Create"** 클릭  

> **📸 화면 확인:** "Standards" 목록에 "CustomSecurityStandard" 추가됨.

**CLI 명령어:**
```bash
# Security Hub Standard 생성
aws securityhub create-standards \
--name "CustomSecurityStandard" \
--standards-subscription-ids "CIS-Custom" \
--controls "AWS_CloudTrail", "AWS_GuardDuty"
```

#### ✅ Step 2 완료 확인
- [ ] Security Hub 활성화 완료  
- [ ] Custom Standard 생성 및 통합 완료  
- [ ] AWS 콘솔에서 "Standards" 탭이 표시됨

---

### Step 3: CloudTrail 및 Trusted Advisor 설정 (약 10분)

#### 3.1 CloudTrail 활성화
**AWS 콘솔에서:**
1. 서비스 검색창에서 "CloudTrail" 입력 후 클릭  
2. **"Create trail"** 클릭  
3. **Trail Name** 입력 (예: `MySecurityTrail`)  
4. **"S3 bucket name"** 입력 (예: `mysecuritytrail-bucket`)  
5. **"Enable logging"** 선택  
6. **"Create"** 클릭  

> **📸 화면 확인:** "Trail status"가 "ACTIVE"로 표시됨.

**CLI 명령어:**
```bash
# CloudTrail 활성화
aws cloudtrail create-trail --name "MySecurityTrail" \
--s3-bucket-name "mysecuritytrail-bucket" \
--is-log-validation-enabled "false"
```

**예상 출력:**
```json
{
    "Trail": {
        "TrailARN": "arn:aws:cloudtrail:us-east-1:123456789012:trail/MySecurityTrail"
    }
}
```

#### 3.2 Trusted Advisor 정책 설정
**AWS 콘솔에서:**
1. 서비스 검색창에서 "Trusted Advisor" 입력 후 클릭  
2. **"Check all recommendations"** 클릭  
3. **"View recommendations"**에서 **"Security"** 필터 선택  
4. **"Apply"** 버튼 클릭 (예: IAM 정책 최적화)  

> **📸 화면 확인:** "Security" 카테고리의 권장 사항이 표시되고 "Apply" 버튼 활성화됨.

**CLI 명령어:**
```bash
# Trusted Advisor 권장 사항 확인
aws support describe-trusted-advisor-checks --region us-east-1
```

**예상 출력:**
```json
{
    "Checks": [
        {
            "CheckId": "AWS Security Best Practices",
            "Name": "Security Best Practices",
            "Status": "PENDING"
        }
    ]
}
```

#### ✅ Step 3 완료 확인
- [ ] CloudTrail 활성화 완료  
- [ ] Trusted Advisor 권장 사항 확인 완료  
- [ ] AWS 콘솔에서 "Trusted Advisor" 탭이 표시됨

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] GuardDuty Detector 생성 완료  
- [ ] Security Hub 통합 설정 완료  
- [ ] CloudTrail 로깅 활성화 완료  
- [ ] Trusted Advisor 권장 사항 적용 완료

### 예상 최종 결과
```bash
# 모든 서비스 상태 확인
aws guardduty get-detectors
aws securityhub get-security-hub
aws cloudtrail get-trail-status
```

**예상 출력:**
```json
{
    "Detectors": [
        {
            "DetectorId": "123456789012",
            "DetectorArn": "arn:aws:guardduty:us-east-1:123456789012:detector/123456789012"
        }
    ]
}
```

---

## 🔧 트러블슈팅

### 문제 1: "AccessDenied" 오류
**증상:** `aws guardduty create-detector` 명령어 실행 시 `AccessDenied` 오류 발생  
**원인:** IAM 사용자에 GuardDuty 권한이 부족함  
**해결 방법:**
1. IAM 사용자에 `GuardDutyFullAccess` 정책 부여  
2. CLI 명령어 재실행

```bash
# IAM 정책 확인
aws iam get-user-policy --user-name "your-username" --policy-name "GuardDutyFullAccess"
```

### 문제 2: CloudTrail S3 버킷 생성 실패
**증상:** `aws cloudtrail create-trail` 명령어 실행 시 S3 버킷 생성 실패  
**원인:** S3 버킷이 미리 생성되지 않음  
**해결 방법:**
1. `aws s3api create-bucket --bucket "mysecuritytrail-bucket" --region us-east-1` 명령어로 버킷 생성  
2. CloudTrail 재설정

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!  
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] GuardDuty Detector  
- [ ] Security Hub Standard  
- [ ] CloudTrail Trail  
- [ ] S3 버킷 (mysecuritytrail-bucket)

### 리소스 정리 명령어
```bash
# 1. GuardDuty Detector 삭제
aws guardduty delete-detector --detector-id "123456789012"

# 2. Security Hub Standard 삭제
aws securityhub delete-standards --standards-subscription-ids "CIS-Custom"

# 3. CloudTrail Trail 삭제
aws cloudtrail delete-trail --name "MySecurityTrail"

# 4. S3 버킷 삭제
aws s3 rb s3://mysecuritytrail-bucket --force
```

### 정리 완료 확인
```bash
# 리소스 삭제 확인
aws guardduty list-detectors
aws securityhub list-standards
aws cloudtrail list-trails
```

---

## 📚 추가 학습 자료
- [AWS GuardDuty 공식 문서](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_introduction.html)  
- [Security Hub 통합 가이드](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-security-hub.html)  
- [CloudTrail 로깅 설정 튜토리얼](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-getting-started.html)  
- [Trusted Advisor 최적화 가이드](https://aws.amazon.com/trustedadvisor/)