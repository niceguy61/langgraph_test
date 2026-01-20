# Week 1 Day 3 실습 가이드

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
- [ ] EC2 인스턴스 생성 및 SSH로 접속하여 웹서버 구성
- [ ] AMI 사용하여 빠른 인스턴스 복제
- [ ] EBS 볼륨을 사용하여 데이터 저장 및 관리

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분
- Step 1: 약 10분
- Step 2: 약 15분
- Step 3: 약 10분
- 리소스 정리: 약 5분

---

## 📝 실습 단계

### Step 1: EC2 인스턴스 생성 (약 10분)

#### 1.1 EC2 인스턴스 생성
```bash
# 기본 옵션으로 EC2 인스턴스 생성 (t2.micro 타입, Ubuntu AMI)
aws ec2 run-instances \
  --image-id ami-0c948555173646c23 \
  --count 1 \
  --instance-type t2.micro \
  --key-name MyKeyPair \
  --security-group-ids sg-0a1b2c3d4e5f67890 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=WebServer}]'
```

**예상 출력:**
```
{
  "Instances": [
    {
      "InstanceId": "i-0abcdef1234567890",
      "State": {
        "Name": "running"
      },
      "Tags": [
        {
          "Key": "Name",
          "Value": "WebServer"
        }
      ]
    }
  ]
}
```

> **💡 설명:**  
> - `ami-0c948555173646c23`은 Ubuntu 20.04 LTS AMI ID  
> - `t2.micro`는 AWS 프리티어로 제공되는 무료 타입  
> - `--key-name`은 사전 생성된 SSH 키 쌍을 사용  
> - `--security-group-ids`는 허용되는 트래픽을 제어  

**AWS 콘솔에서:**
1. 서비스 검색창에 `EC2` 입력 후 클릭  
2. 좌측 메뉴에서 `인스턴스` > `인스턴스 생성`  
3. **기본 옵션**에서 `t2.micro` 선택  
4. AMI 선택: `Ubuntu Server 20.04 LTS`  
5. SSH 키 쌍: 사전 생성한 `MyKeyPair.pem` 파일 선택  
6. 보안 그룹: `Default` 또는 새 보안 그룹 생성  
7. 태그 추가: `Name` 키에 `WebServer` 값 입력  
8. 인스턴스 생성 후 `Wait` 상태에서 `Running`으로 전환될 때까지 기다림  

> **📸 화면 확인:**  
> - 인스턴스 목록에서 `WebServer` 태그가 적용된 인스턴스가 표시  
> - 상태가 `Running`으로 변경됨  

#### ✅ Step 1 완료 확인
다음이 보이면 Step 1이 완료된 것입니다:
- [ ] EC2 인스턴스가 생성되고 `Running` 상태로 전환  
- [ ] SSH 키 쌍이 올바르게 연결  
- [ ] 보안 그룹 설정이 완료됨  

---

### Step 2: 웹서버 구성 (약 15분)

#### 2.1 SSH로 인스턴스 접속
```bash
# SSH 접속 명령어 (키 파일 경로를 실제 경로로 변경)
ssh -i "MyKeyPair.pem" ubuntu@ec2-13-123-45-67.compute-1.amazonaws.com
```

> **💡 설명:**  
> - `ubuntu`는 Ubuntu AMI의 기본 사용자  
> - IP 주소는 AWS 콘솔에서 확인 (인스턴스 > Public IP)  
> - `MyKeyPair.pem` 파일은 `.pem` 확장자로 저장되어야 함  

**AWS 콘솔에서:**
1. 인스턴스 목록에서 `WebServer` 인스턴스 클릭  
2. `Connect` 버튼 클릭  
3. SSH 클라이언트 선택: `EC2 Instance Connect` 또는 `SSH Client`  
4. `Copy` 버튼을 눌러 SSH 명령어 복사  
5. `ssh` 명령어를 실행하여 접속  

#### 2.2 웹서버 설치 및 구성
```bash
# Apache 웹서버 설치
sudo apt update
sudo apt install apache2 -y

# 서비스 시작 및 방화벽 설정
sudo systemctl start apache2
sudo ufw allow 80
sudo ufw enable
```

**예상 출력:**
```
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following NEW packages will be installed:
  apache2
0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
Need to download new packages: 1.2 MB
After this operation, 15.8 MB of additional disk space will be used.
Do you want to continue? [Y/n] y
```

> **💡 설명:**  
> - `apt update`는 패키지 목록 갱신  
> - `apache2` 설치 후 `systemctl`로 서비스 시작  
> - `ufw`는 Ubuntu의 방화벽 도구로 80번 포트(HTTP) 허용  

#### ✅ Step 2 완료 확인
다음이 보이면 Step 2가 완료된 것입니다:
- [ ] SSH로 인스턴스에 성공적으로 접속  
- [ ] Apache 웹서버가 실행 중인 상태  
- [ ] 웹 브라우저에서 `http://<Public IP>` 접속 시 기본 웹 페이지가 표시  

---

### Step 3: AMI 생성 및 복제 (약 10분)

#### 3.1 AMI 생성
```bash
# 인스턴스에서 AMI 생성
aws ec2 create-image \
  --instance-id i-0abcdef1234567890 \
  --name "WebServer-AMI" \
  --description "WebServer with Apache2"
```

**예상 출력:**
```
{
  "ImageId": "ami-09876543210987654"
}
```

> **💡 설명:**  
> - `--name`은 AMI의 이름  
> - `--description`은 AMI 설명  
> - 생성된 AMI는 `EC2 Console > AMIs`에서 확인 가능  

**AWS 콘솔에서:**
1. 인스턴스 목록에서 `WebServer` 인스턴스 클릭  
2. `Actions` > `Image` > `Create Image`  
3. 이름 및 설명 입력 후 생성  

#### 3.2 AMI 기반 인스턴스 복제
```bash
# AMI 기반 인스턴스 생성
aws ec2 run-instances \
  --image-id ami-09876543210987654 \
  --count 1 \
  --instance-type t2.micro \
  --key-name MyKeyPair \
  --security-group-ids sg-0a1b2c3d4e5f67890 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=WebServerCopy}]'
```

> **💡 설명:**  
> - 생성된 AMI를 기반으로 새로운 인스턴스 생성  
> - 이 방법은 동일한 설정으로 빠르게 인스턴스 복제 가능  

#### ✅ Step 3 완료 확인
다음이 보이면 Step 3가 완료된 것입니다:
- [ ] AMI 생성 및 저장 완료  
- [ ] AMI 기반 인스턴스가 생성됨  
- [ ] 두 인스턴스 모두 웹서버 작동 확인  

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] EC2 인스턴스 생성 및 SSH 접속 완료  
- [ ] Apache 웹서버 작동 확인  
- [ ] AMI 생성 및 복제 완료  

### 예상 최종 결과
```bash
# 웹서버 상태 확인
curl http://ec2-13-123-45-67.compute-1.amazonaws.com
```

**예상 출력:**
```
<!doctype html><html><head><title>Apache2 Ubuntu Default Page</title>
...
</head><body><h1>Apache2 Ubuntu Default Page</h1>
...
</body></html>
```

---

## 🔧 트러블슈팅

### 문제 1: SSH 접속 실패
**증상:** `Permission denied (publickey)` 오류  
**원인:** 키 파일 경로 오류 또는 키 권한 문제  
**해결 방법:**
1. `chmod 400 MyKeyPair.pem` 명령어로 키 파일 권한 변경  
2. `ssh -i MyKeyPair.pem ubuntu@IP` 형식으로 명령어 재실행  

### 문제 2: 웹서버 접근 거부
**증상:** 브라우저 접속 시 오류 발생  
**원인:** 보안 그룹 설정 오류  
**해결 방법:**
1. AWS 콘솔에서 보안 그룹 설정 확인  
2. `HTTP` 트래픽을 허용하는 규칙이 있는지 확인  

### 문제 3: 권한 오류 (AccessDenied)
**증상:** `AccessDenied` 또는 `UnauthorizedAccess` 오류  
**해결 방법:**
1. IAM 사용자 권한 확인  
2. `AmazonEC2FullAccess` 정책 연결  
```bash
# 현재 사용자 권한 확인
aws sts get-caller-identity
```

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!  
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] EC2 인스턴스 (WebServer, WebServerCopy)  
- [ ] AMI (WebServer-AMI)  
- [ ] EBS 볼륨 (필요 시)  

### 리소스 정리 명령어
```bash
# 1. EC2 인스턴스 종료
aws ec2 terminate-instances --instance-ids i-0abcdef1234567890 i-09876543210987654

# 2. AMI 삭제
aws ec2 deregister-image --image-id ami-09876543210987654

# 3. 삭제 확인
aws ec2 describe-instances --instance-ids i-0abcdef1234567890 i-09876543210987654
```

### 정리 완료 확인
```bash
# 리소스가 모두 삭제되었는지 확인
aws ec2 describe-instances
```

---

## 📚 추가 학습 자료
- [AWS EC2 공식 문서](https://docs.aws.amazon.com/ko-kr/ec2/)  
- [AMI 사용 가이드](https://docs.aws.amazon.com/ko-kr/AWSEC2/latest/UserGuide/AMIs.html)  
- [EBS 볼륨 관리 튜토리얼](https://docs.aws.amazon.com/ko-kr/AWSEC2/latest/UserGuide/EBSVolumeManagement.html)