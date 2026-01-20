# Week 2 Day 2 실습 가이드

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
- [ ] VPC Peering 연결을 생성하고 라우팅 테이블을 구성할 수 있다
- [ ] VPC 간의 네트워크 통신을 테스트할 수 있다
- [ ] VPC Peering 연결을 정리하고 비용을 최소화할 수 있다

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분
- Step 1: 약 10분
- Step 2: 약 15분
- Step 3: 약 10분
- 리소스 정리: 약 5분

---

## 📝 실습 단계

### Step 1: VPC Peering 연결 생성 (약 10분)

#### 1.1 [세부 단계] VPC 생성 및 설정
```bash
# 2개의 VPC 생성 (VPC 1과 VPC 2)
aws ec2 create-vpc --cidr 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=VPC1}]'
aws ec2 create-vpc --cidr 10.1.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=VPC2}]'
```

**예상 출력:**
```
{
    "Vpc": {
        "VpcId": "vpc-0abcdef1234567890",
        "InstanceId": "i-1234567890abcdef0",
        ...
    }
}
```

> **💡 설명:**  
> 1. `create-vpc` 명령어로 두 개의 VPC를 생성합니다.  
> 2. `--tag-specifications` 옵션으로 VPC 이름을 설정해 편리하게 관리합니다.  
> 3. VPC 생성 후 `aws ec2 describe-vpcs` 명령어로 생성된 VPC를 확인할 수 있습니다.

#### 1.2 [세부 단계] VPC Peering 연결 생성
**AWS 콘솔에서:**
1. 서비스 검색창에 `VPC` 입력 후 클릭
2. 왼쪽 메뉴에서 **Peering Connections** → **Create Peering Connection** 선택
3. **Peering Connection Name** 입력 후 **Request Peering Connection** 클릭

> **📸 화면 확인:**  
> 1. **Peering Connection** 탭에서 생성된 연결이 보이면 정상입니다.  
> 2. **Status**가 `Pending Acceptance`로 표시되어야 합니다.

#### ✅ Step 1 완료 확인
다음이 보이면 Step 1이 완료된 것입니다:
- [ ] 두 개의 VPC가 생성되었고 이름이 설정됨
- [ ] Peering Connection이 생성되었고 상태가 `Pending Acceptance`임

---

### Step 2: VPC Peering 연결 수락 및 라우팅 설정 (약 15분)

#### 2.1 [세부 단계] Peering 연결 수락
**AWS 콘솔에서:**
1. **Peering Connections** 탭에서 생성된 연결을 선택
2. **Actions** → **Accept Peering Connection** 클릭
3. **Accept** 버튼 클릭

> **💡 설명:**  
> 1. Peering 연결은 수락해야만 통신이 가능합니다.  
> 2. 수락 후 두 VPC 간의 네트워크 통신이 가능해집니다.

#### 2.2 [세부 단계] 라우팅 테이블 구성
```bash
# VPC1의 라우팅 테이블 생성
aws ec2 create-route-table --vpc-id vpc-0abcdef1234567890

# VPC2의 라우팅 테이블 생성
aws ec2 create-route-table --vpc-id vpc-01234567890abcdef
```

**예상 출력:**
```
{
    "RouteTable": {
        "RouteTableId": "rtb-01234567890abcdef",
        ...
    }
}
```

> **💡 설명:**  
> 1. 라우팅 테이블은 VPC 내부에서 네트워크 트래픽을 제어하는 핵심 구성 요소입니다.  
> 2. 라우팅 테이블을 생성한 후, `create-route` 명령어로 Peering 연결을 구성해야 합니다.

#### ✅ Step 2 완료 확인
다음이 보이면 Step 2가 완료된 것입니다:
- [ ] Peering 연결이 수락되었고 상태가 `Active`임
- [ ] 라우팅 테이블이 생성되었고 ID가 확인됨

---

### Step 3: 네트워크 통신 테스트 (약 10분)

#### 3.1 [세부 단계] 라우팅 규칙 추가
```bash
# VPC1의 라우팅 테이블에 VPC2 CIDR 추가
aws ec2 create-route --route-table-id rtb-01234567890abcdef \
--destination-cidr-block 10.1.0.0/16 \
--transit-gateway-id tgw-0abcdef1234567890

# VPC2의 라우팅 테이블에 VPC1 CIDR 추가
aws ec2 create-route --route-table-id rtb-0abcdef1234567890 \
--destination-cidr-block 10.0.0.0/16 \
--transit-gateway-id tgw-01234567890abcdef
```

> **💡 설명:**  
> 1. `create-route` 명령어로 라우팅 규칙을 추가합니다.  
> 2. Peering 연결을 통해 다른 VPC의 CIDR 범위에 접근할 수 있도록 설정합니다.

#### 3.2 [세부 단계] 인스턴스 생성 및 통신 테스트
```bash
# VPC1에 EC2 인스턴스 생성
aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 \
--count 1 --instance-type t2.micro \
--subnet-id subnet-0abcdef1234567890 \
--security-group-ids sg-01234567890abcdef

# VPC2에 EC2 인스턴스 생성
aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 \
--count 1 --instance-type t2.micro \
--subnet-id subnet-01234567890abcdef \
--security-group-ids sg-0abcdef1234567890
```

**예상 출력:**
```
{
    "Instances": [
        {
            "InstanceId": "i-01234567890abcdef",
            ...
        }
    ]
}
```

> **💡 설명:**  
> 1. 두 VPC에 EC2 인스턴스를 생성해 통신 테스트를 수행합니다.  
> 2. 인스턴스 생성 후 `ssh` 명령어로 서로의 IP 주소에 접속해 통신이 가능한지 확인합니다.

#### ✅ Step 3 완료 확인
다음이 보이면 Step 3가 완료된 것입니다:
- [ ] 라우팅 규칙이 추가되고 상태가 `active`임
- [ ] 두 인스턴스 간의 SSH 통신이 성공적으로 이루어짐

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] VPC Peering 연결이 생성되고 수락됨
- [ ] 라우팅 테이블과 라우팅 규칙이 구성됨
- [ ] EC2 인스턴스 간 통신이 성공적으로 이루어짐

### 예상 최종 결과
```bash
# 인스턴스 IP 확인
aws ec2 describe-instances --filters Name=vpc-id,Values=vpc-0abcdef1234567890
```

**예상 출력:**
```
{
    "Reservations": [
        {
            "Instances": [
                {
                    "InstanceId": "i-01234567890abcdef",
                    "PrivateIpAddress": "10.0.0.10",
                    ...
                }
            ]
        }
    ]
}
```

---

## 🔧 트러블슈팅

### 문제 1: `InvalidVpcId` 오류
**증상:**  
```
An error occurred (InvalidVpcId) when calling the CreateVpc operation: The vpc ID 'vpc-01234567890abcdef' does not exist.
```

**원인:**  
VPC ID가 잘못 입력되었거나 생성되지 않았습니다.

**해결 방법:**
```bash
# VPC 목록 확인
aws ec2 describe-vpcs
```

### 문제 2: 라우팅 테이블 구성 실패
**증상:**  
```
An error occurred (InvalidRouteTableId) when calling the CreateRoute operation: The route table ID 'rtb-01234567890abcdef' does not exist.
```

**원인:**  
라우팅 테이블이 생성되지 않았거나 ID가 잘못 입력되었습니다.

**해결 방법:**
```bash
# 라우팅 테이블 생성 확인
aws ec2 create-route-table --vpc-id vpc-0abcdef1234567890
```

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!  
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] EC2 인스턴스
- [ ] VPC
- [ ] 라우팅 테이블
- [ ] Peering 연결

### 리소스 정리 명령어
```bash
# 1. EC2 인스턴스 종료
aws ec2 terminate-instances --instance-ids i-01234567890abcdef

# 2. VPC 삭제
aws ec2 delete-vpc --vpc-id vpc-0abcdef1234567890
aws ec2 delete-vpc --vpc-id vpc-01234567890abcdef

# 3. 라우팅 테이블 삭제
aws ec2 delete-route-table --route-table-id rtb-01234567890abcdef
aws ec2 delete-route-table --route-table-id rtb-0abcdef1234567890

# 4. Peering 연결 해지
aws ec2 delete-vpc-peering-connection --vpc-peering-connection-id pcx-0abcdef1234567890
```

### 정리 완료 확인
```bash
# 리소스가 모두 삭제되었는지 확인
aws ec2 describe-vpcs
aws ec2 describe-instances
```

---

## 📚 추가 학습 자료
- [AWS VPC Peering 공식 문서](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-peering.html)
- [AWS Transit Gateway 튜토리얼](https://docs.aws.amazon.com/vpc/latest/tg/what-is-transit-gateway.html)
- [AWS VPC Endpoints 가이드](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints.html)