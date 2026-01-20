# VS Code 개발 환경 설정 가이드

> **📚 이 문서는 선택 사항입니다.**
> CLI와 코드 편집을 더 편리하게 사용하고 싶다면 이 가이드를 따라하세요.

## 📋 이 가이드에서 배우는 것

- [ ] VS Code 설치하기
- [ ] AWS 관련 확장 프로그램 설치
- [ ] 터미널에서 AWS CLI 사용하기
- [ ] 유용한 설정 적용하기

---

## 🔍 왜 VS Code인가?

**Visual Studio Code**는 Microsoft에서 만든 무료 코드 편집기입니다.

### VS Code의 장점

| 장점 | 설명 |
|-----|------|
| 무료 | 완전 무료, 오픈소스 |
| 가벼움 | 빠른 실행, 낮은 리소스 사용 |
| 확장성 | 수천 개의 확장 프로그램 |
| 통합 터미널 | 에디터 내에서 CLI 사용 |
| 다국어 지원 | 한국어 인터페이스 지원 |

---

## 📥 VS Code 설치

### Windows

1. [https://code.visualstudio.com](https://code.visualstudio.com) 접속
2. **"Download for Windows"** 클릭
3. 다운로드한 설치 파일 실행
4. 설치 옵션:
   - ✅ "Add to PATH" (환경 변수에 추가) - **권장**
   - ✅ "Register Code as an editor for supported file types"
   - ✅ "Add 'Open with Code' action to Windows Explorer"
5. **"Install"** 클릭
6. 설치 완료 후 VS Code 실행

### macOS

#### 방법 1: 공식 웹사이트
1. [https://code.visualstudio.com](https://code.visualstudio.com) 접속
2. **"Download for Mac"** 클릭
3. 다운로드한 .zip 파일 압축 해제
4. `Visual Studio Code.app`을 Applications 폴더로 이동

#### 방법 2: Homebrew
```bash
brew install --cask visual-studio-code
```

### Linux (Ubuntu/Debian)

```bash
# Microsoft GPG 키 추가
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg

# 저장소 추가
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'

# 설치
sudo apt update
sudo apt install code
```

---

## 🌐 한국어 설정

1. VS Code 실행
2. `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`)로 명령 팔레트 열기
3. "Configure Display Language" 입력 후 선택
4. "Install Additional Languages" 클릭
5. "Korean Language Pack" 찾아서 **Install**
6. VS Code 재시작

---

## 🔌 AWS 관련 확장 프로그램

### 필수 확장 프로그램

#### 1. AWS Toolkit
AWS 서비스를 VS Code에서 직접 관리

1. 왼쪽 확장 프로그램 아이콘 클릭 (또는 `Ctrl+Shift+X`)
2. "AWS Toolkit" 검색
3. **"Install"** 클릭

**주요 기능:**
- Lambda 함수 편집/배포
- S3 버킷 탐색
- CloudWatch 로그 확인
- ECS/ECR 관리

#### 2. YAML
AWS CloudFormation, SAM 템플릿 작성에 필수

1. "YAML" 검색 (Red Hat 제공)
2. **"Install"** 클릭

#### 3. JSON
JSON 파일 편집 개선

1. "Prettier - Code formatter" 검색
2. **"Install"** 클릭

### 추천 확장 프로그램

| 확장 프로그램 | 용도 |
|-------------|------|
| Python | Python 코드 작성 (Lambda) |
| Docker | Docker 컨테이너 관리 |
| GitLens | Git 히스토리 확인 |
| Thunder Client | REST API 테스트 |
| Markdown All in One | 마크다운 편집 |
| Material Icon Theme | 파일 아이콘 테마 |

### 일괄 설치 명령어

터미널에서 다음 명령어로 확장 프로그램을 설치할 수 있습니다:

```bash
# AWS Toolkit
code --install-extension amazonwebservices.aws-toolkit-vscode

# YAML
code --install-extension redhat.vscode-yaml

# Python
code --install-extension ms-python.python

# Docker
code --install-extension ms-azuretools.vscode-docker

# GitLens
code --install-extension eamodio.gitlens
```

---

## ⚙️ AWS Toolkit 설정

### AWS 자격 증명 연결

1. 왼쪽 사이드바에서 **AWS 아이콘** 클릭
2. "Connect to AWS" 또는 "Add Connection" 클릭
3. 연결 방법 선택:

#### 방법 1: 기존 AWS CLI 자격 증명 사용
- AWS CLI를 이미 설정했다면 자동으로 감지됩니다
- "Use shared credentials" 선택

#### 방법 2: IAM Identity Center (SSO)
- 회사에서 SSO를 사용하는 경우
- "Use IAM Identity Center" 선택

### AWS Explorer 사용

연결 후 AWS Explorer에서 다음을 확인할 수 있습니다:

- **S3**: 버킷 목록, 파일 업로드/다운로드
- **Lambda**: 함수 목록, 코드 편집, 호출
- **CloudWatch Logs**: 로그 그룹, 로그 스트림
- **API Gateway**: API 목록
- **ECS/ECR**: 컨테이너 서비스

---

## 💻 통합 터미널 사용

VS Code의 통합 터미널에서 AWS CLI를 사용할 수 있습니다.

### 터미널 열기

- 단축키: `` Ctrl+` `` (백틱)
- 메뉴: View → Terminal

### 기본 터미널 설정

**Windows:**
1. `Ctrl+Shift+P` → "Terminal: Select Default Profile"
2. 선택:
   - **PowerShell** (권장)
   - **Command Prompt**
   - **Git Bash** (설치된 경우)

**macOS/Linux:**
- 기본적으로 시스템 쉘 사용 (zsh, bash)

### AWS CLI 테스트

```bash
# 터미널에서 AWS CLI 확인
aws --version

# 자격 증명 확인
aws sts get-caller-identity
```

---

## 📁 작업 폴더 설정

AWS 실습을 위한 폴더 구조를 만듭니다.

### 폴더 구조 예시

```
aws-learning/
├── week1/
│   ├── day1/
│   │   ├── notes.md
│   │   └── scripts/
│   ├── day2/
│   └── ...
├── week2/
├── week3/
├── week4/
├── templates/         # CloudFormation 템플릿
├── scripts/           # 자주 사용하는 스크립트
└── README.md
```

### VS Code에서 폴더 열기

1. **File → Open Folder** (또는 `Ctrl+K Ctrl+O`)
2. 작업 폴더 선택
3. 폴더가 사이드바에 표시됨

---

## ⌨️ 유용한 단축키

### 기본 단축키

| 단축키 (Windows) | 단축키 (Mac) | 기능 |
|-----------------|-------------|------|
| `Ctrl+Shift+P` | `Cmd+Shift+P` | 명령 팔레트 |
| `Ctrl+P` | `Cmd+P` | 파일 빠른 열기 |
| `Ctrl+`` ` | `Cmd+`` ` | 터미널 열기/닫기 |
| `Ctrl+B` | `Cmd+B` | 사이드바 토글 |
| `Ctrl+Shift+E` | `Cmd+Shift+E` | 탐색기 열기 |
| `Ctrl+Shift+F` | `Cmd+Shift+F` | 전체 검색 |
| `Ctrl+/` | `Cmd+/` | 주석 토글 |
| `Ctrl+S` | `Cmd+S` | 저장 |
| `Ctrl+Shift+S` | `Cmd+Shift+S` | 다른 이름으로 저장 |

### 편집 단축키

| 단축키 (Windows) | 단축키 (Mac) | 기능 |
|-----------------|-------------|------|
| `Alt+Up/Down` | `Option+Up/Down` | 줄 이동 |
| `Shift+Alt+Up/Down` | `Shift+Option+Up/Down` | 줄 복사 |
| `Ctrl+D` | `Cmd+D` | 같은 단어 선택 |
| `Ctrl+Shift+K` | `Cmd+Shift+K` | 줄 삭제 |
| `Ctrl+Enter` | `Cmd+Enter` | 아래에 새 줄 삽입 |

---

## 🛠️ 추천 설정

### settings.json 설정

1. `Ctrl+Shift+P` → "Preferences: Open Settings (JSON)"
2. 다음 설정 추가:

```json
{
    // 기본 설정
    "editor.fontSize": 14,
    "editor.tabSize": 2,
    "editor.wordWrap": "on",
    "editor.minimap.enabled": false,

    // 자동 저장
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000,

    // 터미널 설정
    "terminal.integrated.fontSize": 13,

    // 파일 연결
    "files.associations": {
        "*.yaml": "yaml",
        "*.yml": "yaml",
        "*.json": "jsonc"
    },

    // AWS CloudFormation 스키마
    "yaml.schemas": {
        "https://raw.githubusercontent.com/awslabs/goformation/master/schema/cloudformation.schema.json": [
            "*.cfn.yaml",
            "*.cfn.yml",
            "template.yaml",
            "template.yml"
        ]
    }
}
```

---

## ✅ 완료 체크리스트

다음 항목을 모두 완료했는지 확인하세요:

- [ ] VS Code 설치 완료
- [ ] 한국어 설정 (선택)
- [ ] AWS Toolkit 확장 프로그램 설치
- [ ] AWS 자격 증명 연결
- [ ] 통합 터미널에서 AWS CLI 테스트
- [ ] 작업 폴더 생성 및 열기

---

## 🔧 문제 해결

### AWS Toolkit에서 자격 증명을 찾지 못함

1. AWS CLI가 설정되어 있는지 확인:
```bash
aws configure list
```

2. `~/.aws/credentials` 파일 존재 확인

3. VS Code 재시작

### 터미널에서 aws 명령어가 작동하지 않음

**Windows:**
1. 새 터미널 창 열기 (기존 터미널 닫고)
2. 또는 VS Code 재시작
3. 환경 변수 PATH 확인

**macOS/Linux:**
```bash
# 쉘 설정 파일에 경로 추가
export PATH="/usr/local/bin:$PATH"
```

### 확장 프로그램이 설치되지 않음

1. VS Code 버전 확인 (최신 버전 권장)
2. 인터넷 연결 확인
3. 프록시 설정 확인 (회사 네트워크)

---

## ➡️ 다음 단계

VS Code 설정이 완료되었습니다! 이제:

1. 각 주차별 실습을 진행하세요
2. 통합 터미널에서 AWS CLI 명령어를 실행하세요
3. AWS Toolkit으로 리소스를 확인하세요

---

*마지막 업데이트: 2024*
