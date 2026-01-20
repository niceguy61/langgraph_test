---

| [⬅️ 이전 Day](../day2/README.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 3](../README.md) | [Redshift ➡️](./Redshift.md) |

---

# ElastiCache 완전 정복

> **한 줄 정의:** ElastiCache는 고성능 캐싱을 위한 AWS의 관리형 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 데이터베이스 읽기 요청이 증가할 때 성능 저하 발생  
  *구체적 설명:* 전통적인 RDBMS는 디스크 I/O에 의존해 읽기 속도가 느려지며, 이로 인해 사용자 경험 저하 및 시스템 지연 발생  
- **문제 2:** 확장성 제한으로 인한 성능 향상 어려움  
  *구체적 설명:* 서버 수를 늘려도 데이터 일관성 유지가 어려워, 병렬 처리 효율성이 떨어짐  
- **문제 3:** 캐싱 관리 및 모니터링 부담  
  *구체적 설명:* 캐시 키 관리, TTL 설정, 메모리 누수 감지 등 복잡한 운영이 필요  

**ElastiCache로 해결:**
- **해결 1:** 인메모리 데이터 저장으로 읽기 성능 10~1000배 향상  
  *어떻게 해결되는지:* Redis/Memcached 기반의 메모리 저장소로 데이터 접근 시간 단축  
- **해결 2:** 클러스터링 기능으로 수평 확장 가능  
  *어떻게 해결되는지:* Redis Cluster나 Memcached 클러스터를 통해 데이터 분산 및 병렬 처리 지원  
- **해결 3:** 자동 백업, 모니터링, 업데이트 관리  
  *어떻게 해결되는지:* AWS 관리형 서비스로 인프라 운영 부담 감소  

### 비유로 이해하기
**집안에서 빈 자식에게 빵을 주는 비유:**  
ElastiCache는 빵을 항상 준비해 둔 냉장고 같은 존재입니다. 주방에서 빵을 만들 때마다 냉장고를 열어 확인하는 대신, 이미 빵이 준비되어 있어서 시간을 절약할 수 있습니다. 이처럼 ElastiCache는 자주 요청되는 데이터를 메모리에 저장해 DB를 직접 접근하지 않아도 빠르게 응답합니다.  

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 사용자 세션 관리 | 인증 세션을 Redis 클러스터에 저장해 무중단 확장 가능 |
| 시나리오 2 | API 응답 캐싱 | 주요 API 응답을 메모리에 저장해 반복 요청 처리 시간 단축 |
| 시나리오 3 | 실시간 분석 | IoT 데이터를 ElastiCache에 저장해 실시간 시각화 및 처리 |

**이럴 때 ElastiCache를 선택하세요:**
- ✅ 상황 1: 빈번한 읽기 요청이 발생하는 서비스 (예: 인기 뉴스 사이트)  
- ✅ 상황 2: 높은 확장성을 요구하는 백엔드 시스템 (예: 온라인 쇼핑몰)  
- ✅ 상황 3: 저지연 응답이 필수적인 서비스 (예: 온라인 게임)  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ 상황 → 대안 서비스 추천 (이유 포함): 데이터 저장이 필요할 때 → **Amazon DynamoDB** (NoSQL 기반 일관성 보장)  
- ❌ 상황 → 대안 서비스 추천 (이유 포함): 대규모 분석이 필요할 때 → **Amazon Redshift** (데이터 웨어하우스 기능)  
- ❌ 상황 → 대안 서비스 추천 (이유 포함): 트랜잭션 로그가 필요할 때 → **Amazon QLDB** (불변성 보장)  

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **Amazon EC2** | 애플리케이션 서버와 캐싱 서버 분리 | 애플리케이션 → ElastiCache → DB |
| **Amazon Redshift** | 분석 데이터와 실시간 데이터 분리 | ElastiCache → Redshift → BI Tool |
| **Amazon CloudFront** | 캐싱된 콘텐츠를 글로벌 CDN으로 배포 | User → CloudFront → ElastiCache → Origin |

**자주 사용되는 아키텍처 패턴:**
```
User → CloudFront → ElastiCache → EC2 → RDS
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **Redis 클러스터** | $0.25~$2.00/시간 (기본 인스턴스) | 월 750시간 무료 |
| **Memcached 클러스터** | $0.15~$1.00/시간 (기본 인스턴스) | 월 750시간 무료 |
| **Redis 엔터프라이즈** | $1.00~$10.00/시간 (확장형) | 12개월 무료 (최대 300시간) |

**비용 최적화 팁:**
1. 💡 팁 1: **프리티어 활용** - 750시간 무료 사용량을 초과하면 요금 발생  
2. 💡 팁 2: **사용량 모니터링** - CloudWatch로 사용량 추적 후 스케일링 조정  
3. 💡 팁 3: **Redis 엔터프라이즈 선택** - 고성능 요구 시 저비용 대비 높은 확장성 제공  

> **⚠️ 비용 주의:** **Redis 엔터프라이즈**는 기본 인스턴스 대비 4~5배 비용이 더 들 수 있으니, 확장 필요 시만 선택해야 합니다.

## 📚 핵심 개념

### 개념 1: ElastiCache Redis vs. Memcached의 차이점  
ElastiCache는 Redis와 Memcached 두 가지 인메모리 데이터베이스를 지원합니다. **Redis**는 키-값 저장 외에도 리스트, 세트, 해시 등 다양한 데이터 구조를 지원하며, 데이터를 디스크에 백업할 수 있는 **디스크 기반의 지속성**(Persistence) 기능을 제공합니다. 반면 **Memcached**는 단순한 키-값 저장만 지원하며, 데이터는 메모리에만 저장되어 **수명이 짧고 복구 불가능**합니다. Redis는 복잡한 캐싱 로직과 데이터 분석에 적합하며, Memcached는 고속 조회가 필요한 단순한 캐싱 작업에 최적화되어 있습니다.  

#### 왜 중요한가?  
- **Redis의 지속성**은 시스템 장애 시 데이터 손실을 방지하며, 실시간 데이터 분석에 유용합니다.  
- **Memcached의 성능**은 단순한 캐싱 작업에서 최대한 빠른 응답을 제공합니다.  

#### 세부 요소  
| 요소 | 설명 | 예시 |  
|-----|-----|-----|  
| **데이터 구조** | Redis: 리스트, 세트, 해시 등 복잡한 구조 지원 | Redis를 사용해 사용자 세션 데이터를 해시 구조로 저장 |  
| **지속성** | Redis는 디스크에 데이터 백업 가능 | Redis의 `RDB` 및 `AOF` 방식으로 데이터 백업 |  
| **성능** | Memcached는 메모리 기반으로 초고속 응답 | Memcached를 사용해 고성능 캐싱 서버 구축 |  

> **💡 Tip:** Redis는 복잡한 캐싱 로직이 필요한 애플리케이션에, Memcached는 단순한 캐싱 작업에 적합합니다.  

---

### 개념 2: Redshift의 데이터 웨어하우스 아키텍처  
Redshift는 **컬럼 기반 저장**(Columnar Storage)과 **분산 컴퓨팅**(Distributed Computing)을 기반으로 설계된 클라우드 데이터 웨어하우스입니다. 데이터는 **파티셔닝**(Partitioning)과 **스레시잉**(Sorting)을 통해 분산되어 저장되며, **MPP 아키텍처**(Massively Parallel Processing)를 통해 병렬 처리를 지원합니다. 이는 대규모 데이터 집약적인 분석 작업에 최적화되어 있습니다.  

#### 작동 원리  
1. **데이터 입력**: 데이터는 Redshift 클러스터에 입력되며, 파티셔닝과 스티칭을 통해 분산 저장됩니다.  
2. **쿼리 처리**: 쿼리는 각 노드에서 병렬로 실행되며, 결과는 조인 및 집계를 통해 통합됩니다.  
3. **쿼리 최적화**: Redshift는 **query planner**를 통해 최적화된 실행 계획을 생성하여 성능을 향상시킵니다.  

> **💡 Tip:** Redshift는 대규모 분석 작업에 적합하지만, 실시간 트랜잭션 처리에는 적합하지 않습니다.  

---

### 개념 3: Neptune의 그래프 데이터베이스 및 SPARQL 쿼리  
Neptune은 **그래프 데이터베이스**(Graph Database)로, 데이터를 **노드**(Node), **엣지**(Edge), **프로퍼티**(Property)로 구성됩니다. 이는 **사회 네트워크**, **지식 그래프**, **위험 감지** 등 복잡한 관계를 표현하기에 적합합니다. Neptune은 **SPARQL**이라는 표준 쿼리 언어를 지원하여, 그래프 데이터를 효율적으로 검색하고 분석할 수 있습니다.  

#### 주요 특징  
1. **그래프 트라버설**: SPARQL을 통해 노드 간의 관계를 탐색할 수 있습니다.  
2. **RDF 지원**: Resource Description Framework(RDF) 기반으로 데이터를 저장 및 검색합니다.  
3. **AWS 통합**: S3, Lambda, DynamoDB 등과 연동하여 복잡한 애플리케이션을 구축할 수 있습니다.  

> **💡 Tip:** Neptune은 사회적 네트워크 분석이나 사기 탐지에 활용할 수 있습니다.  

---

### 개념 4: DocumentDB의 문서 모델과 스케일링  
DocumentDB는 **NoSQL 데이터베이스**로, JSON 형식의 문서를 저장하고 관리합니다. **유연한 스키마**(Schema-less)를 지원하여, 데이터 구조 변경 없이 신규 필드 추가가 가능합니다. 또한, **자동 스케일링**(Auto Scaling)을 통해 트래픽 증가 시 자동으로 용량을 확장할 수 있습니다.  

#### 주요 특징  
1. **유연한 스키마**: JSON 문서 형식으로 데이터를 저장할 수 있어, 구조 변경이 필요 없는 애플리케이션에 적합합니다.  
2. **높은 가용성**: 복제 클러스터를 통해 데이터 무중단 처리와 고가용성을 제공합니다.  
3. **MongoDB 호환**: MongoDB의 API와 드라이버를 사용할 수 있어, 기존 애플리케이션에 쉽게 통합됩니다.  

> **💡 Tip:** 문서 기반 데이터 저장이 필요한 애플리케이션(예: 콘텐츠 관리 시스템)에 적합합니다.  

---

### 개념 5: Amazon Keyspaces의 서버리스 아키텍처  
Amazon Keyspaces는 **서버리스**(Serverless) 방식의 NoSQL 데이터베이스로, 사용자가 서버 관리를 하지 않아도 데이터베이스를 운영할 수 있습니다. **자동 스케일링**과 **서버리스 프런트엔드**를 통해 **가용성**, **성능**, **비용**을 최적화합니다.  

#### 주요 특징  
1. **서버리스**: 사용자는 클러스터 관리, 업데이트, 백업 등 서버 관리 작업을 하지 않아도 됩니다.  
2. **자동 스케일링**: 트래픽 증가 시 자동으로 용량을 확장하고, 감소 시 자동으로 축소합니다.  
3. **AWS 서비스 통합**: Lambda, S3, DynamoDB 등과 연동하여 복잡한 애플리케이션을 구축할 수 있습니다.  

> **💡 Tip:** 높은 확장성과 저비용이 필요한 애플리케이션(예: IoT 데이터 수집)에 적합합니다.  

---

### 개념 6: QLDB의 불변성 및 트랜잭션 로그  
QLDB(Quantum Ledger Database)는 **불변성**(Immutability)과 **트랜잭션 로그**(Transaction Log) 기능을 통해 **보안**, **투명성**, **감사 트레이스**를 제공합니다. 모든 트랜잭션은 **암호화된 블록**(Block) 형태로 저장되며, **메타데이터**(Metadata)와 함께 **트랜잭션 로그**를 통해 변경 내역을 추적할 수 있습니다.  

#### 주요 특징  
1. **불변성**: 데이터는 생성 후 수정 또는 삭제될 수 없습니다.  
2. **트랜잭션 로그**: 모든 트랜잭션을 로그로 저장하여 감사 및 분석에 활용할 수 있습니다.  
3. **AWS 서비스 통합**: Lambda, S3, DynamoDB 등과 연동하여 복잡한 애플리케이션을 구축할 수 있습니다.  

> **💡 Tip:** 금융 거래, 의료 기록 등 **데이터 무결성**이 중요한 분야에서 활용됩니다.  

---

### 개념 7: Timestream의 시간 시리즈 데이터 처리  
Timestream은 **시간 시리즈 데이터**(Time Series Data)를 처리하는 **서버리스 데이터 웨어하우스**로, **자동 스케일링**, **다중 시리즈 처리**, **지속적 쿼리**(Continuous Query) 기능을 제공합니다. 이는 **IoT**, **모니터링**, **로그 분석** 등 시간 기반 데이터 처리에 최적화되어 있습니다.  

#### 주요 특징  
1. **시간 시리즈 최적화**: 시간 기반 데이터를 효율적으로 저장하고 분석할 수 있습니다.  
2. **자동 스케일링**: 트래픽 증가 시 자동으로 용량을 확장하고, 감소 시 자동으로 축소합니다.  
3. **지속적 쿼리**: 실시간으로 데이터를 분석하여 시각화나 알림을 제공할 수 있습니다.  

> **💡 Tip:** IoT 센서 데이터 수집 및 분석에 적합합니다.

## 🖥️ AWS 콘솔에서 ElastiCache 사용하기

### Step 1: ElastiCache 서비스 접속  
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
   - AWS 계정이 활성화되어 있고, IAM 권한이 부여된 상태여야 합니다.  
2. 상단 검색창에서 "ElastiCache"를 입력하고, 검색 결과에서 "ElastiCache"를 클릭합니다  
   - **AWS 콘솔 메뉴 트리**에서 "ElastiCache"를 찾을 수 없습니다면, "All Services"를 클릭하여 전체 서비스 목록에서 검색하세요.  

> **📸 화면 확인:** ElastiCache 대시보드가 표시되면 정상입니다.  
> 대시보드에는 생성된 캐시 클러스터 목록, 서비스 상태, 메트릭 정보가 표시됩니다.  

---

### Step 2: [주요 작업 1 - 리소스 생성]  
**목표:** ElastiCache 클러스터 생성  
1. **"Create Cache Cluster" 버튼 클릭**  
   - "Create" 탭에서 "Create Cache Cluster"를 선택합니다.  
   - **엔진 선택**: Redis 또는 Memcached 중 하나를 선택합니다.  
     - *Redis*: 고급 데이터 구조 지원, 실시간 분석에 적합  
     - *Memcached*: 단순 키-값 저장에 최적화됨  
2. **기본 설정 입력**  
   - **Cluster Name**: 클러스터 이름 입력 (예: `MyRedisCluster`)  
   - **Node Type**: `cache.t2.micro` (프리티어 기준) 또는 `cache.m5.large` (실무 권장)  
   - **Number of Nodes**: 1~10개 선택 (단일 노드 시 클러스터 내 고가용성 비활성화)  
   - **VPC/Subnet**: 기본 VPC와 Subnet 선택 (필요 시 사설 IP 설정)  
3. **보안 그룹 설정**  
   - **Security Group**: 생성할 클러스터에 접근할 수 있는 IP 범위 및 포트 설정  
   - **Port**: Redis 기본 포트는 `6379`, Memcached는 `11211`  

> **📸 화면 확인:** "Create Cache Cluster" 창에서 포트, 보안 그룹, 노드 수 설정이 완료되었는지 확인하세요.  
> **💡 Tip:** 프리티어는 750시간(30일) 동안 `cache.t2.micro`를 무료로 제공합니다.  

---

### Step 3: [주요 작업 2 - 설정/구성]  
**목표:** 클러스터 구성 및 모니터링 설정  
1. **모니터링 설정**  
   - **CloudWatch Metrics**: CPU 사용량, 메모리 사용량 등 실시간 모니터링 활성화  
   - **Log Groups**: Redis의 `slowlog` 또는 Memcached의 `debug` 로그 수집 설정  
2. **고가용성 구성**  
   - **Multi-AZ Deployment**: "Yes"로 설정하여 장애 시 자동 failover 활성화  
   - **Replication Groups**: Redis Cluster로 구성하여 데이터 동기화 및 확장성 확보  
3. **데이터 백업 및 복원**  
   - **Snapshot Schedule**: 주간 백업 정책 설정 (예: 매일 0시에 백업)  
   - **Point-in-Time Recovery**: 특정 시점의 데이터 복원 기능 활성화  

> **⚠️ 주의:** 보안 그룹 규칙을 잘못 설정하면 외부 공격에 취약해질 수 있습니다.  
> **AWS 콘솔에서 생성된 클러스터의 보안 그룹 설정을 반드시 확인하세요.**  

---

### Step 4: 설정 확인 및 테스트  
**목표:** 클러스터 상태 확인 및 정상 동작 검증  
1. **생성된 리소스 확인 방법**  
   - "Cache Clusters" 탭에서 생성한 클러스터 이름을 클릭합니다.  
   - **Status**: `Available` 상태일 경우 정상 작동 중입니다.  
2. **상태 확인 방법**  
   - **CloudWatch Metrics**: CPU, 메모리, 연결 수 등을 실시간으로 모니터링  
   - **Logs**: "Logs" 탭에서 Redis/Memcached 로그를 확인합니다.  
3. **정상 동작 테스트 방법**  
   - **Redis CLI 테스트**:  
     ```bash
     redis-cli -h <endpoint> -p 6379
     127.0.0.1:6379> SET test_key "test_value"
     127.0.0.1:6379> GET test_key
     "test_value"
     ```  
   - **Memcached CLI 테스트**:  
     ```bash
     memcached-tool <endpoint>:11211 stats
     ```  

> **📸 화면 확인:** 클러스터 상세 정보 화면에서 "Status"가 `Available`이고, "Logs" 탭에서 로그가 정상적으로 수집되는지 확인하세요.  
> **💡 Tip:** 테스트 후 클러스터를 삭제하면 비용이 발생하지 않으므로, 실습 완료 후 "Delete" 버튼을 클릭하세요.

## ⌨️ AWS CLI로 ElastiCache 사용하기

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
AWS CLI를 사용하기 전에 버전을 확인하고, 현재 사용 중인 자격 증명과 리전을 확인해야 합니다.  
- `aws --version`은 CLI 버전을 확인합니다.  
- `aws sts get-caller-identity`는 현재 사용자 계정 정보를 확인합니다.  
- `aws configure get region`은 현재 설정된 리전을 확인합니다.  
**⚠️ 주의:** AWS CLI는 기본적으로 `us-east-1` 리전을 사용합니다. 다른 리전에서 작업할 경우 `aws configure set region`으로 설정해야 합니다.

---

### 예제 1: ElastiCache 리소스 조회
```bash
# ElastiCache 캐시 클러스터 목록 조회
aws elasticache list-cache-clusters --query "[].CacheClusterId" --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| `--query` | 결과 필터링 | `"[].CacheClusterId"` (캐시 클러스터 ID만 출력) |
| `--output` | 출력 형식 | `json`, `table`, `text` (테이블 형식으로 보기 편리) |

**예상 출력:**
```
| CacheClusterId |
+----------------+
| example-cluster |
| another-cluster |
```

**설명:**  
`list-cache-clusters` 명령어는 현재 AWS 계정에 속한 모든 캐시 클러스터를 목록화합니다. `--query` 옵션을 사용해 특정 필드만 출력할 수 있으며, `--output table`은 테이블 형식으로 보기 쉽게 합니다.

---

### 예제 2: ElastiCache 리소스 생성
```bash
# ElastiCache 캐시 클러스터 생성
aws elasticache create-cache-cluster \
    --cache-cluster-name "example-cluster" \
    --engine "redis" \
    --cache-node-type "cache.r5.large" \
    --num-cache-nodes 1
```

**필수 옵션:**
- `--cache-cluster-name`: 캐시 클러스터 이름 (중복 불가)
- `--engine`: 사용할 캐시 엔진 (redis/memcached)
- `--cache-node-type`: 노드 타입 (예: `cache.r5.large`)
- `--num-cache-nodes`: 노드 수 (최소 1)

**예상 출력:**
```json
{
    "CacheCluster": {
        "CacheClusterId": "example-cluster",
        "Status": "creating"
    }
}
```

**설명:**  
`create-cache-cluster` 명령어는 캐시 클러스터를 생성합니다. Redis 또는 Memcached 엔진을 선택할 수 있으며, 노드 타입과 수를 설정해야 합니다. 생성 후 `Status`가 `creating`으로 표시됩니다. 생성 완료 후 `describe-cache-clusters` 명령어로 상태를 확인할 수 있습니다.

---

### 예제 3: ElastiCache 리소스 수정
```bash
# ElastiCache 캐시 클러스터 수정
aws elasticache modify-cache-cluster \
    --cache-cluster-id "example-cluster" \
    --num-cache-nodes 2
```

**설명:**  
`modify-cache-cluster` 명령어는 캐시 클러스터의 노드 수를 변경할 수 있습니다.  
- `--num-cache-nodes` 옵션으로 노드 수를 조정합니다.  
- 수정 중에는 `Status`가 `modifying`으로 변경됩니다.  
**💡 Tip:** 수정 과정은 시간이 소요되며, 클러스터가 중단될 수 있으므로 사전에 백업을 권장합니다.

---

### 예제 4: ElastiCache 리소스 삭제
```bash
# ElastiCache 캐시 클러스터 삭제
aws elasticache delete-cache-cluster --cache-cluster-id "example-cluster" --finalizing

# 삭제 확인
aws elasticache describe-cache-clusters --cache-cluster-id "example-cluster"
```

**설명:**  
`delete-cache-cluster` 명령어는 캐시 클러스터를 삭제합니다.  
- `--finalizing` 옵션은 삭제를 즉시 실행합니다 (기본값은 `false`로, 삭제 후 상태 변경만 수행).  
- 삭제 후 `describe-cache-clusters` 명령어로 상태를 확인할 수 있습니다.  
**⚠️ 주의:** 삭제는 되돌릴 수 없으므로, 반드시 `--finalizing` 옵션을 사용해 신중하게 실행해야 합니다.

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws elasticache list-cache-clusters
aws elasticache describe-cache-clusters --cache-cluster-id "id"

# 생성
aws elasticache create-cache-cluster --cache-cluster-name "name" --engine "redis" --cache-node-type "type" --num-cache-nodes 1

# 수정
aws elasticache modify-cache-cluster --cache-cluster-id "id" --num-cache-nodes 2

# 삭제
aws elasticache delete-cache-cluster --cache-cluster-id "id" --finalizing
```

**💡 Tip:**  
- CLI 명령어는 `aws elasticache [command]` 형식으로 입력합니다.  
- `--query`와 `--output` 옵션을 사용해 결과를 필터링하고 보기 쉽게 합니다.  
- 캐시 클러스터 생성 시 `--engine` 옵션으로 Redis 또는 Memcached를 선택해야 합니다.  
- 생성/수정/삭제 시 `--cache-cluster-id`를 정확히 입력해야 합니다.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 ElastiCache 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **Redis vs Memcached 차이점**:  
   - 설명: ElastiCache의 두 주요 캐시 엔진(Redis, Memcached)은 데이터 저장 방식과 성능 특성이 완전히 다릅니다. Redis는 키-값 저장 외에 리스트, 세트, 해시 등의 복잡한 데이터 구조를 지원하며, Memcached는 단순한 키-값 저장만 가능합니다. 이 차이점은 시험에서 반드시 구분해야 하는 핵심 개념입니다.  
   - 키워드: `Redis`, `Memcached`, `데이터 구조`, `성능 차이`

2. **ElastiCache의 사용 사례**:  
   - 설명: 캐시를 사용하는 주요 시나리오는 데이터베이스 부하 감소, 응답 속도 향상, 세션 저장 등입니다. 시험에서는 "사용 목적"과 "적합한 시나리오"를 묻는 문제가 자주 등장합니다.  
   - 키워드: `세션 저장`, `데이터베이스 캐싱`, `응답 속도`

3. **ElastiCache 아키텍처**:  
   - 설명: ElastiCache는 클러스터 형식으로 배포되며, 인메모리 데이터 저장소로 작동합니다. 클러스터 구성, 노드 확장, 데이터 분산 방식은 시험에서 자주 다루는 주제입니다.  
   - 키워드: `클러스터`, `인메모리`, `노드 확장`

4. **CLI 명령어 활용**:  
   - 설명: `aws elasticache create-cache-cluster`, `describe-cache-clusters` 등 CLI 명령어는 실무 및 시험에서 필수적입니다. 클러스터 생성, 모니터링, 템플릿 관리 등에 대한 이해가 필요합니다.  
   - 키워드: `CLI`, `템플릿`, `모니터링`

5. **비용 및 프리티어 활용**:  
   - 설명: ElastiCache의 비용은 데이터 저장량, 클러스터 크기, 사용 기간에 따라 달라집니다. 프리티어는 7일간 10GB 저장 용량을 제공하므로, 작은 규모의 프로토타입 개발에 적합합니다.  
   - 키워드: `비용 구조`, `프리티어`, `10GB 제한`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | Redis와 Memcached의 차이를 혼동해 Redis의 복잡한 데이터 구조를 Memcached로 적용하는 실수 | Redis는 리스트/세트 지원, Memcached는 단순 키-값 저장 |
| 함정 2 | ElastiCache의 "인메모리" 특성을 무조건 성능 최적화로 오인 | 인메모리가 성능 향상의 핵심이지만, 데이터 손실 위험 존재 |
| 함정 3 | ElastiCache의 클러스터 크기와 비용을 비례 관계로 오해 | 클러스터 크기 증가 시 비용 상승, 하지만 자동 스케일링 기능 제공 |

#### 🔄 ElastiCache vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | ElastiCache | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | 인메모리 캐싱, 빠른 응답 속도 | DynamoDB (NoSQL), RDS (관계형 DB) | 데이터 접근 빈도가 높고, 읽기 위주인 데이터 |
| 확장성 | 클러스터 기반 수평 확장 | DynamoDB의 자동 스케일링 | 고사양 캐싱 시, 클러스터 구성 필요 |
| 비용 | 데이터 저장량에 따라 변동 | DynamoDB는 요청 수 기반 요금 | 캐시 데이터 저장량이 예측 가능한 경우 |
| 지연시간 | 서버로의 데이터 전송 없이 접근 | RDS는 네트워크 지연 발생 | 읽기 성능이 가장 중요한 시나리오 |

#### 📝 시험 대비 체크리스트
- [ ] ElastiCache의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  *예: "고성능 캐싱을 위한 인메모리 데이터 저장소"*  
- [ ] ElastiCache를 선택해야 하는 시나리오를 알고 있는가?  
  *예: "데이터베이스 부하 감소, 세션 저장, 빈도 높은 읽기 요청"*  
- [ ] ElastiCache의 제한사항/한계를 알고 있는가?  
  *예: "데이터 손실 위험, 클러스터 크기 제한, 비용 상승 가능성"*  
- [ ] ElastiCache와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  *예: "Redis vs Memcached: 데이터 구조 지원 여부"*  
- [ ] ElastiCache의 비용 구조를 이해하고 있는가?  
  *예: "데이터 저장량, 클러스터 크기, 사용 기간에 따라 변동"*  

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 ElastiCache를 떠올리세요:  
> - **Redis/Memcached**  
> - **인메모리 캐싱**  
> - **클러스터 구성**  
> - **데이터베이스 부하 감소**  
> - **프리티어 활용**

---

| [⬅️ 이전 Day](../day2/README.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 3](../README.md) | [Redshift ➡️](./Redshift.md) |

---
