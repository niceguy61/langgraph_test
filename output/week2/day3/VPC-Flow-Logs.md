---

| [⬅️ Security Groups](./Security-Groups.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 2](../README.md) | [Network Firewall ➡️](./Network-Firewall.md) |

---

# VPC Flow Logs 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** VPC Flow Logs는 AWS의 네트워크 트래픽을 실시간으로 모니터링하고 분석하여 보안 및 성능 최적화를 지원하는 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 네트워크 트래픽을 수동으로 점검해야 하며, 이는 시간이 많이 소요되고 오류가 발생할 수 있습니다. 예를 들어, 특정 IP의 비정상적인 접근이 발생했을 때 수동으로 로그를 확인해야 했습니다.
- **문제 2:** 트래픽 패턴을 파악하기 어려워 보안 위협을 사전에 탐지하기 어려웠습니다. 예를 들어, DDoS 공격이 발생했을 때 정확한 원인을 분석하는 데 시간이 많이 걸렸습니다.
- **문제 3:** 네트워크 지연이나 성능 문제를 해결하기 위해 트래픽 흐름을 분석해야 했지만, 이 과정이 복잡하고 비효율적이었습니다.

**VPC Flow Logs로 해결:**
- **해결 1:** AWS가 자동으로 VPC 내 모든 네트워크 트래픽을 로깅하여 실시간으로 모니터링할 수 있습니다. 예를 들어, 특정 IP의 비정상 접근 시 알림을 즉시 제공합니다.
- **해결 2:** 트래픽 패턴을 분석하여 보안 위협을 사전에 탐지하고 대응할 수 있습니다. 예를 들어, DDoS 공격이 발생했을 때 트래픽 흐름을 분석해 공격원을 식별합니다.
- **해결 3:** 네트워크 성능을 최적화하기 위해 트래픽 흐름을 분석해 지연 요인을 파악하고 개선할 수 있습니다. 예를 들어, 특정 서버 간 트래픽이 지연되고 있을 경우 원인을 분석합니다.

### 비유로 이해하기
VPC Flow Logs는 도로에 설치된 고속카메라처럼 모든 차량의 이동 경로를 실시간으로 기록합니다. 이를 통해 사고나 교통체증을 사전에 발견하고, 교통 흐름을 최적화할 수 있습니다. 이처럼 네트워크 트래픽을 기록해 보안 및 성능 문제를 예방합니다.

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 보안 모니터링 | 기업이 내부 서버에 대한 비정상적 접근을 감시하고, 사전에 공격을 차단 |
| 시나리오 2 | 네트워크 성능 최적화 | 클라우드 서버 간 지연이 발생했을 때 트래픽 흐름을 분석해 원인을 파악 |
| 시나리오 3 | 규제 준수 | 데이터 보호 규정(예: GDPR)에 따라 네트워크 트래픽 기록을 보관 및 감사 |

**이럴 때 VPC Flow Logs를 선택하세요:**
- ✅ **보안 모니터링**에 필요한 실시간 트래픽 분석
- ✅ **네트워크 성능 개선**을 위해 트래픽 패턴 분석
- ✅ **규제 준수**를 위한 기록 보존 및 감사

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ **웹 트래픽 보호** → **WAF** (웹 애플리케이션 방화벽) 사용
- ❌ **DDoS 공격 대응** → **Shield** (DDoS 방어 서비스) 사용
- ❌ **네트워크 보안 정책 관리** → **Firewall Manager** (일관된 보안 정책 적용)

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **Network Firewall** | 보안 위협 탐지 후 VPC Flow Logs로 세부 분석 | User → Network Firewall → VPC Flow Logs → CloudWatch |
| **WAF** | 웹 트래픽 필터링 후 VPC Flow Logs로 비정상 트래픽 추적 | User → CloudFront → WAF → VPC Flow Logs |
| **Shield** | DDoS 공격 대응 후 VPC Flow Logs로 공격원 분석 | User → Shield → VPC Flow Logs → AWS WAF |

**자주 사용되는 아키텍처 패턴:**
```
User → CloudFront → WAF → VPC Flow Logs → CloudWatch
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **VPC Flow Logs 생성 및 저장** | $0.01/GB/월 | 12개월 무료 (10GB) |
| **CloudWatch Logs 분석** | $0.006/GB/월 | 월 1GB 무료 |
| **S3 저장소 사용** | $0.023/GB/월 | 5GB 무료 (1년) |

**비용 최적화 팁:**
1. 💡 **로그 압축**: 로그를 Gzip 형식으로 압축해 저장 비용 절감
2. 💡 **S3 스토리지 클래스**: infrequent access 또는 glacier 클래스로 장기 보관 비용 최소화
3. 💡 **로그 보존 정책**: 불필요한 로그는 삭제하거나 CloudWatch에서 자동 제거 설정

> **⚠️ 비용 주의:** 고사양 VPC(예: 100개 이상의 서브넷)에서는 예상치 못한 저장 비용이 발생할 수 있으므로, 저장소 크기와 로그 보존 기간을 주기적으로 점검해야 합니다.

## 📚 핵심 개념

### 개념 1: 네트워크 보안 정책: NACL vs 보안 그룹
VPC에서 네트워크 보안을 담당하는 두 주요 메커니즘인 **NACL(Network Access Control List)**과 **보안 그룹**은 서로 다른 방식으로 트래픽을 제어합니다. NACL은 **네트워크 레벨**에서 작동하는 **정적 규칙**을 사용하여 트래픽을 필터링하는 반면, 보안 그룹은 **인스턴스 레벨**에서 작동하는 **동적 규칙**을 통해 트래픽을 제어합니다. NACL은 모든 트래픽을 거부하는 기본 정책을 가지며, 보안 그룹은 모든 트래픽을 허용하는 기본 정책을 가집니다. 이 두 메커니즘은 서로 보완적인 역할을 하며, NACL은 네트워크 레벨에서의 보안을 담당하고, 보안 그룹은 인스턴스 간의 통신을 제어합니다.

#### 왜 중요한가?
- **보안 격차 해결**: NACL은 네트워크 레벨에서의 보안을 강화하고, 보안 그룹은 인스턴스 간의 통신을 세밀하게 제어하여 보안 취약점을 줄입니다.  
- **고유한 목적**: NACL은 정적 규칙으로 인해 네트워크 레벨의 트래픽을 통제하는 데 적합하지만, 보안 그룹은 동적 규칙을 통해 인스턴스 간의 통신을 관리하는 데 최적화되어 있습니다.

#### 세부 요소
| 요소 | 설명 | 예시 |
|-----|------|---|
| **범위** | NACL은 서브넷 수준에서 작동, 보안 그룹은 인스턴스 수준에서 작동 | 서브넷 A에 NACL을 설정하여 특정 IP 트래픽 차단 |
| **상태성** | NACL은 상태 무관, 보안 그룹은 상태 유관 | NACL은 트래픽을 수신/발신 모두 확인, 보안 그룹은 수신 트래픽만 확인 |
| **기본 정책** | NACL은 모든 트래픽을 거부, 보안 그룹은 모든 트래픽을 허용 | NACL에서 정책 추가 전에는 모든 트래픽 차단됨 |

> **💡 Tip:** NACL은 네트워크 레벨의 기본 보안 장벽으로 사용되며, 보안 그룹은 인스턴스 간의 통신을 세밀하게 제어하는 데 주로 활용됩니다. 두 도구를 결합해 보안을 강화해야 합니다.

---

### 개념 2: VPC 흐름 로그(VPC Flow Logs)
VPC 흐름 로그는 **VPC 내에서 발생하는 모든 네트워크 트래픽의 상세 정보를 기록하는 기능**입니다. 이 로그는 트래픽의 출발지, 목적지, 포트, 프로토콜, 상태 등을 기록하여 네트워크 보안 분석, 문제 진단, 규정 준수 확인에 활용됩니다. VPC 흐름 로그는 **CloudWatch Logs**에 저장되며, AWS CLI나 콘솔을 통해 설정 및 확인할 수 있습니다.

#### 작동 원리
1. **트래픽 모니터링**: VPC 내에서 네트워크 트래픽이 발생할 때, VPC 흐름 로그는 해당 트래픽을 모니터링합니다.  
2. **데이터 수집**: 트래픽의 출발지, 목적지, 포트, 프로토콜, 상태, 액세스 권한 등을 기록합니다.  
3. **로그 저장**: 수집된 데이터는 CloudWatch Logs에 저장되어 분석 및 모니터링에 사용됩니다.

> **💡 Tip:** VPC 흐름 로그는 네트워크 보안 사고 발생 시 원인 분석에 필수적이며, 정기적으로 로그를 검토해 보안 취약점을 사전에 발견해야 합니다.

---

### 개념 3: 네트워크 파이어월(Network Firewall)
네트워크 파이어월은 **VPC 내에서 네트워크 트래픽을 필터링하는 데 특화된 보안 서비스**입니다. 이는 전통적인 파이어월과 달리 **VPC 내부의 서브넷, 라우터, 인스턴스 등에 직접 통합**되어 작동하며, AWS의 **AWS WAF**, **Shield**, **Firewall Manager**와도 연동됩니다. 네트워크 파이어월은 **AWS Managed Rules**를 기반으로 트래픽을 필터링하고, 보안 위협을 실시간으로 차단합니다.

#### 주요 특징
1. **중심적 관리**: 단일 포인트에서 모든 네트워크 트래픽을 감시하고 제어할 수 있어 관리 효율성이 높습니다.  
2. **AWS 서비스 통합**: WAF, Shield, Firewall Manager 등과의 연동을 통해 종합적인 보안 네트워크를 구축할 수 있습니다.  
3. **실시간 모니터링**: 트래픽을 실시간으로 분석하고, 위협이 발생할 경우 즉시 차단하여 보안 사고를 예방합니다.

> **💡 Tip:** 네트워크 파이어월은 전통적인 파이어월보다 VPC 내부 트래픽을 보다 세밀하게 제어할 수 있어, AWS 환경에서 고도화된 보안 정책을 구현하는 데 적합합니다.

## 🖥️ AWS 콘솔에서 VPC Flow Logs 사용하기

### Step 1: VPC Flow Logs 서비스 접속  
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
   - **💡 Tip:** AWS 계정이 없으면 [AWS Free Tier](https://aws.amazon.com/free/)를 통해 무료로 시작할 수 있습니다.  
2. 상단 검색창에서 **"VPC Flow Logs"**를 입력하고, 검색 결과에서 **"VPC Flow Logs"**를 클릭합니다.  
   - **⚠️ 주의:** "VPC Flow Logs"는 AWS 서비스 중 하나로, 네트워크 트래픽을 모니터링하는 데 사용됩니다.  

> **📸 화면 확인:** VPC Flow Logs 대시보드가 표시되면 정상입니다.  
> - 대시보드에는 생성된 흐름 로그 목록, 상태, 및 로그 그룹 정보가 표시됩니다.  

---

### Step 2: [주요 작업 1 - 흐름 로그 생성]  
1. **"Create Flow Log"** 버튼 클릭  
   - **설명:** VPC의 네트워크 트래픽을 모니터링하기 위한 흐름 로그를 생성합니다.  
2. **VPC 선택**  
   - **설명:** 로그를 생성할 VPC를 선택합니다.  
   - **입력값:** VPC ID 또는 이름을 입력합니다.  
3. **로깅 대상 설정**  
   - **설명:** 흐름 로그가 수집할 네트워크 리소스를 선택합니다.  
   - **옵션:**  
     - **Subnets**: 특정 서브넷의 트래픽을 로그에 기록합니다.  
     - **Network Interfaces**: 네트워크 인터페이스의 트래픽을 로그에 기록합니다.  
     - **Transit Gateways**: 트랜지트 게이트웨이의 트래픽을 로그에 기록합니다.  

> **📸 화면 확인:** "Create Flow Log" 창에서 VPC 및 리소스 선택 후 "Create" 버튼을 클릭합니다.  
> - 생성 후, 로그 그룹 및 IAM 권한 설정이 자동으로 생성됩니다.  

---

### Step 3: [주요 작업 2 - 로그 구성 및 설정]  
1. **로그 그룹 선택**  
   - **설명:** 로그를 저장할 AWS CloudWatch Logs 그룹을 선택합니다.  
   - **권장 설정:** "AWS Default" 그룹을 사용하거나, 고유한 그룹을 생성합니다.  
2. **트래픽 필터링 설정**  
   - **설명:** 특정 트래픽(예: 특정 IP 주소, 포트)만 로그에 기록할 수 있습니다.  
   - **설정 방법:**  
     - **"Traffic Type"**에서 "All" 또는 "Rejected"을 선택합니다.  
     - **"Filtering"** 섹션에서 IP 주소, 포트, 프로토콜을 필터링합니다.  
3. **IAM 역할 및 권한 설정**  
   - **설명:** 로그를 읽고 관리할 IAM 역할을 설정합니다.  
   - **권장 설정:** "AWSLambdaBasicExecutionRole" 또는 고유한 IAM 역할을 사용합니다.  

> **⚠️ 주의:** 로그 그룹 및 IAM 권한 설정은 비용과 보안에 직접적인 영향을 미칩니다.  
> - 로그 저장소는 데이터 저장 비용이 발생하므로, 필요 시 **AWS Free Tier**를 활용하세요.  

---

### Step 4: 설정 확인 및 테스트  
1. **생성된 리소스 확인**  
   - **방법:** VPC Flow Logs 대시보드에서 로그 목록을 확인합니다.  
   - **확인 사항:** 로그 상태가 "Active"인지 확인합니다.  
2. **로그 상태 확인**  
   - **방법:** AWS CloudWatch Logs에서 로그 그룹을 열어 실시간 트래픽을 확인합니다.  
   - **예시:**  
     ```bash
     aws logs get-log-events --log-group-name <log-group-name> --log-stream-name <log-stream-name>
     ```  
3. **정상 동작 테스트**  
   - **방법:** EC2 인스턴스 간 트래픽을 생성하거나, 외부 IP에 요청을 보내어 로그가 생성되는지 확인합니다.  
   - **예시:**  
     ```bash
     curl http://<public-ip-of-ec2-instance>
     ```  
   - **확인 사항:** CloudWatch Logs에 트래픽 정보가 기록되었는지 확인합니다.  

> **📸 화면 확인:** CloudWatch Logs에서 로그 항목이 생성되고, IP, 포트, 프로토콜 정보가 포함되어 있는지 확인합니다.  

---

### 📊 서비스 비교 및 가격 정보  
| 서비스               | 기능 설명                                 | 비용(예)                     | 주의사항                     |
|----------------------|------------------------------------------|------------------------------|------------------------------|
| VPC Flow Logs        | VPC 내 네트워크 트래픽 모니터링          | $0.001/GB (Free Tier 포함)   | 로그 저장소 비용 발생        |
| Network Firewall     | 네트워크 트래픽 필터링 및 보안           | $0.003/GB (Free Tier 포함)   | 고성능 네트워크 보안 필요    |
| WAF                  | 웹 트래픽의 DDoS 및 악성 요청 필터링     | $0.003/GB (Free Tier 포함)   | HTTP/HTTPS 트래픽에 한함     |
| Shield               | DDoS 공격 대응 및 보호                    | $0.001/GB (Free Tier 포함)   | 자동 보호 기능 제공          |
| Firewall Manager     | 다중 계정 네트워크 보안 관리              | $0.001/GB (Free Tier 포함)   | 조직 전체 보안 정책 관리     |

> **💡 Tip:** AWS Free Tier를 활용해 VPC Flow Logs를 무료로 테스트할 수 있습니다.  
> - [AWS Free Tier 가이드](https://aws.amazon.com/free/)를 참고하세요.

## ⌨️ AWS CLI로 VPC Flow Logs 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

**필수 사전 조건:**  
- AWS CLI가 설치되어 있어야 합니다.  
- 적절한 IAM 권한이 부여되어 있어야 합니다 (예: `ec2:DescribeFlowLogs`, `ec2:CreateFlowLogs` 등).  
- VPC가 생성되어 있어야 합니다.  

---

### 예제 1: VPC Flow Logs 리소스 조회
```bash
# VPC Flow Logs 목록 조회
aws ec2 describe-flow-logs --query 'FlowLogs[*].FlowLogId' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|-----|--------|
| `--query` | 필터링을 위한 JMESPath 표현식 | `'FlowLogs[*].FlowLogId'` |
| `--output` | 출력 형식 (json/table/text) | `table` |

**예상 출력:**
```
No running instances.
```

**⚠️ 주의:**  
리소스가 없을 경우 `No running instances.`와 같은 메시지가 나타납니다.  

---

### 예제 2: VPC Flow Logs 리소스 생성
```bash
# VPC Flow Logs 생성
aws ec2 create-flow-logs \
    --vpc-id vpc-0abcdef1234567890 \
    --traffic-type ALL \
    --log-destination-type S3 \
    --log-destination arn:aws:s3:::example-bucket
```

**필수 옵션:**
- `--vpc-id`: 로그를 생성할 VPC ID  
- `--traffic-type`: 로그 대상 트래픽 (ALL/ACCEPT/REJECT)  
- `--log-destination-type`: 로그 저장 위치 유형 (S3/CloudWatch/Partition)  
- `--log-destination`: 로그 저장 경로 (ARN 형식)  

**예상 출력:**
```json
{
    "FlowLog": {
        "FlowLogId": "fl-0123456789abcdef0",
        "Status": "active"
    }
}
```

**💡 Tip:**  
`--name` 옵션으로 로그 이름을 지정할 수 있습니다. 예: `--name "MyFlowLog"`  

---

### 예제 3: VPC Flow Logs 리소스 수정
```bash
# VPC Flow Logs 수정 (현재 CLI에서는 수정 불가. 삭제 후 재생성 필요)
aws ec2 delete-flow-logs --flow-log-id fl-0123456789abcdef0
```

**⚠️ 주의:**  
AWS CLI는 VPC Flow Logs의 **수정**이 불가능합니다.  
필요 시 **삭제 후 재생성**을 통해 설정을 변경해야 합니다.  

---

### 예제 4: VPC Flow Logs 리소스 삭제
```bash
# VPC Flow Logs 삭제
aws ec2 delete-flow-logs --flow-log-id fl-0123456789abcdef0

# 삭제 확인
aws ec2 describe-flow-logs --flow-log-id fl-0123456789abcdef0
```

**⚠️ 주의:**  
삭제된 리소스는 복구할 수 없습니다.  
삭제 후에는 `describe-flow-logs` 명령어로 상태를 확인할 수 있습니다.  

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws ec2 describe-flow-logs --flow-log-id "fl-0123456789abcdef0"
aws ec2 list-flow-logs

# 생성
aws ec2 create-flow-logs --vpc-id "vpc-0abcdef1234567890" --traffic-type ALL --log-destination-type S3 --log-destination "arn:aws:s3:::example-bucket"

# 삭제
aws ec2 delete-flow-logs --flow-log-id "fl-0123456789abcdef0"
```

---

### 비용 및 프리티어 활용
- **프리티어:** 1개월간 최대 1,000개의 로그 기록 무료 (AWS Free Tier).  
- **비용:**  
  - S3 저장소 기반: 로그 크기 및 저장 기간에 따라 요금이 발생합니다.  
  - CloudWatch Logs 기반: 로그 크기 및 저장 기간에 따라 요금이 발생합니다.  
- **최적화 팁:**  
  - 트래픽 타입을 `ALL`에서 `ACCEPT` 또는 `REJECT`로 제한합니다.  
  - 로그 저장소를 S3에 설정하고, AWS Glacier로 아카이브하여 비용을 절감합니다.  

---

### 관련 서비스 및 비교
| 서비스 | 기능 | VPC Flow Logs와의 관계 |
|-------|-----|-------------------------|
| NACL | 네트워크 ACL로 트래픽 제어 | VPC Flow Logs는 NACL의 트래픽을 로그로 기록 |
| Security Group | 인스턴스 간 트래픽 제어 | VPC Flow Logs는 Security Group의 트래픽을 로그로 기록 |
| Network Firewall | 보안 규칙 기반 필터링 | VPC Flow Logs는 Network Firewall의 트래픽을 로그로 기록 |
| WAF | 웹 공격 방어 | VPC Flow Logs는 WAF의 트래픽을 로그로 기록 |
| Shield | DDoS 보호 | VPC Flow Logs는 Shield의 트래픽을 로그로 기록 |
| Firewall Manager | 다중 계정 보안 관리 | VPC Flow Logs는 Firewall Manager의 트래픽을 로그로 기록 |

---

### ✅ 단계별 확인 사항
1. AWS CLI 버전을 확인하고 최신 상태로 유지합니다.  
2. VPC가 생성되어 있는지 확인합니다.  
3. 로그 저장소 (S3/CloudWatch)가 생성되어 있는지 확인합니다.  
4. IAM 정책에 `ec2:DescribeFlowLogs`, `ec2:CreateFlowLogs` 권한이 부여되었는지 확인합니다.  
5. 로그 생성 후 `describe-flow-logs`로 상태를 확인합니다.  
6. 삭제 시 `--output table`을 사용해 삭제된 리소스를 확인합니다.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 VPC Flow Logs 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **포인트 1: VPC 흐름 로그의 목적 및 사용 사례**  
   - 설명: VPC Flow Logs는 VPC 내 네트워크 트래픽을 모니터링하고, 보안 위협을 감지하는 데 필수적입니다. 시험에서는 트래픽 분석, 보안 조치 개선, 규정 준수를 위한 로그 수집 등 실제 시나리오를 기반으로 출제됩니다.  
   - 키워드: `트래픽 모니터링`, `보안 감사`, `규정 준수`

2. **포인트 2: 로그 데이터의 구조 및 필드 설명**  
   - 설명: 시험에서는 VPC Flow Logs의 JSON 형식 데이터를 분석하는 능력이 평가됩니다. 예를 들어, `source-IP`, `destination-IP`, `protocol`, `bytes-transferred` 등의 필드를 이해하는 것이 중요합니다.  
   - 키워드: `JSON 형식`, `트래픽 메타데이터`, `필드 분석`

3. **포인트 3: VPC Flow Logs와 Network Firewall의 차이점**  
   - 설명: 시험에서는 두 서비스의 목적과 기능을 구분하는 문제가 자주 출제됩니다. VPC Flow Logs는 로그 수집에 중점을 두고, Network Firewall은 트래픽 필터링 및 방화벽 규칙 적용에 집중합니다.  
   - 키워드: `로깅 vs 필터링`, `모니터링 vs 보안`, `VPC vs VPC`

4. **포인트 4: 비용 및 프리티어 제한 사항**  
   - 설명: VPC Flow Logs는 로그 생성량에 따라 비용이 발생하며, 프리티어는 1000개의 로그 그룹만 제공합니다. 시험에서는 비용 계산과 제한 사항을 고려한 설계 문제를 다룹니다.  
   - 키워드: `비용 계산`, `프리티어 제한`, `로그 그룹 수`

5. **포인트 5: 로그 수집 범위의 한계**  
   - 설명: VPC Flow Logs는 VPC 내 트래픽을 기록하지만, 일부 트래픽(예: NAT 게이트웨이, VPC 피어링)은 제외됩니다. 시험에서는 이러한 한계를 고려한 설계가 평가됩니다.  
   - 키워드: `수집 범위`, `제외 트래픽`, `NAT 게이트웨이`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | VPC Flow Logs와 WAF의 기능을 혼동하는 경우 | VPC Flow Logs는 트래픽 로깅, WAF는 HTTP/HTTPS 요청 필터링 |
| 함정 2 | 로그 데이터의 `bytes-transferred` 필드를 이해하지 못하는 경우 | 이 필드는 데이터 전송량을 기록하며, 네트워크 성능 분석에 사용됨 |
| 함정 3 | 로그 생성 비용을 계산할 때 `Flow Log Type`을 잘못 적용하는 경우 | `Standard`는 모든 트래픽, `Detailed`는 추가 메타데이터 포함 |

#### 🔄 VPC Flow Logs vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | VPC Flow Logs | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | VPC 내 네트워크 트래픽 로깅 | Network Firewall, WAF | 네트워크 모니터링 및 보안 분석 |
| 확장성 | 로그 수집량에 따라 비용 증가 | Network Firewall: 고성능 방화벽 | 대규모 트래픽 처리 시 |
| 비용 | 로그 생성량 기반 요금제 | WAF: 요청 수 기반 요금제 | 빈도/데이터량에 따라 선택 |
| 지연시간 | 실시간 로깅 가능 | Network Firewall: 실시간 방화벽 적용 | 실시간 보안 대응 시 |

#### 📝 시험 대비 체크리스트
- [ ] VPC Flow Logs의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  > **VPC 내 네트워크 트래픽을 모니터링하여 보안 위협을 감지하고 분석하는 데 사용됩니다.**
- [ ] VPC Flow Logs를 선택해야 하는 시나리오를 알고 있는가?  
  > **트래픽 분석, 보안 모니터링, 규정 준수 요구사항이 있는 경우**
- [ ] VPC Flow Logs의 제한사항/한계를 알고 있는가?  
  > **NAT 게이트웨이, VPC 피어링 트래픽은 기록되지 않음**
- [ ] VPC Flow Logs와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  > **VPC Flow Logs는 로깅, Network Firewall는 방화벽 필터링**
- [ ] VPC Flow Logs의 비용 구조를 이해하고 있는가?  
  > **로그 생성량에 따라 비용 발생, 프리티어는 1000개 로그 그룹 제공**

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 VPC Flow Logs를 떠올리세요:  
> - `트래픽 모니터링`  
> - `보안 감사`  
> - `규정 준수`  
> - `로그 수집`  
> - `네트워크 분석`

---

| [⬅️ Security Groups](./Security-Groups.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 2](../README.md) | [Network Firewall ➡️](./Network-Firewall.md) |

---
