---

| [⬅️ NACL](./NACL.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 2](../README.md) | [VPC Flow Logs ➡️](./VPC-Flow-Logs.md) |

---

# Security Groups 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** Security Groups는 EC2 인스턴스 및 기타 리소스의 네트워크 트래픽을 제어하기 위한 AWS의 네트워크 보안 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 네트워크 보안 설정이 복잡하고 불완전해 악성 트래픽이 통과할 수 있었습니다.  
  *예: EC2 인스턴스의 포트가 오픈되어 있어 공격자가 직접 접근할 수 있음*  
- **문제 2:** 방화벽 규칙을 관리하는 데 수동으로 설정해야 해서 실수 가능성과 관리 비용이 높았습니다.  
  *예: 매번 인스턴스 생성 시 별도로 방화벽 규칙을 추가해야 함*  
- **문제 3:** 트래픽 흐름을 추적하고 분석하는 기능이 부족해 보안 사고 대응이 어려웠습니다.  
  *예: 로그가 없어 어떤 IP가 어떤 포트를 접근했는지 알 수 없음*  

**Security Groups로 해결:**
- **해결 1:** **포트별 접근 제어**를 통해 공격을 차단합니다.  
  *예: SSH(22포트)만 허용하고 다른 포트는 거부하여 보안 강화*  
- **해결 2:** **중심화된 규칙 관리**로 설정을 간소화합니다.  
  *예: 한 번 설정한 규칙을 여러 인스턴스에 자동 적용 가능*  
- **해결 3:** **VPC Flow Logs**와 연동해 트래픽 흐름을 추적하고 분석합니다.  
  *예: 특정 IP의 이상 트래픽을 실시간으로 감지하여 대응*  

### 비유로 이해하기
**도어맨 역할**을 생각해보세요. 건물의 모든 방문객은 도어맨이 먼저 확인하고, ID를 검증한 후에 들어갑니다. Security Groups도 마찬가지로, 네트워크 트래픽이 VPC 내부로 들어가기 전에 **규칙에 따라 허용/거부**를 결정합니다. 예를 들어, 특정 IP만 SSH 포트(22)에 접근할 수 있도록 규칙을 설정하면, 다른 IP는 거부됩니다. 이처럼 **세부적인 접근 제어**를 통해 네트워크 보안을 강화합니다.

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 웹 서버 보호 | 웹 서버(EC2)에 SSH 접근을 제한하고, HTTP/HTTPS만 허용 |
| 시나리오 2 | 데이터베이스 접근 제한 | RDS 데이터베이스에 특정 IP만 접근 허용 |
| 시나리오 3 | 마이크로서비스 분리 | 서로 다른 VPC에 있는 마이크로서비스 간 통신을 제어 |

**이럴 때 Security Groups를 선택하세요:**
- ✅ **인스턴스 단위의 접근 제어가 필요할 때**  
- ✅ **실시간 트래픽 모니터링이 필요한 경우**  
- ✅ **복잡한 네트워크 아키텍처에서 보안 정책을 일관되게 적용해야 할 때**  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ **네트워크 레벨의 접근 제어가 필요할 때 → NACL**  
  *이유: Security Groups는 인스턴스 단위, NACL은 서브넷 단위 규칙 적용*  
- ❌ **애플리케이션 레벨의 보안이 필요할 때 → WAF**  
  *이유: WAF는 HTTP/HTTPS 요청을 필터링하고, Security Groups는 네트워크 레벨 접근 제어*  
- ❌ **대규모 네트워크 보안 정책을 관리해야 할 때 → Firewall Manager**  
  *이유: Firewall Manager는 다중 VPC 및 리소스에 통일된 보안 정책을 적용 가능*  

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **NACL (Network Access Control List)** | **서브넷 단위의 보안 정책**을 보완합니다. Security Groups는 인스턴스 단위, NACL은 서브넷 단위 규칙 적용 | 예: Security Groups → EC2 인스턴스 → NACL → 서브넷 |
| **VPC Flow Logs** | **트래픽 흐름을 로깅**해 보안 사고 분석에 활용합니다. Security Groups와 결합해 정확한 트래픽 패턴 확인 | 예: EC2 → Security Groups → VPC Flow Logs |
| **Network Firewall** | **고급 네트워크 보안 정책**을 추가합니다. Security Groups와 Network Firewall을 병행해 더 강력한 보안 구현 | 예: Network Firewall → VPC → Security Groups → EC2 |

**자주 사용되는 아키텍처 패턴:**
```
User → CloudFront → S3 (Static Website)  
User → CloudFront → EC2 (Web Server) → Security Groups → RDS (Database)  
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **Security Groups 사용** | AWS Free Tier: 750시간의 EC2 사용량 무료 (Security Groups 자체는 무료) | 월 750시간의 EC2 사용량 무료 |
| **VPC Flow Logs** | $0.10/GB (로그 저장) | 12개월 동안 무료 (일부 서비스) |
| **Network Firewall** | $0.10/GB (데이터 전송) | 12개월 동안 무료 (일부 서비스) |

**비용 최적화 팁:**
1. 💡 **프리티어 활용**: EC2의 750시간 무료 사용량을 극대화해 Security Groups를 사용하세요.  
2. 💡 **정기적인 규칙 검토**: 불필요한 포트 개방을 줄여 불필요한 트래픽을 차단합니다.  
3. 💡 **VPC Flow Logs 최소화**: 로그 저장 비용을 줄이기 위해 필요한 트래픽만 로깅하도록 설정합니다.  

> **⚠️ 비용 주의:** **VPC Flow Logs**는 로그 저장 비용이 발생하므로, **필요한 트래픽만 로깅**하도록 설정해야 합니다. 예를 들어, 모든 트래픽을 로깅하면 데이터 저장 비용이 급격히 증가할 수 있습니다.  

---

## ✅ 실습 예제 (CLI & Console)

### 1. CLI로 Security Group 생성
```bash
aws ec2 create-security-group --group-name my-sg --description "My Security Group" --vpc-id vpc-12345678
```

### 2. CLI로 규칙 추가
```bash
aws ec2 authorize-security-group-ingress --group-id sg-12345678 --ip-permissions '[{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}]'
```

### 3. Console로 규칙 추가
1. AWS 콘솔 → **EC2** → **Security Groups**  
2. 목록에서 **my-sg** 클릭 → **Inbound Rules** 탭  
3. **Edit** → **Add Rule** → **SSH** 선택 → **Save Changes**  

> **💡 Tip:** **SSH 접근**은 보안상 **0.0.0.0/0** 대신 **특정 IP 범위**로 제한하는 것이 좋습니다.  
> **⚠️ 주의:** **0.0.0.0/0**은 모든 IP가 접근 가능해 보안 위험성이 높습니다.  

---

## ✅ 체크리스트 (Checklist)
- [ ] Security Group 생성 및 이름 확인  
- [ ] Inbound/Outbound 규칙 설정 완료  
- [ ] VPC ID 확인 및 연동  
- [ ] 불필요한 포트는 모두 차단  
- [ ] VPC Flow Logs 활성화 여부 확인  
- [ ] CLI/Console 사용 시 권한 확인 (예: `iam user` 권한 부여)  
- [ ] 비용 발생 여부를 주기적으로 모니터링  

> **💡 Tip:** **AWS CloudWatch**를 사용해 Security Group의 트래픽 패턴을 실시간으로 모니터링하세요.

## 📚 핵심 개념

### 개념 1: **Security Groups의 기본 개념 및 역할**
AWS Security Groups는 EC2 인스턴스 및 기타 자원에 대한 네트워크 트래픽을 제어하는 가상 방화벽 역할을 수행합니다. 이는 **인스턴스 레벨**에서 작동하며, **입력 및 출력 트래픽을 필터링**하여 보안을 강화합니다. Security Groups는 **상태 기반**(stateful) 방화벽으로, 연결이 시작된 후 허용된 트래픽은 자동으로 허용됩니다. 예를 들어, HTTP 요청이 허용되면 해당 요청에 대한 응답 트래픽도 자동으로 허용됩니다. 이는 네트워크 보안 정책을 단순화하고, 실시간으로 트래픽을 제어할 수 있는 장점을 제공합니다.

#### 왜 중요한가?
- **자원 보호**: 인스턴스가 외부 네트워크로부터 보호되도록 하여 악성 트래픽을 차단합니다.  
- **고유성**: 각 인스턴스에 고유한 Security Group을 생성해 정책을 세분화할 수 있습니다.  
- **유연성**: 실시간으로 규칙을 수정해 보안 정책을 빠르게 조정할 수 있습니다.  

#### 세부 요소
| 요소 | 설명 | 예시 |
|-----|-----|-----|
| **트래픽 제어 방식** | 입력 및 출력 트래픽을 필터링합니다 | HTTP 요청을 허용하고 SSH 접근을 거부 |
| **상태 기반** | 연결이 시작된 후 허용된 트래픽은 자동으로 허용 | 웹 요청에 대한 응답 트래픽도 허용 |
| **관리 방식** | AWS 콘솔 또는 CLI로 정책을 설정 및 수정 | `aws ec2 describe-security-groups` 명령어 사용 |

> **💡 Tip:** Security Groups는 기본적으로 모든 트래픽을 거부하고, 명시적으로 허용된 트래픽만 허용하므로 "정책 우선" 방식으로 사용해야 합니다. 예를 들어, SSH 접근은 기본적으로 거부되며, 명시적으로 허용해야 합니다.

---

### 개념 2: **VPC Flow Logs의 작동 원리**
VPC Flow Logs는 VPC 내 트래픽 흐름을 로깅하여 네트워크 보안 및 성능 분석에 활용합니다. 이 로그는 **인스턴스, 서브넷, VPC 레벨에서 생성**되며, 모든 트래픽의 출발지, 목적지, 포트, 프로토콜 등을 기록합니다. 이는 **트래픽 이상 탐지**, **보안 사고 분석**, **네트워크 최적화**에 유용합니다. 예를 들어, 의심스러운 트래픽이 발생할 경우 VPC Flow Logs를 통해 원인을 추적할 수 있습니다.

#### 작동 원리
1. **트래픽 모니터링**: VPC 내 모든 트래픽 흐름을 실시간으로 감지합니다.  
2. **로그 생성**: 감지된 트래픽 정보를 JSON 형식의 로그로 저장합니다.  
3. **분석 및 활용**: CloudWatch Logs나 AWS Lambda 등과 연동해 로그를 분석하고, 보안 경고를 생성합니다.  

> **💡 Tip:** VPC Flow Logs는 네트워크 보안 감사 시 필수적인 데이터이며, AWS CLI 명령어 `aws ec2 describe-flow-logs`를 사용해 로그를 확인할 수 있습니다.  

---

### 개념 3: **Network Firewall의 주요 특징**
Network Firewall은 AWS에서 제공하는 **관리형 방화벽 서비스**로, VPC 내에서 **상태 기반의 방화벽 규칙**을 통해 트래픽을 제어합니다. 이는 Security Groups와 함께 사용해 **다중 계층의 보안 정책**을 구축할 수 있습니다. Network Firewall은 **고가용성**, **확장성**, **고성능**을 지원하며, **AWS WAF**와 연동해 DDoS 공격 등을 차단할 수 있습니다. 예를 들어, 특정 IP 범위의 트래픽을 차단하거나, 특정 포트를 제한할 수 있습니다.

#### 주요 특징
1. **상태 기반 규칙**: 연결이 시작된 후 허용된 트래픽은 자동으로 허용됩니다.  
2. **고가용성 및 확장성**: 자동으로 복제되며, 트래픽 증가 시 자동으로 확장됩니다.  
3. **AWS 서비스 통합**: WAF, Shield 등과 연동해 종합 보안 솔루션을 제공합니다.  

> **💡 Tip:** Network Firewall은 Security Groups와 함께 사용해 인스턴스 레벨과 VPC 레벨에서 보안을 병행할 수 있습니다. 예를 들어, Security Groups로 인스턴스 접근을 제어하고, Network Firewall로 네트워크 레벨에서 추가 보호를 제공할 수 있습니다.

## 🖥️ AWS 콘솔에서 Security Groups 사용하기

### Step 1: Security Groups 서비스 접속  
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
   - 로그인 후 **Services** 메뉴에서 **VPC**를 클릭합니다.  
2. 상단 검색창에서 **"Security Groups"**를 입력 후 결과에서 **Security Groups**를 선택합니다.  

> **📸 화면 확인:**  
> - **VPC 대시보드**가 표시되고, **Security Groups** 탭이 활성화된 상태입니다.  
> - 왼쪽 메뉴에서 **Security Groups** 항목이 보여야 합니다.  

---

### Step 2: [주요 작업 1 - 리소스 생성]  
1. **Security Group 생성**  
   - 상단 **Create Security Group** 버튼을 클릭합니다.  
   - **Group Name** 필드에 `MyWebServerSG`를 입력하고, **Description**에 `Web server security group`을 작성합니다.  
   - **VPC** 필드에서 기본 VPC(예: `vpc-12345678`)를 선택합니다.  
   - **Tags**에 필요 시 키-값을 입력합니다.  

2. **규칙 설정**  
   - **Inbound Rules**에서 **HTTP** 포트 80을 허용하고, **SSH** 포트 22를 허용합니다.  
   - **Outbound Rules**에서 **All traffic**를 허용합니다.  

3. **확인 및 생성**  
   - **Create** 버튼을 클릭해 Security Group을 생성합니다.  
   - 생성 후 **Actions > Edit security group**을 통해 설정을 수정할 수 있습니다.  

> **📸 화면 확인:**  
> - **Security Groups** 목록에 생성된 `MyWebServerSG`가 표시됩니다.  
> - **Inbound/Outbound Rules** 탭에서 규칙이 정확히 설정된 상태입니다.  

---

### Step 3: [주요 작업 2 - 설정/구성]  
1. **규칙 수정**  
   - **Edit Security Group**을 클릭해 **Inbound** 규칙을 수정합니다.  
   - 예: 특정 IP 범위(예: `192.168.1.0/24`)를 허용하거나, 포트 443을 추가합니다.  

2. **NACL vs Security Group 비교**  
   - **Network ACL (NACL)**은 Security Group보다 **더 세밀한 네트워크 수준**에서 제어합니다.  
   - NACL은 **IP 기반** 규칙을 사용하며, Security Group은 **프로토콜/포트** 기반입니다.  
   - Security Group은 **VPC 내 리소스 간 통신**을 제어하고, NACL은 **VPC 네트워크 전체**를 보호합니다.  

3. **VPC 흐름 로그 활성화**  
   - **VPC Dashboard > Flow Logs**로 이동해 **Create Flow Log**를 클릭합니다.  
   - **Resource type**에 `vpc`를 선택하고, **Traffic** 필드에서 **ALL**을 선택합니다.  
   - 로그를 저장할 **CloudWatch Logs Group**을 지정합니다.  

> **⚠️ 주의:**  
> - Security Group 규칙은 **정방향**만 적용됩니다. 예: EC2 인스턴스가 외부에 요청을 보내는 경우, **Outbound Rules**에서 허용해야 합니다.  
> - NACL은 **default rules**가 적용되므로, 명시적으로 제외할 규칙을 설정해야 합니다.  

---

### Step 4: 설정 확인 및 테스트  
1. **생성된 리소스 확인**  
   - **Security Groups** 목록에서 `MyWebServerSG`를 선택해 **Description** 및 **Rules**를 확인합니다.  
   - **Actions > View rules**를 클릭해 **Inbound/Outbound** 규칙을 상세히 검토합니다.  

2. **상태 확인**  
   - **EC2 Dashboard**에서 인스턴스를 선택해 **Security Groups** 탭에서 적용된 규칙을 확인합니다.  
   - **VPC Dashboard > Flow Logs**에서 로그를 확인해 트래픽이 제대로 통과하는지 확인합니다.  

3. **정상 동작 테스트**  
   - CLI로 테스트:  
     ```bash
     # SSH 연결 테스트
     ssh -i your-key.pem ec2-user@ec2-instance-public-ip
     # HTTP 요청 테스트
     curl http://ec2-instance-public-ip
     ```
   - **VPC 흐름 로그**에서 요청이 기록되는지 확인합니다.  

> **💡 Tip:**  
> - **AWS Free Tier**는 1개의 Security Group 생성이 가능하며, 1년간 무료입니다.  
> - **Cost Optimization**을 위해 필요 없는 규칙은 삭제하고, **Least Privilege Principle**을 적용하세요.  

---

### ✅ 체크리스트: Security Groups 설정 완료 여부  
- [ ] Security Group 생성 완료  
- [ ] Inbound/Outbound 규칙 설정 완료  
- [ ] NACL vs Security Group 차이 이해 완료  
- [ ] VPC 흐름 로그 활성화 완료  
- [ ] 테스트 환경에서 통신 정상 확인  
- [ ] 비용 관련 주의사항 확인 (프리티어 활용)

## ⌨️ AWS CLI로 Security Groups 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

> **💡 Tip:** CLI 명령어는 `aws ec2` 서비스 명령어를 사용합니다. 모든 명령어는 `ec2` 서비스에 해당합니다.

---

### 예제 1: Security Groups 리소스 조회
```bash
# [Security Groups 리소스 목록 조회]
aws ec2 describe-security-groups --query "[].GroupName" --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| --query | 결과 필터링 | `[].GroupName` |
| --output | 출력 형식 | `json`, `table`, `text` |

**예상 출력:**
```
GroupName
-------
default
my-sg
```

> **⚠️ 주의:** `describe-security-groups` 명령어는 VPC와 Security Groups 간의 관계도 함께 조회합니다. VPC가 없는 경우 기본 Security Group만 표시됩니다.

---

### 예제 2: Security Groups 리소스 생성
```bash
# [Security Groups 리소스 생성]
aws ec2 create-security-group \
    --group-name "example-sg" \
    --description "Example Security Group" \
    --vpc-id "vpc-12345678"
```

**필수 옵션:**
- `--group-name`: Security Group 이름 (1~255자)
- `--description`: 설명 (1~255자)
- `--vpc-id`: VPC ID (생성 시 필수)

**예상 출력:**
```json
{
    "GroupId": "sg-12345678",
    "GroupName": "example-sg",
    "Description": "Example Security Group",
    "VpcId": "vpc-12345678"
}
```

> **💡 Tip:** `--vpc-id`를 생략하면 기본 VPC를 사용합니다. VPC가 없는 경우 `create-security-group` 명령어는 실패합니다.

---

### 예제 3: Security Groups 리소스 수정
```bash
# [Security Groups 규칙 추가]
aws ec2 authorize-security-group-ingress \
    --group-id "sg-12345678" \
    --ip-permissions "[{\"IpProtocol\": \"tcp\", \"FromPort\": 22, \"ToPort\": 22, \"IpRanges\": [{\"CidrIp\": \"0.0.0.0/0\"}]}]"
```

**수정 사항:**
- `authorize-security-group-ingress`: Ingress 규칙 추가
- `revoke-security-group-ingress`: Ingress 규칙 제거
- `authorize-security-group-egress`: Egress 규칙 추가

> **⚠️ 주의:** Security Group는 생성 후 수정이 불가능합니다. 규칙 변경은 기존 규칙을 삭제하고 새로운 규칙을 추가하는 방식으로 수행합니다.

---

### 예제 4: Security Groups 리소스 삭제
```bash
# [Security Groups 리소스 삭제]
aws ec2 delete-security-group --group-id "sg-12345678"

# 삭제 확인
aws ec2 describe-security-groups --group-id "sg-12345678"
```

> **⚠️ 주의:** 삭제는 되돌릴 수 없습니다. 삭제 전에 모든 EC2 인스턴스 및 기타 리소스와의 의존성을 확인하세요.

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws ec2 describe-security-groups
aws ec2 describe-security-groups --group-id "sg-12345678"

# 규칙 관리
aws ec2 authorize-security-group-ingress --group-id "sg-12345678" --ip-permissions "[{...}]"
aws ec2 revoke-security-group-ingress --group-id "sg-12345678" --ip-permission "[{...}]"

# 삭제
aws ec2 delete-security-group --group-id "sg-12345678"
```

> **💡 Tip:** `--ip-permissions` 옵션은 JSON 형식으로 전달해야 합니다. 예시: `"[{\"IpProtocol\": \"tcp\", \"FromPort\": 22, \"ToPort\": 22, \"IpRanges\": [{\"CidrIp\": \"0.0.0.0/0\"}] }]"`

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 Security Groups 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **포인트 1: Security Groups vs NACL 비교**  
   - 설명: 시험에서 가장 자주 출제되는 주제로, **NACL**은 **네트워크 레이어**에서 **비상태적(stateless)** 규칙을 사용해 **하나의 방향만 제어**하고, **Security Groups**는 **애플리케이션 레이어**에서 **상태적(stateful)** 규칙을 사용해 **양방향 통신**을 자동 허용합니다.  
   - 키워드: `NACL`, `stateless`, `stateful`, `layer`

2. **포인트 2: 방향별 규칙 (Inbound/Outbound)**  
   - 설명: Security Groups는 **Inbound**와 **Outbound** 규칙을 별도로 설정해야 하며, 시험에서 규칙의 방향을 실수하지 않도록 주의해야 합니다. 예: SSH는 Inbound에 설정해야 합니다.  
   - 키워드: `Inbound`, `Outbound`, `rule direction`

3. **포인트 3: 상태성(stateful) 특징**  
   - 설명: Security Groups는 **상태를 유지**해 응답 트래픽을 자동으로 허용하므로, **고정 IP**가 필요하지 않으며, **TCP/UDP/ICMP** 트래픽의 응답이 자동 처리됩니다.  
   - 키워드: `stateful`, `response traffic`, `TCP/UDP`

4. **포인트 4: 리소스 연관성**  
   - 설명: Security Groups는 **EC2 인스턴스**, **RDS**, **ELB** 등 다양한 리소스와 연결 가능하며, 시험에서는 특정 리소스에 적용된 규칙을 정확히 파악해야 합니다.  
   - 키워드: `resource association`, `EC2`, `RDS`

5. **포인트 5: 기본 규칙(Default Deny)**  
   - 설명: Security Groups는 **기본적으로 모든 트래픽을 거부**하는 정책을 따르므로, **규칙을 명시적으로 허용**해야 합니다. 실수로 규칙을 빠뜨리면 보안 위험이 발생합니다.  
   - 키워드: `default deny`, `explicit allow`, `security policy`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | "NACL은 상태적이고 Security Groups는 비상태적"이라고 오인할 수 있음 | **NACL는 stateless, Security Groups는 stateful** |
| 함정 2 | "Inbound 규칙만 설정해도 충분하다"고 오해 | **Outbound 규칙도 반드시 설정 필요** |
| 함정 3 | "Security Groups는 IP 범위만 허용"이라고 생각 | **Security Groups는 IP + 포트 + 프로토콜까지 조합 가능** |

#### 🔄 Security Groups vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | Security Groups | Network Firewall | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | **인스턴스/리소스별 접근 제어** | **네트워크 트래픽 필터링** | **리소스 보호** vs **트래픽 모니터링** |
| 확장성 | **리소스당 1개만 적용** | **VPC 전체에 적용 가능** | **유연성** vs **확장성** |
| 비용 | **무료** (프리티어 포함) | **요금제 별도** | **비용 최적화** |
| 지연시간 | **0ms** | **추가 지연 발생** | **성능 최적화** |

#### 📝 시험 대비 체크리스트
- [ ] Security Groups의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  → **리소스에 대한 네트워크 접근 제어**
- [ ] Security Groups를 선택해야 하는 시나리오를 알고 있는가?  
  → **인스턴스 간 통신 보호**, **포트 제어 필요 시**
- [ ] Security Groups의 제한사항/한계를 알고 있는가?  
  → **리소스당 1개만 적용**, **IP 범위만 허용**
- [ ] Security Groups와 Network Firewall의 차이점을 설명할 수 있는가?  
  → **stateful vs stateless**, **리소스별 vs VPC 전체**
- [ ] Security Groups의 비용 구조를 이해하고 있는가?  
  → **프리티어 포함**, **요금 없음**

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 Security Groups를 떠올리세요:  
> - `stateful`  
> - `Inbound/Outbound`  
> - `default deny`  
> - `resource association`  
> - `TCP/UDP`

---

| [⬅️ NACL](./NACL.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 2](../README.md) | [VPC Flow Logs ➡️](./VPC-Flow-Logs.md) |

---
