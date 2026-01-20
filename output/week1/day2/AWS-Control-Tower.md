---

| [⬅️ AWS Organizations](./AWS-Organizations.md) | [📑 Day 2 목차](./README.md) | [🏠 Week 1](../README.md) | [다음 Day ➡️](../day3/README.md) |

---

# AWS Control Tower 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** AWS Control Tower는 AWS의 보안 및 규정 준수 관리를 위한 통합형 관리 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 기업이 AWS 환경에서 IAM 역할 위임, SCP 정책 적용 등을 수동으로 관리할 때 일관성 부족으로 인한 보안 취약점 발생.  
  *기존에는 개별 AWS 계정별로 정책을 수동으로 설정해야 했고, 중복된 권한 부여나 오류가 발생할 수 있었습니다.*
- **문제 2:** 다중 AWS 계정 환경에서 권한 경계(Permission Boundary) 적용 시, 수동 설정으로 인한 실수로 인한 권한 누수.  
  *예를 들어, 특정 사용자가 예상치 못한 리소스에 접근할 수 있는 경우가 자주 발생했습니다.*
- **문제 3:** 서비스 연결 역할(Service Linked Role) 구성 시, 정책 문서 작성 및 연결 과정에서 발생하는 오류로 인한 서비스 중단.  
  *수동 설정 과정에서 역할 권한이 잘못 설정되면 서비스가 정상적으로 동작하지 않을 수 있습니다.*

**AWS Control Tower로 해결:**
- **해결 1:** 통합된 정책 관리 시스템을 통해 IAM 역할 위임, SCP 정책, 권한 경계를 일관되게 적용할 수 있습니다.  
  *예: 모든 계정에 동일한 SCP 정책을 자동으로 적용하여 권한 누수를 방지합니다.*
- **해결 2:** 권한 경계를 단일 정책으로 관리하여 사용자가 특정 리소스에 접근하는 것을 제한할 수 있습니다.  
  *예: 개발팀은 특정 S3 버킷만 접근할 수 있도록 경계를 설정합니다.*
- **해결 3:** 서비스 연결 역할 구성 시 자동화된 정책 생성 및 연결 과정을 통해 실수를 최소화합니다.  
  *예: Lambda 함수에 연동된 서비스 역할이 자동으로 생성되어 정확한 권한을 부여합니다.*

### 비유로 이해하기
AWS Control Tower는 회사의 보안 감시원을 비유할 수 있습니다. 모든 직원이 특정 영역에만 접근할 수 있도록 권한을 설정하고, 불법적인 접근 시 즉시 경고를 보냅니다. 예를 들어, 회사의 서버에 접근할 수 있는 직원은 IT 부서만이 가능하며, 다른 부서가 접근하려고 하면 시스템이 자동으로 차단하고 경고를 발신합니다. 이처럼 Control Tower는 AWS 환경의 보안을 체계적으로 관리해줍니다.

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 기업이 다중 AWS 계정을 운영하고, 일관된 보안 정책을 관리해야 할 때 | 대규모 기업이 100개 이상의 AWS 계정을 운영하며, 모든 계정에 동일한 SCP 정책을 적용 |
| 시나리오 2 | 규정 준수 요구사항(예: GDPR, SOC 2)을 충족해야 할 때 | 금융기관이 데이터 보호 규정을 준수하기 위해 IAM 역할 위임과 서비스 연결 역할을 자동화 |
| 시나리오 3 | 외부 파트너나 제3자 서비스에 AWS 리소스 접근 권한을 부여해야 할 때 | 클라우드 서비스 제공업체가 고객의 S3 버킷에 접근 권한을 제한적으로 부여 |

**이럴 때 AWS Control Tower를 선택하세요:**
- ✅ 상황 1: 다중 AWS 계정 환경에서 일관된 정책 관리가 필요할 때  
- ✅ 상황 2: 규정 준수 요구사항을 충족해야 할 때  
- ✅ 상황 3: 제3자 서비스에 리소스 접근 권한을 제한적으로 부여해야 할 때  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ 상황 → **AWS IAM** 추천: 단일 계정에서의 정책 관리에 적합하지만, 다중 계정 환경에서는 한계가 있음  
- ❌ 상황 → **AWS Organizations** 추천: 계정 그룹화 및 정책 관리에 유용하지만, 서비스 연결 역할 구성은 별도 설정 필요  

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **AWS IAM** | IAM 역할 위임 및 서비스 연결 역할 구성 | Control Tower → IAM 역할 생성 → 서비스 연결 역할 연결 |
| **AWS STS** | 임시 자격 증명 생성을 통한 보안 관리 | Control Tower → STS를 통해 제3자에 임시 권한 부여 |
| **AWS CloudTrail** | 정책 변경 및 활동 로깅을 통한 감사 기능 | Control Tower → CloudTrail 로그 수집 → 감사 및 보고 |
| **AWS SCP (Service Control Policy)** | 정책 기반 접근 제어를 통한 리소스 접근 제한 | Control Tower → SCP 정책 적용 → 특정 리소스 접근 차단 |

**자주 사용되는 아키텍처 패턴:**
```
User → [AWS Control Tower] → [IAM 역할] → [STS 임시 자격 증명] → [AWS 서비스(예: S3)]
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **AWS Control Tower 사용** | $0.25/월 (최소 1개 계정) | 12개월 무료 |
| **서비스 연결 역할 생성** | $0.10/월 (최대 10개) | 12개월 무료 |
| **정책 변경 로그 저장** | $0.05/GB/월 | 12개월 무료 |

**비용 최적화 팁:**
1. 💡 팁 1: **프리티어 기간 동안 서비스를 테스트**하고, 필요한 기능만 활성화하여 비용 절감  
2. 💡 팁 2: **AWS Cost Explorer**를 사용해 사용량을 분석하고, 과다 사용되는 서비스를 정리  
3. 💡 팁 3: **SCP 정책을 최소 권한 원칙**에 따라 작성하여 불필요한 리소스 접근을 차단  

> **⚠️ 비용 주의:** **서비스 연결 역할**과 **정책 변경 로그**는 사용량에 따라 비용이 증가할 수 있으므로, 정기적으로 사용량을 점검하고 **AWS Budgets**를 설정하여 예산 초과를 방지해야 합니다.

## 📚 핵심 개념

### 개념 1: IAM 역할 위임 및 Trust 정책  
AWS Control Tower에서는 AWS Identity and Access Management (IAM) 역할을 통해 서비스 간 권한을 위임합니다. IAM 역할은 특정 AWS 서비스(예: Lambda, EC2)가 다른 서비스(예: S3, DynamoDB)에 접근할 수 있도록 권한을 부여하는 기능을 제공합니다. 이 역할을 사용하려면 **Trust 정책**(Trust Policy)을 구성해야 합니다. Trust 정책은 역할을 가진 서비스가 어떤 다른 서비스나 AWS 리소스에 접근할 수 있는지 명시합니다. 예를 들어, Lambda 함수가 S3 버킷에 데이터를 저장하려면 Lambda 역할에 S3 서비스를 Trust 정책에 추가해야 합니다.  

#### 왜 중요한가?  
- **보안 강화**: 역할을 통해 리소스에 대한 접근 권한을 제한하여 사전 허가 없이 리소스를 변경하는 위험을 줄입니다.  
- **중앙화 관리**: AWS Control Tower는 IAM 역할을 통한 권한 위임을 통해 조직 전체의 보안 정책을 일관되게 적용할 수 있습니다.  
- **서비스 간 통합**: 다양한 AWS 서비스 간의 협업이 필요할 때, Trust 정책을 통해 서비스 간 권한을 명확히 정의할 수 있습니다.  

#### 세부 요소  
| 요소 | 설명 | 예시 |
|-----|-----|-----|
| **Trust 정책** | 역할이 특정 서비스나 리소스에 접근할 수 있는 권한을 정의합니다. | `{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}` |
| **Role ARN** | 역할의 고유 식별자로, `arn:aws:iam::<account-id>:role/<role-name>` 형식입니다. | `arn:aws:iam::123456789012:role/LambdaExecutionRole` |
| **예시**: Lambda 함수가 S3 버킷에 접근 | Lambda 역할의 Trust 정책에 `s3.amazonaws.com`을 추가하여 S3 서비스 접근 권한 부여 |

> **💡 Tip:** Trust 정책은 AWS Control Tower에서 생성한 IAM 역할이 다른 AWS 서비스와 통신할 수 있도록 필수적인 구성 요소입니다. 정책은 최소 권한 원칙을 지키며 작성해야 합니다.

---

### 개념 2: STS(Security Token Service)로 임시 자격 증명 생성  
STS는 AWS에서 임시 자격 증명을 생성하는 서비스로, IAM 사용자나 역할을 통해 임시 AWS 계정 자격 증명을 생성할 수 있습니다. 이 임시 자격 증명은 특정 시간(예: 1시간) 동안만 유효하며, 보안성이 높은 환경에서 사용됩니다. 예를 들어, federated access(연합 접근) 시 사용자에게 임시 자격 증명을 제공하여 AWS 서비스에 접근하게 할 수 있습니다. AWS Control Tower에서는 STS를 통해 자격 증명을 생성하여 서비스 간 보안을 강화합니다.  

#### 작동 원리  
1. **요청자**: 사용자 또는 역할이 STS를 호출하여 임시 자격 증명 생성을 요청합니다.  
2. **STS 처리**: STS는 요청한 자격 증명을 생성하고, 해당 자격 증명을 사용자에게 반환합니다.  
3. **임시 자격 증명 사용**: 사용자는 생성된 자격 증명을 AWS CLI 또는 SDK를 통해 AWS 서비스에 접근합니다.  

> **💡 Tip:** AWS Control Tower에서 STS를 활용하면 조직 내부의 자격 증명 관리를 간소화할 수 있으며, 보안 위험을 줄일 수 있습니다.  

---

### 개념 3: 서비스 연결 역할(Service Linked Role) 구성  
AWS 서비스 연결 역할은 특정 AWS 서비스가 다른 서비스와 상호작용할 수 있도록 생성된 IAM 역할입니다. 예를 들어, S3 버킷을 관리하기 위해 AWS Lambda 함수가 실행되는 경우, Lambda 서비스는 S3 서비스와 통신하기 위해 **Service Linked Role**을 생성합니다. 이 역할은 AWS Control Tower에서 자동으로 생성되며, 해당 서비스의 기능을 제한하지 않고도 리소스에 접근할 수 있도록 보장합니다.  

#### 주요 특징  
1. **자동 생성**: AWS 서비스가 필요할 때 자동으로 생성되며, 사용자가 직접 관리할 필요가 없습니다.  
2. **제한된 권한**: 서비스 연결 역할은 해당 서비스의 기능에 필요한 최소한의 권한만 부여합니다.  
3. **보안 보장**: 서비스 간 통신 시 역할을 통해 접근 권한을 제한하여 보안을 강화합니다.  

> **⚠️ 주의:** 서비스 연결 역할을 삭제하면 해당 서비스의 기능이 중단될 수 있으므로, 삭제 전에 서비스 사용 여부를 확인해야 합니다.  

---

### 개념 4: 권한 경계(Permission Boundary) 적용  
권한 경계는 IAM 사용자, 역할, 서비스 계정이 가질 수 있는 최대 권한을 제한하는 정책입니다. AWS Control Tower에서는 권한 경계를 통해 조직 내 모든 사용자가 특정 리소스에 접근할 수 있는 권한을 제한합니다. 예를 들어, 권한 경계를 통해 특정 사용자가 S3 버킷을 생성하거나 삭제할 수 없도록 설정할 수 있습니다. 이는 조직 전체의 보안을 강화하고, 사전 허가 없이 리소스를 변경하는 위험을 줄입니다.  

#### 세부 요소  
| 요소 | 설명 | 예시 |
|-----|-----|-----|
| **권한 경계 정책** | 사용자나 역할이 가질 수 있는 최대 권한을 제한하는 IAM 정책입니다. | `{"Version": "2012-10-17", "Statement": [{"Effect": "Deny", "Action": "s3:PutObject", "Resource": "*"}]}` |
| **적용 대상** | 사용자, 역할, 서비스 계정 등 AWS Control Tower에서 관리하는 모든 리소스입니다. | 사용자 `AdminUser`에 권한 경계를 적용하여 S3 버킷 생성을 제한 |
| **예시**: S3 버킷 생성 제한 | 권한 경계 정책에 `s3:CreateBucket` 권한을 거부하여 사용자 접근 차단 |

> **💡 Tip:** 권한 경계는 IAM 정책보다 더 엄격한 제한을 가집니다. 사용자는 권한 경계를 통해 제한된 권한만 사용할 수 있습니다.  

---

### 개념 5: SCP(Service Control Policy) 정책 관리  
SCP는 AWS Organizations에서 조직 내 모든 AWS 계정에 적용되는 정책으로, 특정 AWS 서비스에 대한 접근 권한을 제한합니다. AWS Control Tower에서는 SCP를 통해 조직 내 모든 계정이 특정 서비스(예: EC2, S3)에 접근할 수 있는지 명확히 제어할 수 있습니다. 예를 들어, SCP를 통해 특정 계정이 S3 버킷 생성을 금지할 수 있습니다. 이는 조직 전체의 보안 및 규정 준수를 강화하는 데 필수적입니다.  

#### 세부 요소  
| 요소 | 설명 | 예시 |
|-----|-----|-----|
| **SCP 유형** | 서비스 접근 제한, 리소스 타입 제한, AWS 서비스 제한 등 다양한 유형이 있습니다. | `s3:PutObject` 권한을 특정 리소스에 제한 |
| **적용 범위** | 조직 내 특정 조직 단위(Organization Unit) 또는 전체 계정에 적용됩니다. | 모든 계정에 "S3 접근 제한" SCP 적용 |
| **예시**: EC2 인스턴스 생성 제한 | SCP를 통해 특정 계정이 EC2 인스턴스를 생성할 수 없도록 설정 |

> **💡 Tip:** SCP는 IAM 정책과 함께 사용하여 더 세밀한 보안 정책을 구현할 수 있습니다. AWS Control Tower에서는 SCP를 통해 조직 전체의 보안을 일관되게 관리할 수 있습니다.

## 🖥️ AWS 콘솔에서 AWS Control Tower 사용하기

### Step 1: AWS Control Tower 서비스 접속  
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
   - **AWS ID**와 **비밀번호**를 입력해 로그인합니다.  
2. 상단 검색창에서 "AWS Control Tower"를 입력하고, 검색 결과에서 해당 서비스를 클릭합니다.  
   - **AWS Control Tower 대시보드**가 열리면 정상적으로 서비스에 접근한 것입니다.  

> **📸 화면 확인:** AWS Control Tower 대시보드가 표시되면 정상입니다.  
> **💡 Tip:** 처음 접속 시 **"Get started"** 버튼을 클릭해 기본 설정을 진행하세요.  

---

### Step 2: [주요 작업 1 - 리소스 생성]  
1. **IAM 사용자 생성**  
   - **AWS Control Tower** 메뉴에서 **"AWS Organizations"** → **"Account Settings"** → **"IAM"** → **"Users"**로 이동합니다.  
   - **"Add user"** 버튼을 클릭해 새 사용자를 생성합니다.  
   - **"Programmatic access"**를 선택하고, **"Set password"**를 체크해 비밀번호를 설정합니다.  
   - **"User name"**을 입력하고, **"Next"**를 클릭합니다.  
2. **정책 연결**  
   - **"Attach existing policies directly"** 섹션에서 **"AmazonS3ReadOnlyAccess"** 정책을 선택합니다.  
   - **"Next"** → **"Create user"** 버튼을 클릭해 사용자를 생성합니다.  
3. **서비스 연결 역할 생성**  
   - **"Service-linked roles"** 섹션에서 **"AWSControlTowerServiceRoleForOrganizations"** 역할을 확인합니다.  
   - **"Create service-linked role"** 버튼을 클릭해 역할을 생성합니다.  

> **📸 화면 확인:** IAM 사용자 생성 후 **"User details"** 탭에서 생성된 사용자를 확인하고, **"Service-linked roles"**에서 역할이 생성되었는지 확인합니다.  

---

### Step 3: [주요 작업 2 - 설정/구성]  
1. **권한 경계 설정**  
   - **AWS Control Tower** 메뉴에서 **"AWS Organizations"** → **"Settings"** → **"Permission boundaries"**로 이동합니다.  
   - **"Create permission boundary"** 버튼을 클릭해 새로운 경계 정책을 생성합니다.  
   - **"Policy name"**을 입력하고, **"AmazonS3ReadOnlyAccess"** 정책을 선택합니다.  
   - **"Create"** 버튼을 클릭해 경계를 적용합니다.  
2. **SCP 설정**  
   - **"AWS Organizations"** → **"Settings"** → **"SCP"**로 이동합니다.  
   - **"Create SCP"** 버튼을 클릭해 새로운 SCP를 생성합니다.  
   - **"Policy name"**을 입력하고, **"AmazonS3ReadOnlyAccess"** 정책을 선택합니다.  
   - **"SCP"**를 조직 전체에 적용합니다.  
3. **정책 적용 확인**  
   - **"AWS Organizations"** → **"Account Settings"** → **"IAM"** → **"Users"**에서 사용자에게 경계 정책이 적용되었는지 확인합니다.  

> **⚠️ 주의:** SCP는 조직 내 모든 계정에 영향을 미치므로, **테스트 환경에서 먼저 적용**하고 실제 환경으로 확장하세요.  

---

### Step 4: 설정 확인 및 테스트  
1. **생성된 리소스 확인**  
   - **AWS Control Tower** 대시보드에서 **"Accounts"** 섹션에서 생성된 계정과 역할을 확인합니다.  
   - **"IAM"** → **"Users"**에서 생성된 사용자를 확인하고, **"Security credentials"** 탭에서 비밀번호를 확인합니다.  
2. **정책 적용 상태 확인**  
   - **"AWS Organizations"** → **"Settings"** → **"SCP"**에서 정책이 정상적으로 적용되었는지 확인합니다.  
3. **테스트 실행**  
   - **AWS CLI**를 사용해 S3 버킷에 접근해 테스트합니다:  
     ```bash
     aws s3 ls s3://example-bucket --region us-east-1
     ```
   - **"Access Denied"** 오류가 발생하면 정책이 제대로 적용되지 않았습니다.  
   - **"AWS Control Tower"** 대시보드에서 **"Audit"** 섹션에서 정책이 작동하는지 확인합니다.  

> **📸 화면 확인:** CLI 명령어 실행 후 결과를 확인하고, **"Audit"** 섹션에서 정책이 정상적으로 작동하는지 확인합니다.  

---

### ✅ 체크리스트: AWS Control Tower 설정 완료 여부  
- [ ] IAM 사용자 생성 및 정책 연결  
- [ ] 서비스 연결 역할 생성  
- [ ] 권한 경계 및 SCP 설정  
- [ ] 정책 적용 상태 확인  
- [ ] S3 접근 테스트 실행  
- [ ] AWS Control Tower 대시보드에서 모든 리소스 상태 확인  

> **💡 Tip:** AWS Free Tier 사용 시, **1년간 1000시간의 컴퓨팅 시간**과 **10GB의 스토리지**가 제공됩니다. AWS Control Tower는 Free Tier에 포함됩니다.  
> **⚠️ 주의:** 권한 경계와 SCP는 **역할을 제한하는 강력한 도구**이므로, **테스트 환경에서 먼저 적용**하고 실제 환경으로 확장하세요.

## ⌨️ AWS CLI로 AWS Control Tower 사용하기

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
AWS CLI를 사용하기 전에 버전을 확인하고, 현재 사용 중인 자격 증명(예: IAM 사용자)과 리전을 확인해야 합니다.  
`aws sts get-caller-identity` 명령어는 현재 로그인한 사용자의 ARN, ID, 리전을 보여줍니다.  
AWS Control Tower는 IAM, STS, Organizations 등과 연동하므로, 이 자격 증명이 정확히 설정되어야 합니다.

---

### 예제 1: AWS Control Tower 리소스 조회
```bash
# AWS Organizations 조직 목록 조회 (Control Tower 기반)
aws organizations list-organizations --query 'Organizations[?Status==`ACTIVE`].Id' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| `--query` | JSON 결과 필터링 | `'Organizations[?Status==`ACTIVE`].Id'` |
| `--output` | 출력 형식 | `table` (테이블 형식으로 보기) |

**예상 출력:**
```
| Id         |
|------------|
| org-123456 |
| org-789012 |
```

**설명:**  
AWS Control Tower는 AWS Organizations를 기반으로 구성됩니다. `list-organizations` 명령어는 활성 상태의 조직을 조회합니다.  
`--query` 옵션을 통해 필터링하여 필요한 정보만 출력할 수 있습니다.

---

### 예제 2: AWS Control Tower 리소스 생성
```bash
# Control Tower용 서비스 연결 역할 생성 (IAM 역할 생성)
aws iam create-role \
    --role-name "ControlTowerServiceRole" \
    --assume-role-policy-document file://trust-policy.json
```

**필수 옵션:**
- `--role-name`: 생성할 IAM 역할 이름
- `--assume-role-policy-document`: 역할이 신뢰하는 서비스 정책 파일 경로 (예: `trust-policy.json`)

**trust-policy.json 예시:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "controltower.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

**예상 출력:**
```json
{
    "Role": {
        "RoleId": "ARO1234567890ABCDEF",
        "RoleName": "ControlTowerServiceRole",
        "Arn": "arn:aws:iam::123456789012:role/ControlTowerServiceRole"
    }
}
```

**설명:**  
Control Tower는 서비스 연결 역할을 통해 AWS 서비스와 통신합니다. `create-role` 명령어로 역할을 생성하고, `trust-policy.json` 파일로 신뢰하는 서비스를 정의합니다.  
이 역할은 Control Tower의 기능 실행에 필수적입니다.

---

### 예제 3: AWS Control Tower 리소스 수정
```bash
# SCP 정책 수정 (Organizations SCP 업데이트)
aws organizations update-policy \
    --policy-id "policy-123456" \
    --name "ControlTowerSCP" \
    --description "ControlTower SCP for compliance" \
    --content file://scp-policy.json
```

**필수 옵션:**
- `--policy-id`: 수정할 SCP 정책 ID
- `--content`: 정책 내용 파일 경로 (예: `scp-policy.json`)

**scp-policy.json 예시:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "ec2:*",
      "Resource": "*"
    }
  ]
}
```

**예상 출력:**
```json
{
    "Policy": {
        "PolicyId": "policy-123456",
        "PolicyName": "ControlTowerSCP",
        "Arn": "arn:aws:organizations::123456789012:policy/o-123456789012/policy-123456"
    }
}
```

**설명:**  
AWS Control Tower는 AWS Organizations를 통해 정책을 관리합니다. `update-policy` 명령어로 SCP 정책을 수정할 수 있습니다.  
SCP는 리소스에 대한 최소 권한을 설정하는 데 사용되며, 보안 준수에 필수적입니다.

---

### 예제 4: AWS Control Tower 리소스 삭제
```bash
# IAM 역할 삭제
aws iam delete-role --role-name "ControlTowerServiceRole"

# 삭제 확인
aws iam get-role --role-name "ControlTowerServiceRole"
```

> **⚠️ 주의:** 삭제는 되돌릴 수 없습니다. Control Tower용 역할을 삭제하면 서비스가 중단될 수 있습니다.  
> 삭제 전에 `--dry-run` 옵션으로 확인하세요:  
> `aws iam delete-role --role-name "ControlTowerServiceRole" --dry-run`

**예상 출력:**
```
An error occurred (InvalidInput) when calling the DeleteRole operation: The role 'ControlTowerServiceRole' cannot be deleted because it is being used by an AWS service.
```

**설명:**  
Control Tower가 사용하는 역할은 삭제할 수 없습니다. 서비스 연결 역할을 삭제하려면 먼저 해당 역할을 해지해야 합니다.  
`--dry-run` 옵션은 실제 삭제 전에 유효성을 검증합니다.

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws organizations list-organizations
aws iam list-roles
aws iam get-role --role-name "ControlTowerServiceRole"

# 생성
aws iam create-role --role-name "ControlTowerServiceRole" --assume-role-policy-document file://trust-policy.json
aws organizations create-policy --name "ControlTowerSCP" --description "ControlTower SCP" --content file://scp-policy.json

# 수정
aws organizations update-policy --policy-id "policy-123456" --content file://scp-policy.json

# 삭제
aws iam delete-role --role-name "ControlTowerServiceRole"
```

**팁:**  
- Control Tower용 역할은 `controltower.amazonaws.com`을 신뢰하는 서비스 연결 역할로 생성해야 합니다.  
- SCP는 리소스에 대한 권한을 제어하는 필수 정책이며, `aws organizations list-policies`로 확인할 수 있습니다.  
- CLI 명령어는 AWS Control Tower의 기능을 직접 조작하는 데 사용되며, **IAM 역할과 정책 설정에 주의**해야 합니다.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 AWS Control Tower 포인트

#### 📌 핵심 출제 포인트 TOP 5  
1. **SCP(Service Control Policy) 정책 관리**:  
   - 설명: AWS Control Tower는 SCP를 통해 조직 내 모든 계정에 일관된 보안 정책을 적용합니다. 이는 IAM 정책과 차별화되며, 최소 권한 원칙을 강제하는 핵심 개념입니다.  
   - 키워드: `SCP`, ` centralized policy`, `least privilege`

2. **서비스 연결 역할(Service Linked Role) 구성**:  
   - 설명: Control Tower는 AWS 서비스(예: CloudTrail, Config)와 통합될 때 자동으로 서비스 연결 역할을 생성합니다. 이 역할은 서비스의 기능을 제한하고 보안 위험을 최소화하는 데 핵심입니다.  
   - 키워드: `Service Linked Role`, `service integration`, `role delegation`

3. **권한 경계(Permission Boundary) 적용**:  
   - 설명: 권한 경계는 사용자 및 역할의 권한을 추가로 제한하는 정책입니다. Control Tower는 이 기능을 통해 최소 권한을 보장하며, 시험에서 보안 정책 설계 문제에 자주 등장합니다.  
   - 키워드: `Permission Boundary`, `least privilege`, `policy restriction`

4. **IAM 역할 위임 및 trust 정책**:  
   - 설명: Control Tower는 IAM 역할을 다른 서비스 또는 사용자에게 위임할 때 trust 정책을 필수적으로 적용합니다. 이는 자원 접근 권한의 범위를 정확히 제어하는 핵심 메커니즘입니다.  
   - 키워드: `trust policy`, `role delegation`, `cross-account access`

5. **STS(Service Security Token Service) 활용**:  
   - 설명: Control Tower는 STS를 통해 임시 자격 증명을 생성하여 보안 자원 접근 시 임시 권한을 제공합니다. 이는 장기 자격 증명보다 보안성이 높은 시나리오에서 필수적인 개념입니다.  
   - 키워드: `STS`, `temporary credentials`, `security token`

#### ⚠️ 시험에서 자주 나오는 함정  
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | SCP와 IAM 정책의 차이를 혼동하는 경우 | SCP는 조직 수준에서 강제되며, IAM 정책은 개별 사용자/역할에 적용됩니다. |
| 함정 2 | 서비스 연결 역할을 일반 역할로 오인하는 경우 | 서비스 연결 역할은 AWS 서비스와 자동 생성되며, 수동으로 생성할 수 없습니다. |
| 함정 3 | 권한 경계를 IAM 정책으로 오인하는 경우 | 권한 경계는 별도 정책으로 설정되며, IAM 정책과 병렬로 작동합니다. |

#### 🔄 AWS Control Tower vs 비슷한 서비스 비교 (시험 단골!)  
| 비교 항목 | AWS Control Tower | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | 조직 전체 보안 및 정책 통합 | AWS Organizations | 계정 관리에 중점 |
| 확장성 | 자동화된 정책 적용 및 서비스 통합 | AWS CloudFormation | 인프라 코드화에 중점 |
| 비용 | SCP 및 서비스 연결 역할 관리 비용 | AWS IAM 정책 | 개별 사용자/역할 관리 |
| 지연시간 | 서비스 자동 통합으로 즉시 적용 | AWS CLI/Console | 수동 설정이 필요 |
| 보안 강도 | SCP와 서비스 연결 역할로 보안 강화 | IAM 정책 | 개별 권한 관리 |

#### 📝 시험 대비 체크리스트  
- [ ] AWS Control Tower의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  - *예: "AWS Control Tower는 AWS 조직의 보안 및 정책을 통합적으로 관리하는 서비스입니다."*  
- [ ] AWS Control Tower를 선택해야 하는 시나리오를 알고 있는가?  
  - *예: "다수의 AWS 계정이 존재하고, 일관된 보안 정책을 강제해야 할 경우"*  
- [ ] AWS Control Tower의 제한사항/한계를 알고 있는가?  
  - *예: "서비스 연결 역할은 AWS 서비스에 제한되며, 수동 생성 불가"*  
- [ ] AWS Control Tower와 AWS Organizations의 차이점을 설명할 수 있는가?  
  - *예: "Organizations는 계정 관리에 중점, Control Tower는 보안 및 정책 통합에 중점"*  
- [ ] AWS Control Tower의 비용 구조를 이해하고 있는가?  
  - *예: "SCP 및 서비스 연결 역할 관리 비용, 프리티어는 7일간 100달러 제공"*  

#### 💡 시험 팁  
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 AWS Control Tower를 떠올리세요:  
> - `SCP`(Service Control Policy)  
> - `Service Linked Role`  
> - `Permission Boundary`  
> - `trust policy`  
> - `temporary credentials`

---

| [⬅️ AWS Organizations](./AWS-Organizations.md) | [📑 Day 2 목차](./README.md) | [🏠 Week 1](../README.md) | [다음 Day ➡️](../day3/README.md) |

---
