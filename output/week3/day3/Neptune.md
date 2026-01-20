---

| [⬅️ Redshift](./Redshift.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 3](../README.md) | [DocumentDB ➡️](./DocumentDB.md) |

---

# Neptune 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** Neptune는 관계형 데이터베이스에서 그래프 데이터베이스로 전환할 때 필요한 강력한 그래프 데이터베이스 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- 문제 1: 복잡한 관계 네트워크를 처리할 때 SQL 기반 데이터베이스가 성능 저하를 겪는다. 예를 들어, 사회관계망 서비스에서 사용자 간의 연결 관계를 실시간으로 분석할 때 복잡한 JOIN 쿼리가 발생한다.
- 문제 2: 데이터 모델링 시 유연성 부족으로 인해 새로운 관계 타입을 추가하는 것이 어렵다. 예를 들어, 기존에 '사용자-친구' 관계만 지원하던 시스템에서 '사용자-좋아요' 관계를 추가하려면 스키마 변경이 필요했다.
- 문제 3: 대규모 그래프 데이터를 처리할 때 서버 리소스가 과도하게 소모되어 비용이 증가한다. 예를 들어, 10만 개 이상의 노드와 엣지를 가진 그래프를 처리할 때 성능 최적화가 어려웠다.

**Neptune로 해결:**
- 해결 1: 그래프 데이터베이스 엔진을 통해 복잡한 관계를 효과적으로 저장하고, SPARQL 쿼리로 실시간으로 분석할 수 있다. 예를 들어, 사용자 간의 연결 관계를 100배 빠르게 조회할 수 있다.
- 해결 2: 유연한 데이터 모델링을 통해 새로운 관계 타입을 추가할 때 스키마 변경이 필요하지 않다. 예를 들어, '사용자-좋아요' 관계를 추가할 때 데이터 모델을 변경하지 않고도 처리 가능하다.
- 해결 3: 자동 스케일링과 최적화된 쿼리 처리로 대규모 그래프 데이터를 효율적으로 관리할 수 있다. 예를 들어, 100만 개의 노드와 엣지를 가진 그래프도 100% 성능 유지가 가능하다.

### 비유로 이해하기
Neptune는 사회관계망 서비스의 연결 관계를 맵으로 표현하는 것처럼, 사람 간의 친구 관계, 좋아요 관계, 팔로우 관계를 모두 시각적으로 연결해주는 지도 같은 서비스입니다. 기존의 SQL 데이터베이스는 도로망처럼 복잡한 연결을 처리하기 어려웠지만, Neptune는 도로와 교차로를 그래프로 표현해 주행 경로를 빠르게 찾을 수 있도록 해줍니다. 이처럼 Neptune는 복잡한 관계 네트워크를 효율적으로 저장하고 분석하는 데 최적화되어 있습니다.

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 추천 시스템에서 사용자-상품 간의 관계 분석 | Netflix에서 영화 추천 시, 사용자와 영화 간의 관계를 그래프로 저장해 추천 알고리즘 최적화 |
| 시나리오 2 | 사기 탐지 시 거래 네트워크 분석 | 신용카드 사기 탐지 시, 거래자 간의 연결 관계를 분석해 이상 트랜잭션 식별 |
| 시나리오 3 | 지식 그래프 구성 | 기업의 제품, 고객, 파트너사 간의 복잡한 관계를 시각화해 데이터 통합 |

**이럴 때 Neptune를 선택하세요:**
- ✅ 상황 1: 사용자 간의 연결 관계를 실시간으로 분석해야 할 때
- ✅ 상황 2: 대규모 그래프 데이터를 효율적으로 저장하고 처리해야 할 때
- ✅ 상황 3: 데이터 모델링 시 유연성과 확장성을 요구할 때

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ 상황: 관계형 데이터베이스에서 복잡한 JOIN 쿼리가 필요할 때 → **Redshift** (데이터 웨어하우스로 대규모 데이터 분석)
- ❌ 상황: 메모리 기반의 고성능 캐시가 필요할 때 → **ElastiCache (Redis/Memcached)** (실시간 데이터 캐싱)
- ❌ 상황: 시간 시리즈 데이터를 분석해야 할 때 → **Timestream** (시간 기반 데이터 저장 및 분석)

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **ElastiCache (Redis)** | 캐싱을 통해 Neptune의 쿼리 성능 향상 | Neptune → ElastiCache → Application |
| **Redshift** | Neptune의 그래프 데이터를 분석용 데이터 웨어하우스로 전송 | Neptune → Redshift → BI Tool |
| **S3** | Neptune의 백업 및 아카이브 데이터 저장 | Neptune → S3 (백업) → Glacier (아카이브) |

**자주 사용되는 아키텍처 패턴:**
```
[사용자] → [API Gateway] → [Neptune] → [ElastiCache] → [Application]
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **그래프 데이터 저장소** | $0.25~$1.25/GB/월 | 12개월 무료 (1GB, 100GB/월) |
| **SPARQL 쿼리 처리** | $0.10~$0.30/1,000 쿼리 | 12개월 무료 (1,000,000 쿼리) |
| **백업 및 복제** | $0.05~$0.15/GB/월 | 항상 무료 |

**비용 최적화 팁:**
1. 💡 팁 1: 프리티어 기간 동안 1GB의 그래프 데이터 저장소를 사용해 비용 절감
2. 💡 팁 2: 쿼리 처리량을 모니터링해 불필요한 쿼리 제거 또는 캐싱 전략 도입
3. 💡 팁 3: 백업 데이터를 Glacier로 이동해 저장 비용 절감

> **⚠️ 비용 주의:** SPARQL 쿼리 처리 비용은 쿼리 복잡도와 데이터량에 따라 급격히 증가할 수 있으므로, 성능 최적화와 쿼리 리뷰가 필수적입니다.

## 📚 핵심 개념

### 개념 1: Neptune의 그래프 데이터베이스 및 SPARQL 쿼리  
Neptune는 AWS에서 제공하는 **그래프 데이터베이스 서비스**로, 노드와 엣지로 구성된 관계형 데이터를 효율적으로 저장하고 쿼리할 수 있도록 설계되었습니다. 이 서비스는 **SPARQL**이라는 웹 기반의 쿼리 언어를 지원하여, 복잡한 관계 데이터를 탐색하고 분석할 수 있습니다. Neptune는 웹 애플리케이션, 추천 시스템, 사회 네트워크 분석 등에서 활용되며, 실시간으로 엄격한 일관성을 보장합니다.  

#### 왜 중요한가?  
- **관계형 데이터의 효율적 저장**: 노드(엔티티)와 엣지(관계)를 구조화하여 데이터를 저장하고, 이를 기반으로 복잡한 쿼리가 가능합니다.  
- **SPARQL 쿼리 지원**: 웹 기반의 쿼리 언어로, 데이터를 탐색하고 분석하는 데 유연한 기능을 제공합니다.  
- **실시간 일관성**: 트랜잭션 처리 시 데이터 일관성을 보장하여 신뢰할 수 있는 결과를 제공합니다.  

#### 세부 요소  
| 요소 | 설명 | 예시 |
|-----|-----|-----|
| 그래프 데이터 모델 | 노드(엔티티), 엣지(관계), 속성을 기반으로 데이터를 저장 | "사람-직업-회사" 관계 저장 |
| SPARQL 쿼리 언어 | 웹 기반의 쿼리로 복잡한 관계 데이터를 탐색 | `SELECT ?person WHERE { ?person <http://example.org/worksFor> <http://example.org/Amazon> }` |
| 실시간 일관성 | 트랜잭션 처리 시 데이터 일관성을 보장 | 결제 시 사용자 정보 변경 시 자동 반영 |

> **💡 Tip:** Neptune는 SPARQL 쿼리로 데이터를 정렬하고 필터링할 수 있어, 추천 시스템이나 사회 네트워크 분석에 적합합니다. 예를 들어, 사용자의 친구 추천을 위해 "사람-친구-사람" 관계를 SPARQL로 쿼리할 수 있습니다.

---

### 개념 2: ElastiCache Redis vs Memcached의 차이점  
ElastiCache는 AWS의 **메모리 데이터베이스 서비스**로, Redis와 Memcached 두 가지 인스턴스 유형을 제공합니다. 두 서비스는 모두 고성능 캐싱을 목표로 하지만, **데이터 저장 방식과 사용 사례**에서 차이가 있습니다.  

#### 작동 원리  
1. **Redis**: 키-값 저장 외에 **리스트, 세트, 해시, 스택, 큐** 등 복잡한 데이터 구조를 지원하며, **데이터 만료 시간**, **스키마 없이 데이터 저장**, **서버 측 스크립팅**이 가능합니다.  
2. **Memcached**: 단순한 **키-값 저장**만 지원하며, 데이터는 **모든 키가 동일한 값 형식**을 가정합니다.  
3. **ElastiCache**: Redis와 Memcached를 기반으로 클러스터 형식으로 배포하여 **높은 가용성과 확장성**을 제공합니다.  

> **💡 Tip:** Redis는 복잡한 데이터 구조와 트랜잭션 처리가 필요할 때, Memcached는 단순한 캐싱에 적합합니다. 예를 들어, Redis는 사용자 세션 데이터를, Memcached는 이미지 캐시를 관리하는 데 사용됩니다.

---

### 개념 3: Redshift의 데이터 웨어하우스 아키텍처  
Redshift는 AWS의 **클라우드 기반 데이터 웨어하우스** 서비스로, 대규모 데이터를 저장하고 복잡한 분석 쿼리에 최적화되어 있습니다. 이 서비스는 **columnar storage**, **parallel processing**, **query optimization** 기술을 통해 성능을 극대화합니다.  

#### 주요 특징  
1. **Columnar Storage**: 데이터를 열 기반으로 저장하여, 특정 열만 읽을 수 있어 **성능 향상**과 **저장 공간 절약**이 가능합니다.  
2. **Parallel Processing**: 여러 노드가 병렬로 쿼리를 처리하여 **대규모 데이터 분석**에 적합합니다.  
3. **Query Optimization**: 쿼리 최적화 기능을 통해 **리소스 효율성**을 높이고, **성능 최적화**를 지원합니다.  

> **💡 Tip:** Redshift는 대규모 데이터 분석에 적합하며, 예를 들어, 고객 구매 패턴 분석이나 실시간 리포트 생성에 활용됩니다. Redshift는 **S3**와 연동하여 데이터를 저장할 수 있으며, **AWS Glue**를 통해 ETL 작업을 수행할 수 있습니다.

## 🖥️ AWS 콘솔에서 Neptune 사용하기

### Step 1: Neptune 서비스 접속  
1. AWS Management Console에 로그인합니다.  
   - URL: https://console.aws.amazon.com  
   - 로그인 후 "Services" 메뉴에서 "Neptune"를 검색합니다.  
2. 검색 결과에서 "Neptune"을 클릭해 대시보드로 이동합니다.  
   - **AWS Region 선택**: Neptune 서비스는 특정 리전에서만 사용 가능하므로, 예를 들어 `us-east-1`을 선택합니다.  
   - **IAM 권한 확인**: Neptune 생성 및 관리 권한이 있는 IAM 사용자로 로그인해야 합니다.  

> **📸 화면 확인:** Neptune 대시보드가 표시되면 정상입니다. 왼쪽 메뉴에서 "DB clusters" 또는 "DB instances"를 클릭해 리소스 목록을 확인할 수 있습니다.  

---

### Step 2: [주요 작업 1 - 리소스 생성]  
1. **Neptune DB 클러스터 생성**  
   - **클릭할 버튼**: "Create DB cluster" 버튼을 클릭합니다.  
   - **입력해야 할 값**:  
     - **DB cluster identifier**: 고유한 이름을 입력합니다 (예: `neptune-cluster-01`).  
     - **Edition**: "Serverless" 또는 "Standard"을 선택합니다. Serverless는 프리티어로 1개 클러스터 생성 가능.  
     - **Storage**: 100GB 이하로 설정합니다 (프리티어 제한).  
     - **Network**: VPC를 선택하고, 보안 그룹을 설정합니다.  
2. **설정 옵션 설명**  
   - **Encryption**: 암호화를 활성화해 데이터 보안을 강화합니다.  
   - **Monitoring**: CloudWatch 통합을 활성화해 실시간 모니터링을 설정합니다.  
3. **확인 사항**  
   - **리소스 생성 시간**: 약 5~10분 소요됩니다.  
   - **상태 확인**: "DB cluster" 목록에서 "Available" 상태가 표시될 때까지 기다립니다.  

> **📸 화면 확인:** "Create DB cluster" 화면에서 입력값을 확인하고, 생성 완료 후 "DB clusters" 목록에서 상태를 확인합니다.  

---

### Step 3: [주요 작업 2 - 설정/구성]  
1. **보안 그룹 설정**  
   - Neptune 클러스터에 접근할 수 있는 IP 주소나 VPC를 정의합니다.  
   - **AWS CLI 예시**:  
     ```bash
     aws ec2 describe-security-groups --group-ids sg-1234567890abcdef0
     ```  
2. **연결 포트 확인**  
   - Neptune의 기본 포트는 `8182`입니다.  
   - **포트 설정**: VPC 설정 시 포트를 허용해 외부 접근을 허용합니다.  
3. **모니터링 설정**  
   - CloudWatch에서 "DB cluster" 메트릭을 확인해 성능을 모니터링합니다.  

> **⚠️ 주의:** 보안 그룹 설정 시, 외부 IP를 허용하지 않도록 주의해야 합니다. 리소스 노출 위험이 있습니다.  

---

### Step 4: 설정 확인 및 테스트  
1. **생성된 리소스 확인 방법**  
   - "DB clusters" 목록에서 생성한 클러스터 이름을 클릭해 상세 정보를 확인합니다.  
   - **Endpoint**: 클러스터에 연결할 수 있는 DNS 주소를 확인합니다.  
2. **상태 확인 방법**  
   - **Status**: "Available" 상태인지 확인합니다.  
   - **CloudWatch**: CPU 사용량, 네트워크 트래픽 등을 모니터링합니다.  
3. **정상 동작 테스트 방법**  
   - **AWS CLI 테스트**:  
     ```bash
     aws neptune describe-db-clusters --db-cluster-identifier neptune-cluster-01
     ```  
   - **Gremlin 쿼리 테스트**:  
     ```bash
     aws neptune query --cluster-identifier neptune-cluster-01 --query "g.V().hasLabel('person').limit(5)"
     ```  

> **💡 Tip:** Neptune는 Gremlin, SPARQL, Apache Cypher 쿼리 언어를 지원합니다. 쿼리 테스트 시 언어를 선택해 주세요.  

---

### 📌 비용 및 프리티어 활용  
- **프리티어 제한**:  
  - 1개의 DB 클러스터, 100GB 저장소, 1개의 DB 인스턴스.  
- **비용 관리**:  
  - AWS Cost Explorer에서 Neptune 사용량을 추적합니다.  
  - **Serverless 모드**: 프로비저닝 없이 자동 스케일링됩니다.  

> **✅ 실무 팁**: Neptune는 그래프 데이터베이스로, 연결 관계 분석에 적합합니다. 쿼리 성능 최적화를 위해 인덱스 설정을 반드시 확인하세요.

## ⌨️ AWS CLI로 Neptune 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

**필요 사항:**  
- AWS CLI 버전 1.18.0 이상  
- Neptune 서비스 활성화된 리전에서 실행 (예: us-east-1, eu-west-1)  
- Neptune 클러스터 생성 시 `--engine-version` 파라미터로 엔진 버전 지정 (예: `1.0.1.11`)

---

### 예제 1: Neptune 리소스 조회
```bash
# Neptune 클러스터 목록 조회
aws neptune list-db-clusters --query '[].DBClusterIdentifier' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| --query | 결과 필터링 | '[].DBClusterIdentifier' |
| --output | 출력 형식 | json, table, text |

**예상 출력:**
```
DBClusterIdentifier
-------------------
my-neptune-cluster
```

---

### 예제 2: Neptune 리소스 생성
```bash
# Neptune 클러스터 생성
aws neptune create-db-cluster \
    --db-cluster-identifier "my-neptune-cluster" \
    --engine "neptune-graph" \
    --engine-version "1.0.1.11" \
    --db-subnet-group-name "my-subnet-group" \
    --vpc-security-group-ids "sg-12345678" \
    --preferred-maintenance-window "sun:07:00-sun:07:30" \
    --backup-retention-period 7
```

**필수 옵션:**  
- `--db-cluster-identifier`: 클러스터 고유 이름  
- `--engine`: Neptune 엔진 유형 (ex: `neptune-graph`, `neptune-sql`)  
- `--db-subnet-group-name`: VPC 서브넷 그룹 이름  
- `--vpc-security-group-ids`: 보안 그룹 ID  

**예상 출력:**
```json
{
    "DBCluster": {
        "DBClusterIdentifier": "my-neptune-cluster",
        "Status": "creating"
    }
}
```

---

### 예제 3: Neptune 리소스 수정
```bash
# Neptune 클러스터 엔진 버전 업데이트
aws neptune update-db-cluster \
    --db-cluster-identifier "my-neptune-cluster" \
    --engine-version "1.0.1.12"
```

**수정 가능한 옵션:**  
- `--engine-version`: 엔진 버전 변경  
- `--backup-retention-period`: 백업 보존 기간 조정  

---

### 예제 4: Neptune 리소스 삭제
```bash
# Neptune 클러스터 삭제
aws neptune delete-db-cluster --db-cluster-identifier "my-neptune-cluster"

# 삭제 확인
aws neptune describe-db-clusters --db-cluster-identifier "my-neptune-cluster"
```

> **⚠️ 주의:** 삭제는 되돌릴 수 없습니다. `--skip-snapshot` 파라미터로 스티치 생성 여부 조정 가능.

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws neptune list-db-clusters
aws neptune describe-db-clusters --db-cluster-identifier "id"

# 생성
aws neptune create-db-cluster --db-cluster-identifier "name" --engine "neptune-graph"

# 수정
aws neptune update-db-cluster --db-cluster-identifier "id" --engine-version "1.0.1.12"

# 삭제
aws neptune delete-db-cluster --db-cluster-identifier "id"
```

---

### 💡 Tip: Neptune CLI 사용 팁
1. **비용 최적화:** `--backup-retention-period`를 1일로 설정하면 데이터 손실 위험이 있으니 주의  
2. **프리티어 활용:** 7일간 무료로 사용 가능 (1 DB 클러스터, 100MB 스토리지)  
3. **리전 제한:** Neptune는 `us-east-1`, `eu-west-1`, `ap-northeast-1` 리전에서만 사용 가능  

---

### 📊 Neptune CLI 명령어 비교표
| 명령어 | 기능 | 필수 파라미터 |
|-------|------|----------------|
| `list-db-clusters` | 클러스터 목록 조회 | 없음 |
| `create-db-cluster` | 클러스터 생성 | `--db-cluster-identifier` |
| `update-db-cluster` | 클러스터 업데이트 | `--db-cluster-identifier` |
| `delete-db-cluster` | 클러스터 삭제 | `--db-cluster-identifier` |

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 Neptune 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **포인트 1: Neptune의 그래프 데이터베이스 및 SPARQL 쿼리**  
   - 설명: Neptune는 RDF(리소스 desc립션 프레임워크) 기반의 그래프 데이터베이스로, SPARQL 쿼리 언어를 사용해 관계형 데이터를 분석합니다. 시험에서 SPARQL의 구문 구조, 그래프 모델링 방식, 쿼리 최적화 전략이 주요 평가 항목입니다.  
   - 키워드: `그래프 데이터베이스`, `SPARQL 쿼리`, `RDF`

2. **포인트 2: Neptune의 실제 적용 사례 및 제한 사항**  
   - 설명: 시험에서 Neptune를 선택해야 하는 시나리오(예: 사회적 네트워크 분석, 보이스 피싱 탐지)와 제한 사항(예: 비용, 복잡한 스키마 설계)이 출제됩니다. 특히, 데이터 모델링의 유연성과 확장성에 대한 이해가 중요합니다.  
   - 키워드: `그래프 모델링`, `스케일링`, `비용 효율성`

3. **포인트 3: Neptune의 비용 구조 및 프리티어 활용**  
   - 설명: Neptune는 프리티어가 제공되며, 데이터 저장량, 쿼리 수, 노드 수에 따라 비용이 달라집니다. 시험에서는 비용 최적화 전략(예: 캐싱, 쿼리 최적화)이 직접적으로 묻는 경우가 많습니다.  
   - 키워드: `프리티어`, `데이터 저장량`, `쿼리 비용`

4. **포인트 4: Neptune vs DynamoDB/RDS의 차이점**  
   - 설명: Neptune는 그래프 데이터베이스로, DynamoDB(NoSQL), RDS(SQL)과는 구조적 차이가 큽니다. 시험에서는 "관계형 데이터 vs 그래프 데이터" 구분, 쿼리 언어(예: SPARQL vs SQL) 비교가 주요 출제 포인트입니다.  
   - 키워드: `그래프 vs 관계형`, `SPARQL vs SQL`, `스키마 유연성`

5. **포인트 5: Neptune의 성능 최적화 전략**  
   - 설명: Neptune의 지연 시간 최소화를 위한 전략(예: 인덱스 설정, 캐싱, 쿼리 최적화)과, 메모리/디스크 사용량 관리가 시험에서 자주 다루집니다. 특히, SPARQL 쿼리의 성능 튜닝 방법이 중요합니다.  
   - 키워드: `인덱스 설정`, `쿼리 최적화`, `지연 시간`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | "Neptune는 관계형 데이터베이스입니다"라는 문장이 출제될 수 있음 | **정답: 오류** (Neptune는 그래프 데이터베이스) |
| 함정 2 | "SPARQL은 SQL의 하위 집합입니다"라는 문장이 출제될 수 있음 | **정답: 오류** (SPARQL는 RDF 기반의 독립적 언어) |
| 함정 3 | "Neptune의 비용은 데이터 저장량에만 의존합니다"라는 문장이 출제될 수 있음 | **정답: 오류** (쿼리 수, 노드 수도 비용에 영향) |

#### 🔄 Neptune vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | Neptune | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | 그래프 데이터 관리, 관계형 분석 | DynamoDB(Relational DB), RDS | 복잡한 관계형 데이터 분석 시 |
| 확장성 | 자동 스토리지 확장, 노드 수 조절 | DynamoDB(수평 확장), RDS(수직 확장) | 고유한 그래프 모델링이 필요한 경우 |
| 비용 | 데이터 저장량, 쿼리 수 기반 | DynamoDB(요금 정책), RDS(스토리지/CPUs) | 쿼리 성능 최적화가 필수인 경우 |
| 지연 시간 | 캐싱, 인덱스 설정으로 최소화 | DynamoDB(요청 지연), RDS(쿼리 최적화) | 실시간 분석이 필요한 시나리오 |

#### 📝 시험 대비 체크리스트
- [ ] Neptune의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  (예: "그래프 데이터를 관리하고 SPARQL 쿼리로 관계형 분석을 수행하는 데이터베이스")
- [ ] Neptune를 선택해야 하는 시나리오를 알고 있는가?  
  (예: 사회적 네트워크 분석, 보이스 피싱 탐지)
- [ ] Neptune의 제한사항/한계를 알고 있는가?  
  (예: 복잡한 스키마 설계, 쿼리 최적화 필요)
- [ ] Neptune와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  (예: DynamoDB vs Neptune의 데이터 모델 차이)
- [ ] Neptune의 비용 구조를 이해하고 있는가?  
  (예: 데이터 저장량, 쿼리 수, 노드 수에 따른 요금)

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 Neptune를 떠올리세요:  
> - **그래프 데이터베이스**  
> - **SPARQL 쿼리**  
> - **RDF 모델링**  
> - **관계형 분석**  
> - **프리티어 활용**

---

| [⬅️ Redshift](./Redshift.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 3](../README.md) | [DocumentDB ➡️](./DocumentDB.md) |

---
