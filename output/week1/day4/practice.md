# Week 1 Day 4 실습 가이드

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
- [ ] EBS 볼륨 생성 및 인스턴스에 연결
- [ ] EBS 스냅샷 생성 및 관리
- [ ] 보안 그룹 규칙을 통해 트래픽 제어

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분
- Step 1: 약 10분
- Step 2: 약 15분
- Step 3: 약 10분
- 리소스 정리: 약 5분

---

## 📝 실습 단계

### Step 1: EBS 볼륨 생성 및 인스턴스 연결 (약 10분)

#### 1.1 EBS 볼륨 생성
**AWS CLI 명령어:**
```bash
aws ec2 create-volume --availability-zone ap-northeast-2a --size 20 --volume-type gp3
```

**예상 출력:**
```
{
    "VolumeId": "vol-0abcdef1234567890"
}
```

> **💡 설명:**  
> - `--availability-zone`: 볼륨을 배치할 존 선택 (예: `ap-northeast-2a`)  
> - `--size`: 볼륨 크기 (GB 단위)  
> - `--volume-type`: 볼륨 유형 (gp3, io2, st1, sc1 중 선택)  
> - `gp3`는 일반적인 IOPS/Throughput 성능을 제공하는 볼륨 유형입니다.

#### 1.2 EBS 볼륨 인스턴스에 연결
**AWS CLI 명령어:**
```bash
aws ec2 attach-volume --volume-id vol-0abcdef1234567890 --instance-id i-01234567890abcdef --device /dev/sdh
```

**예상 출력:**
```
{
    "Attachments": [
        {
            "AttachTime": "2023-10-05T08:00:00.000Z",
            "Device": "/dev/sdh",
            "State": "attached",
            "VolumeId": "vol-0abcdef1234567890"
        }
    ]
}
```

> **📸 화면 확인:**  
> AWS 콘솔에서 **EC2 > Volumes** 탭에서 생성한 볼륨이 `attached` 상태인지 확인합니다.

#### ✅ Step 1 완료 확인
- [ ] `vol-0abcdef1234567890` 볼륨 생성 완료  
- [ ] 볼륨이 인스턴스 `i-01234567890abcdef`에 연결됨

---

### Step 2: EBS 스냅샷 생성 및 관리 (약 15분)

#### 2.1 EBS 스냅샷 생성
**AWS CLI 명령어:**
```bash
aws ec2 create-snapshot --volume-id vol-0abcdef1234567890 --description "Backup for my EC2 instance"
```

**예상 출력:**
```
{
    "SnapshotId": "snap-01234567890abcdef"
}
```

> **💡 설명:**  
> - `--description`: 스냅샷 설명 (관리 용도)  
> - 스냅샷 생성 시 볼륨이 `detached` 상태가 되며, 볼륨이 다시 연결되어야 합니다.

#### 2.2 스냅샷 상태 확인
**AWS CLI 명령어:**
```bash
aws ec2 describe-snapshots --snapshot-ids snap-01234567890abcdef
```

**예상 출력:**
```
{
    "Snapshots": [
        {
            "SnapshotId": "snap-01234567890abcdef",
            "VolumeId": "vol-0abcdef1234567890",
            "State": "completed",
            "OwnerId": "123456789012",
            "Description": "Backup for my EC2 instance"
        }
    ]
}
```

> **📸 화면 확인:**  
> AWS 콘솔에서 **EC2 > Snapshots** 탭에서 스냅샷이 `completed` 상태인지 확인합니다.

#### ✅ Step 2 완료 확인
- [ ] `snap-01234567890abcdef` 스냅샷 생성 완료  
- [ ] 스냅샷 상태가 `completed`로 변경됨

---

### Step 3: 보안 그룹 설정 (약 10분)

#### 3.1 보안 그룹 생성
**AWS CLI 명령어:**
```bash
aws ec2 create-security-group --group-name MySecurityGroup --description "Allow SSH and HTTP"
```

**예상 출력:**
```
{
    "GroupId": "sg-0abcdef1234567890"
}
```

> **💡 설명:**  
> - `--group-name`: 보안 그룹 이름  
> - `--description`: 보안 그룹 설명 (관리 용도)

#### 3.2 보안 규칙 추가
**AWS CLI 명령어:**
```bash
aws ec2 authorize-security-group-ingress --group-id sg-0abcdef1234567890 --protocol tcp --port-range 22,80 --cidr 0.0.0.0/0
```

**예상 출력:**
```
{
    "Return": true
}
```

> **📸 화면 확인:**  
> AWS 콘솔에서 **EC2 > Security Groups** 탭에서 생성한 보안 그룹이 `MySecurityGroup`인지 확인하고, 허용 규칙이 `SSH (22)` 및 `HTTP (80)`인지 확인합니다.

#### ✅ Step 3 완료 확인
- [ ] `MySecurityGroup` 보안 그룹 생성 완료  
- [ ] `22` 및 `80` 포트가 `0.0.0.0/0`으로 허용됨

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] EBS 볼륨 생성 및 인스턴스 연결 완료
- [ ] EBS 스냅샷 생성 및 상태 확인 완료
- [ ] 보안 그룹 생성 및 규칙 설정 완료

### 예상 최종 결과
```bash
# EBS 볼륨 상태 확인
aws ec2 describe-volumes --volume-ids vol-0abcdef1234567890
```

**예상 출력:**
```
{
    "Volumes": [
        {
            "Attachments": [
                {
                    "AttachTime": "2023-10-05T08:00:00.000Z",
                    "Device": "/dev/sdh",
                    "State": "attached",
                    "VolumeId": "vol-0abcdef1234567890"
                }
            ],
            "CreateTime": "2023-10-05T07:00:00.000Z",
            "Size": 20,
            "State": "in-use",
            "VolumeId": "vol-0abcdef1234567890"
        }
    ]
}
```

---

## 🔧 트러블슈팅

### 문제 1: `InvalidVolume.NotFound` 오류
**증상:**  
```bash
An error occurred (InvalidVolume.NotFound) when calling the AttachVolume operation: The volume 'vol-0abcdef1234567890' does not exist.
```

**원인:**  
볼륨 ID가 잘못 입력되었거나, 볼륨이 삭제되었을 수 있습니다.

**해결 방법:**
1. `aws ec2 describe-volumes`로 존재 여부 확인
2. `aws ec2 delete-volume --volume-id vol-0abcdef1234567890`로 삭제된 볼륨 제거

### 문제 2: `AuthorizationRequired` 오류
**증상:**  
```bash
An error occurred (AuthorizationRequired) when calling the CreateVolume operation: You are unauthorized to perform this operation.
```

**원인:**  
IAM 사용자 권한 부족

**해결 방법:**
1. IAM 사용자에 `AmazonEC2FullAccess` 정책 부여
2. `aws sts get-caller-identity`로 사용자 확인

### 문제 3: 권한 오류 (AccessDenied)
**증상:** `AccessDenied` 또는 `UnauthorizedAccess` 오류

**해결 방법:**
1. IAM 사용자 권한 확인
2. 필요한 정책 연결
```bash
# 현재 사용자 권한 확인
aws sts get-caller-identity
```

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!  
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] EBS 볼륨 `vol-0abcdef1234567890`
- [ ] 스냅샷 `snap-01234567890abcdef`
- [ ] 보안 그룹 `MySecurityGroup`

### 리소스 정리 명령어
```bash
# 1. EBS 볼륨 삭제
aws ec2 delete-volume --volume-id vol-0abcdef1234567890

# 2. 스냅샷 삭제
aws ec2 delete-snapshot --snapshot-id snap-01234567890abcdef

# 3. 보안 그룹 삭제
aws ec2 delete-security-group --group-id sg-0abcdef1234567890
```

### 정리 완료 확인
```bash
# 리소스가 모두 삭제되었는지 확인
aws ec2 describe-volumes --filters Name=status-name,Values=in-use
aws ec2 describe-snapshots --filters Name=status-name,Values=completed
aws ec2 describe-security-groups --group-ids sg-0abcdef1234567890
```

---

## 📚 추가 학습 자료
- [AWS EBS 공식 문서](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volumes.html)
- [AWS EFS 공식 문서](https://docs.aws.amazon.com/efs/latest/ug/whatis-efs.html)
- [AWS Security Groups 공식 문서](https://docs.aws.amazon.com/vpc/latest/userguide/security-groups.html)