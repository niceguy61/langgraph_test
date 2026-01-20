---

| [⬅️ Inspector](./Inspector.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 4](../README.md) | [Detective ➡️](./Detective.md) |

---

# Security Hub 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** Security Hub는 AWS의 통합 보안 관리 및 위협 탐지 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 기존에는 AWS 서비스별로 분산된 보안 도구를 사용해 위협 탐지, 정책 준수, 위험 분석을 별도로 수행해야 했습니다. 예를 들어, S3 버킷 보안을 위해 CloudTrail, IAM 정책을 별도로 검토해야 했습니다.
- **문제 2:** 수동적인 보안 정책 검토로 인해 인력 비용이 높고, 규칙을 누락하거나 실수로 인한 보안 사고 위험이 있었습니다. 예를 들어, EC2 인스턴스의 보안 그룹 설정을 매번 수동으로 점검해야 했습니다.
- **문제 3:** 다양한 보안 도구에서 발생한 알림을 별도의 대시보드에서 합쳐보기 위해 시간이 많이 소요되었고, 중복된 알림으로 인해 중요 사항을 놓치는 경우가 많았습니다.

**Security Hub로 해결:**
- **해결 1:** Security Hub는 AWS 보안 서비스(예: GuardDuty, Inspector, CloudTrail)를 통합해 단일 대시보드에서 위협 탐지, 정책 준수, 위험 분석을 실시간으로 제공합니다. 예를 들어, S3 버킷의 접근 로그를 CloudTrail과 Security Hub로 연결해 이상 트래픽을 즉시 감지할 수 있습니다.
- **해결 2:** Config Rules를 통해 자동화된 보안 정책 검토를 수행해 인력 오류를 줄이고, 실시간으로 보안 위반을 감지합니다. 예를 들어, EC2 인스턴스의 보안 그룹이 공개 IP를 허용하는 경우 자동으로 경고를 전달합니다.
- **해결 3:** Security Hub는 여러 서비스에서 발생한 알림을 중앙 집중식으로 수집해 분류하고, 위험 수준에 따라 우선순위를 매겨 알림을 최소화합니다. 예를 들어, GuardDuty의 위협 탐지 결과와 Detective의 분석 결과를 결합해 보안 이슈를 효율적으로 관리합니다.

### 비유로 이해하기
**보안 감시원이 여러 카메라를 통해 전체 시설을 감시하는 것처럼**, Security Hub는 AWS 내부의 다양한 보안 도구(예: GuardDuty, Inspector, CloudTrail)를 통합해 클라우드 환경의 모든 활동을 실시간으로 감시하고, 위협을 즉시 감지해 대응하는 서비스입니다. 이처럼 복잡한 보안 체계를 단일 플랫폼에서 관리해 보안 리스크를 줄이고, 운영 효율성을 높입니다.

## 📚 핵심 개념

### 개념 1: GuardDuty의 위협 탐지 및 머신러닝 기반 분석  
GuardDuty는 AWS 환경에서의 보안 위협을 자동으로 감지하는 서비스로, 네트워크, 계정, 클라우드 리소스의 이상 징후를 실시간으로 분석합니다. 머신러닝 기반의 분석을 통해 알려지지 않은 위협(예: 악성 IP, 악성 소프트웨어, 데이터 유출)을 탐지하며, 이를 통해 보안 사고를 사전에 방지할 수 있습니다.  
GuardDuty는 AWS 계정 및 리소스의 활동을 모니터링하여 위협을 탐지하고, 위협 타입별로 위험 수준을 평가합니다. 탐지된 위협은 알림으로 제공되며, 보안 팀이 대응 전략을 수립할 수 있도록 지원합니다.  

#### 왜 중요한가?  
- **위협을 사전에 탐지**: 공격이 발생하기 전에 이상 징후를 감지하여 피해를 최소화할 수 있습니다.  
- **자동화된 분석**: 머신러닝 기반 분석으로 수동 검토를 줄이고, 빠른 대응이 가능합니다.  

#### 세부 요소  
| 요소 | 설명 | 예시 |  
|-----|-----|-----|  
| **위협 탐지 범위** | 네트워크 트래픽, 클라우드 리소스, AWS 서비스 활동을 감시합니다. | 예: S3 버킷에 대한 비정상적인 접근 시도 |  
| **머신러닝 분석** | 패턴을 학습하여 알려지지 않은 위협을 감지합니다. | 예: 악성 IP의 패턴을 학습하여 새로운 위협 탐지 |  
| **알림 및 대응** | 탐지된 위협을 이메일, AWS console, SNS 등으로 알리고 대응 전략을 제공합니다. | 예: 악성 IP 접근 시 이메일 알림 및 보안 정책 적용 권장 |  

> **💡 Tip:** GuardDuty는 AWS 계정 수준에서 작동하므로, 모든 리소스를 통합적으로 보호할 수 있습니다.  

---

### 개념 2: Security Hub의 통합 보안 데이터 수집 및 위험 분류  
Security Hub는 AWS 보안 서비스의 통합 플랫폼으로, GuardDuty, Inspector, Detective 등 다양한 보안 서비스의 데이터를 수집하고 분석하여 위험 수준을 분류합니다. 이 서비스는 모든 보안 관련 데이터를 하나의 대시보드에서 관리할 수 있어, 보안 팀이 효율적으로 위협을 대응할 수 있습니다.  
Security Hub는 위험을 "Finding"이라는 형식으로 정리하여, 위험 수준, 영향 범위, 해결 방안 등을 명확히 제공합니다. 이를 통해 보안 팀이 우선순위를 설정하고 대응 전략을 수립할 수 있습니다.  

#### 작동 원리  
1. **데이터 수집**: Security Hub는 다양한 AWS 보안 서비스(예: GuardDuty, Inspector, CloudTrail)에서 발생하는 보안 관련 데이터를 수집합니다.  
2. **위험 분류**: 수집된 데이터를 기반으로 위험 수준을 분류하고, 해당 위험을 "Finding"으로 기록합니다.  
3. **대시보드 및 알림**: 위험을 대시보드에서 시각화하고, 이메일, SNS, AWS console 등으로 알림을 제공합니다.  

> **💡 Tip:** Security Hub는 자동화된 보안 모니터링을 통해 수동 검토를 줄이고, 보안 팀의 작업 효율성을 높입니다.  

---

### 개념 3: Config Rules의 자동화된 보안 준수 검증 및 정책 적용  
Config Rules는 AWS 리소스의 구성이 보안 정책에 부합하는지 자동으로 검증하는 서비스입니다. 예를 들어, S3 버킷의 접근 제어 설정이 적절한지, IAM 정책이 보안 기준에 부합하는지 등을 확인하여, 보안 준수 위험을 사전에 방지합니다.  
Config Rules는 규칙을 정의하여 리소스를 실시간으로 모니터링하고, 위반 시 알림을 제공하며, 자동으로 정책을 수정할 수 있도록 지원합니다. 이는 보안 위험을 줄이고, 지속적인 준수를 유지할 수 있습니다.  

#### 주요 특징  
1. **자동화된 준수 검증**: 리소스 구성이 정책에 부합하는지 자동으로 검증하여, 수동 점검을 줄입니다.  
2. **실시간 모니터링**: 리소스 변경 시 즉시 검증을 수행하여, 즉각적인 대응이 가능합니다.  
3. **정책 적용 및 수정**: 위반 시 알림을 제공하고, 정책을 자동으로 수정할 수 있도록 지원합니다.  

> **💡 Tip:** Config Rules는 보안 정책을 표준화하고, 리소스의 일관된 관리를 통해 보안 위험을 최소화할 수 있습니다.

## 🖥️ AWS 콘솔에서 Security Hub 사용하기

### Step 1: Security Hub 서비스 접속  
1. AWS Management Console에 로그인합니다.  
   - URL: https://console.aws.amazon.com  
   - 로그인 후 `Security Hub` 서비스에 접근할 수 있는 권한이 있는지 확인합니다.  
2. 상단 검색창에서 "Security Hub"를 입력하고, 검색 결과에서 "Security Hub"를 클릭합니다.  
   - 이때 `Security Hub` 대시보드가 표시되면 정상적으로 접속되었습니다.  

> **📸 화면 확인:**  
> - 상단 메뉴바에 `Security Hub` 아이콘 또는 브랜드 로고가 표시되는지 확인합니다.  
> - 좌측 메뉴에서 `Standards`, `Findings`, `Settings` 등의 탭이 보이는지 확인합니다.  

---

### Step 2: [주요 작업 1 - GuardDuty 기본 구성]  
1. **GuardDuty 활성화**  
   - 좌측 메뉴에서 `Standards` → `GuardDuty`를 클릭합니다.  
   - `GuardDuty` 탭에서 **"Enable GuardDuty"** 버튼을 선택합니다.  
   - **Region 선택:** 기본적으로 `US East (N. Virginia)`이 선택되어 있습니다.  
   - **Email 알림 설정:** `Notifications` 섹션에서 이메일 주소를 입력해 이상 징후를 실시간으로 알림받습니다.  

2. **CloudTrail 통합 설정**  
   - `GuardDuty` 설정 완료 후, `Settings` → `Integrations` → `CloudTrail`을 클릭합니다.  
   - `CloudTrail`을 활성화하고, `AWS CloudTrail` 서비스를 연결해 로그를 실시간으로 모니터링합니다.  
   - **주의:** CloudTrail 통합은 AWS 계정 내 모든 리소스 활동을 기록하므로, 보안 및 비용 관리에 주의해야 합니다.  

3. **비용 및 리소스 확인**  
   - `GuardDuty` 활성화 후, `Costs` 탭에서 **"GuardDuty"** 항목을 선택해 비용을 확인합니다.  
   - **프리티어 활용:** 12개월 동안 월 $100까지 무료 사용 가능 (AWS Free Tier).  

> **📸 화면 확인:**  
> - `GuardDuty` 설정 완료 후, `Findings` 탭에서 초기 감지 결과가 표시되는지 확인합니다.  
> - `CloudTrail` 통합 설정 시, `Integrations` 섹션에서 상태가 `Enabled`인지 확인합니다.  

---

### Step 3: [주요 작업 2 - Security Hub 설정 및 통합]  
1. **Security Hub 규칙 구성**  
   - 좌측 메뉴에서 `Standards` → `Security Hub`를 클릭합니다.  
   - `Standards` 섹션에서 `AWS Foundational Security Best Practices`를 선택해 기본 보안 정책을 활성화합니다.  
   - **Custom Rule 추가:** `Rules` → `Create rule`을 클릭해 사용자 정의 규칙을 설정합니다.  
     - 예: "EC2 인스턴스에 보안 그룹이 부여되지 않은 경우 경고"  

2. **Config Rules 연동**  
   - `Security Hub` 메뉴에서 `Integrations` → `Config Rules`를 선택합니다.  
   - `Config Rules`를 활성화해 AWS Config의 정책을 Security Hub에 실시간으로 반영합니다.  
   - **예시:** "EC2 인스턴스의 보안 그룹이 비공개 상태인지 확인"  

3. **Trusted Advisor 통합 설정**  
   - `Integrations` → `Trusted Advisor`를 클릭해 통합을 활성화합니다.  
   - Trusted Advisor의 보안, 성능, 비용 최적화 등의 권장 사항을 Security Hub에서 실시간으로 확인할 수 있습니다.  

> **⚠️ 주의:**  
> - Security Hub에서 설정한 규칙은 AWS 계정 전체에 적용되므로, **권한 관리 (IAM)**을 철저히 해야 합니다.  
> - Config Rules와 CloudTrail 통합 시, **데이터 전송 비용**이 발생할 수 있으므로, 사용량을 모니터링해야 합니다.  

---

### Step 4: 설정 확인 및 테스트  
1. **리소스 상태 확인**  
   - `Findings` 탭에서 `GuardDuty`의 감지 결과, `Security Hub`의 정책 위반 사례, `Trusted Advisor`의 권장 사항을 확인합니다.  
   - **필터링:** `Severity` 또는 `Resource Type`을 선택해 특정 리소스만 검색할 수 있습니다.  

2. **정상 동작 테스트**  
   - **테스트용 리소스 생성:**  
     - AWS CLI로 EC2 인스턴스를 생성해 보안 그룹을 비공개 상태로 설정합니다.  
     - 예:  
       ```bash
       aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 --count 1 --instance-type t2.micro --security-groups ""
       ```  
   - **감지 결과 확인:**  
     - `Findings` 탭에서 생성한 EC2 인스턴스에 대한 보안 위험 신호가 표시되는지 확인합니다.  

3. **알림 및 대응 테스트**  
   - `GuardDuty`의 이메일 알림을 설정해, 감지 결과를 실제 이메일로 수신하는지 확인합니다.  
   - **예시:**  
     ```bash
     aws guardduty update-findings --findings "[{\"id\":\"<finding-id>\",\"severity\":\"LOW\"}]"
     ```  
   - 테스트 후, `Findings`에서 상태가 `Resolved`로 변경되는지 확인합니다.  

> **💡 Tip:**  
> - AWS 콘솔에서의 설정은 CLI로도 동일하게 수행 가능합니다.  
> - 예: `aws securityhub update-security-hub-configuration` 명령어로 설정을 자동화할 수 있습니다.  
> - **비용 최적화:** `GuardDuty`와 `CloudTrail`은 별도의 비용이 발생하므로, 사용량을 정기적으로 점검해야 합니다.

## ⌨️ AWS CLI로 Security Hub 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

> **💡 Tip:** CLI 명령어 실행 전, AWS CLI가 최신 버전인지 확인하세요. `aws --version`으로 버전을 확인하고, 필요 시 `aws upgrade` 명령어로 업데이트하세요.

---

### 예제 1: Security Hub 리소스 조회
```bash
# Security Hub에서 Finding 목록 조회
aws securityhub list-findings --query 'Findings[*].Id' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| `--query` | 결과 필터링 | `'Findings[*].Id'` (Finding ID 목록 출력) |
| `--output` | 출력 형식 | `json`, `table`, `text` (표 형식으로 보기 편하게 `table` 사용) |

**예상 출력:**
```
ID
--------------------------------
arn:aws:securityhub:us-east-1:123456789012:finding/abc123
arn:aws:securityhub:us-east-1:123456789012:finding/def456
```

> **⚠️ 주의:** `list-findings`는 Security Hub에 등록된 모든 Finding을 반환하므로, 필터링 없이 실행 시 대량의 데이터가 출력될 수 있습니다.

---

### 예제 2: GuardDuty 필터 생성
```bash
# GuardDuty에서 특정 조건에 맞는 Finding 필터 생성
aws guardduty create-filter \
    --name "Critical-Resource-Access" \
    --description "Access to critical resources detected" \
    --rank 100 \
    --action "ARCHIVE" \
    --criteria "{\"resourceType.EQ\": \"AWS::EC2::Instance\"}" 
```

**필수 옵션:**
- `--name`: 필터 이름 (예: "Critical-Resource-Access")
- `--rank`: 중요도 (0~100, 낮을수록 우선순위 높음)
- `--action`: 필터 실행 시 동작 (`ARCHIVE`, `NOOP`, `STOP`)  
- `--criteria`: JSON 형식의 조건 필터 (예: `resourceType.EQ`로 EC2 인스턴스만 필터링)

**예상 출력:**
```json
{
    "FilterId": "f-1234567890abcdef",
    "Status": "ACTIVE"
}
```

> **💡 Tip:** `--criteria`는 JSON 형식으로 작성해야 하며, `resourceType`, `findingType` 등 다양한 필터 조건이 지원됩니다.

---

### 예제 3: GuardDuty 필터 수정
```bash
# GuardDuty 필터 수정
aws guardduty update-filter \
    --filter-id "f-1234567890abcdef" \
    --name "Updated-Critical-Resource-Access" \
    --rank 80 \
    --action "STOP"
```

**필수 옵션:**
- `--filter-id`: 수정할 필터의 ID
- `--name`: 새 이름
- `--rank`: 수정된 중요도
- `--action`: 변경된 동작

**예상 출력:**
```json
{
    "FilterId": "f-1234567890abcdef",
    "Status": "ACTIVE"
}
```

---

### 예제 4: GuardDuty 필터 삭제
```bash
# GuardDuty 필터 삭제
aws guardduty delete-filter --filter-id "f-1234567890abcdef"

# 삭제 확인 (존재 여부 확인)
aws guardduty get-filter --filter-id "f-1234567890abcdef"
```

> **⚠️ 주의:** 삭제 후 `get-filter` 명령어는 오류를 반환하므로, 삭제 전 반드시 확인하세요.

---

### 자주 사용하는 명령어 정리
```bash
# Security Hub Finding 조회
aws securityhub list-findings --query 'Findings[*].Id' --output table

# GuardDuty 필터 생성
aws guardduty create-filter --name "Filter-Name" --rank 100 --action "ARCHIVE" --criteria "{\"resourceType.EQ\": \"AWS::EC2::Instance\"}"

# GuardDuty 필터 수정
aws guardduty update-filter --filter-id "f-1234567890abcdef" --rank 80 --action "STOP"

# GuardDuty 필터 삭제
aws guardduty delete-filter --filter-id "f-1234567890abcdef"
```

---

### 🔍 CLI 사용 시 주의사항
1. **리전 설정**: 모든 명령어는 실행 시점의 리전에 적용됩니다. `aws configure set region us-east-1`로 리전을 변경하세요.
2. **비용 관리**: `GuardDuty`는 리전별로 요금이 부과되므로, 사용량을 체크리스트로 관리하세요.
3. **프리티어 활용**: Security Hub 및 GuardDuty는 프리티어로 1년간 50개 리소스까지 무료입니다. 대규모 시스템에서는 리소스 수를 점검하세요.
4. **리소스 ID**: `list-findings`의 출력 결과에서 `Id`를 복사해 `delete-filter` 등에 사용하세요.

> **💡 Tip:** CLI 명령어를 실행하기 전, `aws help`로 명령어 목록을 확인하거나, `aws [service] help`로 특정 서비스의 명령어를 확인하세요.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 Security Hub 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **Security Hub의 통합 보안 데이터 수집 및 위험 분류**  
   - 설명: Security Hub는 AWS 보안 서비스(예: GuardDuty, Inspector, CloudTrail)의 결과를 통합하여 위험을 분류하고, 위험 등급을 기반으로 우선순위를 설정합니다. 이는 보안 팀이 자원을 효율적으로 할당할 수 있도록 도와 시험에서 자주 출제됩니다.  
   - 키워드: `통합 분석`, `위험 등급`, `결과 통합`

2. **GuardDuty와의 연동 및 위협 탐지**  
   - 설명: Security Hub는 GuardDuty의 위협 탐지 결과를 자동으로 수집하여 시각화하고, 분석을 간소화합니다. 이는 보안 사고 대응 전략 수립에 핵심적인 역할을 하며, 시험에서 주요 개념으로 다룹니다.  
   - 키워드: `GuardDuty 연동`, `위협 탐지`, `자동 수집`

3. **Config Rules 기반 자동 준수 검증**  
   - 설명: Security Hub는 AWS Config Rules를 통해 자동화된 보안 정책 검증을 수행합니다. 이는 클라우드 환경에서 보안 준수 상태를 실시간으로 모니터링하는 데 필수적이며, 시험에서 자주 다루는 주제입니다.  
   - 키워드: `Config Rules`, `자동 검증`, `준수 상태`

4. **비용 효율성과 프리티어 활용**  
   - 설명: Security Hub는 기존 보안 서비스와의 통합을 통해 비용 절감을 가능하게 합니다. 시험에서 자주 출제되는 주제로, 프리티어 사용 방법과 비용 구조를 이해하는 것이 중요합니다.  
   - 키워드: `비용 절감`, `프리티어`, `비용 구조`

5. **Security Hub의 제한 사항 및 한계**  
   - 설명: Security Hub는 자체 보안 분석 기능이 없고, 외부 서비스에 의존합니다. 이 한계를 인지하는 것은 시험에서 주의해야 할 포인트로, 시험 문제에서 혼동을 방지하기 위해 반드시 숙지해야 합니다.  
   - 키워드: `외부 의존`, `분석 기능 없음`, `한계 사항`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | "Security Hub는 자체 보안 분석을 수행한다"는 문장이 출제될 수 있음 | **정답: 오답** (Security Hub는 외부 서비스에 의존함) |
| 함정 2 | "Security Hub는 CloudTrail과의 통합이 필수적이지 않다"는 문장이 출제될 수 있음 | **정답: 오답** (CloudTrail 통합은 보안 감사에 필수적) |
| 함정 3 | "Security Hub는 모든 보안 위협을 실시간으로 탐지한다"는 문장이 출제될 수 있음 | **정답: 오답** (실시간 탐지는 GuardDuty 등의 서비스에 의존함) |

#### 🔄 Security Hub vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | Security Hub | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | 보안 위험 통합 분석 및 관리 | Detective: 자동화된 보안 분석 | 복잡한 위험 분류가 필요할 때 |
| 확장성 | 여러 서비스와의 통합이 용이 | Detective: 고급 분석 기능 포함 | 다양한 데이터 소스 통합이 필요할 때 |
| 비용 | 기존 서비스와의 통합으로 비용 절감 | Detective: 고급 기능으로 비용 증가 | 예산 제약이 있을 때 |
| 지연시간 | 실시간 분석이 가능함 | Detective: 분석 기능이 별도로 작동 | 즉시 분석이 필요할 때 |

#### 📝 시험 대비 체크리스트
- [ ] Security Hub의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  (예: "보안 위험을 통합하여 분석하고 우선순위를 설정하는 중앙 집중식 플랫폼")  
- [ ] Security Hub를 선택해야 하는 시나리오를 알고 있는가?  
  (예: "다양한 보안 서비스 결과를 통합 분석해야 할 때")  
- [ ] Security Hub의 제한사항/한계를 알고 있는가?  
  (예: "자체 분석 기능 없음, 외부 서비스에 의존")  
- [ ] Security Hub와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  (예: "Detective는 자동화 분석에 특화, Security Hub는 통합 분석에 특화")  
- [ ] Security Hub의 비용 구조를 이해하고 있는가?  
  (예: "기존 서비스 통합으로 비용 절감, 프리티어 사용 가능")

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 Security Hub를 떠올리세요:  
> - **통합 분석**  
> - **위험 등급**  
> - **Config Rules**  
> - **비용 절감**  
> - **외부 서비스 의존**

---

| [⬅️ Inspector](./Inspector.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 4](../README.md) | [Detective ➡️](./Detective.md) |

---
