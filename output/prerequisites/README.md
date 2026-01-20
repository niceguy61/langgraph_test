# 📚 AWS 실습 사전 준비 가이드

> **모든 실습을 시작하기 전에 이 가이드들을 먼저 완료하세요!**

---

## 🎯 가이드 순서

아래 순서대로 진행하세요:

### 1️⃣ [AWS 계정 생성 가이드](./aws-account-setup.md) ✅ 필수
- AWS 계정이 없다면 먼저 계정을 생성하세요
- 루트 사용자 MFA 설정
- 결제 알림 설정

### 2️⃣ [IAM 사용자 생성 가이드](./iam-user-setup.md) ✅ 필수
- 일상적인 작업을 위한 IAM 사용자 생성
- 적절한 권한 부여
- Access Key 생성

### 3️⃣ [AWS CLI 설치 가이드](./aws-cli-setup.md) ✅ 필수
- 운영체제별 AWS CLI 설치
- 자격 증명 설정
- 기본 명령어 테스트

### 4️⃣ [VS Code 설정 가이드](./vscode-setup.md) 📝 선택
- VS Code 설치 및 설정
- AWS Toolkit 확장 프로그램
- 편리한 개발 환경 구성

---

## ✅ 전체 체크리스트

실습을 시작하기 전 모든 항목이 완료되었는지 확인하세요:

### 필수 항목
- [ ] AWS 계정 보유 및 로그인 가능
- [ ] 루트 사용자 MFA 활성화
- [ ] 결제 알림 설정 완료
- [ ] IAM 사용자 생성 완료
- [ ] IAM 사용자 Access Key 생성 및 저장
- [ ] AWS CLI 설치 완료 (`aws --version`)
- [ ] AWS CLI 자격 증명 설정 완료 (`aws sts get-caller-identity`)

### 선택 항목
- [ ] VS Code 설치
- [ ] AWS Toolkit 확장 프로그램 설치

---

## 🧪 빠른 확인 명령어

터미널에서 다음 명령어로 설정이 완료되었는지 확인하세요:

```bash
# AWS CLI 버전 확인
aws --version

# 자격 증명 확인
aws sts get-caller-identity

# 리전 설정 확인
aws configure get region

# S3 버킷 목록 (권한 테스트)
aws s3 ls
```

**정상 출력 예시:**
```bash
$ aws --version
aws-cli/2.x.x Python/3.x.x ...

$ aws sts get-caller-identity
{
    "UserId": "AIDAEXAMPLE...",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-username"
}

$ aws configure get region
ap-northeast-2
```

---

## ⚠️ 주의사항

1. **루트 사용자를 일상 작업에 사용하지 마세요**
   - 항상 IAM 사용자로 작업하세요
   - 루트 사용자는 계정 관리에만 사용

2. **Access Key를 안전하게 보관하세요**
   - 절대 코드에 직접 입력하지 마세요
   - 공개 저장소에 올리지 마세요
   - 분실 시 즉시 비활성화하고 새로 생성하세요

3. **결제 알림을 설정하세요**
   - 예상치 못한 비용을 방지할 수 있습니다
   - 프리티어 한도 초과 알림을 받으세요

4. **실습 후 리소스를 정리하세요**
   - 사용하지 않는 리소스는 비용이 발생합니다
   - 각 실습 가이드의 "리소스 정리" 섹션을 따르세요

---

## 🔧 도움이 필요하신가요?

- 각 가이드의 **"문제 해결"** 섹션을 참고하세요
- [AWS 공식 문서](https://docs.aws.amazon.com/)
- [AWS 한국어 사용자 가이드](https://docs.aws.amazon.com/ko_kr/)

---

*준비가 완료되었다면 Week 1 실습을 시작하세요!*
