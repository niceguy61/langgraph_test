---

| [⬅️ 이전 Day](../../week2/day5/README.md) | [📑 Day 1 목차](./README.md) | [🏠 Week 3](../README.md) | [Aurora ➡️](./Aurora.md) |

---

# RDS 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** RDS는 관리형 데이터베이스 서비스로, RDS 다중 AZ, 읽기 전용 복제본, RDS Proxy, Aurora 클러스터, Aurora Serverless, Aurora Global Database 등 다양한 기능을 통해 고가용성, 확장성, 글로벌 데이터 동기화를 제공합니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 전통적인 데이터베이스 관리 시, 서버 설정, 백업, 백업, 업데이트, 유지보수 등의 작업이 수동으로 이루어져 실수와 downtime이 발생합니다.  
- **문제 2:** 고가용성 및 재해 복구를 위해 별도의 클러스터를 구성해야 하며, 복잡한 네트워크 설정과 연동이 필요했습니다.  
- **문제 3:** 읽기 트래픽 확장을 위해 별도의 서버를 구성해야 하며, 데이터 동기화 로직 개발과 관리가 복잡했습니다.  

**RDS로 해결:**
- **해결 1:** RDS는 자동으로 서버 설정, 백업, 업데이트, 유지보수를 관리해 실수를 줄이고, 24/7 가용성을 제공합니다.  
- **해결 2:** RDS 다중 AZ 배포를 통해 단일 지점 장애를 방지하고, 자동 복제와 장애 터널링 기능으로 재해 복구 시간을 단축합니다.  
- **해결 3:** 읽기 전용 복제본을 통해 읽기 트래픽을 분산하고, AWS의 자동 데이터 동기화 기능으로 복제 지연을 최소화합니다.  

### 비유로 이해하기
RDS는 식당의 주방을 대신해주는 전문 셰프 팀입니다. 고객이 주문을 내면 셰프가 재료를 준비하고 요리해 주는 대신, RDS는 데이터베이스 서버를 관리해 주는 역할을 합니다. 이로 인해 식당 운영자는 주방을 직접 관리할 필요 없이, 맛있고 신속한 서비스를 제공할 수 있습니다.  

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 고가용성과 재해 복구가 필수적인 웹 애플리케이션 | 온라인 쇼핑몰(예: Amazon) |
| 시나리오 2 | 읽기 트래픽이 많은 서비스에서 확장성 확보 | SaaS 플랫폼(예: Salesforce) |
| 시나리오 3 | 글로벌 사용자에게 데이터 일관성을 제공해야 하는 서비스 | 국제 온라인 결제 시스템(예: PayPal) |

**이럴 때 RDS를 선택하세요:**
- ✅ 상황 1: 24/7 가용성이 필요한 시스템  
- ✅ 상황 2: 읽기 트래픽이 급증하는 서비스  
- ✅ 상황 3: 데이터를 여러 지역에 실시간으로 동기화해야 하는 글로벌 서비스  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ 상황: 서버리스 아키텍처를 사용하는 경우 → **Lambda** (RDS와의 통합이 복잡할 수 있음)  
- ❌ 상황: 초저비용 데이터 저장이 필요한 경우 → **DynamoDB** (RDS의 비용 효율성에 비해 비용이 높음)  

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| Lambda | 서버리스 함수로 RDS와 연동하여 비즈니스 로직 처리 | RDS → Lambda (API Gateway) |
| CloudFront | 정적 콘텐츠 캐싱 및 보안 인증을 통한 RDS 접근 제어 | CloudFront → RDS (AWS WAF 연동) |
| Aurora Serverless | 자동 스케일링이 필요한 데이터베이스 트래픽 처리 | Aurora Serverless → RDS (Aurora 클러스터) |

**자주 사용되는 아키텍처 패턴:**
```
User → CloudFront → API Gateway → Lambda → RDS → DynamoDB
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| 인스턴스 사용 | $0.10~$1.50/시간 (가상 머신 기준) | 월 750시간 무료 |
| 스토리지 | $0.025~$0.15/GB/월 | 12개월 무료 (10GB) |
| 데이터 전송 | $0.02~$0.10/GB | 항상 무료 (AWS 내부 전송) |

**비용 최적화 팁:**
1. 💡 팁 1: 읽기 전용 복제본을 사용해 읽기 트래픽을 분산하고, 마스터 DB 부담을 줄이세요.  
2. 💡 팁 2: Aurora Serverless를 사용해 트래픽 급증 시 자동으로 스케일링해 비용을 절감하세요.  
3. 💡 팁 3: CloudWatch를 통해 사용량 모니터링하고, 비용이 많이 드는 쿼리나 캐시를 최적화해 효율성을 높이세요.  

> **⚠️ 비용 주의:** 데이터 전송 비용이 급증할 수 있으므로, VPC 내부 전송을 활용하거나, RDS Proxy를 통해 연결을 최적화해 주의해야 합니다.

## 📚 핵심 개념

### 개념 1: RDS 다중 AZ 배포의 고가용성 및 재해 복구  
RDS 다중 AZ 배포는 단일 AZ에 집중된 DB 인스턴스의 단점을 보완하기 위해 두 개 이상의 가용성 존(AZ)에 DB 인스턴스를 배치하는 방식입니다. 이 구조는 단일 AZ 장애 발생 시 자동으로 다른 AZ로 failover를 수행해 서비스 중단을 방지합니다. 데이터는 주 AZ와 보조 AZ 간 실시간으로 동기화되며, DB 인스턴스가 이중화된 상태에서 고가용성을 유지합니다.  

#### 왜 중요한가?  
- **데이터 안정성 확보**: 단일 AZ 장애 시 자동 복구로 데이터 손실 방지  
- **업무 중단 최소화**: 10초 이내 failover로 서비스 가용성 99.99% 달성  
- **재해 복구 효율성**: AWS가 데이터 복제 및 복구 프로세스 자동 관리  

#### 세부 요소  
| 요소 | 설명 | 예시 |
|-----|-----|-----|
| AZ 구성 | 주 AZ와 보조 AZ가 서로 다른 물리적 데이터 센터에 위치 | 서울과 인천 AZ로 구성 |
| failover 프로세스 | 주 AZ 장애 발생 시 보조 AZ로 자동 전환 | DB 인스턴스 IP 주소 변경 없이 연결 유지 |
| 자동 백업 | 주 AZ의 데이터가 실시간으로 보조 AZ로 복제 | 5분 간격으로 데이터 동기화 |

> **💡 Tip:** 핵심 애플리케이션에는 Multi-AZ 배포를 필수적으로 적용하고, DB 인스턴스의 failover 테스트를 정기적으로 수행하세요.  

---

### 개념 2: 읽기 전용 복제본의 읽기 확장 및 데이터 동기화  
읽기 전용 복제본은 주 DB 인스턴스의 데이터를 복제하여 읽기 작업만 수행하는 DB 인스턴스입니다. 이는 읽기 작업 부담을 분산해 성능 향상과 리소스 효율화를 도모합니다. 데이터는 주 인스턴스에서 실시간으로 복제되며, 주 인스턴스의 변경 사항은 복제본에 즉시 반영됩니다.  

#### 작동 원리  
1. **복제본 생성**: AWS 콘솔에서 주 DB 인스턴스를 기반으로 읽기 전용 복제본 생성  
2. **데이터 복제**: 주 인스턴스의 변경 사항이 복제본으로 실시간 동기화  
3. **읽기 요청 분산**: 읽기 작업은 복제본에 분배되며, 쓰기 작업은 주 인스턴스에만 집중  

> **💡 Tip:** 분석 작업이나 보고서 생성 시 복제본을 활용해 주 인스턴스 부하를 줄이고, 복제본을 여러 개 생성해 더 많은 읽기 요청을 처리하세요.  

---

### 개념 3: RDS Proxy의 연결 풀링과 연결 관리  
RDS Proxy는 DB 인스턴스에 연결하는 클라이언트 요청을 중간에 관리해 연결 풀링을 최적화하는 서비스입니다. 연결 풀링을 통해 반복적인 연결 생성/해제를 줄이고, DB 인스턴스의 부하를 낮춥니다. 또한, 실패한 연결을 자동으로 재연결해 고가용성을 보장합니다.  

#### 주요 특징  
1. **연결 풀링**: 클라이언트 요청을 기반으로 DB 인스턴스에 연결을 재사용해 리소스 효율성 향상  
2. **고가용성**: 연결 실패 시 자동 재연결 및 failover 지원  
3. **보안 강화**: SSL/TLS 암호화를 통해 데이터 전송 중 보안 강화  

> **💡 Tip:** 고 트래픽 애플리케이션에서 RDS Proxy를 사용해 DB 인스턴스의 연결 수를 제한하고, 연결 풀링 설정을 최적화해 성능 향상을 도모하세요.

## 🖥️ AWS 콘솔에서 RDS 사용하기

### Step 1: RDS 서비스 접속
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
   - **AWS 계정 ID와 암호를 입력해 로그인합니다.**
2. 상단 검색창에서 "RDS"를 입력하고 검색합니다  
   - **검색 결과에서 "RDS"를 클릭해 대시보드로 이동합니다.**
3. 대시보드에서 RDS 인스턴스 목록을 확인합니다  
   - **생성된 인스턴스가 없으면 "Create database" 버튼을 클릭해 시작합니다.**

> **📸 화면 확인:** RDS 대시보드가 표시되면 정상입니다.  
> **💡 Tip:** "Create database" 버튼은 새로운 RDS 인스턴스 생성을 위한 주요 메뉴입니다.

---

### Step 2: [주요 작업 1 - Multi-AZ RDS 인스턴스 생성]
1. **"Create database" 버튼 클릭**  
   - **"Create database" 메뉴에서 "Standard Create"를 선택합니다.**
2. **데이터베이스 엔진 선택**  
   - **MySQL, PostgreSQL, MariaDB, SQL Server 중 하나를 선택합니다.**  
   - **"Multi-AZ deployment" 옵션을 활성화합니다.**  
     - **Multi-AZ는 장애 시 자동 복구를 위한 고가용성 설계입니다.**
3. **인스턴스 설정**  
   - **Instance class**: CPU 및 메모리 요구사항에 따라 선택 (예: db.t3.micro)  
   - **Storage**: 저장소 용량 설정 (기본값 20GB)  
   - **DB subnet group**: VPC 설정 시 자동 생성된 subnet group을 선택  
   - **Security group**: 접근 제어를 위한 보안 그룹 설정  
   - **Master username/password**: 관리자 계정 생성  

> **📸 화면 확인:** "Create database" 화면에서 Multi-AZ 옵션이 활성화된 상태로 설정이 완료된 모습  

---

### Step 3: [주요 작업 2 - 읽기 전용 복제본 구성]
1. **복제본 생성**  
   - **RDS 대시보드에서 생성한 인스턴스를 선택한 후 "Read replicas" 메뉴 클릭**  
   - **"Create read replica" 버튼을 클릭해 복제본 생성 시작**  
2. **복제본 설정**  
   - **Instance class**: 복제본의 성능에 따라 선택 (예: db.t3.small)  
   - **DB subnet group**: 원본 인스턴스와 동일한 subnet group 사용  
   - **VPC**: 원본 인스턴스와 동일한 VPC 설정  
   - **Replication mode**: "Read-only" 모드로 설정  
   - **Security group**: 원본 인스턴스와 동일한 보안 그룹을 적용  
3. **확인 및 생성**  
   - **"Create" 버튼을 클릭해 복제본 생성을 요청합니다.**  
   - **생성 완료 후 복제본 상태를 "Available"로 확인해야 합니다.**

> **⚠️ 주의:** 복제본 생성 시 원본 인스턴스의 네트워크 설정과 보안 그룹을 동일하게 설정해야 복제가 성공합니다.  
> **💡 Tip:** 복제본은 읽기 전용으로만 사용할 수 있으며, 쓰기 작업은 원본 인스턴스에서만 수행해야 합니다.

---

### Step 4: 설정 확인 및 테스트
1. **리소스 확인 방법**  
   - **RDS 대시보드에서 "Instances" 탭을 선택해 생성된 인스턴스와 복제본을 확인합니다.**  
   - **Multi-AZ 인스턴스는 "Multi-AZ" 상태로 표시됩니다.**  
2. **상태 확인 방법**  
   - **"Status" 섹션에서 인스턴스 상태를 확인합니다.**  
   - **복제본은 "Read replica" 상태로 표시되어야 합니다.**  
3. **정상 동작 테스트**  
   - **AWS CLI로 복제본에 연결해 쿼리 실행**  
     ```bash
     mysql -h <read-replica-endpoint> -u <username> -p
     ```
   - **원본 인스턴스에 데이터를 입력 후 복제본에 데이터가 동기화되는지 확인**  
   - **CloudWatch에서 RDS의 CPU 사용률, 네트워크 트래픽을 모니터링**  

> **📸 화면 확인:** RDS 대시보드에서 생성된 인스턴스와 복제본의 상태가 "Available"로 표시된 모습  
> **💡 Tip:** 복제본은 원본 인스턴스의 데이터를 실시간으로 반영하지 않으므로, 읽기 작업 전에 데이터 동기화 상태를 확인해야 합니다.  

---

### 📊 서비스 비교 및 주의사항
| 서비스         | 특징                                 | 주의사항                              |
|----------------|--------------------------------------|----------------------------------------|
| Multi-AZ       | 장애 시 자동 복구, 고가용성          | 비용이 일반 AZ보다 약 15~30% 높음     |
| 읽기 전용 복제본 | 읽기 작업 분산, 성능 개선             | 복제본은 쓰기 작업 불가, 데이터 지연 가능성 |
| RDS Proxy      | 연결 관리 및 연결 풀링               | 복잡한 설정이 필요함                   |
| Aurora Serverless | 자동 스케일링, 높은 유연성           | 쿼리 성능에 따라 비용 변동 가능         |

> **⚠️ 주의:** RDS 인스턴스 생성 시 **DB subnet group**과 **VPC** 설정을 올바르게 하지 않으면 네트워크 연결이 실패할 수 있습니다.  
> **💰 비용 절약 팁:** 프리티어 사용 시 Multi-AZ와 읽기 전용 복제본을 동시에 사용하면 1년간 200달러 이내로 사용 가능합니다.

## ⌨️ AWS CLI로 RDS 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

> **💡 Tip:** CLI 버전이 1.18.0 이상이고, IAM 자격 증명이 정상적으로 설정되어 있어야 RDS 명령어 사용이 가능합니다. `aws configure` 명령어로 기본 설정을 확인하세요.

---

### 예제 1: RDS 리소스 조회
```bash
# RDS DB 인스턴스 목록 조회
aws rds list-db-instances --query 'DBInstances[*].DBInstanceIdentifier' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| --query | 결과 필터링 | `'DBInstances[*].DBInstanceIdentifier'` |
| --output | 출력 형식 | `json`, `table`, `text` |

**예상 출력:**
```
DBInstanceIdentifier
--------------------
my-multi-az-db
my-read-replica
```

> **⚠️ 주의:** `--query`는 JSON 형식의 응답을 필터링해 특정 필드만 출력합니다. `--output table`은 테이블 형식으로 정리해 읽기 쉽게 만듭니다.

---

### 예제 2: RDS 리소스 생성
```bash
# Multi-AZ RDS 인스턴스 생성
aws rds create-db-instance \
    --db-instance-identifier "my-multi-az-db" \
    --engine "mysql" \
    --master-user-password "SecureP@ss123!" \
    --allocated-storage 20 \
    --multi-az \
    --region "ap-northeast-2"
```

**필수 옵션:**
- `--db-instance-identifier`: 인스턴스 고유 이름 (ex: `my-multi-az-db`)
- `--engine`: 사용할 데이터베이스 엔진 (ex: `mysql`, `postgres`)
- `--master-user-password`: 관리자 비밀번호
- `--allocated-storage`: 저장 공간 크기 (GB 단위)
- `--multi-az`: Multi-AZ 설정 활성화

**예상 출력:**
```json
{
    "DBInstance": {
        "DBInstanceIdentifier": "my-multi-az-db",
        "Status": "creating"
    }
}
```

> **💡 Tip:** `--multi-az` 옵션을 사용하면 장애 시 자동 failover가 활성화됩니다. 프리티어는 750시간/월 제공됩니다.

---

### 예제 3: RDS 리소스 수정
```bash
# 읽기 전용 복제본 생성 (Read Replica)
aws rds create-read-replica \
    --db-instance-identifier "my-multi-az-db" \
    --read-replica-identifier "my-read-replica" \
    --region "ap-northeast-2"
```

**필수 옵션:**
- `--db-instance-identifier`: 마스터 인스턴스 ID
- `--read-replica-identifier`: 복제본 고유 이름
- `--region`: 복제본 지역 (마스터와 동일하거나 다른 리전 가능)

**예상 출력:**
```json
{
    "DBInstance": {
        "DBInstanceIdentifier": "my-read-replica",
        "Status": "creating"
    }
}
```

> **⚠️ 주의:** 복제본 생성 시 마스터 인스턴스의 `--read-write` 설정이 필요합니다. `aws rds modify-db-instance`로 설정 변경 가능합니다.

---

### 예제 4: RDS 리소스 삭제
```bash
# RDS 인스턴스 삭제
aws rds delete-db-instance --db-instance-identifier "my-multi-az-db" --skip-final-snapshot

# 삭제 확인
aws rds describe-db-instances --db-instance-identifier "my-multi-az-db"
```

> **⚠️ 주의:** `--skip-final-snapshot` 옵션으로 최종 백업을 생략할 수 있습니다. 삭제 후 데이터 복구는 불가능합니다.

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws rds list-db-instances
aws rds describe-db-instances --db-instance-identifier "id"

# 생성
aws rds create-db-instance --db-instance-identifier "name" --engine "mysql" --allocated-storage 20
aws rds create-read-replica --db-instance-identifier "master-id" --read-replica-identifier "replica-name"

# 수정
aws rds modify-db-instance --db-instance-identifier "id" --allocated-storage 30 --apply-immediately

# 삭제
aws rds delete-db-instance --db-instance-identifier "id" --skip-final-snapshot
```

> **💡 Tip:** `--apply-immediately` 옵션은 즉시 변경사항을 적용합니다. 대규모 수정 시 `--no-apply-immediately`로 배치 후 적용 가능합니다.

---

### CLI 사용 팁
| 팁 | 설명 |
|----|------|
| **비용 최적화** | Aurora Serverless는 자동 스케일링이 가능하며, 프리티어는 750시간/월 제공됩니다. |
| **복제본 관리** | `aws rds describe-db-replicas`로 복제본 상태를 확인할 수 있습니다. |
| **Proxy 설정** | `aws rds create-db-proxy`로 RDS Proxy를 생성하고, `--target-group-arn`으로 연결할 수 있습니다. |

> **⚠️ 주의:** CLI 명령어 실행 시 `--region` 파라미터를 반드시 지정해야 리전별 리소스를 제대로 조회할 수 있습니다.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 RDS 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **포인트 1: RDS 다중 AZ 배포의 고가용성 및 재해 복구 메커니즘**  
   - 설명: RDS Multi-AZ 배포는 단일 AZ 장애 시 자동 failover를 통해 서비스 중단을 방지합니다. 이는 AWS의 고가용성(Availability Zone) 기능과 백업/복원 프로세스를 이해하는 데 필수적입니다. 시험에서 고가용성 구현 방식, 데이터 복제 방식, 복구 시간 목표(RTO/RPO) 등이 주요 테스트 항목입니다.  
   - 키워드: `High Availability`, `Disaster Recovery`, `Multi-AZ`

2. **포인트 2: 읽기 전용 복제본의 읽기 확장 및 데이터 동기화 방식**  
   - 설명: 읽기 전용 복제본은 읽기 작업 분산을 통해 성능 최적화를 가능하게 하며, 데이터 동기화 방식(예: 주기적 복제, 실시간 복제)을 이해해야 합니다. 시험에서 복제 지연, 복제본 수 제한, 데이터 일관성 보장 방식 등이 주요 포인트입니다.  
   - 키워드: `Read Replication`, `Data Sync`, `Read Scaling`

3. **포인트 3: RDS Proxy의 연결 풀링과 연결 관리 기능**  
   - 설명: RDS Proxy는 연결 풀링을 통해 DB 연결 자원을 최적화하고, 연결 수를 제한하여 비용 절감 및 성능 향상을 도모합니다. 시험에서 연결 관리 방식, 연결 풀링의 장단점, RDS Proxy와 직접 연결의 차이가 주요 검증 항목입니다.  
   - 키워드: `Connection Pooling`, `Connection Management`, `RDS Proxy`

4. **포인트 4: Aurora 클러스터의 마스터-슬레이브 아키텍처 및 자동 백업**  
   - 설명: Aurora 클러스터는 마스터-슬레이브 아키텍처를 기반으로 하며, 실시간 백업 및 복제 기능을 제공합니다. 시험에서 Aurora의 자동 백업 메커니즘, 복제 지연 최소화 기술, 클러스터의 고가용성 구조 등이 중요합니다.  
   - 키워드: `Master-Slave Architecture`, `Automatic Backup`, `Aurora Cluster`

5. **포인트 5: Aurora Global Database의 글로벌 데이터 동기화 및 지역 복제본 관리**  
   - 설명: Aurora Global Database는 글로벌 데이터 동기화를 통해 여러 지역 간 일관성을 유지하며, 지역 복제본을 통해 지연 시간 최소화를 가능하게 합니다. 시험에서 글로벌 복제본 구성, 데이터 동기화 지연 시간, 지역 복제본의 사용 목적 등이 주요 검증 항목입니다.  
   - 키워드: `Global Data Sync`, `Regional Replication`, `Aurora Global DB`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | RDS Proxy와 읽기 전용 복제본을 혼동하여 연결 풀링 기능을 오해함 | RDS Proxy는 연결 풀링을 통해 연결 자원을 최적화하는 반면, 읽기 전용 복제본은 복제본을 통해 읽기 확장을 수행함 |
| 함정 2 | Aurora Serverless를 단일 노드 DB로 오인하여 확장성 관련 질문에 오답함 | Aurora Serverless는 자동 확장 기능을 가진 클러스터 형태로, 고가용성과 스케일 아웃이 가능함 |
| 함정 3 | Multi-AZ 배포와 Aurora Global Database를 혼동하여 글로벌 복제본 구성 방식을 오해함 | Multi-AZ는 단일 지역 내 AZ 복제를 제공하지만, Aurora Global DB는 여러 지역 간 복제본을 관리함 |

#### 🔄 RDS vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | RDS | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | 관계형 데이터베이스 관리, 고가용성, 백업 | DynamoDB(NoSQL), Aurora(클라우드 관계형 DB) | 관계형 데이터베이스 필요 시, SQL 기능 지원 필요 |
| 확장성 | 수동 스케일링, Multi-AZ, 읽기 전용 복제본 | Aurora Serverless(자동 확장), DynamoDB(자동 스케일링) | 트래픽 증가 시 자동 확장 필요 여부 |
| 비용 | 인스턴스 기반 요금, 데이터 저장 비용 | Aurora Serverless(기본 제한량 포함), DynamoDB(요금 구조 복잡) | 비용 최적화, 스케일링 방식 고려 |
| 지연시간 | 지역 내 복제본으로 지연 최소화 | Aurora Global DB(글로벌 복제본), DynamoDB(지역/글로벌 복제본) | 글로벌 사용자 대상 시 지연 시간 최소화 필요 |

#### 📝 시험 대비 체크리스트
- [ ] RDS의 핵심 목적을 한 문장으로 설명할 수 있는가? (예: "AWS에서 관계형 데이터베이스를 관리하고 고가용성/백업 제공")
- [ ] RDS를 선택해야 하는 시나리오를 알고 있는가? (예: "고가용성, 백업, SQL 기능 지원 필요 시")
- [ ] RDS의 제한사항/한계를 알고 있는가? (예: "비동기 복제로 인한 데이터 지연, 수동 스케일링 필요")
- [ ] RDS와 비슷한 서비스의 차이점을 설명할 수 있는가? (예: "Aurora는 RDS의 클라우드 버전, DynamoDB는 NoSQL 기반)
- [ ] RDS의 비용 구조를 이해하고 있는가? (예: "인스턴스 타입, 데이터 저장량, 백업 주기에 따라 요금 변동)

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 RDS를 떠올리세요:  
> - **High Availability** (고가용성)  
> - **Read Replication** (읽기 복제)  
> - **Connection Pooling** (연결 풀링)  
> - **Multi-AZ** (다중 AZ)  
> - **Disaster Recovery** (재해 복구)

---

| [⬅️ 이전 Day](../../week2/day5/README.md) | [📑 Day 1 목차](./README.md) | [🏠 Week 3](../README.md) | [Aurora ➡️](./Aurora.md) |

---
