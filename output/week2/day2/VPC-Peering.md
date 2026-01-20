---

| [⬅️ 이전 Day](../day1/README.md) | [📑 Day 2 목차](./README.md) | [🏠 Week 2](../README.md) | [Transit Gateway ➡️](./Transit-Gateway.md) |

---

# VPC Peering 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** VPC Peering는 **VPC 간 네트워크 연결**을 위한 AWS의 **네트워크 인터커넥션** 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 동일 VPC 내외에서 통신이 필요한 경우 NAT 게이트웨이나 IP 주소 공유를 통해 비효율적인 통신이 발생했습니다. 예를 들어, 두 개의 VPC가 서로의 인스턴스에 접근하려면 공용 IP를 사용해야 하며, 이로 인해 보안 리스크와 비용이 증가했습니다.
- **문제 2:** 여러 VPC 간의 복잡한 네트워크 연결을 관리할 때 라우팅 테이블 설정이 수동으로 이루어져 오류가 발생할 수 있었습니다. 특히, 동적 IP 주소나 IP 대역폭 제한으로 인해 연결이 중단될 수 있었습니다.
- **문제 3:** 클라우드 환경에서 온프레미스 네트워크와 VPC 간의 직접적인 연결이 필요했으나, 별도의 전용 링크나 프록시를 통해 연결해야 했습니다. 이는 설정이 복잡하고 지연이 발생할 수 있었습니다.

**VPC Peering로 해결:**
- **해결 1:** 두 VPC 간에 **직접적인 라우팅 경로**를 설정해 통신이 가능하도록 합니다. 이로 인해 NAT 게이트웨이나 IP 공유 없이도 VPC 간 통신이 가능해집니다.
- **해결 2:** **자동 라우팅 테이블 설정**을 통해 관리자의 수동 설정이 줄어들고, 오류를 최소화할 수 있습니다. 또한, IP 주소 변경 없이도 연결이 유지됩니다.
- **해결 3:** **Direct Connect**와 결합해 온프레미스 네트워크와 VPC 간에 전용 링크를 구성할 수 있습니다. 이는 데이터 전송 지연을 줄이고 보안성을 높입니다.

### 비유로 이해하기
VPC Peering은 두 사무실 간에 **직접 전화선**을 연결하는 것처럼 작동합니다. 기존에는 공용 네트워크를 통해 통신했지만, VPC Peering을 사용하면 사무실 간에 전용 네트워크를 통해 데이터를 바로 전송할 수 있습니다. 이로 인해 보안성이 높아지고, 통신 지연이 줄어듭니다. 예를 들어, 개발 VPC와 프로덕션 VPC 간에 직접 연결하면, 개발 팀이 프로덕션 서버에 접근하는 데 시간이 줄어듭니다.

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 개발/테스트 VPC와 프로덕션 VPC 간의 직접 통신이 필요한 경우 | 쇼핑몰 업체가 개발 VPC에서 프로덕션 VPC에 DB 접근 |
| 시나리오 2 | 온프레미스 네트워크와 VPC 간의 전용 연결이 필요한 경우 | 금융 기관이 온프레미스 서버와 VPC 간 데이터 전송 |
| 시나리오 3 | 다중 AWS 계정 간의 VPC 간 통신이 필요한 경우 | 빅테크 기업이 개발/운영/보안 계정 간 VPC 연결 |

**이럴 때 VPC Peering를 선택하세요:**
- ✅ **VPC 간 직접 통신**이 필요한 경우  
- ✅ **고성능 및 저지연 통신**이 요구되는 경우  
- ✅ **보안성과 격리**가 중요한 환경에서  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ **복잡한 네트워크 구조**가 필요한 경우 → **Transit Gateway** 사용 (중앙 집중형 연결)  
- ❌ **온프레미스와 VPC 간 전용 링크**가 필요한 경우 → **Direct Connect** 사용 (전용 네트워크 인터페이스)  
- ❌ **VPC 내부 서비스 접근**이 필요한 경우 → **VPC Endpoint** 사용 (게이트웨이/인터페이스 엔드포인트)

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **Transit Gateway** | 중앙 집중형 네트워크 연결을 통해 여러 VPC 간의 통신을 단순화 | VPC A → Transit Gateway → VPC B |
| **VPC Endpoint** | VPC 내부 서비스에 대한 프라이빗 접근을 제공 | VPC → VPC Endpoint (S3/ DynamoDB) |
| **Direct Connect** | 온프레미스와 VPC 간 전용 네트워크 인터페이스 구성 | 온프레미스 → Direct Connect → VPC |

**자주 사용되는 아키텍처 패턴:**
```
[사용자] → [CloudFront] → [S3] (VPC Endpoint)
         ↘
         ↘ [VPC Peering] → [Transit Gateway] → [온프레미스 네트워크] (Direct Connect)
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **VPC Peering 연결 수** | $0.02/일 (월 100개까지 무료) | 월 100개 무료 |
| **데이터 전송 비용** | $0.10/GB (100GB 이상) | 12개월 무료 |
| **VPC Peering 연결 관리** | $0.01/일 | 항상 무료 |

**비용 최적화 팁:**
1. 💡 **프리티어 활용**: 최대 100개의 VPC Peering 연결을 무료로 사용해 초기 비용을 절감하세요.
2. 💡 **데이터 전송 최소화**: VPC 간 데이터 전송을 줄이거나, 데이터 전송 비용이 낮은 서비스(예: S3)를 우선 사용하세요.
3. 💡 **Transit Gateway 대안 검토**: 복잡한 네트워크 구조에서는 Transit Gateway를 선택해 비용을 절감할 수 있습니다.

> **⚠️ 비용 주의:** **데이터 전송량**이 예상보다 많을 경우 비용이 급증할 수 있으므로, **CloudWatch**를 통해 모니터링하고, 필요 시 **VPC Peering 대신 Direct Connect**를 고려하세요.

## 📚 핵심 개념

### 개념 1: VPC 피어링 연결 및 라우팅 테이블 설정  
VPC 피어링은 두 개 이상의 VPC 간에 **직접적인 프라이빗 네트워크 연결**을 설정하는 기능입니다. 이는 외부 인터넷을 통한 중개 없이 VPC 간 데이터 전송을 가능하게 하며, 보안성이 높은 환경에서 중요한 역할을 합니다. 피어링 연결을 설정하면 각 VPC의 라우팅 테이블에 상대 VPC의 CIDR 블록을 추가해야 하며, 이로 인해 패킷이 직접적으로 전달됩니다.  
VPC 피어링은 **IP 주소 공유 없이** 네트워크를 연결할 수 있어, IP 주소 부족 문제를 해결합니다. 또한, 네트워크 라우팅을 관리할 수 있는 유연성과, 고성능의 저지연 통신을 제공합니다.  

#### 왜 중요한가?  
- **보안성 강화**: 외부 인터넷을 거치지 않고 VPC 간 데이터 전송으로 보안 위험 감소  
- **IP 주소 효율성**: IP 주소 공유 없이 네트워크 연결 가능  
- **고성능 통신**: 중간 라우터 없이 직접 전송으로 지연 최소화  

#### 세부 요소  
| 요소 | 설명 | 예시 |  
|-----|-----|-----|  
| **VPC 피어링 연결** | 두 VPC 간의 직접 연결 | `us-east-1a` VPC와 `eu-west-1b` VPC 연결 |  
| **라우팅 테이블 설정** | 각 VPC의 라우팅 테이블에 상대 CIDR 추가 | `10.0.0.0/16` CIDR 블록 추가 |  
| **프리티어 활용** | 5개 VPC 피어링까지 무료 사용 가능 | 3개 VPC 간 연결 시 비용 절약 |  

> **💡 Tip:** 피어링 연결 후 라우팅 테이블을 정확히 설정해야 하며, **ACL 및 NAT 설정**도 함께 검토해야 합니다.  

---

### 개념 2: 트랜지트 게이트웨이의 중앙 집중형 네트워크 연결  
트랜지트 게이트웨이(Transit Gateway)는 여러 VPC와 하이브리드 네트워크를 **중앙 집중식으로 연결**하는 기능입니다. 이는 복잡한 네트워크 아키텍처에서 여러 VPC 간의 통신을 단일 포인트에서 관리할 수 있도록 합니다. 예를 들어, 10개 이상의 VPC가 서로 연결해야 할 경우, 트랜지트 게이트웨이를 사용하면 라우팅 테이블 관리가 간소화됩니다.  

#### 작동 원리  
1. **트랜지트 게이트웨이 생성**: AWS 콘솔에서 트랜지트 게이트웨이를 생성하고, VPC에 연결합니다.  
2. **라우팅 테이블 구성**: 각 VPC의 라우팅 테이블에 트랜지트 게이트웨이의 IP 주소를 라우트 대상으로 추가합니다.  
3. **하이브리드 연결**: Direct Connect나 VPN을 통해 온프레미스 네트워크와 트랜지트 게이트웨이를 연결해 통합 네트워크 구축.  

> **💡 Tip:** 트랜지트 게이트웨이를 사용하면 **VPC 피어링 대신** 복잡한 네트워크 구조를 효율적으로 관리할 수 있습니다.  

---

### 개념 3: VPC 게이트웨이 엔드포인트 vs 인터페이스 엔드포인트 차이  
VPC 엔드포인트는 AWS 서비스에 대한 **프라이빗 연결**을 제공합니다. 이 중 **게이트웨이 엔드포인트**는 S3, DynamoDB 등 일부 서비스에만 지원되며, **인터페이스 엔드포인트**는 모든 AWS 서비스에 적용 가능합니다.  

#### 주요 특징  
1. **게이트웨이 엔드포인트**  
   - **특징 1**: AWS 서비스(예: S3, DynamoDB)에 대한 프라이빗 액세스 가능  
   - **특징 2**: 서브넷에 연결되어 데이터 전송 시 헤더 수정 없이 통신  
   - **특징 3**: NAT 없이 서비스에 직접 접근 가능 (IP 주소 공유 필요 없음)  

2. **인터페이스 엔드포인트**  
   - **특징 1**: 모든 AWS 서비스에 적용 가능 (예: Lambda, EC2)  
   - **특징 2**: 고정 IP 주소를 통해 서비스에 접근 가능  
   - **특징 3**: 서브넷에 직접 연결되어 통신 효율성 향상  

> **💡 Tip:** 게이트웨이 엔드포인트는 특정 서비스만 지원하므로, 서비스 범위에 따라 적절한 엔드포인트를 선택해야 합니다.

## 🖥️ AWS 콘솔에서 VPC Peering 사용하기

### Step 1: VPC Peering 서비스 접속
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
   - 로그인 후 **"VPC Peering"**을 검색합니다.  
2. 검색 결과에서 **"VPC Peering"** 메뉴를 클릭합니다.  
   - 이는 VPC 간 연결 관리 대시보드로 이동합니다.  

> **📸 화면 확인:** VPC Peering 대시보드가 표시되면 정상입니다.  
> **💡 Tip:** VPC Peering 연결 생성 후, **"Peering Connections"** 탭에서 상태를 확인할 수 있습니다.  

---

### Step 2: [주요 작업 1 - 리소스 생성]  
#### 1. VPC Peering 연결 요청 생성  
1. **"Create Peering Connection"** 버튼을 클릭합니다.  
2. **"Peering Connection Name"** 필드에 이름을 입력합니다 (예: `MyVpcPeering-1`).  
3. **"Requester VPC"**에서 연결할 VPC를 선택합니다.  
   - **"Accepter VPC"**는 요청을 수락할 VPC를 선택합니다.  
   - **"Peer VPC"**는 타겟 VPC를 선택합니다.  
4. **"Enable DNS resolution"** 및 **"Enable VPC route table propagation"** 옵션을 설정합니다.  

#### 2. 요청 생성 및 확인  
1. **"Create Peering Connection"** 버튼을 클릭하여 요청을 제출합니다.  
2. **"Peering Connections"** 탭에서 생성된 연결을 확인합니다.  
   - **Status**가 `Pending Acceptance`로 표시되면 요청이 수락을 기다리는 상태입니다.  

> **📸 화면 확인:** "Peering Connections" 목록에 생성된 연결이 표시되고 상태가 "Pending Acceptance"인지 확인합니다.  

---

### Step 3: [주요 작업 2 - 설정/구성]  
#### 1. 요청 수락 및 라우팅 설정  
1. **"Accept Peering Connection"** 버튼을 클릭하여 요청을 수락합니다.  
   - 수락 후, **"Status"**가 `Active`로 변경됩니다.  
2. 라우팅 테이블에 라우트를 추가합니다:  
   - **"Route Tables"** > **"Routes"** > **"Create Route"**  
   - **Destination CIDR**에 타겟 VPC의 CIDR을 입력하고, **Target**으로 VPC Peering 연결을 선택합니다.  

#### 2. DNS 설정 및 보안 그룹 조정  
1. **"DNS Resolution"** 설정을 확인합니다:  
   - **"Enable DNS resolution"**이 활성화되어 있는지 확인합니다.  
2. 보안 그룹 및 네트워크 ACL을 업데이트하여 트래픽 허용 범위를 확장합니다.  

> **⚠️ 주의:** 라우팅 테이블의 라우트가 정확히 구성되지 않으면 트래픽이 통신되지 않습니다.  

---

### Step 4: 설정 확인 및 테스트  
#### 1. 생성된 리소스 확인 방법  
1. **"Peering Connections"** 탭에서 **Status**가 `Active`인지 확인합니다.  
2. **"Route Tables"**에서 라우트가 추가되었는지 확인합니다.  

#### 2. 상태 확인 방법  
1. CLI 명령어를 사용하여 상태를 확인합니다:  
   ```bash
   aws ec2 describe-vpc-peering-connections --vpc-peering-connection-id <peering-id>
   ```  
2. **"Status"** 필드가 `active`인지 확인합니다.  

#### 3. 정상 동작 테스트  
1. 두 VPC에 EC2 인스턴스를 생성하고, 서로의 IP 주소로 ping 또는 SSH를 시도합니다.  
2. **VPC Peering**이 성공적으로 구성되지 않으면, **"No route found"** 또는 **"Connection timed out"** 오류가 발생합니다.  

> **💰 비용 주의사항:** VPC Peering 자체는 무료이지만, 데이터 전송 비용이 발생할 수 있습니다. 프리티어를 활용해 무료로 테스트하세요.  
> **💡 Tip:** VPC Peering은 하이브리드 클라우드 구성이나 다중 VPC 통신에 유용합니다.

## ⌨️ AWS CLI로 VPC Peering 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

**설명:**  
AWS CLI를 사용하기 전에 버전, 권한, 리전을 확인하세요.  
- `aws --version`: CLI 버전 확인  
- `aws sts get-caller-identity`: 현재 사용자의 AWS 계정 및 리전 확인  
- `aws configure get region`: 설정된 리전 확인  

---

### 예제 1: VPC Peering 리소스 조회
```bash
# VPC Peering 연결 목록 조회
aws ec2 describe-vpc-peering-connections \
    --query 'VpcPeeringConnections[].VpcPeeringConnectionId' \
    --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| `--query` | 결과 필터링 | `'VpcPeeringConnections[].VpcPeeringConnectionId'` |
| `--output` | 출력 형식 | `json`, `table`, `text` |

**예상 출력:**
```
VpcPeeringConnectionId
------------------------
pcx-1234567890abcdef0
```

**설명:**  
`describe-vpc-peering-connections` 명령어는 VPC Peering 연결 목록을 반환합니다. `--query` 옵션을 사용해 특정 필드만 출력할 수 있습니다.

---

### 예제 2: VPC Peering 리소스 생성
```bash
# VPC Peering 연결 생성
aws ec2 create-vpc-peering-connection \
    --vpc-id vpc-12345678 \
    --peer-vpc-id vpc-09876543 \
    --peer-region us-west-2
```

**필수 옵션:**
- `--vpc-id`: 본 로컬 VPC ID  
- `--peer-vpc-id`: 피어링할 VPC ID  
- `--peer-region`: 피어링할 VPC의 리전  

**예상 출력:**
```json
{
    "VpcPeeringConnection": {
        "VpcPeeringConnectionId": "pcx-1234567890abcdef0",
        "Status": "pending-acceptance"
    }
}
```

**설명:**  
`create-vpc-peering-connection` 명령어는 두 VPC 간의 피어링 연결을 생성합니다. 생성 후 피어링 요청을 수락해야 연결이 완료됩니다.

---

### 예제 3: VPC Peering 리소스 수정
```bash
# VPC Peering 연결 수정 (예: 상태 확인)
aws ec2 describe-vpc-peering-connections \
    --vpc-peering-connection-id pcx-1234567890abcdef0
```

**설명:**  
VPC Peering 연결의 상태를 확인하거나, 연결에 대한 세부 정보를 조회할 수 있습니다.  
- `describe-vpc-peering-connections`는 연결 상태, VPC 정보 등을 반환합니다.

---

### 예제 4: VPC Peering 리소스 삭제
```bash
# VPC Peering 연결 삭제
aws ec2 delete-vpc-peering-connection \
    --vpc-peering-connection-id pcx-1234567890abcdef0

# 삭제 확인
aws ec2 describe-vpc-peering-connections \
    --vpc-peering-connection-id pcx-1234567890abcdef0
```

> **⚠️ 주의:** 삭제는 되돌릴 수 없습니다. 신중하게 실행하세요.  
> 삭제 후 `describe` 명령어로 상태를 확인해 삭제가 완료되었는지 확인하세요.

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws ec2 describe-vpc-peering-connections
aws ec2 describe-vpc-peering-connections --vpc-peering-connection-id "pcx-id"

# 생성
aws ec2 create-vpc-peering-connection --vpc-id "vpc-id" --peer-vpc-id "peer-vpc-id" --peer-region "region"

# 삭제
aws ec2 delete-vpc-peering-connection --vpc-peering-connection-id "pcx-id"
```

**팁:**  
- VPC Peering 연결은 **2개의 VPC**가 동일한 리전에 있어야 합니다.  
- 연결 생성 후 **피어링 요청을 수락**해야 통신이 가능합니다.  
- 데이터 전송 비용은 **AWS Pricing**을 참고하세요.  

---

### CLI 사용 시 주의사항
| 항목 | 설명 |
|------|------|
| **리전 일치** | VPC Peering은 동일 리전 내에서만 생성 가능합니다. |
| **VPC 상태** | VPC가 **활성 상태**여야 피어링이 가능합니다. |
| **비용** | VPC Peering은 자체 비용이 없지만, **데이터 전송**에 따라 비용이 발생할 수 있습니다. |
| **프리티어** | VPC Peering은 프리티어 사용 가능하며, 750시간/월까지 무료입니다. |

**참고:**  
AWS CLI 명령어는 실제 서비스명(`ec2`)과 리소스명(`vpc-peering-connection`)을 사용해야 합니다.  
스크린샷은 AWS 콘솔에서 "VPC Peering"을 검색해 연결 상태를 확인할 수 있습니다.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 VPC Peering 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **포인트 1: VPC Peering의 목적과 사용 사례**  
   - 설명: VPC Peering은 두 VPC 간의 직접적인 네트워크 연결을 제공해 데이터 전송 지연 최소화와 사내 네트워크 통합을 가능하게 합니다. 시험에서는 이 연결 방식의 장단점과 적절한 사용 시나리오(예: 동일 회사의 VPC 간 통신)를 묻는 경우가 많습니다.  
   - 키워드: `VPC 연결`, `데이터 전송`, `사내 네트워크 통합`

2. **포인트 2: 라우팅 테이블 구성과 제한 사항**  
   - 설명: VPC Peering 연결 시 라우팅 테이블에 `Peer VPC`를 추가해야 하며, 이 과정에서 IP 주소 충돌, 라우팅 루프, 네트워크 보안 정책 위반 등 문제가 발생할 수 있습니다. 시험에서는 이러한 제한 사항과 해결 방법을 묻는 문제가 자주 출제됩니다.  
   - 키워드: `라우팅 테이블`, `IP 충돌`, `보안 정책`

3. **포인트 3: VPC Peering vs Transit Gateway 비교**  
   - 설명: VPC Peering은 두 VPC 간 직접 연결을 제공하지만, Transit Gateway는 여러 VPC와 온프레미스 네트워크를 중앙 집중식으로 연결할 수 있습니다. 시험에서는 두 서비스의 적절한 사용 시나리오(예: 10개 이상 VPC 연결 시 Transit Gateway 선택)를 비교하는 문제가 자주 출제됩니다.  
   - 키워드: `중앙 집중형`, `다중 VPC 연결`, `Transit Gateway`

4. **포인트 4: CLI 명령어와 콘솔 설정 절차**  
   - 설명: AWS CLI 명령어(`aws ec2 create-vpc-peering-connection`)와 콘솔에서의 연결 생성, 승인, 라우팅 테이블 수정 단계는 시험에서 실습 문제로 출제될 수 있습니다. 특히, CLI를 사용한 구성 절차와 오류 해결 방법이 핵심입니다.  
   - 키워드: `CLI 명령어`, `VPC Peering 콘솔`, `라우팅 테이블 수정`

5. **포인트 5: 비용 구조 및 프리티어 활용**  
   - 설명: VPC Peering은 데이터 전송량에 따라 요금이 발생하며, 프리티어는 1년간 100만 건의 트래픽을 무료로 제공합니다. 시험에서는 비용 계산 방식과 프리티어 사용 조건을 묻는 문제가 포함됩니다.  
   - 키워드: `데이터 전송 요금`, `프리티어`, `비용 계산`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | VPC Peering이 Transit Gateway와 동일한 기능을 가지는지 혼동 | VPC Peering은 두 VPC 간 직접 연결, Transit Gateway는 중앙 집중형 네트워크 연결 |
| 함정 2 | 라우팅 테이블에 Peer VPC를 추가하지 않아 연결 실패 | 라우팅 테이블에 `Peer VPC`를 명시적으로 추가해야 연결이 성공 |
| 함정 3 | VPC Peering이 모든 VPC 간 연결을 지원한다고 오인 | VPC Peering은 2개 VPC 간만 연결 가능, 3개 이상 연결 시 Transit Gateway 사용 권장 |

#### 🔄 VPC Peering vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | VPC Peering | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | 두 VPC 간 직접 연결 | Transit Gateway, Direct Connect | VPC 간 간접 연결 시 Transit Gateway 사용 |
| 확장성 | 2개 VPC만 지원 | Transit Gateway | 10개 이상 VPC 연결 시 Transit Gateway 선택 |
| 비용 | 데이터 전송량에 따라 요금 | Direct Connect | 고대역폭 연결 시 Direct Connect 선택 |
| 지연시간 | 저지연 (직접 연결) | Transit Gateway | 중간 경로가 있는 경우 지연 증가 |

#### 📝 시험 대비 체크리스트
- [ ] VPC Peering의 핵심 목적을 한 문장으로 설명할 수 있는가?  
- [ ] VPC Peering를 선택해야 하는 시나리오를 알고 있는가? (예: 동일 회사의 VPC 간 통신)  
- [ ] VPC Peering의 제한사항/한계를 알고 있는가? (예: 2개 VPC만 지원, 라우팅 테이블 수정 필요)  
- [ ] VPC Peering와 Transit Gateway의 차이점을 설명할 수 있는가?  
- [ ] VPC Peering의 비용 구조를 이해하고 있는가? (데이터 전송량 기반 요금, 프리티어 활용 방법)

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 VPC Peering를 떠올리세요:  
> - `VPC 연결`  
> - `데이터 전송`  
> - `사내 네트워크 통합`  
> - `라우팅 테이블`  
> - `프리티어`

---

| [⬅️ 이전 Day](../day1/README.md) | [📑 Day 2 목차](./README.md) | [🏠 Week 2](../README.md) | [Transit Gateway ➡️](./Transit-Gateway.md) |

---
