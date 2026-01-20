---

| ⬅️ 시작 | [📑 Day 1 목차](./README.md) | [🏠 Week 1](../README.md) | [IAM ➡️](./IAM.md) |

---

# AWS Global Infrastructure 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** AWS Global Infrastructure는 글로벌 규모의 클라우드 서비스를 제공하기 위한 AWS의 기반 인프라 및 보안 관리 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 데이터 전송 지연 문제 (예: 동남아 사용자가 서버 미국 서부에서 서비스 접근 시 1000ms 이상 지연)  
- **문제 2:** 보안 취약성 (예: 관리자 계정이 직접 서버에 접근해 악성 코드 주입 위험)  
- **문제 3:** 데이터 주소지 이행 문제 (예: EU 기업이 미국 서버에서 데이터 저장 시 GDPR 위반 리스크)

**AWS Global Infrastructure로 해결:**
- **해결 1:** 200개 이상의 리전과 1000개 이상의 AZ를 통해 지역별 최적화된 데이터 전송 경로 제공  
- **해결 2:** IAM 정책과 MFA를 통해 접근 제어와 이중 인증으로 보안 강화  
- **해결 3:** AWS Organizations로 데이터 주소지 이행 규제 준수 및 복수 리전 배포 지원

### 비유로 이해하기
AWS Global Infrastructure는 글로벌 공장 네트워크를 운영하는 기업을 상상해보세요. 각 리전은 독립적인 공장, AZ는 공장 내부의 백업 시스템, IAM은 직원의 권한 관리, MFA는 출입 시 인증 체크를 담당합니다. 이 구조로 인해 글로벌 고객에게 최적화된 서비스와 보안을 제공할 수 있습니다.

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 글로벌 사용자 대상 서비스 확장 | Netflix: 200개 리전에서 동영상 스트리밍 제공 |
| 시나리오 2 | 보안 강화 요구 사항 | 금융 기관: IAM 정책으로 데이터 접근 제어 |
| 시나리오 3 | 데이터 주소지 이행 준수 | EU 기업: GDPR 준수를 위해 EU 리전에 데이터 저장 |

**이럴 때 AWS Global Infrastructure를 선택하세요:**
- ✅ 상황 1: 지역별 사용자 접근 성능 최적화 필요  
- ✅ 상황 2: 클라우드 환경에서 보안 정책 강제 적용 필요  
- ✅ 상황 3: 데이터 주소지 이행 규제 준수 요구  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ 상황: 단일 리전에서만 운영 가능 → 대안: AWS Outposts (온프레미스 클라우드 연동)  
- ❌ 상황: 단일 계정 관리만 필요 → 대안: AWS Organizations (복수 계정 통합 관리)  
- ❌ 상황: 실시간 데이터 처리 필요 → 대안: AWS Wavelength (지역별 고성능 처리)

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **Amazon S3** | 데이터 저장소로 리전별 배포 | 예: EU 리전 S3 버킷 → EU 리전 EC2 인스턴스 |
| **Amazon EC2** | 계산 자원 제공 및 리전/AZ 선택 | 예: AWS Global Infrastructure → EC2 → Application Layer |
| **AWS CloudFront** | 글로벌 캐싱을 통한 지연 최소화 | 예: User → CloudFront (엣지 로케이션) → S3 |

**자주 사용되는 아키텍처 패턴:**
```
User → [CloudFront (Edge Location)] → [S3 (Storage)]  
        ↑                            ↑  
        └── [EC2 (Compute)]         └── [RDS (Database)]  
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **EC2 인스턴스** | $0.01/시간 (기본 요금) | 월 750시간 무료 |
| **S3 스토리지** | $0.023/GB/월 | 5GB 무료 |
| **IAM 정책 관리** | $0.005/정책/월 | 항상 무료 |

**비용 최적화 팁:**
1. 💡 팁 1: **Reserved Instances** 구매로 75% 비용 절감 (1년 기준)  
2. 💡 팁 2: **Spot Instances** 사용으로 컴퓨팅 비용 90% 절감  
3. 💡 팁 3: **AWS Cost Explorer**를 통해 비용 트렌드 분석 및 비용 최적화  

> **⚠️ 비용 주의:** **AWS Wavelength** 또는 **Graviton2 인스턴스**는 초기 설정 비용이 높아서 테스트 후 사용 권장. **Spot Instances**는 중단 가능성이 있어 장애 허용 가능한 작업에만 사용.

## 📚 핵심 개념

### 개념 1: AWS 리전과 가용 존 (Regions and Availability Zones)
AWS 리전은 전 세계에 위치한 물리적 데이터 센터 그룹으로, 각 리전 내부에는 여러 가용 존(Availability Zone)이 포함됩니다. 리전은 네트워크 지연 최소화, 데이터 주소지 요구사항 충족, 장애 복구를 위해 설계되었습니다. 가용 존은 동일 리전 내부에 위치한 독립적인 데이터센터로, 장애 시 다른 존에 자동으로 트래픽을 분산해 시스템의 가용성을 높입니다.  
이 개념은 클라우드 환경에서 고가용성, 확장성, 지역 데이터 보호를 구현하는 데 필수적입니다. 예를 들어, EC2 인스턴스를 두 개 이상의 가용 존에 배치하면 단일 존의 장애가 전체 시스템에 영향을 주지 않도록 합니다. 또한, 글로벌 리전 선택은 데이터 유럽 지역에 주소지가 필요한 기업에 최적화된 솔루션을 제공합니다.

#### 왜 중요한가?
- **장애 복구**: 단일 가용 존의 장애 시 다른 존으로 자동 전환  
- **데이터 주소지**: 특정 국가에 데이터를 저장해야 할 경우 리전 선택이 필수  
- **성능 최적화**: 사용자 지역에 가까운 리전 선택으로 네트워크 지연 감소  

#### 세부 요소
| 요소 | 설명 | 예시 |
|-----|-----|-----|
| 리전(Region) | 전 세계에 위치한 물리적 데이터 센터 그룹 | US-East-1, EU-West-1 |
| 가용 존(Availability Zone) | 동일 리전 내부의 독립적인 데이터센터 | us-east-1a, us-east-1b |
| 엣지 로케이션 | 글로벌 네트워크를 통해 사용자 근처에 배치된 CDN 서버 | CloudFront의 글로벌 엣지 노드 |
| 데이터센터 고가용성 | 가용 존 간 네트워크 연결과 전력/냉각 시스템 별도 | AWS의 내부 다중 경로 네트워크 |

> **💡 Tip:** 인스턴스 배포 시 두 개 이상의 가용 존을 선택해 장애 대비 확장성 확보. 리전 선택 시 데이터 주소지 요구사항 반드시 검토.

---

### 개념 2: IAM 사용자, 역할 및 정책 (IAM Users, Roles, Policies)
AWS Identity and Access Management(IAM)은 클라우드 리소스에 대한 접근 제어를 관리하는 핵심 서비스입니다. **사용자**는 인간 관리자에게 권한을 부여하고, **역할**은 EC2 인스턴스 같은 서비스로 권한을 부여합니다. **정책**은 특정 작업에 대한 권한을 정의하는 규칙으로, **관리 정책**은 AWS가 제공하고, **인라인 정책**은 직접 생성할 수 있습니다.  
이 개념은 보안을 강화하고, 권한 부여를 최소화하는 "최소 권한 원칙"을 구현하는 데 필수적입니다. 예를 들어, EC2 인스턴스는 "EC2 역할"을 통해 S3 버킷에 접근할 수 있도록 설정할 수 있습니다.

#### 작동 원리
1. **사용자 생성**: AWS 콘솔에서 사용자 계정을 만들고, MFA를 설정해 보안 강화  
2. **역할 생성**: EC2 인스턴스용 역할을 생성하고, S3 접근 권한을 포함한 정책을 부여  
3. **정책 적용**: 인라인 정책을 직접 생성하거나, AWS 관리 정책(예: `AmazonS3ReadOnlyAccess`)을 연결해 권한 제어  

> **💡 Tip:** 역할을 사용해 서비스 간 권한 부여 시 사용자 계정 권한을 최소화해 보안 위험 감소.

---

### 개념 3: AWS Organizations 및 다중 인증 (AWS Organizations & MFA)
**AWS Organizations**는 여러 AWS 계정을 통합 관리하는 서비스로, 중앙 집중식 정책 관리, 비용 통합, 보안 표준 통일 등을 지원합니다. **다중 인증(MFA)**은 사용자 로그인 시 비밀번호 외에 추가 인증 요소(예: 휴대폰 앱)를 요구해 보안을 강화합니다.  
이 개념은 조직의 보안 강화, 비용 관리, 표준화된 정책 적용을 위한 필수 요소입니다. 예를 들어, AWS Organizations를 통해 모든 계정에 MFA를 강제 적용하면 보안 위험을 줄일 수 있습니다.

#### 주요 특징
1. **계정 통합 관리**: 여러 AWS 계정을 한 곳에서 관리해 정책 일관성 확보  
2. **정책 전파**: 조직 수준에서 정책을 자동으로 계정에 적용해 일관된 보안 표준  
3. **비용 통합**: 여러 계정의 비용을 하나의 지표로 모니터링해 예산 관리 용이  

> **💡 Tip:** AWS Organizations를 사용해 조직 전체에 MFA를 강제 적용해 보안 위험 최소화.  
> **⚠️ 주의:** MFA를 사용하지 않으면 AWS가 제공하는 보안 정책에 위반될 수 있습니다.

## 🖥️ AWS 콘솔에서 AWS Global Infrastructure 사용하기

### Step 1: AWS Global Infrastructure 서비스 접속  
1. AWS Management Console에 로그인합니다.  
   - URL: https://console.aws.amazon.com  
   - 로그인 후, 상단 메뉴에서 **"Services"**를 클릭합니다.  
2. 검색창에 **"AWS Global Infrastructure"**를 입력하고, 검색 결과에서 해당 서비스를 선택합니다.  
   - 이 서비스는 리전, AZ, 엣지 로케이션, IAM 구성 등을 관리하는 주요 대시보드입니다.  
3. **"AWS Global Infrastructure"** 클릭 후, 대시보드가 표시되면 정상적으로 접근했습니다.  

> **📸 화면 확인:** 대시보드 상단에 **"Regions"**, **"Availability Zones"**, **"Edge Locations"** 탭이 표시되고, IAM 관리 섹션이 포함되어야 합니다.  

---

### Step 2: [주요 작업 1 - 리소스 생성]  
1. **리전 및 AZ 설정**  
   - **"Regions"** 탭을 클릭하여 현재 사용 가능한 리전 목록을 확인합니다.  
   - **"Create Region"** 버튼을 클릭하면, 해당 리전에 대한 설정(예: VPC, EC2 인스턴스 배포)이 가능합니다.  
   - **"Region"** 필드에서 목록에서 리전을 선택하고, **"Create"** 버튼을 클릭합니다.  
2. **IAM 사용자 생성**  
   - **"IAM"** 탭에서 **"Users"**를 클릭하고, **"Add user"**를 선택합니다.  
   - **"User name"**을 입력하고, **"Programmatic access"** 및 **"AWS Management Console access"** 권한을 부여합니다.  
   - **"Next"** 버튼을 클릭한 후, **"Set permissions"**에서 **"Attach existing policies"**를 선택하여 정책을 연결합니다.  
3. **정책 생성 및 할당**  
   - **"Policies"** 탭에서 **"Create policy"**를 클릭하고, **"JSON"** 탭에서 정책을 직접 작성합니다.  
   - 예: `{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": "ec2:*", "Resource": "*"}]}`  
   - **"Create policy"** 버튼을 클릭해 정책을 저장하고, IAM 사용자에 연결합니다.  

> **📸 화면 확인:** IAM 사용자 목록에 생성된 사용자가 표시되고, 정책이 성공적으로 연결된 상태를 확인합니다.  

---

### Step 3: [주요 작업 2 - 설정/구성]  
1. **MFA 설정**  
   - IAM 사용자에 **"Multi-Factor Authentication (MFA)"**를 활성화합니다.  
   - **"Users"** 목록에서 사용자 클릭 후 **"Security credentials"** 탭에서 **"Enable MFA"**를 선택합니다.  
   - **"Authentication device"**에서 **"Virtual MFA device"**를 선택하고, **"Next"** 버튼을 클릭합니다.  
2. **IAM 그룹 및 역할 관리**  
   - **"Groups"** 탭에서 새 그룹을 생성하고, 사용자를 그룹에 할당합니다.  
   - **"Roles"** 탭에서 **"Create role"**을 클릭하고, **"AWS service"**에서 서비스 역할을 선택합니다.  
   - 역할 생성 후, **"Trust policy"**에서 권한을 설정하고 **"Create role"** 버튼을 클릭합니다.  
3. **AWS Organizations 구성**  
   - **"AWS Organizations"** 탭에서 **"Create organization"**을 클릭하고, **"Create"** 버튼을 선택합니다.  
   - 조직 생성 후, **"Create account"**를 통해 여러 리전에 걸친 계정을 관리할 수 있습니다.  

> **⚠️ 주의:** MFA를 활성화하면 원격 로그인 시 2단계 인증이 필요하며, 이는 보안 강화에 필수적입니다.  

---

### Step 4: 설정 확인 및 테스트  
1. **리소스 확인 방법**  
   - **"Regions"** 탭에서 생성한 리전이 목록에 포함되었는지 확인합니다.  
   - **"IAM"** 탭에서 사용자, 정책, 그룹, 역할의 상태를 검토합니다.  
2. **상태 확인 방법**  
   - **"CloudTrail"** 서비스에서 로그를 확인하여 리전 생성 및 IAM 설정이 성공적으로 기록되었는지 확인합니다.  
   - **"CloudWatch"**에서 리전 및 서비스의 상태 코드를 확인합니다.  
3. **정상 동작 테스트 방법**  
   - 생성한 IAM 사용자를 로그인해 리전 및 서비스 접근성을 테스트합니다.  
   - MFA를 사용해 로그인 시 2단계 인증이 제대로 작동하는지 확인합니다.  

> **💡 Tip:** AWS 프리티어는 IAM 사용자 및 리전 설정에 무료로 사용 가능하며, 비용 절감을 위해 초기 설정 시 활용하세요.  

---  

### 📊 서비스 비교 및 가격 요약  
| 서비스 | 기능 | 비용 | 주의사항 |  
|--------|------|------|----------|  
| **AWS Global Infrastructure** | 리전/AZ/엣지 로케이션 관리 | 무료(프리티어 포함) | 리전 생성 불가, 사전 정의 리전 사용 |  
| **IAM** | 사용자/정책/역할 관리 | 무료(프리티어 포함) | MFA 필수, 정책 권한 조심 |  
| **AWS Organizations** | 다중 계정 관리 | 무료(프리티어 포함) | 조직 생성 시 계정 수 제한 |  

> **⚠️ 주의:** 리전 및 AZ는 AWS가 사전에 정의한 위치로, 사용자가 직접 생성할 수 없습니다.  
> **📌 팁:** IAM 정책 작성 시 권한을 최소화하여 보안 위험을 줄이는 것이 중요합니다.

## ⌨️ AWS CLI로 AWS Global Infrastructure 사용하기

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
AWS CLI를 사용하기 전에 버전을 확인하고, IAM 자격 증명이 정상적으로 설정되었는지 확인해야 합니다. `aws configure get region` 명령어는 현재 사용 중인 리전을 확인합니다.  
**💡 Tip:** AWS CLI 설정은 `~/.aws/config` 파일에 저장됩니다.

---

### 예제 1: AWS Global Infrastructure 리소스 조회
```bash
# [AWS Global Infrastructure 리소스 목록 조회]
aws ec2 describe-regions --query 'Regions[].RegionName' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| `--query` | 결과 필터링 | `'Regions[].RegionName'` |
| `--output` | 출력 형식 | `table`, `json`, `text` |

**예상 출력:**
```
RegionName
----------------
us-east-1
eu-west-1
ap-northeast-1
...
```

**설명:**  
`describe-regions` 명령어는 AWS Global Infrastructure에 있는 모든 리전을 조회합니다. `--query` 옵션으로 특정 필드만 출력할 수 있습니다.

---

### 예제 2: AWS Global Infrastructure 리소스 생성
```bash
# [AWS Global Infrastructure 리소스 생성]
aws iam create-user --user-name "example-user"
```

**필수 옵션:**
- `--user-name`: IAM 사용자 이름 (필수)

**예상 출력:**
```json
{
    "User": {
        "UserName": "example-user",
        "UserId": "AIDAJQXLMBQBAI7E7Z7ZQ",
        "Arn": "arn:aws:iam::123456789012:user/example-user"
    }
}
```

**설명:**  
IAM 사용자를 생성할 때 `create-user` 명령어를 사용합니다. 생성된 사용자의 ARN은 리소스 식별에 사용됩니다.

---

### 예제 3: AWS Global Infrastructure 리소스 수정
```bash
# [AWS Global Infrastructure 리소스 수정]
aws iam attach-user-policy --user-name "example-user" --policy-arn "arn:aws:iam::123456789012:policy/ExamplePolicy"
```

**필수 옵션:**
- `--user-name`: 수정할 사용자 이름
- `--policy-arn`: 적용할 IAM 정책 ARN

**설명:**  
`attach-user-policy` 명령어는 사용자에게 IAM 정책을 부여합니다. 이는 리소스 접근 권한을 관리하는 데 사용됩니다.

---

### 예제 4: AWS Global Infrastructure 리소스 삭제
```bash
# [AWS Global Infrastructure 리소스 삭제]
aws iam delete-user --user-name "example-user"

# 삭제 확인
aws iam get-user --user-name "example-user"
```

> **⚠️ 주의:** 삭제는 되돌릴 수 없습니다. 신중하게 실행하세요.  
**예상 출력:**  
`get-user` 명령어는 삭제된 사용자를 조회할 수 없습니다. 삭제 후 확인 시 오류가 발생합니다.

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws ec2 describe-regions --query 'Regions[].RegionName' --output table
aws iam list-users
aws iam get-user --user-name "example-user"

# 생성
aws iam create-user --user-name "example-user"
aws ec2 create-tags --resources "arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0" --tags Key=Environment,Value=Production

# 수정
aws iam attach-user-policy --user-name "example-user" --policy-arn "arn:aws:iam::123456789012:policy/ExamplePolicy"

# 삭제
aws iam delete-user --user-name "example-user"
aws ec2 delete-tags --resources "arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0" --tags Key=Environment,Value=Production
```

**💡 Tip:**  
- 리전을 변경하려면 `aws configure set region us-west-2` 명령어를 사용합니다.  
- AWS Organizations를 관리하려면 `aws organizations` 명령어를 사용합니다.  
- MFA를 활성화하려면 `aws iam enable-mfa-device` 명령어를 사용합니다.  

**비용 주의사항:**  
- IAM 사용자 및 정책은 대부분 무료입니다.  
- EC2 인스턴스, S3 버킷 등 리소스는 사용량에 따라 비용이 발생할 수 있습니다.  
- AWS Free Tier를 활용해 초기 설정을 무료로 진행할 수 있습니다.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 AWS Global Infrastructure 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **AWS Regions 및 Availability Zones의 구조 및 역할**  
   - 설명: 리전은 데이터센터 그룹으로, AZ는 고가용성 및 장애 복구를 위한 독립적인 데이터센터입니다. 시험에서 리전/AZ의 수치적 비교(예: AWS의 21 리전, 185 AZ)와 데이터 전송 지연 시간 계산 문제가 자주 출제됩니다.  
   - 키워드: `Region`, `Availability Zone`, `High Availability`, `Fault Tolerance`

2. **Edge Locations의 기능 및 사용 사례**  
   - 설명: 글로벌 인프라스트럭처의 끝단 위치(Edge Locations)는 CDN 및 글로벌 애플리케이션의 지연 시간 최소화에 핵심입니다. 예: CloudFront의 글로벌 캐싱 전략과 관련된 문제는 빈도가 높습니다.  
   - 키워드: `Edge Locations`, `CDN`, `Latency Optimization`

3. **IAM 사용자 vs 역할의 차이점**  
   - 설명: IAM 사용자는 AWS 계정 내에서 자원에 접근하는 개체이며, 역할은 EC2 인스턴스나 다른 서비스 간 권한 위임에 사용됩니다. 시험에서 'IAM 역할이 왜 EC2 인스턴스에 필요하지?'와 같은 질문이 자주 등장합니다.  
   - 키워드: `IAM User`, `IAM Role`, `Service Principal`, `Trust Policy`

4. **AWS Organizations의 통합 관리 구조**  
   - 설명: Organizations는 다중 AWS 계정을 관리하는 데 사용되며, 태그 정책, 보안 정책 통합 등이 시험에서 자주 출제됩니다. 예: '어떤 경우에 Organizations를 사용해야 하나?'는 핵심 질문입니다.  
   - 키워드: `Multi-Account Management`, `Tagging Policy`, `Consolidated Billing`

5. **MFA의 필수성 및 구현 방법**  
   - 설명: MFA는 보안 강화를 위해 필수적입니다. 시험에서 'IAM 사용자에 MFA를 강제할 수 있는 방법'이나 'MFA 장치 종류'와 관련된 문제는 필수적으로 정리해야 합니다.  
   - 키워드: `Multi-Factor Authentication`, `Hardware MFA`, `Virtual MFA`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | "AZ는 리전 내부의 서버 클러스터"라고 설명하는 문제에서, AZ가 단일 데이터센터가 아니라 복수의 데이터센터를 포함한다고 오해할 수 있음 | AZ는 독립적인 데이터센터로 구성되며, 리전 내부에 위치함 |
| 함정 2 | "Edge Locations는 리전과 동일한 위치에 있다"고 잘못 인식하는 문제 | Edge Locations는 글로벌 네트워크의 끝단 위치로, 리전과는 별도의 위치에 있음 |
| 함정 3 | "IAM 사용자와 역할은 동일한 권한을 가진다"는 오해 | IAM 사용자는 특정 계정에 접근하고, 역할은 서비스 간 권한 위임에 사용됨 |

#### 🔄 AWS Global Infrastructure vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | AWS Global Infrastructure | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | 글로벌 네트워크 및 데이터센터 인프라 관리 | VPC, CloudFront | 지역적 네트워크 설정 vs 글로벌 리소스 최적화 |
| 확장성 | 리전/AZ 기반의 유연한 확장 | Route 53, Global Accelerator | 지역적 확장 vs 글로벌 트래픽 분산 |
| 비용 | 리전별 데이터 전송 비용 발생 | AWS Direct Connect | 고비용 대용량 트래픽 vs 저비용 연결 |
| 지연시간 | 리전 간 데이터 전송 지연 발생 | CloudFront | 지역적 지연 vs 글로벌 캐싱 최적화 |

#### 📝 시험 대비 체크리스트
- [ ] AWS Global Infrastructure의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  → 글로벌 네트워크 및 데이터센터 인프라를 통해 고가용성, 저지연, 확장성을 제공합니다.  
- [ ] AWS Global Infrastructure를 선택해야 하는 시나리오를 알고 있는가?  
  → 글로벌 사용자 대상 애플리케이션, 높은 가용성 요구, 데이터 전송 최적화 시  
- [ ] AWS Global Infrastructure의 제한사항/한계를 알고 있는가?  
  → 리전 간 데이터 전송 비용, 리전 확장 제한, Edge Locations의 위치 제약  
- [ ] AWS Global Infrastructure와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  → VPC는 지역적 네트워크, CloudFront는 글로벌 캐싱, Route 53는 DNS 해석에 집중  
- [ ] AWS Global Infrastructure의 비용 구조를 이해하고 있는가?  
  → 리전별 데이터 전송 비용, 리전 확장 비용, Edge Locations 사용 시 추가 비용  

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 AWS Global Infrastructure를 떠올리세요:  
> - **Region** (리전)  
> - **Availability Zone** (가용성 존)  
> - **Edge Location** (엣지 위치)  
> - **Global Accelerator** (글로벌 가속기)  
> - **Latency Optimization** (지연 최적화)

---

| ⬅️ 시작 | [📑 Day 1 목차](./README.md) | [🏠 Week 1](../README.md) | [IAM ➡️](./IAM.md) |

---
