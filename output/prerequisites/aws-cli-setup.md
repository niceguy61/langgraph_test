# AWS CLI 설치 및 설정 가이드

> **📚 이 문서는 필수 선행 문서입니다.**
> CLI 기반 실습을 진행하기 전에 이 가이드를 완료해야 합니다.

## 📋 이 가이드에서 배우는 것

- [ ] AWS CLI가 무엇인지 이해하기
- [ ] 운영체제별 AWS CLI 설치하기
- [ ] AWS 자격 증명 설정하기
- [ ] 기본 CLI 명령어 테스트하기

---

## 🔍 AWS CLI란?

AWS CLI(Command Line Interface)는 터미널/명령 프롬프트에서 AWS 서비스를 관리할 수 있는 도구입니다.

### AWS CLI를 사용하는 이유

| 장점 | 설명 |
|-----|------|
| 자동화 | 스크립트로 반복 작업 자동화 가능 |
| 빠른 작업 | 콘솔보다 빠르게 작업 수행 |
| 원격 관리 | SSH로 서버에서 직접 AWS 리소스 관리 |
| CI/CD | 배포 파이프라인에서 AWS 리소스 제어 |

---

## 📥 AWS CLI 설치

### Windows

#### 방법 1: MSI 설치 프로그램 (권장)

1. AWS CLI 다운로드 페이지 접속:
   - [https://aws.amazon.com/cli/](https://aws.amazon.com/cli/)

2. **"Windows용 64비트"** 다운로드 클릭
   - 또는 직접 링크: [AWSCLIV2.msi 다운로드](https://awscli.amazonaws.com/AWSCLIV2.msi)

3. 다운로드한 `AWSCLIV2.msi` 파일 실행

4. 설치 마법사 진행:
   - **"Next"** 클릭
   - 라이센스 동의 체크 → **"Next"**
   - 설치 경로 확인 (기본값 유지) → **"Next"**
   - **"Install"** 클릭
   - 설치 완료 후 **"Finish"** 클릭

5. 설치 확인:
   - **새로운** 명령 프롬프트(CMD) 또는 PowerShell 열기
   - 다음 명령어 실행:

```powershell
aws --version
```

**예상 출력:**
```
aws-cli/2.x.x Python/3.x.x Windows/10 exe/AMD64
```

#### 방법 2: winget 사용 (Windows 10/11)

```powershell
winget install Amazon.AWSCLI
```

#### 방법 3: Chocolatey 사용

```powershell
choco install awscli
```

---

### macOS

#### 방법 1: PKG 설치 프로그램 (권장)

1. 터미널 열기

2. 설치 파일 다운로드:
```bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
```

3. 설치 실행:
```bash
sudo installer -pkg AWSCLIV2.pkg -target /
```

4. 설치 확인:
```bash
aws --version
```

#### 방법 2: Homebrew 사용

```bash
brew install awscli
```

---

### Linux (Ubuntu/Debian)

1. 설치 파일 다운로드:
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
```

2. 압축 해제:
```bash
unzip awscliv2.zip
```

3. 설치:
```bash
sudo ./aws/install
```

4. 설치 확인:
```bash
aws --version
```

---

## 🔑 AWS 자격 증명 설정

AWS CLI를 사용하려면 자격 증명(Access Key)이 필요합니다.

### Step 1: IAM 사용자 Access Key 생성

> **⚠️ 주의:** 루트 사용자가 아닌 IAM 사용자의 Access Key를 사용하세요!
> IAM 사용자가 없다면 먼저 [IAM 사용자 생성 가이드](./iam-user-setup.md)를 완료하세요.

1. AWS Console에 로그인
2. 상단 검색창에 "IAM" 입력 → **IAM** 서비스 클릭
3. 왼쪽 메뉴에서 **"사용자"** 클릭
4. 자격 증명을 생성할 사용자 클릭
5. **"보안 자격 증명"** 탭 클릭
6. **"액세스 키"** 섹션에서 **"액세스 키 만들기"** 클릭
7. **"Command Line Interface(CLI)"** 선택
8. 확인 체크박스 선택 → **"다음"**
9. (선택) 설명 태그 입력 → **"액세스 키 만들기"**
10. **Access Key ID**와 **Secret Access Key** 저장

> **🚨 중요:**
> - Secret Access Key는 이 시점에만 확인 가능합니다!
> - 반드시 안전한 곳에 저장하세요
> - **절대로** 코드에 직접 입력하거나 공개 저장소에 올리지 마세요

### Step 2: AWS CLI 설정

터미널에서 다음 명령어 실행:

```bash
aws configure
```

프롬프트에 따라 정보 입력:

```
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: ap-northeast-2
Default output format [None]: json
```

| 항목 | 설명 | 추천 값 |
|-----|------|---------|
| Access Key ID | IAM에서 생성한 Access Key ID | 본인 키 입력 |
| Secret Access Key | IAM에서 생성한 Secret Key | 본인 키 입력 |
| Default region | 기본 리전 | `ap-northeast-2` (서울) |
| Default output | 출력 형식 | `json` |

### Step 3: 설정 확인

```bash
# 설정된 자격 증명 확인
aws sts get-caller-identity
```

**예상 출력:**
```json
{
    "UserId": "AIDAEXAMPLEUSERID",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-username"
}
```

이 출력이 나오면 설정이 완료된 것입니다! 🎉

---

## 📁 설정 파일 위치

AWS CLI는 두 개의 설정 파일을 사용합니다:

| 파일 | 위치 | 내용 |
|-----|------|------|
| credentials | `~/.aws/credentials` | Access Key, Secret Key |
| config | `~/.aws/config` | 리전, 출력 형식 |

### Windows 경로
```
C:\Users\<사용자명>\.aws\credentials
C:\Users\<사용자명>\.aws\config
```

### macOS/Linux 경로
```
~/.aws/credentials
~/.aws/config
```

### 설정 파일 내용 확인

```bash
# credentials 파일
cat ~/.aws/credentials
```

```ini
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

```bash
# config 파일
cat ~/.aws/config
```

```ini
[default]
region = ap-northeast-2
output = json
```

---

## 🧪 기본 명령어 테스트

설정이 완료되었는지 확인하는 기본 명령어들입니다.

### 현재 사용자 정보 확인
```bash
aws sts get-caller-identity
```

### S3 버킷 목록 조회
```bash
aws s3 ls
```

### 현재 리전의 EC2 인스턴스 목록
```bash
aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId'
```

### IAM 사용자 목록
```bash
aws iam list-users --query 'Users[].UserName'
```

### 현재 설정된 리전 확인
```bash
aws configure get region
```

---

## 🔄 프로필 관리 (여러 계정 사용)

여러 AWS 계정을 사용해야 할 경우 프로필을 활용합니다.

### 새 프로필 추가

```bash
aws configure --profile work
```

### 프로필 사용

```bash
# 특정 프로필로 명령 실행
aws s3 ls --profile work

# 환경 변수로 기본 프로필 설정
export AWS_PROFILE=work
```

### 프로필 목록 확인

```bash
# credentials 파일에서 확인
cat ~/.aws/credentials
```

---

## ⚠️ 보안 베스트 프랙티스

### 1. 루트 사용자 키 사용 금지
- 항상 IAM 사용자의 Access Key 사용
- 루트 사용자 Access Key는 생성하지 않기

### 2. 최소 권한 원칙
- 필요한 권한만 가진 IAM 사용자 사용
- AdministratorAccess는 필요할 때만 사용

### 3. Access Key 관리
```bash
# Access Key 주기적으로 교체
aws iam create-access-key --user-name your-username
aws iam delete-access-key --user-name your-username --access-key-id OLD_KEY_ID
```

### 4. 환경 변수 사용 시 주의
```bash
# 환경 변수로 임시 설정 (세션 종료 시 사라짐)
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# 절대 .bashrc나 .zshrc에 저장하지 마세요!
```

---

## ✅ 완료 체크리스트

다음 항목을 모두 완료했는지 확인하세요:

- [ ] AWS CLI 설치 완료 (`aws --version` 확인)
- [ ] IAM 사용자 Access Key 생성
- [ ] `aws configure` 설정 완료
- [ ] `aws sts get-caller-identity` 정상 출력 확인
- [ ] 기본 명령어 테스트 성공

---

## 🔧 문제 해결

### 'aws' 명령을 찾을 수 없음

**Windows:**
- 새 명령 프롬프트/PowerShell 창 열기
- 시스템 환경 변수 PATH에 AWS CLI 경로 추가 확인

**macOS/Linux:**
```bash
# 쉘 설정 파일에 경로 추가
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### InvalidClientTokenId 오류

```
An error occurred (InvalidClientTokenId) when calling the ... operation:
The security token included in the request is invalid.
```

**해결:**
- Access Key ID가 정확한지 확인
- Access Key가 활성 상태인지 IAM 콘솔에서 확인
- `aws configure`로 다시 설정

### SignatureDoesNotMatch 오류

```
An error occurred (SignatureDoesNotMatch) when calling the ... operation:
The request signature we calculated does not match the signature you provided.
```

**해결:**
- Secret Access Key가 정확한지 확인
- 복사/붙여넣기 시 공백이 들어가지 않았는지 확인
- `aws configure`로 다시 설정

### Access Denied 오류

```
An error occurred (AccessDenied) when calling the ... operation:
User: arn:aws:iam::123456789012:user/... is not authorized to perform: ...
```

**해결:**
- IAM 사용자에게 필요한 권한이 있는지 확인
- 필요한 정책을 IAM 사용자에게 연결

---

## ➡️ 다음 단계

AWS CLI 설정이 완료되었으면 다음 가이드로 진행하세요:

1. 실습을 시작할 준비가 되었습니다!
2. 각 주차별 실습 가이드를 따라 진행하세요

---

*마지막 업데이트: 2024*
