# IAM 사용자 생성 가이드

> **📚 이 문서는 필수 선행 문서입니다.**
> 모든 실습에서 루트 사용자 대신 IAM 사용자를 사용해야 합니다.

## 📋 이 가이드에서 배우는 것

- [ ] IAM이 무엇인지 이해하기
- [ ] 실습용 IAM 사용자 생성하기
- [ ] IAM 사용자에 권한 부여하기
- [ ] IAM 사용자로 로그인하기

---

## 🔍 IAM이란?

**IAM (Identity and Access Management)**은 AWS 리소스에 대한 액세스를 안전하게 관리하는 서비스입니다.

### 왜 IAM 사용자를 사용해야 하나요?

| 루트 사용자 | IAM 사용자 |
|-----------|-----------|
| 모든 권한 보유 | 필요한 권한만 부여 |
| 해킹 시 전체 계정 위험 | 해킹 시 피해 제한 |
| 권한 제한 불가 | 권한 세밀하게 제어 |
| 감사 추적 어려움 | 개별 활동 추적 가능 |

> **⚠️ AWS 보안 모범 사례:**
> 루트 사용자는 계정 생성/결제 관리에만 사용하고,
> 일상적인 작업에는 항상 IAM 사용자를 사용하세요!

---

## 👤 IAM 사용자 생성

### Step 1: IAM 콘솔 접속

1. AWS Management Console에 **루트 사용자**로 로그인
2. 상단 검색창에 **"IAM"** 입력
3. **"IAM"** 서비스 클릭

### Step 2: 사용자 생성 시작

1. 왼쪽 메뉴에서 **"사용자"** 클릭
2. **"사용자 생성"** 버튼 클릭

### Step 3: 사용자 세부 정보

1. **사용자 이름** 입력:
   - 예: `aws-learner`, `admin-user`, `developer`
   - 영문, 숫자, `-`, `_`, `.` 사용 가능

2. **"AWS Management Console에 대한 사용자 액세스 권한 제공"** 체크

3. **"IAM 사용자를 생성하고 싶음"** 선택

4. **콘솔 암호** 설정:
   - **"자동 생성된 암호"** 또는 **"사용자 지정 암호"** 선택
   - 사용자 지정 시 강력한 암호 입력

5. **"사용자는 다음 로그인 시 새 암호를 생성해야 합니다"**:
   - 본인이 사용할 계정이면 체크 해제
   - 다른 사람에게 줄 계정이면 체크

6. **"다음"** 클릭

### Step 4: 권한 설정

권한을 부여하는 3가지 방법이 있습니다:

#### 방법 1: 그룹에 사용자 추가 (권장)

1. **"사용자를 그룹에 추가"** 선택
2. **"그룹 생성"** 클릭
3. 그룹 이름 입력: `Administrators` 또는 `Developers`
4. 정책 검색 및 선택:
   - 학습용: **AdministratorAccess** (전체 권한)
   - 개발용: **PowerUserAccess** (IAM 제외 전체)
5. **"사용자 그룹 생성"** 클릭
6. 생성된 그룹 체크
7. **"다음"** 클릭

#### 방법 2: 직접 정책 연결

1. **"직접 정책 연결"** 선택
2. 정책 검색 및 선택:
   - **AdministratorAccess**: 전체 권한
   - **PowerUserAccess**: IAM 제외 전체 권한
   - **ViewOnlyAccess**: 읽기 전용
3. **"다음"** 클릭

#### 권장 정책 설명

| 정책 | 권한 범위 | 사용 용도 |
|-----|----------|----------|
| AdministratorAccess | 모든 AWS 서비스 | 학습, 개발 환경 관리 |
| PowerUserAccess | IAM 제외 모든 서비스 | 개발자 |
| ViewOnlyAccess | 모든 서비스 읽기 전용 | 모니터링 |
| AmazonEC2FullAccess | EC2만 전체 권한 | EC2 관리자 |
| AmazonS3FullAccess | S3만 전체 권한 | S3 관리자 |

### Step 5: 검토 및 생성

1. 설정 내용 검토
2. **"사용자 생성"** 클릭

### Step 6: 로그인 정보 저장

> **🚨 중요:** 이 화면은 한 번만 표시됩니다!

1. **콘솔 로그인 URL** 복사 및 저장
   - 형식: `https://123456789012.signin.aws.amazon.com/console`
   - 또는: `https://your-alias.signin.aws.amazon.com/console`

2. **사용자 이름** 기록

3. **비밀번호** 기록 (자동 생성 시)
   - **".csv 다운로드"** 클릭하여 저장 (권장)

4. **"사용자 목록으로 돌아가기"** 클릭

---

## 🔑 IAM 사용자 Access Key 생성

CLI나 SDK를 사용하려면 Access Key가 필요합니다.

### Step 1: 사용자 선택

1. IAM 콘솔 → **"사용자"** 클릭
2. Access Key를 생성할 사용자 클릭

### Step 2: Access Key 생성

1. **"보안 자격 증명"** 탭 클릭
2. **"액세스 키"** 섹션에서 **"액세스 키 만들기"** 클릭
3. 사용 사례 선택:
   - **"Command Line Interface(CLI)"** 선택
4. 확인 체크박스 선택 → **"다음"**
5. (선택) 설명 태그 입력
6. **"액세스 키 만들기"** 클릭

### Step 3: 키 저장

> **🚨 매우 중요:** Secret Access Key는 이 시점에만 표시됩니다!

1. **Access Key ID** 복사 및 저장
2. **Secret Access Key** 복사 및 저장
3. **".csv 파일 다운로드"** 클릭 (권장)
4. **"완료"** 클릭

---

## 🔒 IAM 사용자 MFA 설정

IAM 사용자에게도 MFA를 설정하는 것이 좋습니다.

### Step 1: 보안 자격 증명 탭

1. IAM 콘솔 → **"사용자"** → 사용자 선택
2. **"보안 자격 증명"** 탭 클릭

### Step 2: MFA 디바이스 할당

1. **"MFA 디바이스 할당"** 섹션에서 **"MFA 디바이스 할당"** 클릭
2. 디바이스 이름 입력: `my-phone-mfa`
3. MFA 디바이스 유형 선택:
   - **"인증 관리자 앱"** (권장)
4. **"다음"** 클릭
5. QR 코드를 인증 앱(Google Authenticator 등)으로 스캔
6. 연속된 두 개의 MFA 코드 입력
7. **"MFA 추가"** 클릭

---

## 🌐 IAM 사용자로 로그인

### Step 1: 로그인 URL 접속

두 가지 방법이 있습니다:

#### 방법 1: 계정 ID 로그인
1. [https://console.aws.amazon.com](https://console.aws.amazon.com) 접속
2. **"IAM 사용자"** 탭 선택
3. **계정 ID (12자리)** 또는 **계정 별칭** 입력
4. **"다음"** 클릭

#### 방법 2: 직접 URL 사용
1. 사용자 생성 시 받은 로그인 URL 접속
   - `https://123456789012.signin.aws.amazon.com/console`

### Step 2: 자격 증명 입력

1. **IAM 사용자 이름** 입력
2. **비밀번호** 입력
3. MFA 설정 시 **MFA 코드** 입력
4. **"로그인"** 클릭

### Step 3: 비밀번호 변경 (필요 시)

첫 로그인 시 비밀번호 변경을 요구받을 수 있습니다:
1. 기존 비밀번호 입력
2. 새 비밀번호 입력 (2번)
3. **"비밀번호 변경 확인"** 클릭

---

## 🏷️ 계정 별칭 설정 (선택)

로그인 URL을 더 기억하기 쉽게 만들 수 있습니다.

### 별칭 생성

1. IAM 콘솔 → **대시보드**
2. 오른쪽의 **"AWS 계정"** 섹션
3. **"계정 별칭"** 옆의 **"생성"** 클릭
4. 별칭 입력 (예: `my-company-aws`)
5. **"별칭 생성"** 클릭

### 새 로그인 URL

```
https://my-company-aws.signin.aws.amazon.com/console
```

---

## 👥 IAM 그룹 활용

여러 사용자에게 같은 권한을 부여할 때 그룹을 활용합니다.

### 그룹 생성

1. IAM 콘솔 → **"사용자 그룹"** 클릭
2. **"그룹 생성"** 클릭
3. 그룹 이름 입력: `Developers`, `Administrators` 등
4. 정책 연결
5. 사용자 추가
6. **"그룹 생성"** 클릭

### 권장 그룹 구성

| 그룹 | 정책 | 용도 |
|-----|------|------|
| Administrators | AdministratorAccess | 관리자 |
| Developers | PowerUserAccess | 개발자 |
| ReadOnly | ViewOnlyAccess | 읽기 전용 사용자 |
| EC2Admins | AmazonEC2FullAccess | EC2 관리자 |

---

## ✅ 완료 체크리스트

다음 항목을 모두 완료했는지 확인하세요:

- [ ] IAM 사용자 생성 완료
- [ ] 적절한 권한 정책 연결
- [ ] 로그인 URL 저장
- [ ] 사용자 이름/비밀번호 저장
- [ ] Access Key 생성 및 저장 (CLI 사용 시)
- [ ] MFA 설정 (권장)
- [ ] IAM 사용자로 로그인 테스트

---

## 🔧 문제 해결

### 로그인 URL을 잊어버린 경우

1. 루트 사용자로 AWS 콘솔 로그인
2. IAM 대시보드 접속
3. 오른쪽의 "AWS 계정" 섹션에서 로그인 URL 확인

### 비밀번호를 잊어버린 경우

1. 루트 사용자로 AWS 콘솔 로그인
2. IAM → 사용자 → 해당 사용자 선택
3. "보안 자격 증명" 탭
4. "콘솔 암호" 섹션에서 "암호 관리" 클릭
5. 새 비밀번호 설정

### Access Key를 분실한 경우

1. 분실한 Access Key 비활성화/삭제
2. 새 Access Key 생성

```bash
# CLI로 Access Key 비활성화
aws iam update-access-key --user-name USERNAME --access-key-id OLD_KEY --status Inactive

# CLI로 Access Key 삭제
aws iam delete-access-key --user-name USERNAME --access-key-id OLD_KEY
```

### 권한 부족 오류

1. IAM 콘솔에서 사용자에게 필요한 정책 추가
2. 또는 사용자를 적절한 그룹에 추가

---

## ➡️ 다음 단계

IAM 사용자 생성이 완료되었으면:

1. **[AWS CLI 설치 가이드](./aws-cli-setup.md)** - CLI 설정하기
2. 실습을 진행하세요!

---

*마지막 업데이트: 2024*
