---

| [⬅️ 이전 Day](../day2/README.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 4](../README.md) | [Inspector ➡️](./Inspector.md) |

---

# GuardDuty 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** GuardDuty는 클라우드 환경에서의 위협 탐지를 위한 AWS의 **실시간 보안 분석 서비스**입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 수동적인 보안 모니터링으로 인한 실시간 위협 탐지 어려움  
  기존에는 로그를 수동으로 분석하거나, 비정형 데이터를 처리하는 데 시간이 많이 소요되었으며, 사전에 위협을 인지하는 데 한계가 있었습니다.  
- **문제 2:** 가짜 경보(FA)로 인한 인력 낭비와 정확한 위협 식별 어려움  
  기존 시스템은 많은 양의 경보를 생성했으나, 그 중 실제 위협은 적어 정확한 분석이 어렵고, 인력 자원이 낭비되었습니다.  
- **문제 3:** 다중 AWS 서비스 간 보안 데이터 통합 및 관리 어려움  
  기존에는 각 서비스 별로 로그를 관리해야 했으며, 통합 분석을 위해 별도의 도구나 인프라가 필요했습니다.  

**GuardDuty로 해결:**
- **해결 1:** 머신러닝 기반의 실시간 위협 탐지  
  GuardDuty는 AWS 서비스의 네트워크 트래픽, 클라우드 리소스 접근 패턴, 로그 등을 분석해 **자동화된 위협 탐지**를 제공합니다.  
- **해결 2:** 정교한 분석으로 가짜 경보 감소  
  머신러닝과 규칙 기반 분석을 결합해 **정확도를 높여 가짜 경보를 줄이고**, 실제 위협에 집중할 수 있습니다.  
- **해결 3:** 통합 보안 데이터 관리 및 분석  
  AWS 내 모든 리소스의 보안 데이터를 한 곳에서 수집해 **위험 수준을 분류하고, 시각화된 보고서를 제공**합니다.  

### 비유로 이해하기
**보안 감시원을 생각해보세요.**  
GuardDuty는 24시간 동안 AWS 환경을 감시하는 감시원으로, 이상 트래픽을 탐지하고 즉시 경보를 발령합니다. 또한, 감시원은 단순히 경보를 내기보다는 **패턴을 분석해 위협의 유형과 심각도를 판단**해 줍니다. 이처럼 GuardDuty는 수동 감시의 한계를 극복하고, 보안 인력의 업무 효율성을 높입니다.  

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | **사용자 권한 침해 탐지** | AWS EC2 인스턴스에 비인가된 SSH 접근이 발생한 경우, GuardDuty는 해당 트래픽을 탐지하고 경보를 내립니다. |
| 시나리오 2 | **마alusware 감지 및 대응** | EC2 인스턴스에 악성 코드가 실행된 경우, GuardDuty는 이상한 프로세스를 감지하고 사전에 대응할 수 있습니다. |
| 시나리오 3 | **구성 변경 위험 감지** | S3 버킷의 접근 정책이 변경된 경우, GuardDuty는 이 변경이 위험한지 분석해 경보를 내립니다. |

**이럴 때 GuardDuty를 선택하세요:**
- ✅ **실시간 위협 탐지가 필요한 상황**  
- ✅ **다양한 AWS 서비스 간 보안 데이터 통합이 필요한 상황**  
- ✅ **가짜 경보를 최소화하고 정확한 분석이 필요한 상황**  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ **정기적인 보안 검사 및 정책 준수 여부 확인이 필요** → **Config Rules** (예: IAM 정책 검증)  
- ❌ **심층 분석 및 위협 탐지가 필요** → **Detective** (예: 네트워크 흐름 분석)  
- ❌ **보안 이벤트의 위험 수준을 분류하고 시각화** → **Security Hub** (예: 위험 점수 기반 대시보드)  

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **Security Hub** | **통합 보안 데이터 분석 및 위험 분류** | GuardDuty → Security Hub → 대시보드 및 알림 |
| **CloudTrail** | **AWS API 호출 로그 수집 및 감사** | CloudTrail → GuardDuty → 이상 트래픽 분석 |
| **Trusted Advisor** | **보안 및 성능 최적화 권장 사항 제공** | GuardDuty → Trusted Advisor → 리소스 최적화 권장 |

**자주 사용되는 아키텍처 패턴:**
```
User → CloudFront → S3 (CloudTrail 로그)  
          ↑  
          ↓  
GuardDuty → Security Hub (통합 분석)  
          ↑  
          ↓  
Trusted Advisor (권장 사항 제공)  
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **GuardDuty 기본 사용** | $0.10/월 (100,000개 이상의 리소스 감시) | 월 12개월 무료 |
| **추가 리소스 감시** | $0.01/리소스 | 12개월 무료 |
| **경보 알림 서비스** | $0.05/월 | 항상 무료 |

**비용 최적화 팁:**
1. 💡 **프리티어 기간 동안 사용량을 최대한 활용**하세요. 12개월 무료 기간 동안 보안 모니터링을 강화해 비용을 절감할 수 있습니다.  
2. 💡 **필요한 리소스만 감시 대상으로 설정**해 과다한 데이터 수집을 방지하세요. 예: 특정 S3 버킷만 대상으로 설정.  
3. 💡 **경보 알림을 최소화**하고, 자동화된 대응 시스템을 구축해 인력 비용을 절감하세요.  

> **⚠️ 비용 주의:** **GuardDuty는 AWS 리소스 사용량에 따라 요금이 변동**되므로, 프리티어 기간 이후에는 정기적으로 사용량을 모니터링하고, 필요 없는 리소스 감시를 제거하는 것이 중요합니다.

## 📚 핵심 개념

### 개념 1: GuardDuty의 위협 탐지 및 머신러닝 기반 분석
GuardDuty는 AWS 환경에서 **위협 탐지**를 위한 서비스로, 머신러닝 기반의 분석을 통해 **위험 요소를 자동으로 식별**합니다. 이 서비스는 네트워크 활동, 시스템 로그, AWS 리소스의 이상 징후를 감시하여 **사전에 보안 위협을 예방**하는 데 기여합니다. 특히, 보안 팀이 수동으로 감시하기 어려운 미세한 위협(예: 악성 코드, 비정상적인 접근)을 효과적으로 포착할 수 있도록 설계되었습니다.

#### 왜 중요한가?
- **위협 탐지의 자동화**: 수동 감시의 한계를 극복하여 실시간으로 위협을 감지합니다.  
- **머신러닝 기반 분석**: 대규모 데이터를 기반으로 패턴을 학습하여 정확도를 높입니다.  

#### 세부 요소
| 요소 | 설명 | 예시 |
|-----|------|---|
| **위협 탐지** | AWS 리소스의 이상 활동을 감지합니다. | 악성 코드 실행, 비정상적인 네트워크 트래픽 |
| **머신러닝 분석** | 기존 데이터 패턴을 학습해 새로운 위협을 예측합니다. | 유사한 악성 활동의 패턴을 기반으로 예측 |
| **통합 분석** | Security Hub와 연동해 보안 위험을 종합적으로 분석합니다. | 여러 서비스에서 수집된 데이터를 종합 판단 |

> **💡 Tip:** 실무에서는 GuardDuty의 알림을 Security Hub에 연결해 통합 보안 분석을 수행하는 것이 권장됩니다. 예를 들어, GuardDuty에서 탐지된 악성 활동은 Security Hub에서 위험 수준을 분류하여 대응 전략을 수립할 수 있습니다.

---

### 개념 2: Security Hub의 통합 보안 데이터 수집 및 위험 분류
Security Hub는 AWS 내 다양한 보안 서비스(예: GuardDuty, Inspector, CloudTrail)에서 수집된 **보안 데이터를 통합**하고, **위험 수준을 분류**해 보안 팀이 효율적으로 대응할 수 있도록 돕는 서비스입니다. 이는 복잡한 AWS 환경에서 **단일 포인트에서 모든 보안 정보를 확인**할 수 있도록 해줍니다.

#### 작동 원리
1. **데이터 수집**: 다양한 AWS 서비스에서 생성된 보안 관련 데이터를 수집합니다 (예: GuardDuty의 위협 정보, CloudTrail의 API 로그).  
2. **위험 분류**: 수집된 데이터를 기반으로 위험 수준을 자동으로 분류합니다 (예: 고위험, 중위험, 저위험).  
3. **통합 보고**: 보안 팀이 한 화면에서 모든 위험 정보를 확인하고 대응 조치를 수행할 수 있도록 제공합니다.

> **💡 Tip:** Security Hub는 보안 정책을 설정해 위험 수준에 따라 자동 알림을 보내거나, AWS Lambda를 통해 자동 대응 프로세스를 실행할 수 있습니다. 예를 들어, 고위험 이벤트 발생 시 Lambda 함수를 트리거해 보안 로그를 자동으로 분석할 수 있습니다.

---

### 개념 3: Config Rules의 자동화된 보안 준수 검증 및 정책 적용
Config Rules는 AWS 리소스가 **보안 정책과 일치하는지 자동으로 검증**하는 서비스입니다. 이는 리소스 구성이 잘못되었을 경우를 사전에 방지해 **보안 준수**를 유지하는 데 중요한 역할을 합니다. 특히, **정책을 설정하고 자동으로 리소스를 조정**할 수 있어 운영 효율성을 높입니다.

#### 주요 특징
1. **자동 검증**: 리소스 구성이 설정된 정책에 부합하는지 실시간으로 점검합니다.  
   - 예: EC2 인스턴스에 암호화된 암호화폐 키 저장이 금지된 경우, 해당 리소스가 자동으로 탐지됩니다.  
2. **정책 적용**: 설정된 정책에 따라 리소스를 자동으로 수정하거나 경고를 발생시킵니다.  
   - 예: S3 버킷이 공개 접근 권한을 허용하고 있을 경우, 정책에 따라 접근 권한을 제한하도록 수정합니다.  
3. **통합 기능**: Security Hub와 CloudTrail과 연동해 보안 위험을 종합적으로 분석합니다.  
   - 예: Config Rules에서 탐지된 위험은 Security Hub에서 위험 수준을 분류해 대응 전략을 수립합니다.  

> **💡 Tip:** Config Rules는 보안 정책을 설정하고 자동화된 조치를 수행해 운영 부담을 줄일 수 있습니다. 예를 들어, IAM 정책에 따라 모든 사용자에게 특정 권한을 제한할 수 있도록 정책을 설정하고, 리소스가 변경될 때 자동으로 검증합니다.

## 🖥️ AWS 콘솔에서 GuardDuty 사용하기

### Step 1: GuardDuty 서비스 접속  
1. AWS Management Console에 로그인합니다.  
   - URL: https://console.aws.amazon.com  
   - 로그인 후 **Services** 메뉴에서 **Security Hub**를 클릭합니다.  
2. 상단 검색창에 "GuardDuty"를 입력하고, 결과창에서 **GuardDuty**를 클릭합니다.  
   - 이때 **Security Hub**와 **GuardDuty**는 서로 다른 서비스이지만, 보안 분석을 통합할 수 있습니다.  

> **📸 화면 확인:**  
> - **GuardDuty** 대시보드가 표시되면 **"GuardDuty"** 서비스가 정상적으로 접근되었습니다.  
> - 대시보드 상단에 **"Findings"**, **"Rules"**, **"Data Sources"** 등의 탭이 보여야 합니다.  

---

### Step 2: [주요 작업 1 - 리소스 생성]  
1. **GuardDuty 서비스 활성화**  
   - 왼쪽 메뉴에서 **"GuardDuty"**를 클릭한 후, **"Create detector"** 버튼을 선택합니다.  
   - **Detector**는 GuardDuty의 핵심 리소스로, 보안 분석을 위한 데이터 수집 및 분석을 담당합니다.  
   - **Account** 필드: 현재 계정을 선택합니다.  
   - **Regions**: 분석 대상 지역을 선택합니다 (예: us-east-1, ap-northeast-1).  

2. **데이터 소스 설정**  
   - **Data sources** 탭에서 **"CloudTrail"**, **"S3"**, **"EBS"** 등의 데이터 소스를 활성화합니다.  
   - **CloudTrail**은 로그 데이터를 수집하고, **S3**는 저장소 보안을 모니터링합니다.  
   - **EBS**는 볼륨 복제 및 악성 코드 검출을 지원합니다.  

3. **설정 확인**  
   - **"Create detector"** 버튼을 클릭 후, 생성된 **Detector**가 **"Active"** 상태인지 확인합니다.  
   - **Status**가 **"Enabled"**이어야 하며, **"Findings"** 탭에서 초기 분석 결과가 표시됩니다.  

> **📸 화면 확인:**  
> - **"Data Sources"** 탭에서 **"CloudTrail"**과 **"S3"**가 **"Enabled"** 상태여야 합니다.  
> - **"Findings"** 탭에서 0개 이상의 **Finding**이 표시되면 정상적으로 데이터 수집이 시작되었습니다.  

---

### Step 3: [주요 작업 2 - 설정/구성]  
1. **규칙(Rules) 설정**  
   - **"Rules"** 탭에서 **"Create rule"** 버튼을 선택합니다.  
   - **Rule type**: **"Finding"** 또는 **"Custom"**을 선택합니다.  
     - **Finding**은 AWS가 제공하는 기본 규칙 (예: 악성 코드 감지)  
     - **Custom**은 사용자 정의 규칙 (예: 특정 S3 버킷 접근 시 경고)  
   - **Description**: 규칙 이름 및 설명을 입력합니다.  

2. **알림 설정**  
   - **"Actions"** 탭에서 **"Create action"**을 클릭합니다.  
   - **Action type**: **"Email"**, **"Lambda"**, **"SNS"** 등의 알림 방식을 선택합니다.  
   - **Email**은 보안 경고를 이메일로 전송하고, **Lambda**는 자동 처리 로직을 실행합니다.  

3. **연동 설정**  
   - **"Integrations"** 탭에서 **Security Hub** 또는 **Detective**와의 연동을 설정합니다.  
   - **Security Hub**는 여러 보안 서비스를 통합 분석하고, **Detective**는 실시간 보안 분석을 제공합니다.  

> **⚠️ 주의:**  
> - **CloudTrail**과 **S3**는 **GuardDuty 활성화 전에 설정**해야 합니다.  
> - **Cost**는 데이터 소스 수와 분석 주기로 인해 발생하므로, 프리티어(30일간 무료)를 활용하세요.  

---

### Step 4: 설정 확인 및 테스트  
1. **생성된 리소스 확인 방법**  
   - **"Detectors"** 탭에서 **Detector** 이름을 클릭하면, **"Findings"**, **"Rules"**, **"Data Sources"**를 확인할 수 있습니다.  
   - **"Findings"** 탭에서 **Finding ID**, **Severity**, **Description**을 확인합니다.  

2. **상태 확인 방법**  
   - **"Status"** 탭에서 **"Enabled"** 상태가 표시되면 정상입니다.  
   - **"Last updated"** 필드는 최근 설정 변경 시간을 보여줍니다.  

3. **정상 동작 테스트**  
   - **S3 버킷에 파일 업로드** 또는 **CloudTrail 로그에 의심스러운 활동**을 시뮬레이션합니다.  
   - **"Findings"** 탭에서 **Finding**이 생성되었는지 확인합니다.  
   - **"Actions"** 탭에서 알림이 전송되었는지 확인합니다.  

> **💡 Tip:**  
> - **GuardDuty**는 실시간 보안 분석을 위해 **CloudTrail**, **S3**, **EBS** 등과의 연동이 필수적입니다.  
> - **Security Hub**와의 통합은 **Finding**을 다른 보안 서비스와 비교 분석할 수 있습니다.  

--- 

### ✅ 학습 체크리스트  
- [ ] AWS Management Console에 로그인하여 GuardDuty 서비스 접속  
- [ ] Detector 생성 및 데이터 소스 활성화  
- [ ] 사용자 정의 규칙 및 알림 설정  
- [ ] Security Hub/Detective 연동 설정  
- [ ] Findings 생성 및 알림 테스트  
- [ ] 비용 및 프리티어 사용 여부 확인

## ⌨️ AWS CLI로 GuardDuty 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

> **💡 Tip:** GuardDuty CLI 명령어는 리전에 따라 동작이 다를 수 있으므로, `aws configure get region` 명령어로 현재 리전을 확인해 주세요.  
> **⚠️ 주의:** CLI 명령어 실행 전, IAM 역할이 `AmazonGuardDutyFullAccess` 권한을 포함하고 있는지 확인하세요. 권한이 부족할 경우 `AccessDenied` 오류가 발생합니다.

---

### 예제 1: GuardDuty 리소스 조회
```bash
# [GuardDuty Detector 목록 조회]
aws guardduty list-detectors --query '[].DetectorId' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| `--query` | 결과 필터링 (예: `'[].DetectorId'`로 Detector ID만 추출) | `'[]'` |
| `--output` | 출력 형식 (table, json, text 등) | `table` |

**예상 출력:**
```
| DetectorId |
|-------------|
| 123456789012 |
| 987654321098 |
```

> **💡 Tip:** `list-findings` 명령어로 특정 Detector의 위협 분석 결과를 조회할 수 있습니다.  
> `aws guardduty list-findings --detector-id <DetectorId>` 형식으로 사용합니다.

---

### 예제 2: GuardDuty 리소스 생성
```bash
# [GuardDuty Detector 생성]
aws guardduty create-detector \
    --name "Example-Detector" \
    --enable
```

**필수 옵션:**
- `--name`: Detector 이름 (예: "Example-Detector")
- `--enable`: 자동 감시 기능 활성화 (선택 사항, 기본값: `false`)

**예상 출력:**
```json
{
    "DetectorId": "123456789012",
    "Arn": "arn:aws:guardduty:region:account-id:detector/123456789012",
    "CreatedAt": "2023-10-01T12:00:00Z"
}
```

> **💡 Tip:** `--tags` 옵션으로 리소스 태그를 추가할 수 있습니다. 예: `--tags Key1=Value1,Key2=Value2`.

---

### 예제 3: GuardDuty 리소스 수정
```bash
# [GuardDuty Detector 설정 수정]
aws guardduty update-detector \
    --detector-id "123456789012" \
    --name "Updated-Detector"
```

**수정 가능한 옵션:**
- `--name`: Detector 이름 변경
- `--tags`: 태그 추가/수정 (기존 태그는 유지됨)

> **⚠️ 주의:** `update-detector`는 Detector ID를 필수 파라미터로 요구합니다. 잘못된 ID를 입력하면 `ResourceNotFoundException`이 발생합니다.

---

### 예제 4: GuardDuty 리소스 삭제
```bash
# [GuardDuty Detector 삭제]
aws guardduty delete-detector --detector-id "123456789012"

# 삭제 확인 (오류 발생 시 삭제 완료)
aws guardduty describe-detector --detector-id "123456789012"
```

**예상 출력 (삭제 후):**
```
An error occurred (ResourceNotFoundException) when calling the DescribeDetector operation: The resource 'detector/123456789012' was not found.
```

> **⚠️ 주의:** 삭제는 영구적입니다. 삭제 전 `list-detectors` 명령어로 확인 후 실행하세요.

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws guardduty list-detectors
aws guardduty describe-detector --detector-id "id"
aws guardduty list-findings --detector-id "id"

# 생성
aws guardduty create-detector --name "name" --enable

# 수정
aws guardduty update-detector --detector-id "id" --name "new-name"

# 삭제
aws guardduty delete-detector --detector-id "id"
```

> **💡 Tip:** `--region` 옵션을 명시적으로 추가하면 리전을 변경할 수 있습니다. 예: `--region us-east-1`.

---

### CLI 사용 시 주의사항
| 주의사항 | 설명 |
|---------|------|
| **비용 관리** | GuardDuty는 사용량 기반 요금이므로, `list-findings`로 이상 징후를 사전에 탐지해 비용 절감을 도와주세요. |
| **프리티어 제한** | 프리티어는 1개의 Detector만 생성 가능합니다. 추가 시 `LimitExceeded` 오류 발생. |
| **리전별 호환성** | CLI 명령어는 리전에 따라 동작이 다를 수 있습니다. `aws configure get region`으로 리전을 확인하세요. |
| **보안 권장 사항** | `--enable` 옵션을 사용해 자동 감시를 활성화하고, `Security Hub`와 연동해 분석 결과를 중앙 집중식으로 관리하세요. |

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 GuardDuty 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **포인트 1**: **머신러닝 기반의 위협 탐지**  
   - 설명: GuardDuty는 AWS에서 수집된 데이터를 기반으로 머신러닝 알고리즘을 활용해 위협을 실시간으로 탐지합니다. 이 기능은 시험에서 빈도가 높으며, 특히 **threat detection**, **machine learning**, **real-time monitoring** 키워드와 관련된 문제에서 자주 출제됩니다.  
   - 키워드: `threat detection`, `machine learning`, `real-time monitoring`

2. **포인트 2**: **Security Hub와의 통합**  
   - 설명: GuardDuty는 Security Hub에 데이터를 실시간으로 전송해 통합된 보안 분석을 제공합니다. 이는 **security integration**, **centralized security data**와 같은 키워드로 묶이며, 시험에서 보안 데이터 통합의 중요성에 대한 이해를 평가합니다.  
   - 키워드: `security integration`, `centralized security data`, `Security Hub`

3. **포인트 3**: **자동화된 보안 정책 적용**  
   - 설명: GuardDuty는 AWS Config Rules와 연동해 위협 발생 시 자동으로 보안 정책을 수정합니다. 이는 **automated remediation**, **compliance automation**과 관련된 시험 주제로, 자동화된 보안 관리 시나리오를 평가합니다.  
   - 키워드: `automated remediation`, `compliance automation`, `Config Rules`

4. **포인트 4**: **비용 효율성 및 프리티어 활용**  
   - 설명: GuardDuty는 사용량 기반 요금제로, 프리티어는 1년간 250달러의 무료 사용 권한을 제공합니다. 이는 **cost-effective**, **free tier**, **budget management** 키워드와 연결되어, 클라우드 보안 예산 관리에 대한 이해를 시험에 반영합니다.  
   - 키워드: `cost-effective`, `free tier`, `budget management`

5. **포인트 5**: **위협 탐지의 한계와 제한**  
   - 설명: GuardDuty는 AWS 내부 리소스에 한해 탐지하며, 외부 네트워크나 온프레미스 시스템은 지원하지 않습니다. 이는 **scope limitations**, **on-premises integration**과 관련된 시험 포인트로, 보안 서비스의 범위 이해를 평가합니다.  
   - 키워드: `scope limitations`, `on-premises integration`, `boundary constraints`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | "GuardDuty는 실시간으로 네트워크 침입을 탐지할 수 없다"는 문장이 주어지면, Inspector를 선택하는 경우가 많음 | **정답: GuardDuty는 실시간으로 AWS 내부 리소스의 위협을 탐지** |
| 함정 2 | "GuardDuty는 CloudTrail 데이터를 분석해 위협을 탐지한다"는 문장이 주어지면, Detective를 선택하는 경우가 많음 | **정답: GuardDuty는 CloudTrail 데이터를 분석하지 않음, Detective가 분석** |
| 함정 3 | "GuardDuty는 보안 정책을 자동으로 수정할 수 없다"는 문장이 주어지면, Config Rules를 선택하는 경우가 많음 | **정답: GuardDuty는 Config Rules와 연동해 자동화된 정책 수정 가능** |

#### 🔄 GuardDuty vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | GuardDuty | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| **용도** | AWS 내부 리소스의 실시간 위협 탐지 | **Inspector**: 보안 검사 및 위험 분석<br>**Detective**: 장기적 위협 분석 | **실시간 위협 탐지 시 GuardDuty, 장기 분석 시 Detective** |
| **확장성** | 대규모 AWS 환경에서 높은 성능 유지 | **Inspector**: 클라우드 환경에서의 보안 검사<br>**Detective**: 장기 분석에 적합 | **확장성 요구 시 GuardDuty, 장기 분석 시 Detective** |
| **비용** | 사용량 기반 요금제, 프리티어 제공 | **Inspector**: 프리티어 없음<br>**Detective**: 고정 비용 또는 사용량 기반 | **비용 효율성 우선 시 GuardDuty, 장기 분석 시 Detective** |
| **지연시간** | 실시간 분석, 저지연 | **Inspector**: 실시간 검사<br>**Detective**: 장기 분석으로 지연 발생 | **실시간 분석 시 GuardDuty, 장기 분석 시 Detective** |

#### 📝 시험 대비 체크리스트
- [ ] GuardDuty의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  *예: "AWS 내부 리소스의 실시간 위협을 머신러닝 기반으로 탐지하고, Security Hub에 통합하여 보안 분석을 제공합니다."*
- [ ] GuardDuty를 선택해야 하는 시나리오를 알고 있는가?  
  *예: "AWS VPC에 이상적인 트래픽 패턴이 감지될 때, 실시간 보안 분석이 필요한 경우"*
- [ ] GuardDuty의 제한사항/한계를 알고 있는가?  
  *예: "외부 네트워크나 온프레미스 시스템은 지원하지 않으며, 보안 정책 수정은 Config Rules와 연동해야 합니다."*
- [ ] GuardDuty와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  *예: "GuardDuty는 실시간 분석, Inspector는 보안 검사, Detective는 장기 분석에 적합합니다."*
- [ ] GuardDuty의 비용 구조를 이해하고 있는가?  
  *예: "사용량 기반 요금제, 프리티어는 1년간 250달러의 무료 사용 권한 제공"*

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 GuardDuty를 떠올리세요:  
> - **threat detection**  
> - **machine learning**  
> - **real-time monitoring**  
> - **Security Hub integration**  
> - **automated remediation**  
> - **cost-effective**  
> - **free tier**  
> - **on-premises integration**

---

| [⬅️ 이전 Day](../day2/README.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 4](../README.md) | [Inspector ➡️](./Inspector.md) |

---
