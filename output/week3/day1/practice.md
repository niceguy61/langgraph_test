# Week 3 Day 1 실습 가이드

## ⚠️ 필수 사전 준비

> **🚨 중요:** 실습을 시작하기 전에 반드시 아래 가이드를 먼저 완료하세요!

### 📚 필수 선행 문서
실습을 시작하기 전에 다음 문서들을 **반드시** 먼저 읽고 완료하세요:

| 문서 | 설명 | 필수 여부 |
|-----|------|----------|
| [AWS 계정 생성 가이드](../prerequisites/aws-account-setup.md) | AWS 계정이 없다면 이 가이드를 따라 계정을 생성하세요 | ✅ 필수 |
| [AWS CLI 설치 가이드](../prerequisites/aws-cli-setup.md) | AWS CLI 설치 및 설정 방법 | ✅ 필수 |
| [IAM 사용자 생성 가이드](../prerequisites/iam-user-setup.md) | 실습용 IAM 사용자 생성 방법 | ✅ 필수 |
| [VS Code 설정 가이드](../prerequisites/vscode-setup.md) | 개발 환경 설정 (선택) | 선택 |

### ✅ 사전 체크리스트
실습을 시작하기 전 아래 항목들을 모두 확인하세요:

- [ ] AWS 계정이 있고 로그인할 수 있다
- [ ] AWS CLI가 설치되어 있다 (`aws --version` 으로 확인)
- [ ] AWS CLI 자격 증명이 설정되어 있다 (`aws sts get-caller-identity` 로 확인)
- [ ] 실습에 필요한 IAM 권한이 있다
- [ ] 결제 알림이 설정되어 있다 (예상치 못한 비용 방지)

```bash
# 사전 준비 확인 명령어
aws --version
aws sts get-caller-identity
```

> **⚠️ 주의:** 위 체크리스트가 모두 완료되지 않았다면 실습을 진행하지 마세요!
> 문제 발생 시 해결이 어려울 수 있습니다.

---

## 🎯 실습 목표
이 실습을 완료하면 다음을 할 수 있습니다:
- [ ] Multi-AZ RDS 인스턴스 생성
- [ ] 읽기 전용 복제본 구성
- [ ] RDS Proxy 연결 풀링 기능 확인

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분
- Step 1: 약 10분
- Step 2: 약 15분
- Step 3: 약 10분
- 리소스 정리: 약 5분

---

## 📝 실습 단계

### Step 1: Multi-AZ RDS 인스턴스 생성 (약 10분)

#### 1.1 RDS 인스턴스 생성
**AWS 콘솔에서:**
1. 서비스 검색창에 "RDS" 입력 후 클릭
2. "Databases" → "Create database"로 이동
3. **Database engine**에서 MySQL 선택
4. **Instance Class**에서 `db.t3.micro` 선택
5. **Multi-AZ Deployment** 체크박스 선택
6. **Database details**에서 DB 이름 입력 (예: `my-multi-az-db`)
7. **Username**과 **Password** 입력
8. **VPC**와 **Subnet group** 선택
9. **Security Group** 설정 후 "Create database" 클릭

> **📸 화면 확인:** "Multi-AZ Deployment"가 활성화된 상태로 인스턴스가 생성되고 있는지 확인

#### 1.2 CLI 명령어로 인스턴스 생성
```bash
aws rds create-db-instance \
  --db-instance-identifier my-multi-az-db \
  --engine mysql5.7 \
  --db-instance-class db.t3.micro \
  --multi-az \
  --master-username admin \
  --master-user-password P@ssw0rd123! \
  --vpc-security-group-ids sg-12345678 \
  --region us-west-2
```

**예상 출력:**
```
{
  "DBInstance": {
    "DBInstanceIdentifier": "my-multi-az-db",
    "DBInstanceStatus": "creating",
    ...
  }
}
```

> **💡 설명:** `--multi-az` 옵션으로 고가용성 구성. AWS는 주/보조 인스턴스를 자동으로 배포하여 장애 시 자동 복구합니다.

#### ✅ Step 1 완료 확인
- [ ] RDS 인스턴스 상태가 `available`로 변경
- [ ] Multi-AZ 배포가 활성화된 상태 확인 (콘솔 > DB 인스턴스 > Multi-AZ 설정)

---

### Step 2: 읽기 전용 복제본 구성 (약 15분)

#### 2.1 복제본 생성
**AWS 콘솔에서:**
1. RDS 인스턴스 목록에서 생성한 인스턴스 클릭
2. "Read replicas" 탭 → "Create read replica" 클릭
3. **Replica identifier** 입력 (예: `my-read-replica`)
4. **Instance class**에서 `db.t3.small` 선택
5. **VPC**와 **Subnet group** 선택
6. "Create" 클릭

> **📸 화면 확인:** 복제본 생성 중인 상태로 "Read replica"가 생성되고 있는지 확인

#### 2.2 CLI 명령어로 복제본 생성
```bash
aws rds create-read-replica \
  --db-instance-identifier my-multi-az-db \
  --read-replica-identifier my-read-replica \
  --db-instance-class db.t3.small \
  --region us-west-2
```

**예상 출력:**
```
{
  "ReadReplica": {
    "DBInstanceIdentifier": "my-read-replica",
    "DBInstanceStatus": "creating",
    ...
  }
}
```

> **💡 설명:** 읽기 전용 복제본은 주 인스턴스의 데이터를 실시간으로 동기화하며, 읽기 트래픽을 분산합니다.

#### ✅ Step 2 완료 확인
- [ ] 복제본 상태가 `available`로 변경
- [ ] 주 인스턴스와 복제본의 데이터 일치 여부 확인 (MySQL CLI로 `SHOW MASTER STATUS` 실행)

---

### Step 3: RDS Proxy 설정 (약 10분)

#### 3.1 RDS Proxy 생성
**AWS 콘솔에서:**
1. 서비스 검색창에 "RDS Proxy" 입력 후 클릭
2. "Create proxy" 클릭
3. **Proxy name** 입력 (예: `my-rds-proxy`)
4. **Engine**에서 MySQL 선택
5. **Target DB instance**에서 생성한 Multi-AZ 인스턴스 선택
6. "Create" 클릭

> **📸 화면 확인:** Proxy 생성 완료 후 "Target" 설정이 제대로 연결된 상태인지 확인

#### 3.2 CLI 명령어로 Proxy 생성
```bash
aws rds create-db-proxy \
  --db-proxy-name my-rds-proxy \
  --engine-engine-version mysql5.7 \
  --target-configuration "DBInstanceIdentifier=my-multi-az-db,Type=read-write" \
  --region us-west-2
```

**예상 출력:**
```
{
  "DBProxy": {
    "DBProxyName": "my-rds-proxy",
    "DBProxyStatus": "creating",
    ...
  }
}
```

> **💡 설명:** RDS Proxy는 연결 풀링을 통해 DB 연결 수를 줄이고, 연결 관리 효율성을 높입니다.

#### ✅ Step 3 완의 확인
- [ ] Proxy 상태가 `available`로 변경
- [ ] 클라이언트에서 Proxy를 통해 연결 가능한지 확인 (예: `mysql -h my-rds-proxy.us-west-2.rds.amazonaws.com -u admin -p`)

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] Multi-AZ RDS 인스턴스 생성 완료
- [ ] 읽기 전용 복제본 구성 완료
- [ ] RDS Proxy 설정 완료

### 예상 최종 결과
```bash
# RDS 인스턴스 상태 확인
aws rds describe-db-instances --db-instance-identifier my-multi-az-db --region us-west-2
```

**예상 출력:**
```
{
  "DBInstances": [
    {
      "DBInstanceIdentifier": "my-multi-az-db",
      "DBInstanceStatus": "available",
      "MultiAZ": true,
      ...
    }
  ]
}
```

---

## 🔧 트러블슈팅

### 문제 1: 인스턴스 생성 실패
**증상:** `InvalidSubnetID` 오류 발생

**원인:** 선택한 Subnet이 Multi-AZ 지원하지 않거나 잘못 선택됨

**해결 방법:**
1. RDS 인스턴스 생성 시 `--availability-zones` 옵션으로 특정 AZ 지정
2. VPC 설정에서 "Multi-AZ" 지원 여부 확인

### 문제 2: 복제본 생성 실패
**증상:** `InvalidDBInstanceState` 오류 발생

**원인:** 주 인스턴스가 `available` 상태가 아닐 때 복제본 생성 시도

**해결 방법:**
1. 주 인스턴스 상태가 `available`인지 확인
2. `aws rds describe-db-instances` 명령어로 상태 확인

### 문제 3: 권한 오류 (AccessDenied)
**증상:** `AccessDenied` 오류 발생

**해결 방법:**
1. IAM 사용자에게 `rds:CreateDBInstance`, `rds:CreateReadReplica` 권한 부여
2. `aws iam get-user` 명령어로 사용자 권한 확인

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] Multi-AZ RDS 인스턴스 (`my-multi-az-db`)
- [ ] 읽기 전용 복제본 (`my-read-replica`)
- [ ] RDS Proxy (`my-rds-proxy`)

### 리소스 정리 명령어
```bash
# 1. RDS 인스턴스 삭제
aws rds delete-db-instance --db-instance-identifier my-multi-az-db --region us-west-2

# 2. 복제본 삭제
aws rds delete-db-instance --db-instance-identifier my-read-replica --region us-west-2

# 3. RDS Proxy 삭제
aws rds delete-db-proxy --db-proxy-name my-rds-proxy --region us-west-2
```

### 정리 완료 확인
```bash
# 리소스가 모두 삭제되었는지 확인
aws rds describe-db-instances --region us-west-2
aws rds describe-db-proxies --region us-west-2
```

---

## 📚 추가 학습 자료
- [AWS RDS 다중 AZ 가이드](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)
- [RDS Proxy 사용 설명서](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Proxy.html)
- [Aurora 클러스터 vs RDS 비교](https://aws.amazon.com/rds/aurora/)