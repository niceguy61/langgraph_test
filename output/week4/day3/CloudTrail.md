---

| [⬅️ Config](./Config.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 4](../README.md) | [다음 Day ➡️](../day4/README.md) |

---

# CloudTrail 완전 정복

> **한 줄 정의:** CloudTrail는 AWS에서 모든 AWS 리소스에 대한 활동을 추적하고 기록하여 보안 및 규정 준수를 강화하는 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 수동적인 로그 관리로 인한 실시간 모니터링 불가능  
  기존에는 개발자가 직접 서버 로그를 수집하고 분석해야 했으며, 실시간으로 이상 행동을 탐지하는 데 한계가 있었습니다.  
- **문제 2:** 정책 위반 시 재작업이 복잡하고 시간 소요  
  보안 정책 위반 시 수동으로 로그를 검토해 원인을 파악해야 했고, 이로 인해 디버깅 시간이 길어졌습니다.  
- **문제 3:** 규정 준수 검증이 수동적이고 비효율적  
  GDPR, HIPAA 등 규제 준수를 위해 수작업으로 로그를 정리해 감사 자료를 생성해야 했으며, 인력 및 시간이 많이 소요되었습니다.  

**CloudTrail로 해결:**
- **해결 1:** 모든 AWS 리소스의 API 호출 및 CLI 명령어를 실시간으로 기록  
  CloudTrail은 모든 리소스에 대한 활동을 중앙 집중식으로 기록해 실시간 모니터링이 가능합니다.  
- **해결 2:** 정책 위반 시 자동으로 감지 및 알림  
  AWS Config와 연동해 정책 위반 시 자동으로 로그를 분석하고 알림을 제공해 디버깅 시간을 절약합니다.  
- **해결 3:** 규정 준수 검증을 자동화  
  로그를 분석해 감사 자료를 생성하고, 규제 기준에 맞는 보고서를 자동으로 생성해 인력 부담을 줄입니다.  

### 비유로 이해하기
**CloudTrail은 회사의 CCTV 시스템과 같아요.**  
어떤 직원이 서버에 접근했는지, 어떤 파일을 수정했는지, 언제 어떤 명령어를 실행했는지를 모든 활동을 기록해두고 있습니다. 이를 통해 이상 행동이 발생했을 때 신속하게 조치할 수 있고, 사고 발생 시 책임자 추적도 용이합니다. 예를 들어, 보안 담당자가 특정 시간대에 비정상적인 권한 부여가 발생했을 경우, CloudTrail 로그를 통해 정확히 누가 언제 어떤 권한을 부여했는지를 확인할 수 있습니다.

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | **보안 위협 탐지** | 금융 기관에서 비정상적인 AWS 리소스 접근이 감지되어 로그 분석을 통해 원인을 파악 |
| 시나리오 2 | **구성 관리 및 정책 준수** | 클라우드 환경에서 AWS Config와 연동해 정책 위반 시 자동으로 알림 및 로그 기록 |
| 시나리오 3 | **감사 및 규제 준수** | 의료 기업이 HIPAA 규정에 따라 로그를 분석해 감사 자료를 생성 |

**이럴 때 CloudTrail을 선택하세요:**
- ✅ **실시간 보안 모니터링이 필요할 때**  
- ✅ **AWS 리소스 활동을 기록하고 분석해야 할 때**  
- ✅ **규제 준수를 위한 감사 자료를 자동화해야 할 때**  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ **단순한 로그 저장이 필요할 때** → **CloudWatch Logs**  
  *이유: CloudTrail은 AWS 리소스 활동에 특화된 로그 기록 서비스이므로, 일반 로그 저장은 CloudWatch Logs가 더 적합합니다.*  
- ❌ **실시간 분석이 필요할 때** → **Kinesis Data Streams**  
  *이유: CloudTrail은 로그 저장에 중점을 둔 반면, 실시간 분석은 Kinesis가 더 적합합니다.*  

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **GuardDuty** | 보안 위협 탐지 및 머신러닝 기반 분석 | CloudTrail → GuardDuty → 알림 시스템 |
| **Security Hub** | 통합 보안 데이터 수집 및 위험 분류 | CloudTrail → Security Hub → 보고서 생성 |
| **AWS Config** | 자동화된 보안 준수 검증 및 정책 적용 | CloudTrail → AWS Config → 정책 위반 알림 |

**자주 사용되는 아키텍처 패턴:**
```
User → CLI/API → AWS 리소스 → CloudTrail (로그 기록) → CloudWatch Logs (분석) → Security Hub (통합 보안 분석)
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **로그 저장 용량** | $0.006/GB (월간) | 50GB/월 무료 |
| **데이터 전송 비용** | $0.09/GB (국내/해외) | 무료 |
| **데이터 스캔 비용** | $0.005/GB | 무료 |

**비용 최적화 팁:**
1. 💡 **S3 스토리지 클래스 선택:**  
   로그를 S3 Standard, S3 Glacier, S3 One Zone Glacier 등에 저장할 때, 데이터 접근 빈도에 따라 적절한 스토리지 클래스를 선택해 비용을 절감하세요.  
2. 💡 **로그 압축 활성화:**  
   로그를 GZIP 형식으로 압축해 저장 공간을 절약하고, 데이터 전송 비용을 줄입니다.  
3. 💡 **로그 보존 기간 설정:**  
   S3 Lifecycle 정책을 통해 특정 기간 후 로그를 삭제하거나 아카이브로 전환해 비용을 최적화하세요.  

> **⚠️ 비용 주의:**  
  - **로그 저장량이 예상보다 많을 경우:**  
    예를 들어, 고성능 애플리케이션에서 많은 API 호출이 발생하면 로그 저장 비용이 급증할 수 있습니다.  
  - **국제 데이터 전송:**  
    로그를 해외 S3 버킷에 저장할 경우, 데이터 전송 비용이 증가할 수 있으므로 지역별 버킷 사용을 권장합니다.

## 📚 핵심 개념

### 개념 1: **CloudTrail의 API 로그 추적 및 감사 기능**
CloudTrail은 AWS 리소스에 대한 모든 API 호출을 기록하고, 이 로그를 통해 사용자 활동, 시스템 이벤트, 보안 위협 등을 분석하는 기능을 제공합니다. 이 기능은 리소스의 변경 사항을 추적하고, 보안 위험을 사전에 감지하는 데 필수적입니다. 특히, 감사 및 규정 준수(예: GDPR, SOC2)에 필요한 세부적인 로그 기록이 가능해 조직의 보안 및 운영 투명성을 높입니다. 또한, 로그는 AWS Kinesis Data Firehose, S3 버킷, Lambda 함수 등으로 전송되어 분석 및 대응을 용이하게 합니다.

#### 왜 중요한가?
- **보안 감사**: 모든 API 호출 기록을 통해 부적절한 접근 또는 오류를 감지하고, 사고 조사에 활용할 수 있습니다.
- **규정 준수**: 정부 및 산업 규제를 준수하기 위해 필요한 로그 기록을 자동화하여 내부 감사 및 외부 감사를 지원합니다.

#### 세부 요소
| 요소 | 설명 | 예시 |
|-----|-----|-----|
| **API 로그 기록** | AWS 리소스에 대한 모든 API 호출을 실시간으로 기록합니다. | EC2 인스턴스 생성, S3 버킷 삭제 등 |
| **로그 저장 위치** | S3 버킷, CloudWatch Logs, Kinesis Data Firehose 등으로 전송 가능합니다. | S3 버킷에 로그 저장 후 분석 |
| **로그 분석 기능** | AWS Lambda, Athena 등으로 로그를 분석하여 패턴을 파악합니다. | 사용자별 API 호출 패턴 분석 |

> **💡 Tip:** 로그를 실시간으로 분석하려면 AWS CloudWatch Logs Insights를 활용하세요. 예를 들어, "aws cloudwatch logs insights query" 명령어로 특정 패턴을 검색할 수 있습니다.

---

### 개념 2: **CloudTrail의 보안 분석 및 이벤트 모니터링**
CloudTrail은 AWS 서비스의 이벤트를 실시간으로 모니터링하며, 위협 탐지 및 보안 분석을 지원합니다. 이 기능은 로그를 기반으로 이상 행동(예: 비정상적인 리소스 삭제, 접근 권한 변경 등)을 감지하고, 알림을 제공합니다. 특히, AWS GuardDuty와 연동하여 머신러닝 기반의 위협 분석을 수행할 수 있어, 보안 사고 대응을 신속하게 가능하게 합니다. 또한, 로그를 AWS Security Hub에 전송해 통합된 보안 위험 분류를 수행할 수 있습니다.

#### 작동 원리
1. **이벤트 수집**: AWS 리소스에서 발생하는 모든 API 호출과 이벤트를 CloudTrail에서 수집합니다.
2. **이벤트 분석**: 로그를 기반으로 이상 행동을 감지하고, 보안 위험을 분류합니다.
3. **알림 및 대응**: 감지된 위협에 대해 AWS GuardDuty, CloudWatch 알림, SNS 등을 통해 사용자에게 알리고, 자동화된 대응 프로세스를 실행합니다.

> **💡 Tip:** 이벤트를 실시간으로 모니터링하려면 AWS CloudTrail Event Data Store를 사용하세요. 이 기능은 AWS Organizations 내 모든 계정의 이벤트를 한 번에 수집합니다.

---

### 개념 3: **CloudTrail의 정책 기반 접근 제어 및 경고 시스템**
CloudTrail은 AWS Identity and Access Management(IAM) 정책과 연동해, 특정 API 호출에 대한 접근 권한을 제어하고, 비정상적인 활동에 대한 경고를 제공합니다. 이 기능은 조직의 보안 정책을 준수하고, 임의의 접근을 차단하는 데 중요합니다. 예를 들어, 특정 사용자가 EC2 인스턴스를 삭제할 수 있는 권한이 없으면, CloudTrail은 해당 요청을 기록하고, AWS CloudWatch를 통해 경고를 발송합니다. 또한, 로그를 AWS Config Rules와 연동해 정책 위반을 자동으로 감지할 수 있습니다.

#### 주요 특징
1. **IAM 정책 통합**: AWS IAM 정책을 기반으로 API 호출을 제어하며, 비정상적인 접근을 차단합니다.  
2. **자동 경고 시스템**: CloudWatch 알림, SNS, Lambda 함수 등을 통해 정책 위반 시 즉시 경고를 제공합니다.  
3. **정책 준수 확인**: AWS Config Rules와 연동해 정책 위반을 자동으로 감지하고, 보고서를 생성합니다.

> **💡 Tip:** 정책 위반을 감지하려면 AWS Config Rules를 사용하세요. 예를 들어, "aws config rules create" 명령어로 특정 정책을 설정하고, 위반 시 알림을 받을 수 있습니다.

## 🖥️ AWS 콘솔에서 CloudTrail 사용하기

### Step 1: CloudTrail 서비스 접속  
1. AWS Management Console에 로그인합니다.  
   - URL: [https://console.aws.amazon.com](https://console.aws.amazon.com)  
   - 로그인 후, 상단 메뉴에서 **Services**를 클릭합니다.  
2. 검색창에 **CloudTrail**을 입력하고, 결과에서 **CloudTrail** 서비스를 선택합니다.  
   - **CloudTrail** 서비스는 **Security & Compliance** 카테고리에 있습니다.  
3. **CloudTrail** 대시보드가 열리면, **Trails** 탭에서 작업을 시작합니다.  

> **📸 화면 확인:**  
> - 로그인 후 **CloudTrail** 서비스가 정상적으로 열리고, **Trails** 탭이 표시되는지 확인합니다.  
> - **Trails** 탭에서 **Create trail** 버튼이 보이는지 확인합니다.  

---

### Step 2: [주요 작업 1 - 리소스 생성]  
1. **Create trail** 버튼을 클릭합니다.  
   - **Trail name** 필드에 `MyCloudTrail`과 같은 이름을 입력합니다.  
   - **S3 bucket name** 필드에 기존 S3 버킷 또는 새 버킷을 선택합니다.  
     - 새 버킷을 생성하려면 **Create new bucket**을 클릭하고, 버킷 이름과 지역을 입력합니다.  
2. **CloudWatch Logs** 설정:  
   - **CloudWatch log group**에 `MyCloudTrailLogs`와 같은 이름을 입력합니다.  
   - **Include AWS KMS key usage events**를 **Yes**로 설정합니다.  
3. **Event data delivery** 설정:  
   - **Include additional information**를 **Yes**로 설정하여 보다 상세한 이벤트 데이터를 수집합니다.  
   - **Enable logging**을 **Yes**로 설정하여 로깅을 활성화합니다.  

> **📸 화면 확인:**  
> - **S3 bucket** 및 **CloudWatch log group**이 올바르게 입력되었는지, **Enable logging**이 활성화되었는지 확인합니다.  
> - **Create trail** 버튼을 클릭하여 리소스 생성을 완료합니다.  

---

### Step 3: [주요 작업 2 - 설정/구성]  
1. **Trail details** 설정:  
   - **Trail status**가 **Enabled**로 표시되는지 확인합니다.  
   - **Trail ARN**을 복사하여 다른 서비스(예: GuardDuty)와 연동할 때 사용할 수 있습니다.  
2. **Event history** 확인:  
   - **Event history** 탭에서 최근 이벤트를 확인합니다.  
   - 예: IAM 사용자 생성, S3 버킷 생성 등의 이벤트가 기록되었는지 확인합니다.  
3. **Retention settings** 조정:  
   - **Event data retention**을 설정하여 이벤트 데이터를 보존할 기간을 조정합니다.  
     - 예: 30일, 60일, 90일, 180일, 365일 등 선택 가능합니다.  

> **⚠️ 주의:**  
> - **S3 bucket** 및 **CloudWatch log group**이 존재하지 않으면 리소스 생성이 실패할 수 있습니다.  
> - **Event data retention**을 0일로 설정하면 이벤트 데이터가 즉시 삭제됩니다.  

---

### Step 4: 설정 확인 및 테스트  
1. **생성된 리소스 확인 방법:**  
   - **Trails** 탭에서 생성한 `MyCloudTrail`이 목록에 표시되는지 확인합니다.  
   - **S3 bucket** 및 **CloudWatch log group**이 생성되었는지 AWS 콘솔에서 확인합니다.  
2. **상태 확인 방법:**  
   - **Trail status**가 **Enabled**로 표시되며, **Event data retention**이 설정된 기간으로 보이는지 확인합니다.  
   - **Event history** 탭에서 최근 10개 이벤트가 정상적으로 기록되었는지 확인합니다.  
3. **정상 동작 테스트:**  
   - IAM 사용자로 S3 버킷에 파일을 업로드합니다.  
   - **Event history** 탭에서 해당 이벤트가 1분 이내에 기록되었는지 확인합니다.  
   - **CloudWatch Logs**에서 로그를 검색하여 이벤트 세부 정보를 확인합니다.  

> **💡 Tip:**  
> - **Free Tier**는 CloudTrail에 1GB의 이벤트 데이터를 제공합니다.  
> - **Cost**는 이벤트 데이터 저장소(예: S3) 및 로그 저장소(예: CloudWatch Logs)에 따라 달라집니다.  
> - **Monitoring**을 위해 **CloudWatch Metrics**를 활용하여 이벤트 수를 추적할 수 있습니다.

## ⌨️ AWS CLI로 CloudTrail 사용하기

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
AWS CLI를 사용하기 전에 버전을 확인해 최신 버전인지 확인하세요. `sts get-caller-identity`는 AWS 계정 정보를 확인하는 명령어이며, `configure get region`은 현재 설정된 리전을 확인합니다.  
> **💡 Tip:** CLI 설정은 `aws configure` 명령어로 할 수 있으며, `~/.aws/config` 파일에 자격 증명이 저장됩니다.

---

### 예제 1: CloudTrail 리소스 조회
```bash
# [CloudTrail 트레이 생성 목록 조회]
aws cloudtrail list-trails --query 'Trails[*].TrailName' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| `--query 'Trails[*].TrailName'` | 트레이 이름 필터링 | `Trails[*].TrailName` |
| `--output table` | 테이블 형식으로 출력 | `table`, `json`, `text` |

**예상 출력:**
```
| TrailName         |
+-------------------+
| example-trail-1   |
| example-trail-2   |
```

**설명:**  
`list-trails` 명령어는 현재 AWS 계정에 생성된 모든 CloudTrail 트레이를 조회합니다. `--query` 옵션을 사용해 특정 필드만 출력할 수 있으며, `--output`은 출력 형식을 설정합니다.

---

### 예제 2: CloudTrail 리소스 생성
```bash
# [CloudTrail 트레이 생성]
aws cloudtrail create-trail \
    --name "example-trail" \
    --is-multi-region-trail true \
    --s3-bucket-name "my-cloudtrail-bucket"
```

**필수 옵션:**
- `--name`: 트레이 이름 (예: `example-trail`)
- `--is-multi-region-trail`: 전역 트레이 여부 (true/false)
- `--s3-bucket-name`: 로그 저장할 S3 버킷 이름

**예상 출력:**
```json
{
    "TrailArn": "arn:aws:cloudtrail:us-east-1:123456789012:trail/example-trail",
    "Name": "example-trail",
    "TrailStatus": "Active"
}
```

**설명:**  
`create-trail` 명령어는 S3 버킷에 로그를 저장하는 트레이를 생성합니다. `--is-multi-region-trail`은 전역 트레이(모든 리전의 로그 수집) 여부를 설정합니다.  
> **⚠️ 주의:** S3 버킷이 존재하지 않으면 오류가 발생하므로 사전에 버킷을 생성해야 합니다.

---

### 예제 3: CloudTrail 리소스 수정
```bash
# [CloudTrail 트레이 수정]
aws cloudtrail update-trail \
    --name "example-trail" \
    --s3-bucket-name "updated-bucket"
```

**설명:**  
`update-trail` 명령어는 트레이의 설정을 수정합니다. 예를 들어, S3 버킷 이름 변경이나 로그 보존 기간 조정이 가능합니다.  
> **💡 Tip:** 트레이 이름은 변경할 수 없으므로 `--name` 옵션은 수정 시 사용할 수 없습니다.

---

### 예제 4: CloudTrail 리소스 삭제
```bash
# [CloudTrail 트레이 삭제]
aws cloudtrail delete-trail --name "example-trail"

# 삭제 확인
aws cloudtrail get-trail --name "example-trail"
```

**예상 출력 (삭제 후):**
```
{
    "trail": {
        "name": "example-trail",
        "status": "Inactive"
    }
}
```

> **⚠️ 주의:** 삭제는 되돌릴 수 없습니다. 트레이 삭제 전에 `get-trail` 명령어로 상태를 확인하세요.  
> **💡 Tip:** 삭제 후에는 `describe-trails` 명령어로 남은 트레이 목록을 확인할 수 있습니다.

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws cloudtrail list-trails
aws cloudtrail describe-trails --trail-name "example-trail"

# 생성
aws cloudtrail create-trail --name "example-trail" --is-multi-region-trail true

# 수정
aws cloudtrail update-trail --name "example-trail" --s3-bucket-name "new-bucket"

# 삭제
aws cloudtrail delete-trail --name "example-trail"
```

**설명:**  
위 명령어는 CloudTrail의 주요 작업(생성, 조회, 수정, 삭제)을 수행하는 CLI 명령어입니다.  
> **💡 Tip:** CLI 명령어는 AWS 공식 문서에서 최신 버전을 확인하세요.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 CloudTrail 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **CloudTrail의 API 호출 로깅 기능**  
   - 설명: AWS 리소스에 대한 모든 API 호출을 기록하여 보안 감사 및 사고 조사에 활용 가능. **API 로깅**, **사고 조사** 키워드로 문제가 출제될 확률이 높음.  
   - 키워드: `API 호출`, `사고 조사`, `보안 감사`

2. **CloudTrail과 Security Hub의 통합 활용**  
   - 설명: Security Hub에서 CloudTrail 이벤트를 실시간으로 수집하여 위험 수준을 분류하는 기능. 보안 정책 준수 여부를 검증하는 데 핵심적.  
   - 키워드: `Security Hub`, `위험 분류`, `통합 보안`

3. **이벤트 로그 보존 기간 및 관리**  
   - 설명: 기본적으로 90일간 로그를 보존하지만, S3 버킷에 저장해 장기 보존해야 하는 점. 보존 기간 설정과 데이터 관리 전략이 시험에서 자주 다루어짐.  
   - 키워드: `로그 보존`, `S3 저장`, `데이터 관리`

4. **CloudTrail의 비용 구조 및 프리티어 제한**  
   - 설명: 로그 생성량에 따라 비용이 발생하며, 프리티어는 1년간 50GB까지 무료. 예산 관리 및 비용 최적화 전략이 시험에 빈번히 출제됨.  
   - 키워드: `비용 관리`, `프리티어`, `로그 생성량`

5. **CloudTrail의 제한사항 및 한계**  
   - 설명: 로그 생성 시 지연 시간이 발생하거나, 특정 서비스의 API 호출이 기록되지 않는 경우가 있음. 시험에서는 이와 같은 한계를 파악하는 문제가 자주 등장.  
   - 키워드: `로그 지연`, `제한 사항`, `API 호출 범위`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | "CloudTrail은 모든 API 호출을 실시간으로 기록한다"는 문장에서 실시간 기록이 아닌 **이벤트 기반 로깅**임을 간과할 수 있음 | CloudTrail은 이벤트 발생 후 로그를 생성하므로 실시간이 아님 |
| 함정 2 | CloudTrail과 CloudWatch Logs의 기능을 혼동할 수 있음. 예: 로그 저장 위치를 S3에 설정하는 경우 CloudTrail이 아닌 CloudWatch Logs가 해당됨 | CloudTrail은 AWS 서비스 이벤트 기록, CloudWatch Logs는 일반 로그 관리 |
| 함정 3 | 로그 보존 기간을 설정하지 않으면 **기본적으로 90일**로 자동 설정되지만, 일부 사용자는 14일로 오인할 수 있음 | CloudTrail은 기본값 90일, S3 버킷 설정으로 장기 보존 가능 |

#### 🔄 CloudTrail vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | CloudTrail | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | AWS 리소스에 대한 API 호출 및 관리 이벤트 기록 | CloudWatch Logs (일반 로그 관리), AWS Config (리소스 변경 감시) | **AWS 서비스 이벤트 기록**이 필요한 경우 |
| 확장성 | S3, Glacier, Lambda 등과 통합 가능 | CloudWatch Logs는 로그 저장소만 제공 | **고가용성, 장기 보존**이 필요한 경우 |
| 비용 | 로그 생성량에 따라 요금 발생 | CloudWatch Logs는 데이터 저장량 기준 요금 | **비용 최적화 전략**이 중요할 때 |
| 지연시간 | 이벤트 발생 후 로그 생성 (이벤트 기반) | CloudWatch Logs는 실시간으로 로그 수집 | **실시간 모니터링**이 필요할 때 |

#### 📝 시험 대비 체크리스트
- [ ] CloudTrail의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  → "AWS 리소스에 대한 모든 API 호출 및 관리 이벤트를 기록하여 보안 감사 및 사고 조사에 활용합니다."
- [ ] CloudTrail을 선택해야 하는 시나리오를 알고 있는가?  
  → **보안 감사**, **사고 조사**, **AWS 서비스 이벤트 추적**이 필요한 경우
- [ ] CloudTrail의 제한사항/한계를 알고 있는가?  
  → **로그 지연**, **특정 서비스 API 호출 미기록**, **S3 저장 필수** 등
- [ ] CloudTrail과 비슷한 서비스의 차이점을 설명할 수 있는가?  
  → CloudWatch Logs는 일반 로그 관리, AWS Config는 리소스 변경 감시
- [ ] CloudTrail의 비용 구조를 이해하고 있는가?  
  → 로그 생성량 기준 요금, 프리티어는 1년간 50GB까지 무료

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 CloudTrail을 떠올리세요:  
> - **API 호출 로깅**  
> - **사고 조사**  
> - **보안 감사**  
> - **이벤트 기반 로깅**  
> - **로그 보존 기간**  
> - **비용 최적화**

---

| [⬅️ Config](./Config.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 4](../README.md) | [다음 Day ➡️](../day4/README.md) |

---
