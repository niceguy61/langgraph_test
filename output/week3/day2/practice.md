# Week 3 Day 2 실습 가이드

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
- [ ] DynamoDB 테이블 생성 및 구성
- [ ] GSI/LSI 설정 및 사용
- [ ] DAX 클러스터 설정 및 DynamoDB와 연동
- [ ] DynamoDB Streams 활성화 및 사용

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분
- Step 1: 약 10분
- Step 2: 약 15분
- Step 3: 약 10분
- 리소스 정리: 약 5분

---

## 📝 실습 단계

### Step 1: DynamoDB 테이블 생성 및 구성 (약 10분)

#### 1.1 DynamoDB 테이블 생성
```bash
# DynamoDB 테이블 생성 (Partition Key: UserId, Sort Key: Timestamp)
aws dynamodb create-table \
  --table-name UserActivity \
  --attribute-definitions \
    AttributeName=UserId,AttributeType=S \
    AttributeName=Timestamp,AttributeType=N \
  --key-schema \
    AttributeName=UserId,KeyType=HASH \
    AttributeName=Timestamp,KeyType=RANGE \
  --provisioned-throughput \
    ReadCapacityUnits=5,WriteCapacityUnits=5
```

**예상 출력:**
```
{
    "TableDescription": {
        "TableArn": "arn:aws:dynamodb:us-west-2:123456789012:table/UserActivity",
        "TableName": "UserActivity",
        "TableStatus": "ACTIVE",
        "CreationDate": 1620000000.0,
        "ProvisionedThroughput": {
            "LastIncreaseDateTime": 1620000000.0,
            "LastDecreaseDateTime": 1620000000.0,
            "NumberOfDecreasesToday": 0
        },
        "BillingModeSummary": {
            "BillingModeStatus": "DISABLED"
        }
    }
}
```

> **💡 설명:**  
> - `Partition Key`는 데이터 분산을 위해 사용되는 고유 키 (UserId)  
> - `Sort Key`는 데이터 정렬을 위한 추가 키 (Timestamp)  
> - `Provisioned Throughput`은 예약 용량 모드로, 읽기/쓰기 캐파시티 단위를 설정합니다.

#### 1.2 GSI/LSI 설정
```bash
# Global Secondary Index (GSI) 생성
aws dynamodb update-table \
  --table-name UserActivity \
  --attribute-definitions \
    AttributeName=ActivityType,AttributeType=S \
  --global-secondary-index-updates \
    [
      {
        "Update": {
          "IndexName": "ActivityTypeIndex",
          "KeySchema": [
            {
              "AttributeName": "ActivityType",
              "KeyType": "HASH"
            }
          ],
          "Projection": {
            "ProjectionType": "ALL"
          },
          "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
          }
        }
      }
    ]
```

**AWS 콘솔에서:**
1. 서비스 검색창에 "DynamoDB" 입력 후 클릭
2. "Tables" 탭에서 "UserActivity" 테이블 클릭
3. "Indexes" 섹션에서 "ActivityTypeIndex"가 생성되었는지 확인

> **📸 화면 확인:**  
> - "ActivityTypeIndex"가 목록에 표시되고, "Status"가 "ACTIVE"인 상태여야 합니다.

#### ✅ Step 1 완료 확인
다음이 보이면 Step 1이 완료된 것입니다:
- [ ] 테이블 생성 성공 메시지 확인
- [ ] GSI가 생성되어 "ActivityTypeIndex"가 표시됨

---

### Step 2: DAX 클러스터 설정 및 DynamoDB 연동 (약 15분)

#### 2.1 DAX 클러스터 생성
```bash
# DAX 클러스터 생성 (2개 노드, 2GB 메모리)
aws dax create-cluster \
  --cluster-name UserDAXCluster \
  --replication-factor 2 \
  --node-parameters \
    "NodeGroupConfiguration=[{NodeGroupRole=PRIMARY,InstanceType=dax.r4.large,EngineVersion=1.0.1}]"
```

**예상 출력:**
```
{
    "Cluster": {
        "ClusterName": "UserDAXCluster",
        "ClusterStatus": "creating",
        "ClusterArn": "arn:aws:dax:us-west-2:123456789012:cluster/UserDAXCluster",
        "ClusterDiscoveryEndpoint": "UserDAXCluster.abc123.dax.us-west-2.amazonaws.com",
        "ClusterId": "UserDAXCluster",
        "ClusterType": "cluster",
        "CreationTime": "2023-06-01T00:00:00Z",
        "Status": "creating"
    }
}
```

#### 2.2 DynamoDB 테이블 DAX 연동
```bash
# DynamoDB 테이블에 DAX 연동 설정
aws dynamodb update-table \
  --table-name UserActivity \
  --dax-parameters \
    "DaxClusterArn=arn:aws:dax:us-west-2:123456789012:cluster/UserDAXCluster"
```

**AWS 콘솔에서:**
1. DynamoDB 테이블 "UserActivity" 클릭
2. "Properties" 탭에서 "DAX Cluster"가 연결되었는지 확인

> **📸 화면 확인:**  
> - "DAX Cluster" 섹션이 표시되고, "Status"가 "ACTIVE"여야 합니다.

#### ✅ Step 2 완료 확인
다음이 보이면 Step 2가 완료된 것입니다:
- [ ] DAX 클러스터 생성 성공 메시지 확인
- [ ] DynamoDB 테이블에 DAX 연결 완료

---

### Step 3: DynamoDB Streams 활성화 및 사용 (약 10분)

#### 3.1 DynamoDB Streams 활성화
```bash
# DynamoDB Streams 활성화
aws dynamodb update-table \
  --table-name UserActivity \
  --stream-specification \
    "StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES"
```

**예상 출력:**
```
{
    "TableDescription": {
        "StreamSpecification": {
            "StreamEnabled": true,
            "StreamViewType": "NEW_AND_OLD_IMAGES"
        }
    }
}
```

#### 3.2 Lambda 함수 연동 (예시)
```bash
# Lambda 함수 생성 및 DynamoDB Streams 연동 (AWS CLI로는 직접 생성 불가, 콘솔에서 설정)
aws lambda create-function \
  --function-name UserActivityLambda \
  --runtime python3.9 \
  --role arn:aws:iam::123456789012:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda_function.zip
```

**AWS 콘솔에서:**
1. "Lambda" 서비스로 이동
2. "Functions" > "UserActivityLambda" > "Configuration" > "Event Sources" > "Add event source"
3. "DynamoDB" 선택 후 "UserActivity" 테이블 선택

> **📸 화면 확인:**  
> - "UserActivityLambda" 함수가 DynamoDB Streams에 연결된 상태여야 합니다.

#### ✅ Step 3 완료 확인
다음이 보이면 Step 3가 완료된 것입니다:
- [ ] DynamoDB Streams 활성화 확인
- [ ] Lambda 함수가 Streams에 연결됨

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] DynamoDB 테이블 생성 및 GSI 설정 완료
- [ ] DAX 클러스터 생성 및 DynamoDB 연동 완료
- [ ] DynamoDB Streams 활성화 및 Lambda 연동 완료

### 예상 최종 결과
```bash
# DynamoDB 테이블 상태 확인
aws dynamodb describe-table --table-name UserActivity

# DAX 클러스터 상태 확인
aws dax describe-clusters --cluster-name UserDAXCluster

# DynamoDB Streams 상태 확인
aws dynamodb describe-streams --table-name UserActivity
```

**예상 출력:**
```
{
    "Streams": [
        {
            "StreamArn": "arn:aws:dynamodb:us-west-2:123456789012:table/UserActivity:stream/2023-06-01T00:00:00.000",
            "StreamViewType": "NEW_AND_OLD_IMAGES",
            "StreamStatus": "ENABLED"
        }
    ]
}
```

---

## 🔧 트러블슈팅

### 문제 1: `ResourceNotFoundException` 오류
**증상:**  
```
An error occurred (ResourceNotFoundException) when calling the CreateTable operation: Table with name UserActivity does not exist.
```

**원인:**  
테이블 생성 단계에서 오류가 발생하거나, 테이블 이름이 잘못 입력되었습니다.

**해결 방법:**
1. `aws dynamodb list-tables` 명령어로 테이블 목록 확인
2. `aws dynamodb describe-table --table-name UserActivity` 명령어로 상태 확인

### 문제 2: `AccessDenied` 오류
**증상:**  
```
An error occurred (AccessDenied) when calling the CreateTable operation: User: arn:aws:sts::123456789012:assumed-role/iam-user/iam-user is not authorized to perform: dynamodb:CreateTable
```

**해결 방법:**
1. IAM 사용자 권한 확인:  
   ```bash
   aws iam get-user
   ```
2. 필요 권한 추가:  
   ```bash
   aws iam attach-role-policy --role-name iam-user --policy-arn arn:aws:iam::123456789012:policy/DynamoDBFullAccess
   ```

### 문제 3: DAX 클러스터 생성 실패
**증상:**  
```
An error occurred (InvalidParameterException) when calling the CreateCluster operation: Replication factor must be between 1 and 10.
```

**해결 방법:**  
- `--replication-factor` 값이 1~10 사이여야 합니다 (예: `--replication-factor 2`)

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] DynamoDB 테이블 `UserActivity`
- [ ] DAX 클러스터 `UserDAXCluster`
- [ ] DynamoDB Streams (자동 정리됨)

### 리소스 정리 명령어
```bash
# 1. DynamoDB 테이블 삭제
aws dynamodb delete-table --table-name UserActivity

# 2. DAX 클러스터 삭제
aws dax delete-cluster --cluster-name UserDAXCluster

# 3. 삭제 확인
aws dax describe-clusters
aws dynamodb list-tables
```

### 정리 완료 확인
```bash
# 리소스가 모두 삭제되었는지 확인
aws dax describe-clusters
aws dynamodb list-tables
```

---

## 📚 추가 학습 자료
- [AWS DynamoDB 공식 문서](https://docs.aws.amazon.com/dynamodb/)
- [DAX 사용 가이드](https://docs.aws.amazon.com/dax/latest/developerguide/Welcome.html)
- [DynamoDB Streams 튜토리얼](https://docs.aws.amazon.com/dynamodb/latest/developerguide/Streams.html)