---

| [⬅️ Detective](./Detective.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 4](../README.md) | [CloudTrail ➡️](./CloudTrail.md) |

---

# Config 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** Config는 AWS 클라우드 자원의 **보안 준수 및 구성 관리**를 위한 **자동화된 감시 및 정책 실행** 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 기존에는 수동으로 인프라 구성 상태를 점검해야 했고, 변경 사항을 실시간으로 파악하기 어려웠습니다. 예를 들어, EC2 인스턴스의 보안 그룹 설정이 변경되었는지 확인하려면 수작업으로 확인해야 했습니다.  
- **문제 2:** 보안 정책 위반을 감지하는 데는 별도의 도구가 필요했고, 다양한 서비스에서 발생한 위험 정보를 통합적으로 분석하기 어려웠습니다. 예를 들어, S3 버킷 권한 설정이 잘못되었는지 확인하려면 여러 서비스를 확인해야 했습니다.  
- ** 문제 3:** 자원의 구성 상태를 기록해두지 않아, 사고 발생 시 원인 분석이 어려웠습니다. 예를 들어, RDS 인스턴스가 삭제되었는지 알기 위해 별도의 로그를 관리해야 했습니다.

**Config로 해결:**
- **해결 1:** Config는 자원의 구성 상태를 실시간으로 감시하고, 변경 사항을 자동으로 기록해주는 기능으로 수동 점검을 대체합니다.  
- **해결 2:** Config Rules와 Security Hub 등을 통해 보안 정책 위반을 자동 감지하고, 여러 서비스에서 수집된 위험 정보를 통합적으로 분석합니다.  
- **해결 3:** 모든 자원의 구성 변경 사항을 이력 관리해, 사고 발생 시 원인을 빠르게 추적할 수 있도록 지원합니다.

### 비유로 이해하기
Config는 회사의 **보안 감시원** 역할을 합니다. 회사 건물의 문을 열고 들어오는 사람을 감시하며, 문이 열려 있는지, 위험한 물건이 들어오지 않는지 등을 실시간으로 확인합니다. 이처럼 Config는 AWS 자원의 구성 상태를 감시하고, 이상 징후를 감지해 보안 위험을 예방합니다.  

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | AWS 자원의 구성 상태를 실시간으로 감시하고, 보안 정책 준수 여부를 검증 | 금융 기관이 S3 버킷에 암호화 설정을 강제하는 정책을 통해 데이터 유출 위험을 방지 |
| 시나리오 2 | 보안 위험을 통합적으로 분석하고, 위협을 신속히 대응 | 클라우드 서비스 제공업체가 GuardDuty와 Security Hub를 통해 로그인 시도 이상 징후를 탐지 |
| 시나리오 3 | 자원의 변경 사항을 기록해, 사고 발생 시 원인을 분석 | e-commerce 플랫폼이 RDS 인스턴스 삭제 사고를 조사할 때 이력 데이터를 활용 |

**이럴 때 Config를 선택하세요:**
- ✅ **자원 구성 상태를 실시간으로 모니터링해야 하는 경우**  
- ✅ **보안 정책 위반을 자동 감지하고 대응해야 하는 경우**  
- ✅ **사고 분석을 위해 자원 변경 이력이 필요한 경우**

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ **단순한 로그 수집이 필요한 경우 → CloudWatch** (AWS 내부 로그 모니터링)  
- ❌ **데이터베이스 백업 관리가 필요한 경우 → AWS Backup** (백업 및 복구 관리)  
- ❌ **고성능 컴퓨팅 자원 관리가 필요한 경우 → EC2 Auto Scaling** (자동 확장 및 관리)

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **GuardDuty** | 보안 위협 탐지 결과를 Config에 통합 | Config → GuardDuty → Security Hub |
| **Security Hub** | 보안 위험을 통합 분석하고, Config Rules와 연동 | Config → Security Hub → GuardDuty |
| **CloudTrail** | Config의 이력 데이터를 보완하여 보안 이벤트를 추적 | CloudTrail → Config → AWS Lambda |

**자주 사용되는 아키텍처 패턴:**
```
User → CloudFront → S3 (Config 감시 대상)
           ↓
          EC2 (Config 감시 대상)
           ↓
        CloudWatch (로그 수집)
           ↓
      Security Hub (위험 통합 분석)
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **AWS Config Usage** | $0.10/월 (최대 200개 자원) | 12개월 무료 |
| **Config Rules** | $0.01/월 (Rule 수) | 12개월 무료 |
| **Security Hub Integration** | $0.05/월 (연동 서비스 수) | 12개월 무료 |

**비용 최적화 팁:**
1. 💡 **프리티어 기간 동안 무료로 사용**: 12개월 동안 AWS Config, Rules, Security Hub 연동을 무료로 사용할 수 있습니다.  
2. 💡 **필요한 자원만 감시 대상으로 설정**: 모든 자원을 감시하지 않고, 보안 위험 있는 자원만 대상으로 설정해 비용을 절감합니다.  
3. 💡 **CloudWatch 로그를 통해 이력 데이터 분석**: Config의 이력 데이터를 CloudWatch로 전송해 비용 효율적인 분석을 수행합니다.

> **⚠️ 비용 주의:** **Security Hub**와 **GuardDuty**는 Config와 별도로 과금되므로, 보안 위협 탐지 기능을 사용할 경우 추가 비용이 발생할 수 있습니다. 예를 들어, GuardDuty의 유료 기능을 활성화하면 월 $20 이상의 비용이 발생할 수 있습니다.

## 📚 핵심 개념

### 개념 1: **GuardDuty의 위협 탐지 및 머신러닝 기반 분석**
GuardDuty는 AWS에서 제공하는 실시간 위협 탐지 서비스로, 클라우드 환경에서의 보안 위험을 자동으로 감지합니다. 이 서비스는 머신러닝 기반의 분석을 통해 이상 행동, 악성 활동, 네트워크 공격 등을 식별합니다. 예를 들어, AWS 리소스에 대한 비정상적인 접근이나 데이터 유출 시도를 감지하여 알림을 제공합니다. GuardDuty는 AWS 서비스의 네트워크 트래픽을 분석하며, 보안 위험을 수준별로 분류해 사용자가 우선순위를 설정할 수 있도록 도와줍니다.

#### 왜 중요한가?
- **실시간 위협 탐지**: 클라우드 환경에서 발생하는 위협을 즉시 감지하여 피해를 최소화합니다.  
- **자동화된 분석**: 머신러닝 기반의 분석으로 수동적인 위협 탐지보다 높은 정확도를 제공합니다.  
- **통합 보안 플랫폼**: AWS 보안 서비스 간 연동을 통해 종합적인 보안 전략을 구축할 수 있습니다.  

#### 세부 요소
| 요소 | 설명 | 예시 |
|-----|-----|-----|
| **위협 탐지** | AWS 리소스에 대한 이상적인 네트워크 활동을 감지 | 비정상적인 데이터 유출 시도 감지 |
| **머신러닝 분석** | 기존 패턴을 학습해 새로운 위협을 예측 | 악성 IP 주소의 패턴 분석 |
| **위험 수준 분류** | 위협의 위험도를 1~4단계로 구분 | 중간 위험 수준의 탐지 시 알림 제공 |

> **💡 Tip:** GuardDuty는 AWS CloudTrail과 연동해 보다 정확한 위협 분석을 가능하게 하며, Security Hub와 통합해 종합적인 보안 대시보드를 구성할 수 있습니다.

---

### 개념 2: **Security Hub의 통합 보안 데이터 수집 및 위험 분류**
Security Hub는 AWS 내 보안 데이터를 중앙에서 수집하고, 위험을 분류해 사용자에게 알리는 통합 보안 플랫폼입니다. 이 서비스는 GuardDuty, Inspector, CloudTrail 등 다양한 보안 서비스와 연동해 모든 위협 정보를 한 곳에서 모아 분석합니다. Security Hub는 위험 수준을 기준으로 알림을 제공하며, 사용자가 위험을 우선순위별로 관리할 수 있도록 도와줍니다. 예를 들어, 보안 검사 결과나 로그에서 발견된 이상 징후를 분석해 위험을 평가하고, 관련된 보안 서비스와 연동해 해결 방안을 제안합니다.

#### 작동 원리
1. **데이터 수집**: 다양한 AWS 보안 서비스(Inspector, CloudTrail 등)의 데이터를 수집합니다.  
2. **위험 분류**: 수집된 데이터를 기반으로 위험을 수준별로 분류하고, 위협 유형을 식별합니다.  
3. **알림 및 대응**: 위험 수준에 따라 사용자에게 알림을 제공하고, 관련된 보안 서비스와 연동해 자동화된 대응을 실행합니다.  

> **💡 Tip:** Security Hub는 보안 정책을 통합해 위험을 체계적으로 관리할 수 있도록 하며, 보안 검사 결과를 실시간으로 분석해 대응 전략을 수립하는 데 유용합니다.

---

### 개념 3: **Config Rules의 자동화된 보안 준수 검증 및 정책 적용**
Config Rules는 AWS 리소스의 구성이 보안 정책을 준수하는지 자동으로 검증하는 기능입니다. 이 기능은 사용자가 정의한 정책을 기반으로 리소스 상태를 모니터링하고, 위반 시 알림을 제공합니다. 예를 들어, S3 버킷에 암호화를 적용하지 않은 경우를 감지해 사용자에게 경고를 전송합니다. Config Rules는 AWS 서비스 간 연동을 통해 실시간으로 정책을 적용하고, 리소스 변경 시 즉시 검증을 수행합니다. 이를 통해 보안 정책을 지속적으로 준수할 수 있습니다.

#### 주요 특징
1. **정책 기반 검증**: 사용자가 정의한 보안 정책에 따라 리소스 상태를 자동으로 검사합니다.  
2. **실시간 모니터링**: 리소스 변경 시 즉시 검증을 수행해 문제를 즉시 식별합니다.  
3. **통합 자동화**: AWS 서비스와 연동해 정책 위반 시 자동화된 조치를 실행할 수 있습니다.  

> **💡 Tip:** Config Rules는 보안 정책을 지속적으로 준수하려는 환경에서 필수적인 도구로, 정책 변경 시 자동으로 리소스를 업데이트해 보안 위험을 최소화할 수 있습니다.

## 🖥️ AWS 콘솔에서 Config 사용하기

### Step 1: Config 서비스 접속  
1. AWS Management Console에 로그인합니다  
   - URL: [https://console.aws.amazon.com](https://console.aws.amazon.com)  
2. 상단 검색창에서 "Config"를 입력 후 검색합니다  
   - **팁:** "Config" 서비스는 "Service" 카테고리에 위치합니다  
3. 검색 결과에서 "AWS Config"를 클릭합니다  

> **📸 화면 확인:** Config 대시보드가 표시되면 정상입니다. 좌측 메뉴에서 "Overview" 탭을 확인하세요.  

---

### Step 2: [주요 작업 1 - 리소스 생성]  
1. **Config 서비스 활성화**  
   - 좌측 메뉴에서 "Settings" → "Service roles"로 이동합니다  
   - "AWSConfigServiceRole"이 생성되어 있는지 확인합니다  
   - 없으면 "Create role" 버튼을 클릭해 역할을 생성합니다  
2. **리소스 모니터링 설정**  
   - "Settings" → "Resource types"로 이동합니다  
   - "All resources"를 선택하여 모든 리소스를 모니터링 대상으로 설정합니다  
   - "Include all resources" 체크박스를 선택 후 "Save changes"를 클릭합니다  
3. **모니터링 시작**  
   - "Settings" → "Delivery"로 이동합니다  
   - "Delivery channel"을 클릭해 결과를 S3 버킷 또는 CloudWatch로 전송할 수 있습니다  
   - "Save changes"를 클릭해 설정을 저장합니다  

> **📸 화면 확인:** "Resource types" 탭에서 "All resources"가 선택된 상태로 표시됩니다.  

---

### Step 3: [주요 작업 2 - 설정/구성]  
1. **Config 규칙 생성**  
   - 좌측 메뉴에서 "Rules" → "Create rule"을 클릭합니다  
   - 규칙 이름을 입력 후 "Rule type"에서 "Custom rule"을 선택합니다  
   - "Lambda function"을 연결해 규칙을 구현합니다 (예: IAM 권한 확인)  
2. **GuardDuty 통합 설정**  
   - "Settings" → "Integration" → "GuardDuty"로 이동합니다  
   - "Enable integration" 체크박스를 선택해 GuardDuty와 연동합니다  
   - "Save changes"를 클릭해 설정을 저장합니다  
3. **Security Hub 연동**  
   - "Settings" → "Integration" → "Security Hub"로 이동합니다  
   - "Enable integration" 체크박스를 선택해 Security Hub와 연동합니다  
   - "Save changes"를 클릭해 설정을 저장합니다  

> **⚠️ 주의:** GuardDuty 및 Security Hub 연동 시 IAM 권한을 확인해주세요. 정책이 부족하면 연동 실패가 발생할 수 있습니다.  

---

### Step 4: 설정 확인 및 테스트  
1. **생성된 리소스 확인 방법**  
   - "Overview" 탭에서 "Compliance" 섹션을 확인합니다  
   - "Compliant" 또는 "Non-compliant" 상태를 통해 설정이 적용되었는지 확인합니다  
2. **상태 확인 방법**  
   - "Settings" → "Service roles"에서 역할이 정상적으로 생성되었는지 확인합니다  
   - "Delivery" 탭에서 결과 전송이 설정되었는지 확인합니다  
3. **정상 동작 테스트**  
   - "Rules" 탭에서 "Test rule"을 클릭해 규칙이 작동하는지 테스트합니다  
   - 예상 결과가 표시되면 설정이 성공적으로 완료되었습니다  

> **📸 화면 확인:** "Compliance" 섹션에서 "Compliant" 상태가 표시되면 정상입니다.  

---

### ✅ 체크리스트: Config 설정 완료 여부  
- [ ] AWS Config 서비스에 접근할 수 있는지 확인  
- [ ] 모든 리소스를 모니터링 대상으로 설정했는지 확인  
- [ ] GuardDuty 및 Security Hub 연동이 완료되었는지 확인  
- [ ] Config 규칙이 생성되었고, 테스트를 완료했는지 확인  
- [ ] 결과 전송 설정이 올바르게 구성되었는지 확인  

> **💡 Tip:** AWS 프리티어는 750시간의 무료 사용 권한을 제공합니다. Config 서비스는 20시간 이내 사용 가능합니다.  
> **💡 Tip:** Config의 Cost Explorer를 사용해 비용을 모니터링하세요. 불필요한 리소스 모니터링은 비용 증가를 유발할 수 있습니다.

## ⌨️ AWS CLI로 Config 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

> **💡 Tip:** AWS CLI를 사용하기 전에 [AWS CLI 설치 가이드](https://docs.aws.amazon.com/cli/latest/userguide/cli-install.html)를 참고해 설치 및 설정을 완료하세요.  
> **⚠️ 주의:** AWS CLI 명령어는 서비스별로 다름에 주의하세요. 예를 들어, `config` 서비스는 `config` 명령어로, `guardduty` 서비스는 `guardduty` 명령어로 사용합니다.

---

### 예제 1: Config 리소스 조회
```bash
# [Config 리소스 목록 조회]
aws config list-configuration-recorders --query '[].ConfigurationRecorderName' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| `--query` | 결과 필터링 | `'[].ConfigurationRecorderName'` |
| `--output` | 출력 형식 | `json`, `table`, `text` |

**예상 출력:**
```
ConfigurationRecorderName
--------------------------
example-recorder
```

> **💡 Tip:** `list-configuration-recorders` 명령어는 Config 리소스 기록자(Recorder) 목록을 조회합니다. `--query` 옵션을 사용해 특정 필드만 출력할 수 있습니다.

---

### 예제 2: Config 리소스 생성
```bash
# [Config 리소스 생성]
aws config put-configuration-recorder \
    --configuration-recorder-name "example-recorder" \
    --role-arn "arn:aws:iam::123456789012:role/ConfigRecorderRole"
```

**필수 옵션:**
- `--configuration-recorder-name`: 리소스 이름 (예: `example-recorder`)
- `--role-arn`: IAM 역할 ARN (Config 리소스가 실행할 수 있는 권한)

**예상 출력:**
```json
{
    "ConfigurationRecorder": {
        "ConfigurationRecorderName": "example-recorder",
        "RoleARN": "arn:aws:iam::123456789012:role/ConfigRecorderRole",
        "AWSRegion": "ap-northeast-1",
        "recordingStrategy": {
            "allSupported": true
        }
    }
}
```

> **💡 Tip:** `put-configuration-recorder` 명령어는 Config 리소스 기록자를 생성합니다. IAM 역할 권한은 반드시 `ConfigService` 및 `CloudWatchEvents` 접근 권한을 포함해야 합니다.

---

### 예제 3: Config 리소스 수정
```bash
# [Config 리소스 수정]
aws config update-configuration-recorder \
    --configuration-recorder-name "example-recorder" \
    --role-arn "arn:aws:iam::123456789012:role/UpdatedConfigRecorderRole"
```

> **💡 Tip:** `update-configuration-recorder` 명령어는 기존 리소스의 역할 ARN을 수정할 수 있습니다. 리소스 이름은 변경할 수 없습니다.

---

### 예제 4: Config 리소스 삭제
```bash
# [Config 리소스 삭제]
aws config delete-configuration-recorder --configuration-recorder-name "example-recorder"

# 삭제 확인
aws config get-configuration-recorder --configuration-recorder-name "example-recorder"
```

> **⚠️ 주의:** 삭제는 되돌릴 수 없습니다. 삭제 후 `get-configuration-recorder` 명령어는 오류를 반환합니다.

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws config list-configuration-recorders
aws config get-configuration-recorder --configuration-recorder-name "name"

# 생성
aws config put-configuration-recorder --configuration-recorder-name "name" --role-arn "arn"

# 수정
aws config update-configuration-recorder --configuration-recorder-name "name" --role-arn "arn"

# 삭제
aws config delete-configuration-recorder --configuration-recorder-name "name"
```

---

### 📌 Config 관련 서비스 간 연동
| 서비스 | 설명 | CLI 명령어 |
|-------|------|-----------|
| **Config** | AWS 리소스 구성 상태를 추적 | `config` |
| **GuardDuty** | 보안 위협 탐지 | `guardduty` |
| **Inspector** | 보안 검사 실행 | `inspector` |
| **Security Hub** | 보안 위험 통합 관리 | `securityhub` |
| **Detective** | 보안 이벤트 분석 | `detective` |
| **CloudTrail** | API 호출 로그 추적 | `cloudtrail` |
| **Trusted Advisor** | 최적화 및 보안 권장사항 | `support` |

> **💡 Tip:** Config는 `CloudTrail`와 연동해 API 호출 로그를 분석하고, `Security Hub`와 연동해 보안 위험을 통합적으로 관리할 수 있습니다.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 Config 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **Config Rules의 자동화된 보안 준수 검증**  
   - 설명: AWS Config Rules는 AWS 서비스 및 고객 정책에 기반한 자동화된 준수 검증을 수행합니다. 이는 보안 규정 준수, 인프라 표준화, 리스크 관리에 필수적입니다.  
   - 키워드: `보안 준수`, `정책 적용`, `자동화`

2. **AWS Config의 리소스 상태 추적 기능**  
   - 설명: Config는 AWS 리소스의 현재 상태를 실시간으로 추적해, 이전 상태와의 차이를 비교하는 'Difference View' 기능을 제공합니다. 이는 보안 이벤트 분석 및 변경 관리에 핵심입니다.  
   - 키워드: `리소스 추적`, `차이 분석`, `변경 관리`

3. **Config와 CloudTrail의 통합 활용**  
   - 설명: Config는 리소스 상태를 추적하고, CloudTrail은 API 호출 로그를 제공합니다. 두 서비스를 결합하면 보안 이벤트의 원인과 결과를 심층 분석할 수 있습니다.  
   - 키워드: `CloudTrail 통합`, `API 로그`, `이벤트 분석`

4. **Config의 비용 구조 이해**  
   - 설명: Config는 리소스 수와 상태 저장 기간에 따라 비용이 발생합니다. 프리티어는 1년간 50개 리소스까지 무료로 사용 가능하므로, 작은 규모 환경에서는 비용 절감에 유리합니다.  
   - 키워드: `비용 구조`, `프리티어`, `리소스 수`

5. **Config의 제한사항 및 한계**  
   - 설명: Config는 리소스 상태를 추적하지만, 실시간 변경 감지나 특정 리소스 타입(예: Lambda 함수)은 지원하지 않습니다. 이는 시험에서 흔히 출제되는 구조적 한계입니다.  
   - 키워드: `리소스 제한`, `타입 지원`, `실시간 감지`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | "Config는 리소스 변경을 실시간으로 감지한다"는 문장이 출제될 경우, **False**로 판단해야 합니다. Config는 주기적으로 상태를 체크하므로 실시간 감지가 아닙니다. | **False** |
| 함정 2 | "Config는 모든 리소스 타입을 지원한다"는 문장이 출제될 경우, **False**로 판단해야 합니다. 특정 리소스(예: Lambda)는 지원하지 않습니다. | **False** |
| 함정 3 | "Config의 비용은 리소스 수에만 의존한다"는 문장이 출제될 경우, **False**로 판단해야 합니다. 상태 저장 기간도 비용에 영향을 미칩니다. | **False** |

#### 🔄 Config vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | Config | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| **용도** | 리소스 상태 추적, 보안 준수 검증 | CloudTrail (API 로그), Security Hub (통합 보안 분석) | 리소스 상태 추적 및 정책 검증이 필요한 경우 |
| **확장성** | 리소스 수에 따라 비용 증가 | CloudTrail은 로그 저장 기간에 따라 비용 증가 | 규모에 따라 적절한 서비스 선택 필요 |
| **비용** | 리소스 수 + 상태 저장 기간 | CloudTrail은 로그 저장 기간 | 작은 규모 환경에서는 Config의 프리티어 활용 권장 |
| **지연시간** | 주기적 체크로 지연 발생 | CloudTrail은 실시간 로그 제공 | 실시간 분석이 필요한 경우 CloudTrail 선택 |

#### 📝 시험 대비 체크리스트
- [ ] Config의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  **예시**: "AWS 리소스의 상태를 추적해 보안 준수 및 정책 적용을 자동화합니다."
- [ ] Config를 선택해야 하는 시나리오를 알고 있는가?  
  **예시**: "리소스 상태 변경을 모니터링하고, 정책 위반을 감지해야 할 경우"
- [ ] Config의 제한사항/한계를 알고 있는가?  
  **예시**: "모든 리소스 타입을 지원하지 않으며, 실시간 감지 기능이 없습니다."
- [ ] Config와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  **예시**: "CloudTrail은 API 로그를 제공하고, Config는 리소스 상태 추적에 특화되어 있습니다."
- [ ] Config의 비용 구조를 이해하고 있는가?  
  **예시**: "리소스 수와 상태 저장 기간에 따라 비용이 발생하며, 프리티어는 50개 리소스까지 무료입니다."

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 Config를 떠올리세요:  
> - **보안 준수**  
> - **리소스 상태 추적**  
> - **정책 검증**  
> - **변경 관리**  
> - **비용 효율성**  

> **💡 Tip:** Config는 보안 규정 준수 및 인프라 표준화에 필수적이므로, "AWS 규정 준수" 또는 "리소스 변경 감지" 관련 문제가 나오면 Config가 가장 적합한 서비스입니다.

---

| [⬅️ Detective](./Detective.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 4](../README.md) | [CloudTrail ➡️](./CloudTrail.md) |

---
