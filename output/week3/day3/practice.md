# Week 3 Day 3 실습 가이드

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
- [ ] ElastiCache Redis 클러스터 생성 및 설정  
- [ ] Redis 클러스터 연결 테스트  
- [ ] 클러스터 리소스 정리 및 비용 절감 방법 이해  

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분  
- Step 1: 약 10분  
- Step 2: 약 15분  
- Step 3: 약 10분  
- 리소스 정리: 약 5분  

---

## 📝 실습 단계

### Step 1: ElastiCache Redis 클러스터 생성 (약 10분)

#### 1.1 AWS 콘솔에서 ElastiCache 생성  
1. AWS Management Console → 서비스 검색창에서 **Elasticache** 입력  
2. **Elasticache** 서비스 클릭 → **Create** 버튼 선택  
3. **Engine**에서 **Redis** 선택  
4. **Cluster Name** 입력 (예: `MyRedisCluster`)  
5. **Node Type**에서 `cache.t2.micro` 선택 (프리티어 지원)  
6. **Number of Nodes** 1로 설정  
7. **Security Groups**에서 기본 설정 유지  
8. **Create** 버튼 클릭  

> **📸 화면 확인:** "Your cluster is being created" 메시지가 표시되면 정상입니다.  

#### 1.2 CLI로 클러스터 생성 (선택)  
```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id MyRedisCluster \
  --engine redis \
  --cache-node-type cache.t2.micro \
  --num-cache-nodes 1
```

**예상 출력:**  
```
{
  "CacheCluster": {
    "CacheClusterId": "MyRedisCluster",
    "Status": "create in progress",
    ...
  }
}
```

> **💡 설명:** `cache.t2.micro`는 프리티어로 750시간/월까지 무료 사용 가능.  
> `num-cache-nodes`는 노드 수를 조절하며, 1개 노드로 시작하는 것이 권장됩니다.

#### ✅ Step 1 완료 확인  
- [ ] 콘솔에서 "MyRedisCluster" 클러스터가 생성 완료 상태  
- [ ] CLI 명령어 실행 결과에서 "Status": "create in progress" 확인  

---

### Step 2: Redis 클러스터 연결 및 테스트 (약 15분)

#### 2.1 클러스터 연결 정보 확인  
1. AWS 콘솔 → ElastiCache → **Cache clusters**  
2. `MyRedisCluster` 클릭 → **Configuration** 탭  
3. **Endpoint** 주소와 포트 확인 (예: `myrediscluster.abc123.us-west-2.cache.amazonaws.com:6379`)  

> **📸 화면 확인:** "Endpoint" 필드에 IP 주소와 포트가 표시되면 정상입니다.  

#### 2.2 CLI로 Redis 테스트  
```bash
aws elasticache describe-cache-clusters --cache-cluster-id MyRedisCluster
```

**예상 출력:**  
```
{
  "CacheClusters": [
    {
      "CacheClusterId": "MyRedisCluster",
      "Status": "available",
      "Endpoint": "myrediscluster.abc123.us-west-2.cache.amazonaws.com",
      ...
    }
  ]
}
```

#### 2.3 Redis CLI 명령어 실행  
```bash
redis-cli -h myrediscluster.abc123.us-west-2.cache.amazonaws.com -p 6379
127.0.0.1:6379> SET testkey "testvalue"
127.0.0.1:6379> GET testkey
"testvalue"
```

> **💡 설명:** Redis CLI를 통해 키-값 저장/읽기 테스트를 수행합니다.  
> 테스트 후 `QUIT` 명령어로 Redis CLI 종료.

#### ✅ Step 2 완료 확인  
- [ ] `Status`: "available" 확인  
- [ ] Redis CLI로 `GET testkey` 결과가 "testvalue" 출력  

---

### Step 3: 리소스 정리 및 비용 절감 방법 (약 10분)

#### 3.1 클러스터 종료  
```bash
aws elasticache delete-cache-cluster \
  --cache-cluster-id MyRedisCluster \
  --retention-period 1
```

> **💡 설명:** `--retention-period`는 클러스터 삭제 후 1일간 데이터 보존 (비용 절감용).  
> 실습 완료 후 즉시 종료해야 비용 발생 방지.

#### 3.2 비용 절감 팁  
- 프리티어 사용 시 `cache.t2.micro`로 시작  
- 사용하지 않는 리소스는 즉시 삭제  
- AWS Cost Explorer로 비용 모니터링  

#### ✅ Step 3 완료 확인  
- [ ] `aws elasticache describe-cache-clusters` 결과가 비어 있음  
- [ ] AWS 콘솔에서 리소스 삭제 완료 알림 확인  

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트  
- [ ] ElastiCache 클러스터 생성 및 테스트 완료  
- [ ] 리소스 정리 완료  
- [ ] 비용 절감 방법 이해  

### 예상 최종 결과  
```bash
# 리소스 삭제 확인
aws elasticache describe-cache-clusters --cache-cluster-id MyRedisCluster
```

**예상 출력:**  
```
{
  "CacheClusters": []
}
```

---

## 🔧 트러블슈팅

### 문제 1: `InvalidParameterValue` 오류  
**증상:** `InvalidParameterValue: Invalid parameter...`  
**원인:** 클러스터 이름이 기존 리소스와 중복 또는 유효하지 않음  
**해결 방법:**  
```bash
aws elasticache describe-cache-clusters
```
> 기존 클러스터 이름 확인 후 `MyRedisCluster`로 변경  

### 문제 2: `AccessDenied` 오류  
**증상:** `AccessDenied` 또는 `UnauthorizedAccess`  
**해결 방법:**  
1. IAM 사용자 권한 확인  
2. `elasticache:DescribeCacheClusters` 및 `elasticache:DeleteCacheCluster` 권한 추가  

### 문제 3: 네트워크 연결 실패  
**증상:** Redis CLI 연결 실패  
**해결 방법:**  
1. 보안 그룹 설정 확인 (SSH/Redis 포트 허용)  
2. `aws ec2 describe-security-groups` 명령어로 확인  

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!  
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록  
- [ ] ElastiCache 클러스터 (`MyRedisCluster`)  
- [ ] AWS CLI 자격 증명 (선택)  
- [ ] VS Code 설정 (선택)  

### 리소스 정리 명령어  
```bash
# 1. ElastiCache 클러스터 삭제
aws elasticache delete-cache-cluster \
  --cache-cluster-id MyRedisCluster \
  --retention-period 1

# 2. IAM 사용자 권한 정리 (선택)
aws iam get-user
```

### 정리 완료 확인  
```bash
# 리소스가 모두 삭제되었는지 확인
aws elasticache describe-cache-clusters --cache-cluster-id MyRedisCluster
```

**예상 출력:**  
```
{
  "CacheClusters": []
}
```

---

## 📚 추가 학습 자료
- [AWS ElastiCache 공식 문서](https://docs.aws.amazon.com/elasticache/)  
- [Redis vs Memcached 비교 가이드](https://aws.amazon.com/elasticache/comparison/)  
- [AWS Cost Explorer 사용법](https://aws.amazon.com/cost-management/)