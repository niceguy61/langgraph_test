---

| [⬅️ SNS](./SNS.md) | [📑 Day 5 목차](./README.md) | [🏠 Week 3](../README.md) | [다음 Day ➡️](../../week4/day1/README.md) |

---

> **한 줄 정의:** Kinesis는 실시간 데이터 처리 및 분석을 위한 AWS의 통합 플랫폼 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 전통적인 데이터 처리 시스템은 실시간 데이터 스트림을 처리할 수 없어 지연이 발생했습니다. 예를 들어, 고객의 실시간 채팅 메시지나 IoT 센서 데이터를 즉시 분석하는 데 한계가 있었습니다.  
- **문제 2:** 대규모 데이터 처리 시 메시지 순서를 보장하는 것이 어려웠습니다. 예를 들어, 결제 거래 내역에서 "결제 승인" 메시지가 "결제 실패" 메시지보다 먼저 도착하면 데이터 무결성이 위협받았습니다.  
- **문제 3:** 데이터 인플루언스(ingestion) 시 다양한 시스템 간 연동이 복잡했으며, 데이터 손실이나 중복 전송의 위험이 있었습니다.  

**Kinesis로 해결:**
- **해결 1:** Kinesis Data Streams는 실시간 데이터 스트림을 처리할 수 있는 확장성 있는 인프라로, 수백만 개의 메시지 처리가 가능합니다.  
- **해결 2:** Kinesis Data Streams의 샤드(Shard) 구조와 SQS FIFO 큐를 활용해 메시지 순서를 보장해 데이터 무결성을 유지합니다.  
- **해결 3:** Kinesis Firehose와 Kinesis Analytics를 통해 데이터를 S3, Redshift, Elasticsearch 등 다양한 대상으로 간편하게 전송 및 분석할 수 있습니다.  

### 비유로 이해하기
Kinesis는 **데이터를 흐르게 하는 고속도로**입니다. 예를 들어, 쇼핑몰의 실시간 채팅 메시지나 스마트 센서 데이터는 Kinesis를 통해 빠르게 수집되고, Step Functions로 워크플로우를 정의해 고객 응대 로직을 자동화합니다. 이처럼 Kinesis는 데이터의 흐름을 원활하게 조절해 실시간 처리의 효율성을 높입니다.  

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 실시간 데이터 수집 및 분석이 필요한 경우 | 쇼핑몰의 실시간 채팅 메시지 처리, IoT 센서 데이터 모니터링 |
| 시나리오 2 | 메시지 순서 보장이 필수적인 시스템 | 금융 거래 내역 처리, 의료 장비 데이터 전송 |
| 시나리오 3 | 대규모 데이터 스트림을 다른 시스템에 전송해야 할 때 | 클라우드 기반의 로그 수집 및 분석, 실시간 대시보드 생성 |

**이럴 때 Kinesis를 선택하세요:**
- ✅ **실시간 데이터 처리**가 필수적인 시나리오  
- ✅ **메시지 순서 보장**이 필요한 시스템  
- ✅ **다양한 대상으로 데이터 전송**이 필요한 경우  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ **메시지 순서 보장이 필요하지 않다면** → **SQS 표준 큐** (비순서 메시지 처리 가능)  
- ❌ **데이터 스트림 처리가 필요하지 않다면** → **S3 + Lambda** (이벤트 기반 처리)  
- ❌ **실시간 분석이 아닌 저장용 데이터 처리** → **Kinesis Firehose + S3** (데이터 저장에 집중)  

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **Step Functions** | 워크플로우 오케스트레이션 | Kinesis Data Streams → Step Functions → DynamoDB |
| **EventBridge** | 이벤트 기반 처리 및 로깅 | Kinesis Firehose → EventBridge → CloudWatch Logs |
| **SNS** | 데이터 전송 알림 및 분배 | Kinesis Data Streams → SNS → Lambda 함수 실행 |
| **Redshift** | 실시간 데이터 분석 및 저장 | Kinesis Firehose → Redshift |
| **Elasticsearch** | 실시간 검색 및 분석 | Kinesis Data Streams → Elasticsearch |

**자주 사용되는 아키텍처 패턴:**
```
[사용자] → [CloudFront] → [S3]  
[IoT 센서] → [Kinesis Data Streams] → [Step Functions] → [DynamoDB]  
[Kinesis Firehose] → [S3/Redshift]  
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **Kinesis Data Streams** | $0.00025/GB (데이터 저장) + $0.0000003/1000 개체 (메시지 처리) | 월 10GB 무료 |
| **Kinesis Firehose** | $0.0000025/1000 개체 (데이터 전송) | 12개월 무료 |
| **Kinesis Analytics** | $0.000015/1000 개체 (데이터 분석) | 항상 무료 |

**비용 최적화 팁:**
1. 💡 **데이터 저장 비용 절감:** Kinesis Firehose를 사용해 S3에 데이터 저장하면 데이터 전송 비용이 절감됩니다.  
2. 💡 **메시지 처리 최적화:** 메시지 수신 후 즉시 처리하는 Lambda 함수를 사용해 불필요한 데이터 저장을 방지하세요.  
3. 💡 **비용 모니터링:** CloudWatch Metrics를 통해 데이터 전송량을 추적해 과도한 사용을 방지합니다.  

> **⚠️ 비용 주의:** 데이터 전송량이 급격히 증가할 경우, Kinesis Firehose의 데이터 전송 비용이 급격히 증가할 수 있으므로, 정기적인 모니터링이 필수적입니다.

## 📚 핵심 개념

### 개념 1: **Kinesis 데이터 스트림의 샤드와 데이터 인그레션**
Kinesis 데이터 스트림은 실시간 데이터 흐름을 처리하기 위해 **샤드**(Shard)라는 논리적 단위를 사용합니다. 샤드는 데이터를 분산 저장하고 병렬 처리를 가능하게 하며, 데이터 소스에서 들어오는 데이터를 분할하여 분산 저장합니다. 이는 고성능 및 확장성 요구사항을 충족시키기 위한 핵심 메커니즘입니다. 데이터는 키 값을 기반으로 샤드에 할당되며, 각 샤드는 독립적으로 데이터를 처리할 수 있어 대규모 데이터 처리 시 유연성을 제공합니다.  

#### 왜 중요한가?  
- **고가용성 및 확장성**: 샤드를 추가하거나 제거할 수 있어 트래픽 증가 시 자동 확장이 가능합니다.  
- **데이터 분산 처리**: 병렬 처리를 통해 대규모 데이터 흐름을 효율적으로 관리할 수 있습니다.  
- **실시간 분석**: 실시간 데이터를 즉시 처리하고 분석할 수 있어 대규모 이벤트 처리에 적합합니다.  

#### 세부 요소  
| 요소 | 설명 | 예시 |
|-----|-----|-----|
| **샤드(Shard)** | 데이터를 분산 저장하고 병렬 처리하는 논리적 단위 | 10개의 샤드로 구성된 스트림은 10개의 데이터 파티션을 처리합니다. |
| **데이터 키(Data Key)** | 데이터를 특정 샤드에 할당하는 기준 | 사용자 ID를 데이터 키로 설정해 동일한 사용자 데이터를 같은 샤드에 집중합니다. |
| **데이터 인그레션** | 데이터 소스에서 스트림으로 데이터를 흘려보내는 과정 | IoT 센서 데이터를 Kinesis 데이터 스트림으로 실시간 전송합니다. |

> **💡 Tip:** 샤드 수는 초기 설정 시 고려해야 하며, 동적 확장은 자동화된 스케일링 기능을 활용하세요.  

---

### 개념 2: **Kinesis Firehose의 자동 데이터 전송 및 스토리지 연동**
Kinesis Firehose는 데이터 스트림에서 데이터를 수집하고, AWS 스토리지 서비스(예: S3, Redshift, Elasticsearch)로 자동 전송하는 기능입니다. 이는 실시간 데이터를 저장 및 분석하기 위한 브릿지 역할을 하며, 데이터 전송 과정에서 압축, 암호화, 데이터 변환을 지원합니다. Firehose는 데이터 전송 시도 실패 시 오류를 로깅하고, 복구 시 자동 재전송을 제공합니다.  

#### 작동 원리  
1. **데이터 수집**: Kinesis 데이터 스트림 또는 직접 입력된 데이터를 Firehose에 전달합니다.  
2. **데이터 처리**: 압축, 암호화, 데이터 형식 변환(예: JSON에서 Parquet)을 수행합니다.  
3. **데이터 저장**: 설정된 스토리지 서비스(예: S3 버킷)로 데이터를 저장하거나 데이터베이스에 적재합니다.  

> **💡 Tip:** Firehose는 실시간 데이터 저장에 최적화되어 있으므로, 지연 없는 데이터 전송이 필요한 시나리오에 적합합니다.  

---

### 개념 3: **Kinesis Analytics의 실시간 데이터 분석 기능**
Kinesis Analytics는 실시간 데이터 스트림을 분석하기 위한 서비스로, SQL 기반의 데이터 처리를 지원합니다. 사용자는 데이터 스트림을 입력으로 설정하고, SQL 쿼리로 실시간 지표, 트렌드, 이상 징후를 즉시 분석할 수 있습니다. 분석 결과는 Kinesis Data Streams, S3, Lambda 등으로 전달되어 실시간 대응이 가능합니다.  

#### 주요 특징  
1. **SQL 기반 분석**: SQL 쿼리를 사용해 데이터를 필터링, 집계, 변환할 수 있습니다.  
2. **실시간 처리**: 데이터를 즉시 분석해 실시간 대응이 가능합니다.  
3. **연동 유연성**: 분석 결과를 다른 AWS 서비스(예: Lambda, S3)로 전송해 활용할 수 있습니다.  

> **💡 Tip:** Kinesis Analytics는 데이터 스트림의 실시간 분석에 최적화되어 있으므로, 지연 없는 대시보드 생성이나 이상 감지 시 사용하세요.

## 🖥️ AWS 콘솔에서 Kinesis 사용하기

### Step 1: Kinesis 서비스 접속  
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
   - 사용자 이름과 비밀번호를 입력해 로그인합니다.  
2. 상단 검색창에서 **"Kinesis"**를 입력하고, 검색 결과에서 **"Kinesis"** 서비스를 클릭합니다.  
   - **Kinesis 대시보드**가 표시되면 정상적으로 서비스에 접근했습니다.  

> **📸 화면 확인:** Kinesis 대시보드에서 **"Data Streams"**, **"Firehose"**, **"Analytics"** 등의 서비스 목록이 보여야 합니다.  

---

### Step 2: [주요 작업 1 - 리소스 생성] Step Functions 상태 머신 생성  
1. **Step Functions** 리소스 생성  
   - Kinesis 대시보드에서 상단 메뉴에서 **"Step Functions"**를 클릭합니다.  
   - **"Create state machine"** 버튼을 클릭하여 새 상태 머신을 생성합니다.  
   - **"Name"** 필드에 `KinesisStepFunction`과 같은 이름을 입력합니다.  
   - **"Type"**에서 **"Standard"**를 선택하고, **"Start state"**를 클릭해 상태 머신 구조를 정의합니다.  

2. **상태 머신 정의**  
   - **"Start state"**에서 **"Type"**을 **"Task"**로 설정하고, **"Resource"**에 `arn:aws:states:region:account-id:activity:KinesisActivity`를 입력합니다.  
   - **"Input path"**를 `$$.Payload`로 설정해 전달된 데이터를 사용합니다.  
   - **"Output path"**를 `$$.Payload`로 설정해 결과를 반환합니다.  

3. **리소스 생성 확인**  
   - **"Next"** 버튼을 클릭해 상태 머신을 생성합니다.  
   - 생성 완료 후 **"View state machine"**를 클릭해 상태 머신을 확인합니다.  

> **📸 화면 확인:** 상태 머신이 생성되었고, **"Execution"** 탭에서 실행을 테스트할 수 있어야 합니다.  

---

### Step 3: [주요 작업 2 - 설정/구성] Kinesis와의 연동 설정  
1. **Kinesis Data Streams 연결**  
   - 상태 머신의 **"Task"** 타입에서 **"Resource"** 필드에 `arn:aws:states:region:account-id:stateMachine:KinesisStepFunction`를 입력합니다.  
   - **"Input path"**를 `$$.Payload`로 설정해 전달된 데이터를 사용합니다.  

2. **Kinesis Firehose 설정**  
   - **"Output"** 탭에서 **"Firehose"**를 선택하고, **"Delivery stream"**을 생성합니다.  
   - **"Delivery stream"** 이름을 `KinesisFirehoseStream`으로 설정하고, **"IAM role"**을 선택해 권한을 부여합니다.  

3. **SNS 알림 설정**  
   - **"Notifications"** 탭에서 **"SNS"**를 선택하고, **"Topic"**을 생성합니다.  
   - **"Topic"** 이름을 `KinesisSnsTopic`으로 설정하고, **"Subscribers"**에 이메일 주소를 추가해 알림을 설정합니다.  

> **⚠️ 주의:** Kinesis Data Streams와 Firehose는 별도의 리소스 생성이 필요하며, 권한 설정을 반드시 확인해야 합니다.  

---

### Step 4: 설정 확인 및 테스트  
1. **리소스 확인 방법**  
   - Kinesis 대시보드에서 **"Data Streams"**, **"Firehose"**, **"Analytics"** 탭에서 생성된 리소스가 표시되는지 확인합니다.  

2. **상태 확인 방법**  
   - **"Step Functions"** 대시보드에서 **"Executions"** 탭에서 상태 머신이 실행 중인지 확인합니다.  
   - **"Kinesis Data Streams"**에서 데이터가 전송되고 있는지 확인합니다.  

3. **정상 동작 테스트**  
   - **"Step Functions"**에서 **"Start execution"**을 클릭해 상태 머신을 실행합니다.  
   - **"Kinesis Firehose"**에서 데이터가 정확히 전송되고, **"SNS"**에서 알림이 전달되는지 확인합니다.  

> **💡 Tip:** 프리티어로 12개월 동안 무료로 사용할 수 있으므로, 테스트 시 비용을 철저히 점검하세요.

## ⌨️ AWS CLI로 Kinesis 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

**참고:**  
- `aws --version`은 CLI 버전 확인에 사용됩니다.  
- `aws sts get-caller-identity`는 현재 사용자 계정 및 리전 정보를 확인합니다.  
- `aws configure get region`은 기본 리전을 확인합니다. AWS CLI는 기본 리전 설정 없이도 서비스 사용이 가능하지만, 리전별 리소스 접근 시 명시적으로 리전을 지정해야 합니다.

---

### 예제 1: Kinesis 리소스 조회
```bash
# [Kinesis Data Streams 목록 조회]
aws kinesis list-streams --query 'StreamNames' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| --query | 결과 필터링 | 'StreamNames' |
| --output | 출력 형식 | json, table, text |

**예상 출력:**
```
| StreamName       |
|------------------|
| example-stream   |
| another-stream   |
```

**참고:**  
- `list-streams`는 Kinesis Data Streams의 모든 스트림 이름을 반환합니다.  
- `--query`를 사용하여 특정 필드만 출력할 수 있습니다.  
- `--output table`은 테이블 형식으로 결과를 보기 쉽게 합니다.

---

### 예제 2: Kinesis 리소스 생성
```bash
# [Kinesis Data Stream 생성]
aws kinesis create-stream \
    --stream-name "example-stream" \
    --shard-count 1
```

**필수 옵션:**
- `--stream-name`: 생성할 스트림 이름
- `--shard-count`: 생성할 셰어드 수 (최소 1)

**예상 출력:**
```json
{
    "StreamName": "example-stream",
    "StreamStatus": "ACTIVE"
}
```

**참고:**  
- 셰어드 수는 스트림의 동시 처리 능력을 결정합니다.  
- 생성 후 `describe-stream` 명령어로 상태를 확인할 수 있습니다.  
- 프리티어 사용 시 1일당 100,000개 이하의 데이터 포인트 처리가 가능합니다.

---

### 예제 3: Kinesis 리소스 수정
```bash
# [Kinesis Data Stream 셰어드 수 수정]
aws kinesis increase-stream-retention-period \
    --stream-name "example-stream" \
    --retention-period-seconds 259200
```

**참고:**  
- `increase-stream-retention-period`는 스트림의 데이터 보존 기간을 수정합니다.  
- 수정 시 리전 및 스트림 이름을 반드시 지정해야 합니다.  
- 데이터 보존 기간은 최소 24시간(86,400초)에서 최대 7일(604,800초)까지 설정 가능합니다.

---

### 예제 4: Kinesis 리소스 삭제
```bash
# [Kinesis Data Stream 삭제]
aws kinesis delete-stream \
    --stream-name "example-stream" \
    --enforce-retention

# 삭제 확인
aws kinesis describe-stream \
    --stream-name "example-stream"
```

> **⚠️ 주의:** 삭제는 되돌릴 수 없습니다. `--enforce-retention` 옵션을 사용해 데이터를 24시간 보존한 후 삭제해야 합니다.

**참고:**  
- `delete-stream` 명령어는 스트림을 즉시 삭제하지 않고, 24시간 동안 데이터를 보존합니다.  
- 삭제 후 `describe-stream` 명령어는 `StreamStatus`가 `DELETING`으로 변경되었음을 확인할 수 있습니다.

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws kinesis list-streams
aws kinesis describe-stream --stream-name "example-stream"

# 생성
aws kinesis create-stream --stream-name "example-stream" --shard-count 1

# 수정
aws kinesis increase-stream-retention-period --stream-name "example-stream" --retention-period-seconds 259200

# 삭제
aws kinesis delete-stream --stream-name "example-stream" --enforce-retention
```

**팁:**  
- Kinesis Data Streams는 실시간 데이터 처리에 적합합니다.  
- 데이터 보존 기간 및 셰어드 수는 실무에서 트래픽 패턴에 따라 조정해야 합니다.  
- 프리티어 사용 시 1일당 100,000개 이하의 데이터 포인트 처리가 가능합니다.  
- CLI 사용 시 `--output table` 옵션으로 결과를 쉽게 확인할 수 있습니다.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 Kinesis 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **Kinesis Data Streams의 샤드 관리 및 데이터 인그레션**  
   - 설명: 실시간 데이터 흐름 처리 시 샤드 수 조정, 데이터 분산/집중 방식, 파티셔닝 전략이 시험에서 주요 포인트입니다. 샤드 수가 부족하면 데이터 손실, 과다하면 비용 증가로 인해 리스크 관리가 필수적입니다.  
   - 키워드: `샤드`, `데이터 인그레션`, `파티셔닝`

2. **Kinesis Firehose의 실시간 데이터 저장소 연동**  
   - 설명: Firehose가 S3, Redshift, Elasticsearch 등에 데이터를 자동 전송하는 기능은 시험에서 빈도가 높습니다. 파티션 키 설정, 데이터 압축, 암호화 옵션은 정답 유형에 직접 연결됩니다.  
   - 키워드: `Firehose`, `파티션 키`, `데이터 저장소`

3. **Kinesis Analytics의 SQL 기반 실시간 분석**  
   - 설명: Kinesis Analytics에서 KSQL을 사용해 실시간 데이터 분석 시, 스트림과 저장소 간의 연동 방식, 쿼리 성능 최적화 전략이 시험에서 주요 포인트입니다.  
   - 키워드: `KSQL`, `실시간 분석`, `스트림 연동`

4. **Kinesis의 지연시간 최소화 전략**  
   - 설명: 데이터 전송 지연 시간을 줄이기 위해 파티션 키 최적화, 샤드 수 증가, 데이터 압축 설정이 시험에서 자주 출제됩니다.  
   - 키워드: `지연시간`, `파티션 키`, `데이터 압축`

5. **Kinesis vs SQS/SNS의 데이터 처리 방식 차이**  
   - 설명: SQS는 메시지 큐로 처리, Kinesis는 실시간 스트림 처리로 구분됩니다. 메시지 순서 보장, 데이터 속도, 비용 구조 차이가 시험에서 혼동 요소로 자주 등장합니다.  
   - 키워드: `SQS`, `SNS`, `데이터 속도`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | Kinesis Firehose가 S3에 데이터 저장 시 파티션 키 설정이 필요하지 않다고 오인 | 파티션 키 설정은 Firehose에서 데이터 분산 최적화에 필수적 |
| 함정 2 | Kinesis Data Streams의 샤드 수 증가가 자동으로 데이터 처리 속도를 높인다고 오해 | 샤드 수 증가는 데이터 분산을 최적화하지만, 병렬 처리 능력만 향상 |
| 함정 3 | Kinesis Analytics에서 쿼리 실행 시 데이터 지연 발생 원인을 파티션 키 설정 오류로 오인 | 쿼리 성능 저하 시 데이터 스트림의 파티션 키 분산 불균형이 주요 원인 |

#### 🔄 Kinesis vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | Kinesis | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | 실시간 데이터 스트림 처리, 지연 시간 최소화 | SQS(메시지 큐), SNS(이벤트 알림) | 데이터 처리 속도가 핵심인 경우 |
| 확장성 | 샤드 수 유동 조절로 대규모 처리 가능 | SQS/FIFO(정해진 큐 수 제한) | 유동적인 데이터 처리량이 필요한 경우 |
| 비용 | 데이터 전송량에 따라 비용 증가 | SQS(SQS 기능별 요금) | 실시간 처리가 필요한 경우 |
| 지연시간 | 파티션 키 최적화로 최소화 | SQS(메시지 대기 시간) | 지연 시간 최소화가 핵심인 경우 |

#### 📝 시험 대비 체크리스트
- [ ] Kinesis의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  (예: "실시간 데이터 스트림을 처리하고 분석하는 서비스")
- [ ] Kinesis를 선택해야 하는 시나리오를 알고 있는가?  
  (예: 로그 수집, 실시간 분석, 빅데이터 처리)
- [ ] Kinesis의 제한사항/한계를 알고 있는가?  
  (예: 샤드 수 제한, 데이터 지연 가능성)
- [ ] Kinesis와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  (예: SQS는 메시지 큐, Kinesis는 스트림 처리)
- [ ] Kinesis의 비용 구조를 이해하고 있는가?  
  (예: 데이터 전송량, 파티션 키 설정, 압축 여부에 따른 비용 차이)

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 Kinesis를 떠올리세요:  
> - **실시간 데이터 인그레션**  
> - **스트림 처리**  
> - **데이터 파티셔닝**  
> - **Kinesis Firehose**  
> - **KSQL 쿼리**

---

| [⬅️ SNS](./SNS.md) | [📑 Day 5 목차](./README.md) | [🏠 Week 3](../README.md) | [다음 Day ➡️](../../week4/day1/README.md) |

---
