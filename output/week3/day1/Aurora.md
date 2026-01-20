---

| [⬅️ RDS](./RDS.md) | [📑 Day 1 목차](./README.md) | [🏠 Week 3](../README.md) | [다음 Day ➡️](../day2/README.md) |

---

# Aurora 완전 정복

> **한 줄 정의:** Aurora는 고가용성과 확장성, 자동 백업 및 글로벌 데이터 동기화를 위한 AWS의 관리형 관계형 데이터베이스 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- 문제 1: 전통적인 RDS 서비스는 단일 AZ 배포로 인해 장애 시 데이터 손실 및 서비스 중단 위험이 존재했습니다. 수동 복제본 관리로 인해 복잡도가 높았고, 연결 풀링 기능이 부족해 고사양 트래픽 시 성능 저하가 발생했습니다.
- 문제 2: 읽기 전용 복제본 생성 시 데이터 동기화 지연이 발생하거나, 복제본 수를 늘릴 때 수동 설정으로 관리 부담이 컸습니다. 또한, 글로벌 데이터 동기화 시 지역 간 지연 시간이 문제가 되었습니다.
- 문제 3: 클러스터 관리 시 자동 백업 및 복원 기능이 부족해 데이터 손실 위험이 있으며, 서버리스 환경에서 자동 스케일링이 지원되지 않아 리소스 낭비 또는 성능 부족이 발생했습니다.

**Aurora로 해결:**
- 해결 1: **RDS 다중 AZ 배포**로 장애 시 자동 failover가 가능해 서비스 중단을 방지하고, **RDS Proxy**의 연결 풀링 기능으로 연결 지연을 최소화해 고사양 시 성능을 유지합니다.
- 해결 2: **읽기 전용 복제본**을 간편하게 생성하고, **Aurora 클러스터**의 자동 백업 및 복제본 동기화 기능으로 데이터 일관성을 보장합니다. 복제본 수를 유연하게 조절해 읽기 확장이 가능합니다.
- 해결 3: **Aurora Serverless**로 자동 스케일링을 지원해 리소스 낭비를 방지하고, **Aurora Global Database**를 통해 글로벌 데이터 동기화를 실현해 지연 시간을 최소화합니다.

### 비유로 이해하기
Aurora는 스마트 시티의 데이터베이스 시스템을 상징합니다. 각 지역의 데이터는 실시간으로 중앙 서버에 동기화되며, 장애 시 자동으로 다른 지역 서버로 전환됩니다. 시민들이 다양한 장소에서 데이터를 요청해도, 빠른 연결 풀링과 복제본을 통해 효율적으로 처리됩니다. 이처럼 Aurora는 모든 지역에서 신속하고 안정적으로 데이터를 제공하는 데 최적화되어 있습니다.

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | **고가용성 요구** 시 | 금융 서비스에서 장애 시 99.99% 가용성을 보장하는 시스템 구축 |
| 시나리오 2 | **읽기 확장 필요** 시 | 온라인 쇼핑몰의 주문 조회 요청을 복제본으로 분산 처리 |
| 시나리오 3 | **글로벌 데이터 동기화** 시 | 해외 매장의 매출 데이터를 실시간으로 본사 시스템에 반영 |

**이럴 때 Aurora를 선택하세요:**
- ✅ 상황 1: 단일 AZ에서 장애 발생 시 서비스 중단을 최소화해야 할 경우  
- ✅ 상황 2: 읽기 트래픽이 높아 읽기 전용 복제본을 확장해야 할 경우  
- ✅ 상황 3: 글로벌 사용자에게 실시간 데이터 동기화를 제공해야 할 경우  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ 상황: 단순한 데이터 저장이 필요한 경우 → **Amazon S3** (스토리지 중심)  
- ❌ 상황: NoSQL 데이터베이스가 필요한 경우 → **Amazon DynamoDB** (다양한 데이터 모델 지원)  
- ❌ 상황: 저비용으로 단일 서버 운영이 가능한 경우 → **Amazon EC2** (자체 서버 관리 필요)

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **RDS Proxy** | 연결 풀링으로 연결 지연 최소화 | Aurora → RDS Proxy → 읽기 전용 복제본 |
| **CloudFront** | 읽기 트래픽 분산 및 캐싱 | 사용자 → CloudFront → Aurora 클러스터 |
| **S3** | 백업 및 아카이브 저장 | Aurora → S3 (백업 자동 저장) |

**자주 사용되는 아키텍처 패턴:**
```
User → CloudFront → Aurora (읽기 전용 복제본) → S3 (백업)
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **Aurora 클러스터** | $0.30–$0.80 / vCPU-시간 | 12개월 무료 (1 vCPU, 20GB) |
| **Aurora Serverless** | $0.20–$0.50 / vCPU-시간 | 월 750시간 무료 (1 vCPU, 2GB) |
| **Aurora Global Database** | $0.25–$0.60 / 복제본-시간 | 12개월 무료 (1 복제본, 10GB) |

**비용 최적화 팁:**
1. 💡 팁 1: **Aurora Serverless**를 사용해 자동 스케일링으로 리소스 낭비 방지  
2. 💡 팁 2: **읽기 전용 복제본**을 활용해 읽기 트래픽 분산 및 코스팅 절감  
3. 💡 팁 3: **Aurora Global Database**의 지역 복제본을 사용해 글로벌 사용자 대응  

> **⚠️ 비용 주의:** 고사양 트래픽 시 **RDS Proxy** 연결 풀링 미설정 시 연결 비용이 급증할 수 있으며, **Aurora Global Database**의 복제본 수를 과도하게 늘릴 경우 데이터 동기화 비용이 증가합니다. 프리티어 사용 시 **12개월 무료** 기간 내에 반드시 실제 환경에 적용해야 합니다.

## 📚 핵심 개념

### 개념 1: RDS 다중 AZ 배포의 고가용성 및 재해 복구 메커니즘
Aurora는 RDS 다중 AZ 배포를 기반으로 하여 고가용성과 재해 복구를 보장합니다. 이 구조는 단일 AZ에서의 장애가 발생할 경우, 자동으로 다른 AZ로 failover하여 서비스 중단을 방지합니다. Aurora는 AWS의 AWS Multi-AZ RDS 기능을 기반으로 하되, 데이터 동기화를 위해 Aurora Replicas와 결합해 실시간으로 데이터를 복제하여 장애 시 즉시 복구를 수행합니다. 이는 단순한 RDS 다중 AZ보다 더 빠른 failover 처리와 데이터 일관성을 제공합니다. 또한, Aurora는 AWS의 복제 기능을 기반으로 하되, MySQL 및 PostgreSQL 호환성을 유지하면서도 고가용성과 확장성을 동시에 지원합니다.

#### 왜 중요한가?
- **고가용성 보장**: 단일 AZ 장애 시 자동 failover로 서비스 중단 방지  
- **데이터 보호**: 실시간 복제로 데이터 손실 방지 및 복구 속도 향상  

#### 세부 요소
| 요소 | 설명 | 예시 |
|-----|------|-----|
| 고가용성 구조 | AWS Multi-AZ 기반으로 AZ 간 장애 시 자동 failover | EC2 인스턴스 장애 시 Aurora 클러스터가 다른 AZ로 이동 |
| 데이터 복제 | 실시간으로 AZ 간 데이터 동기화를 수행 | 데이터베이스 변경 사항이 즉시 복제본에 반영 |
| 재해 복구 | 복제본을 통해 데이터 손실 방지 및 복구 | 장애 발생 시 복제본에서 데이터를 복원하여 서비스 재개 |

> **💡 Tip:** 고가용성 요구가 높은 핵심 시스템에는 RDS 다중 AZ를 사용하여 장애 대응력을 높이세요.

---

### 개념 2: 읽기 전용 복제본의 읽기 확장 및 데이터 동기화 방식
Aurora는 읽기 전용 복제본을 통해 읽기 작업을 확장할 수 있습니다. 이 복제본은 마스터 인스턴스에서 실시간으로 데이터를 동기화하며, 읽기 작업을 분산해 마스터의 부하를 줄입니다. Aurora는 복제본이 변경 사항을 즉시 반영하도록 설계되어, 읽기 작업 시 데이터 일관성을 유지합니다. 또한, 복제본은 쿼리 트래픽을 분산해 애플리케이션 성능을 향상시키고, 복제본을 통해 분석 작업이나 보고서 생성을 가능하게 합니다. 이는 단순한 읽기 확장을 넘어, 데이터 분산을 통한 성능 최적화를 제공합니다.

#### 작동 원리
1. **복제본 생성**: 마스터 인스턴스에서 읽기 전용 복제본을 생성  
2. **데이터 동기화**: 마스터의 변경 사항이 실시간으로 복제본에 반영  
3. **읽기 트래픽 분산**: 읽기 작업을 복제본에 전달해 마스터 부하 감소  

> **💡 Tip:** 분석 작업이나 보고서 생성 시 읽기 전용 복제본을 활용해 성능 향상을 도모하세요.

---

### 개념 3: RDS Proxy의 연결 풀링과 연결 관리 기능
RDS Proxy는 데이터베이스 연결을 관리하여 연결 풀링을 통해 성능을 향상시키고, 연결 수를 줄여 비용을 절감합니다. RDS Proxy는 애플리케이션에서 데이터베이스에 연결하는 요청을 중간에 받아, 연결 풀을 관리해 연결을 재사용합니다. 이는 연결 수 제한을 회피하고, 연결 지연을 줄여 응답 속도를 향상시킵니다. 또한, RDS Proxy는 장애 시 자동으로 연결을 다른 인스턴스로 전달해 고가용성을 제공합니다. 이 기능은 높은 동시 요청 시 성능 최적화와 비용 절감에 효과적입니다.

#### 주요 특징
1. **연결 풀링**: 연결을 재사용해 연결 수를 줄이고 성능 향상  
2. **고가용성**: 장애 시 연결을 다른 인스턴스로 자동 전달  
3. **비용 절감**: 연결 관리로 데이터베이스 인스턴스 수를 줄여 비용 감소  

> **💡 Tip:** 고사양 애플리케이션에서는 RDS Proxy를 사용해 연결 풀링을 활용해 비용과 성능을 균형 있게 관리하세요.

## 🖥️ AWS 콘솔에서 Aurora 사용하기

### Step 1: Aurora 서비스 접속  
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
   - 로그인 후 `Services` 메뉴에서 `RDS`를 클릭합니다.  
2. 상단 검색창에서 "Aurora"를 입력하고, `Aurora` 서비스를 선택합니다.  
3. `Aurora` 대시보드에서 `Databases` 탭을 클릭해 데이터베이스 목록을 확인합니다.  

> **📸 화면 확인:** `Aurora` 대시보드가 표시되고 `Databases` 탭이 활성화되면 정상입니다.  

---

### Step 2: [주요 작업 1 - Multi-AZ RDS 인스턴스 생성]  
1. **RDS 인스턴스 생성**  
   - `Databases` 탭에서 `Create database` 버튼을 클릭합니다.  
   - `Create DB instance` 옵션을 선택하고, `DB instance identifier`를 입력합니다 (예: `aurora-multi-az`).  
   - `Master username`과 `Password`를 입력한 후, `Multi-AZ deployment` 옵션을 체크합니다.  
   - `Subnet group`을 선택하고, `Security groups`를 설정합니다.  

2. **네트워크 설정**  
   - `VPC`를 선택하고, `Publicly accessible` 옵션을 `No`로 설정합니다.  
   - `Availability Zones`에서 2개 이상의 존을 선택해 Multi-AZ 구성합니다.  

3. **마스터 계정 설정**  
   - `Master username`과 `Password`를 입력하고, `Database name`을 지정합니다.  
   - `Parameter group`과 `Backup retention period`을 설정합니다.  

> **📸 화면 확인:** `Create DB instance` 창에서 `Multi-AZ deployment`가 체크되어 있고, `Subnet group` 및 `Security groups` 설정이 완료된 상태입니다.  

---

### Step 3: [주요 작업 2 - 읽기 전용 복제본 구성]  
1. **복제본 생성**  
   - 생성한 RDS 인스턴스를 클릭해 `Read replicas` 탭을 선택합니다.  
   - `Create read replica` 버튼을 클릭하고, `Source DB instance`를 선택합니다.  
   - `Read replica identifier`를 입력하고, `Subnet group`을 설정합니다.  

2. **복제본 설정**  
   - `Replication role`을 생성하거나 기존 역할을 선택합니다.  
   - `VPC`와 `Security groups`를 동일하게 설정합니다.  
   - `Automated backups` 옵션을 `No`로 설정해 복제본에 백업을 비활성화합니다.  

3. **설정 확인**  
   - `Create` 버튼을 클릭해 작업을 실행합니다.  
   - 생성된 복제본이 `Read replica` 탭에 표시될 때까지 기다립니다.  

> **⚠️ 주의:** 복제본 생성 시 `Replication role`이 필수적이므로, 미리 역할을 생성하거나 기존 역할을 선택해야 합니다.  

---

### Step 4: 설정 확인 및 테스트  
1. **리소스 확인 방법**  
   - `Databases` 탭에서 생성한 RDS 인스턴스와 복제본을 확인합니다.  
   - 각 인스턴스의 상태가 `Available`로 표시되는지 확인합니다.  

2. **상태 확인 방법**  
   - 인스턴스 클릭 후 `Overview` 탭에서 `Status`를 확인합니다.  
   - 복제본의 `Read replica status`가 `Active`로 표시되는지 확인합니다.  

3. **테스트 방법**  
   - 복제본의 `Endpoint`를 사용해 읽기 작업을 수행합니다.  
   - 예: MySQL CLI에서 `SELECT * FROM table_name;` 명령어로 데이터를 조회합니다.  

> **📸 화면 확인:** `Read replicas` 탭에서 복제본이 `Active` 상태이고, `Overview` 탭에서 인스턴스 상태가 `Available`으로 표시됩니다.  

---

### 💡 추가 팁  
- **비용 최적화:** Multi-AZ 인스턴스는 고가이므로, 필요 시 `Aurora Serverless`를 고려합니다.  
- **CLI 사용:** `aws rds create-db-instance` 및 `aws rds create-read-replica` 명령어로 자동화할 수 있습니다.  
- **비용 모니터링:** `Cost Explorer`에서 Multi-AZ 및 복제본의 비용을 추적하세요.

## ⌨️ AWS CLI로 Aurora 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

**필수 사전 조건:**
- AWS CLI가 최신 버전으로 업데이트 되었는지 확인
- IAM 정책에 `rds:DescribeDBClusters`, `rds:CreateDBCluster`, `rds:CreateReadReplica` 권한이 포함되어 있는지 확인
- `aws configure`로 AWS Access Key ID, Secret Access Key, Default Region 설정 완료

---

### 예제 1: Aurora 리소스 조회
```bash
# [Aurora 클러스터 목록 조회]
aws rds describe-db-clusters --query 'DBClusters[*].DBClusterIdentifier' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| --query | 결과 필터링 | 'DBClusters[*].DBClusterIdentifier' |
| --output | 출력 형식 | json, table, text |

**예상 출력:**
```
DBClusterIdentifier
-------------------
my-aurora-cluster
```

---

### 예제 2: Multi-AZ Aurora 클러스터 생성
```bash
# [Multi-AZ Aurora 클러스터 생성]
aws rds create-db-cluster \
    --db-cluster-identifier "my-aurora-cluster" \
    --engine "aurora" \
    --engine-version "5.7.mysql_aurora.2.07.1" \
    --db-subnet-group-name "my-subnet-group" \
    --availability-zones "us-east-1a,us-east-1b" \
    --master-username "admin" \
    --master-user-password "SecureP@ssw0rd!" \
    --port 3306
```

**필수 옵션:**
- `--db-cluster-identifier`: 클러스터 고유 이름
- `--engine`: Aurora MySQL 또는 Aurora PostgreSQL 선택
- `--availability-zones`: Multi-AZ 구성 (최소 2개 이상의 AZ)

**예상 출력:**
```json
{
    "DBCluster": {
        "DBClusterIdentifier": "my-aurora-cluster",
        "Status": "creating"
    }
}
```

---

### 예제 3: 읽기 전용 복제본 생성
```bash
# [읽기 전용 복제본 생성]
aws rds create-db-instance-read Replica \
    --db-instance-identifier "my-read-replica" \
    --db-cluster-identifier "my-aurora-cluster" \
    --publicly-accessible false \
    --db-instance-class "db.t3.micro" \
    --autoMinorVersionUpgrade true
```

**옵션 설명:**
- `--db-cluster-identifier`: 복제본을 생성할 클러스터 ID
- `--db-instance-class`: 복제본 인스턴스 크기 (비용 최적화 추천)
- `--publicly-accessible`: 외부 IP 접근 여부 (보안상 false 권장)

**예상 출력:**
```json
{
    "DBInstance": {
        "DBInstanceIdentifier": "my-read-replica",
        "Status": "creating"
    }
}
```

---

### 예제 4: 리소스 삭제
```bash
# 복제본 삭제
aws rds delete-db-instance --db-instance-identifier "my-read-replica" --skip-final-snapshot

# 클러스터 삭제
aws rds delete-db-cluster --db-cluster-identifier "my-aurora-cluster"
```

> **⚠️ 주의:** 삭제는 되돌릴 수 없습니다. `--skip-final-snapshot` 옵션으로 최종 스냅샷 생성을 생략할 수 있음

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws rds describe-db-clusters
aws rds describe-db-instances

# 생성
aws rds create-db-cluster
aws rds create-db-instance-read Replica

# 수정
aws rds modify-db-cluster
aws rds modify-db-instance

# 삭제
aws rds delete-db-cluster
aws rds delete-db-instance
```

---

### 💡 CLI 사용 팁
1. **비용 최적화:** `--db-instance-class`를 `db.t3.micro`로 설정하여 비용 절감
2. **Multi-AZ 구성:** `--availability-zones`에 최소 2개 이상의 AZ 지정
3. **보안 강화:** `--publicly-accessible false`로 외부 접근 차단
4. **자동 업데이트:** `--autoMinorVersionUpgrade true`로 보안 패치 자동 적용

---

### 📌 주의사항
| 항목 | 내용 |
|------|------|
| **비용 계산** | `aws rds get-paginator`로 리소스 수량 파악 후 비용 예측 |
| **프리티어 제한** | 750시간/월 (16GB 메모리) 제한 - 상용 전환 시 비용 확인 필수 |
| **AZ 지정 방법** | `aws ec2 describe-availability-zones`로 사용 가능한 AZ 확인 |
| **복제본 최대 개수** | 10개까지 생성 가능 (AWS 계정 제한) |

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 Aurora 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **Aurora 클러스터의 마스터-슬레이브 아키텍처**  
   - 설명: Aurora는 마스터 노드와 슬레이브 노드로 구성된 클러스터 형태로, 자동 백업 및 읽기 확장 기능을 제공합니다. 이는 데이터 일관성과 고가용성을 보장하며, 시험에서 자주 비교/분석 문제로 출제됩니다.  
   - 키워드: `마스터-슬레이브`, `자동 백업`, `고가용성`

2. **Aurora Global Database의 글로벌 데이터 동기화**  
   - 설명: 글로벌 데이터베이스는 여러 지역에 복제본을 생성해 지연 시간 최소화와 지역별 가용성 확보를 제공합니다. 시험에서는 복제본 동기화 방식과 리더십 전환 메커니즘을 묻는 경우가 많습니다.  
   - 키워드: `글로벌 복제본`, `지연 시간`, `리더십 전환`

3. **RDS Proxy의 연결 풀링 기능**  
   - 설명: RDS Proxy는 연결 풀링을 통해 데이터베이스 연결 자원을 최적화하고, 연결 지연 시간을 줄이는 데 중점을 둡니다. 시험에서는 연결 관리 및 성능 최적화 문제에 자주 등장합니다.  
   - 키워드: `연결 풀링`, `연결 관리`, `성능 최적화`

4. **Aurora Serverless의 자동 확장 메커니즘**  
   - 설명: Aurora Serverless는 트래픽 변화에 따라 자동으로 컴퓨팅 자원을 확장/축소하며, 비용 효율성을 강조합니다. 시험에서는 서버리스 아키텍처의 장단점을 묻는 경우가 많습니다.  
   - 키워드: `자동 확장`, `비용 효율성`, `트래픽 변동`

5. **읽기 전용 복제본의 데이터 동기화 방식**  
   - 설명: 읽기 전용 복제본은 실시간 또는 지연 동기화 방식을 사용하며, 시험에서는 동기화 메커니즘과 읽기 확장 전략을 비교 분석하는 문제가 자주 출제됩니다.  
   - 키워드: `동기화 방식`, `읽기 확장`, `데이터 일관성`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | Aurora와 RDS의 차이를 혼동해 Aurora의 고가용성 기능을 RDS에 적용한다고 오인 | Aurora는 RDS의 확장 기능을 기반으로 개선된 고가용성 아키텍처를 제공 |
| 함정 2 | Aurora Global Database의 복제본 동기화 방식을 실시간으로 오인 | 글로벌 복제본은 지연 동기화 방식을 사용하며, 지역별 복제본 간 데이터 일관성 유지 |
| 함정 3 | Aurora Serverless의 비용 구조를 오해해 고정 비용을 적용한다고 오인 | Serverless는 요청별 계산 자원 비용으로, IDLE 시 비용이 0 |

#### 🔄 Aurora vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | Aurora | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| **용도** | 고가용성, 글로벌 데이터베이스, 서버리스 아키텍처 | RDS, DynamoDB, MySQL | 높은 확장성과 지연 최소화가 필요한 시나리오 |
| **확장성** | 자동 스일링, 글로벌 복제본, 서버리스 기능 | RDS의 고정 크기, DynamoDB의 스토리지 확장 | 트래픽 변동이 큰 환경 또는 글로벌 접근이 필요한 경우 |
| **비용** | Serverless는 요청 기반, 복제본 기반 비용 | RDS는 고정 비용, EC2 기반 | 예측 가능한 트래픽 또는 비용 최적화가 필요한 경우 |
| **지연시간** | 글로벌 복제본의 지연 최소화, 자동 백업 | RDS의 지역 데이터베이스, DynamoDB의 분산 처리 | 글로벌 사용자 접근 또는 실시간 읽기 확장이 필요한 경우 |

#### 📝 시험 대비 체크리스트
- [ ] Aurora의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  *예: "Aurora는 고가용성과 글로벌 데이터베이스 기능을 제공하는 관계형 데이터베이스 서비스입니다."*
- [ ] Aurora를 선택해야 하는 시나리오를 알고 있는가?  
  *예: "글로벌 사용자 접근, 자동 확장, 지연 최소화가 필요한 애플리케이션"*
- [ ] Aurora의 제한사항/한계를 알고 있는가?  
  *예: "서버리스 모드는 쿼리 복잡도 제한, 글로벌 복제본은 지역 간 데이터 일관성 유지에 한계 있음"*
- [ ] Aurora와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  *예: "RDS는 고정 크기, Aurora는 서버리스 및 글로벌 복제본 기능을 지원"*  
- [ ] Aurora의 비용 구조를 이해하고 있는가?  
  *예: "Serverless는 요청 기반, 복제본은 데이터 크기 기반, 백업은 저장소 기반 비용"*  

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 Aurora를 떠올리세요:  
> - **고가용성**  
> - **글로벌 복제본**  
> - **자동 백업**  
> - **서버리스**  
> - **데이터 일관성**

---

| [⬅️ RDS](./RDS.md) | [📑 Day 1 목차](./README.md) | [🏠 Week 3](../README.md) | [다음 Day ➡️](../day2/README.md) |

---
