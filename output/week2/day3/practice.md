# Week 2 Day 3 실습 가이드

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
- [ ] NACL을 사용하여 VPC 내 리소스의 네트워크 트래픽을 제어할 수 있다
- [ ] NACL과 Security Group의 차이점 및 사용 시나리오를 이해할 수 있다
- [ ] VPC 흐름 로그를 설정하여 네트워크 트래픽을 모니터링할 수 있다

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분
- Step 1: 약 10분
- Step 2: 약 15분
- Step 3: 약 10분
- 리소스 정리: 약 5분

---

## 📝 실습 단계

### Step 1: VPC 및 리소스 생성 (약 10분)

#### 1.1 VPC 생성
```bash
# VPC 생성 (CIDR: 10.0.0.0/16)
aws ec2 create-vpc --cidr 10.0.0.0/16 --tags Key=Name,Value=MyVPC
```

**예상 출력:**
```
{
    "Vpc": {
        "VpcId": "vpc-0abcdef1234567890",
        "State": "pending",
        "CidrBlock": "10.0.0.0/16",
        ...
    }
}
```

> **💡 설명:** `create-vpc` 명령어는 CIDR 블록을 지정해 VPC를 생성합니다. 생성된 VPC ID는 이후 작업에서 사용됩니다.

#### 1.2 서브넷 생성
**AWS 콘솔에서:**
1. 서비스 검색창에 "VPC" 입력
2. "Virtual Private Cloud (VPC)" 클릭
3. "Subnets" 탭에서 "Create subnet" 클릭
4. CIDR: `10.0.1.0/24`, VPC 선택 후 "Create" 클릭

> **📸 화면 확인:** "MyVPC" 이름으로 생성된 서브넷이 목록에 표시됩니다.

#### ✅ Step 1 완료 확인
- [ ] VPC 생성 완료 (VPC ID 확인)
- [ ] 서브넷 생성 완료 (서브넷 ID 확인)

---

### Step 2: NACL 및 Security Group 구성 (약 15분)

#### 2.1 NACL 생성
```bash
# NACL 생성 (VPC ID 사용)
aws ec2 create-network-acl --vpc-id vpc-0abcdef1234567890 --tags Key=Name,Value=MyNACL
```

**예상 출력:**
```
{
    "NetworkAcl": {
        "NetworkAclId": "acl-0123456789abcdef0",
        "VpcId": "vpc-0abcdef1234567890",
        ...
    }
}
```

> **💡 설명:** NACL은 VPC 수준에서 기본 규칙을 적용합니다. 기본 규칙은 모든 트래픽을 거부합니다.

#### 2.2 NACL 규칙 추가
```bash
# 허용 규칙 추가 (SSH 포트 22)
aws ec2 create-network-acl-rule --network-acl-id acl-0123456789abcdef0 \
--rule-number 100 --priority 100 \
--action allow --rule-number 100 \
--protocol tcp --port-range FromPort=22 ToPort=22 \
--rule-action allow --egress false --dry-run false
```

**예상 출력:**
```
{
    "Return": true
}
```

> **💡 설명:** NACL의 규칙은 우선순위(100)로 설정됩니다. 기본 규칙은 1000으로, 사용자 정의 규칙은 100으로 설정해 우선순위를 조정합니다.

#### 2.3 Security Group 생성
**AWS 콘솔에서:**
1. "Security Groups" 탭에서 "Create security group" 클릭
2. 이름: `MySG`, VPC: `MyVPC` 선택
3. 규칙: "SSH" 허용 (포트 22) 후 "Create" 클릭

> **📸 화면 확인:** "MySG" 이름으로 생성된 Security Group이 표시됩니다.

#### ✅ Step 2 완료 확인
- [ ] NACL 생성 및 규칙 추가 완료
- [ ] Security Group 생성 및 SSH 허용 규칙 추가 완료

---

### Step 3: VPC 흐름 로그 설정 (약 10분)

#### 3.1 흐름 로그 활성화
```bash
# VPC 흐름 로그 생성
aws ec2 create-flow-logs --resource-ids vpc-0abcdef1234567890 \
--traffic-type All --log-destination-type cloudwatch \
--log-destination "cloudwatch-logs://MyVPC-FlowLogs"
```

**예상 출력:**
```
{
    "FlowLog": {
        "FlowLogId": "flow-log-0123456789abcdef0",
        ...
    }
}
```

> **💡 설명:** 흐름 로그는 CloudWatch Logs로 전송됩니다. 로그 그룹 이름은 `MyVPC-FlowLogs`로 설정해야 합니다.

#### 3.2 로그 확인
**AWS 콘솔에서:**
1. "CloudWatch" 서비스로 이동
2. "Logs" 탭에서 "MyVPC-FlowLogs" 로그 그룹 확인
3. 로그 항목이 10분 이내에 생성되는지 확인

> **📸 화면 확인:** 로그 항목이 정상적으로 생성되고 있는지 확인합니다.

#### ✅ Step 3 완료 확인
- [ ] VPC 흐름 로그 생성 완료
- [ ] CloudWatch Logs에서 로그 확인 완료

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] NACL 생성 및 규칙 설정 완료
- [ ] Security Group 생성 및 SSH 허용 완료
- [ ] VPC 흐름 로그 활성화 완료

### 예상 최종 결과
```bash
# NACL 상태 확인
aws ec2 describe-network-acls --network-acl-ids acl-0123456789abcdef0
```

**예상 출력:**
```
{
    "NetworkAcls": [
        {
            "NetworkAclId": "acl-0123456789abcdef0",
            "SubnetIds": [...],
            "Entries": [
                {"RuleNumber": 100, "RuleAction": "allow", ...},
                ...
            ]
        }
    ]
}
```

---

## 🔧 트러블슈팅

### 문제 1: VPC 생성 오류
**증상:** `InvalidVpcId.NotFound` 오류 발생  
**원인:** 잘못된 VPC ID 사용  
**해결 방법:**
```bash
# VPC 목록 확인
aws ec2 describe-vpcs
```

### 문제 2: NACL 규칙 적용 안됨
**증상:** 허용 규칙이 적용되지 않음  
**원인:** 규칙 우선순위가 기본 규칙(1000)보다 낮아야 함  
**해결 방법:**
```bash
# 규칙 우선순위 수정
aws ec2 create-network-acl-rule --network-acl-id acl-0123456789abcdef0 \
--rule-number 100 --priority 100 \
--action allow --protocol tcp --port-range FromPort=22 ToPort=22 \
--rule-action allow --egress false
```

### 문제 3: 권한 오류 (AccessDenied)
**증상:** `AccessDenied` 또는 `UnauthorizedAccess` 오류  
**해결 방법:**
1. IAM 사용자 권한 확인
2. `ec2:CreateNetworkAcl`, `ec2:CreateFlowLogs` 권한 추가
```bash
# 현재 사용자 권한 확인
aws sts get-caller-identity
```

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] VPC (vpc-0abcdef1234567890)
- [ ] NACL (acl-0123456789abcdef0)
- [ ] Flow Logs (flow-log-0123456789abcdef0)

### 리소스 정리 명령어
```bash
# 1. VPC 삭제
aws ec2 delete-vpc --vpc-id vpc-0abcdef1234567890

# 2. NACL 삭제
aws ec2 delete-network-acl --network-acl-id acl-0123456789abcdef0

# 3. Flow Logs 삭제
aws ec2 delete-flow-logs --flow-log-ids flow-log-0123456789abcdef0
```

### 정리 완료 확인
```bash
# 리소스가 모두 삭제되었는지 확인
aws ec2 describe-vpcs
aws ec2 describe-network-acls
aws ec2 describe-flow-logs
```

---

## 📚 추가 학습 자료
- [AWS VPC 공식 문서](https://docs.aws.amazon.com/vpc/latest/userguide/)
- [NACL vs Security Group 비교 가이드](https://aws.amazon.com/ko/networking/vpc/)
- [VPC Flow Logs 설정 튜토리얼](https://aws.amazon.com/ko/getting-started/tutorials/setting-up-vpc-flow-logs/)