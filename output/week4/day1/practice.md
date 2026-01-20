# Week 4 Day 1 실습 가이드

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
- [ ] ECS 클러스터를 생성하고 Fargate 태스크를 배포할 수 있다
- [ ] ECR에 Docker 이미지를 등록하고 ECS 서비스에 연결할 수 있다
- [ ] ECS Anywhere를 사용한 하이브리드 배포 환경을 구성할 수 있다

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분
- Step 1: 약 10분
- Step 2: 약 15분
- Step 3: 약 10분
- 리소스 정리: 약 5분

---

## 📝 실습 단계

### Step 1: ECS 클러스터 생성 (약 10분)

#### 1.1 ECS 클러스터 생성
```bash
# ECS 클러스터 생성
aws ecs create-cluster --cluster-name MyECSCluster
```

**예상 출력:**
```
{
    "cluster": {
        "clusterArn": "arn:aws:ecs:us-east-1:123456789012:cluster/MyECSCluster",
        "clusterName": "MyECSCluster",
        "status": "ACTIVE",
        "registeredContainerInstancesCount": 0,
        "runningTasksCount": 0,
        "pendingTasksCount": 0,
        "activeServicesCount": 0
    }
}
```

> **💡 설명:** `create-cluster` 명령어는 ECS 클러스터를 생성합니다. 생성된 클러스터는 AWS 콘솔에서 "ECS" 서비스 > "Clusters" 탭에서 확인할 수 있습니다. 클러스터 상태가 "ACTIVE"로 표시되면 정상적으로 생성되었습니다.

#### 1.2 Fargate 실행 역할 생성
**AWS 콘솔에서:**
1. 서비스 검색창에서 "IAM" 입력
2. "IAM 콘솔" 클릭
3. 좌측 메뉴에서 "Role" 선택
4. "Create role" 클릭
5. "AWS service" 선택
6. "ECS" 선택
7. "Next: Permissions" 클릭
8. "AmazonEC2ContainerServiceforFargate" 정책 추가
9. "Next: Review" 클릭
10. "Create role" 클릭

> **📸 화면 확인:** 생성된 역할 이름이 "ecs-Fargate-Role"로 표시되며, "AmazonEC2ContainerServiceforFargate" 정책이 연결되어 있는지 확인하세요.

#### ✅ Step 1 완료 확인
다음이 보이면 Step 1이 완료된 것입니다:
- [ ] ECS 클러스터가 생성되었고 상태가 ACTIVE
- [ ] Fargate 실행 역할이 생성되었고 정책이 연결됨

---

### Step 2: Fargate 태스크 배포 (약 15분)

#### 2.1 ECR 리포지토리 생성
```bash
# ECR 리포지토리 생성
aws ecr create-repository --repository-name my-ecs-task
```

**예상 출력:**
```
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-east-1:123456789012:repository/my-ecs-task",
        "repositoryName": "my-ecs-task",
        "repositoryUri": "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-ecs-task"
    }
}
```

> **💡 설명:** ECR 리포지토리는 Docker 이미지를 저장하는 저장소입니다. 생성된 리포지토리 URI를 사용해 이미지를 푸시해야 합니다. 리포지토리 상태가 "ACTIVE"로 표시되면 정상입니다.

#### 2.2 Docker 이미지 빌드 및 ECR 푸시
```bash
# 로컬 Docker 이미지 빌드
docker build -t my-ecs-task:latest .

# ECR 리포지토리 URI 확인
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Docker 이미지 태그 수정
docker tag my-ecs-task:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-ecs-task:latest

# ECR에 이미지 푸시
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-ecs-task:latest
```

**예상 출력:**
```
The push refers to a repository [123456789012.dkr.ecr.us-east-1.amazonaws.com/my-ecs-task]
Layer digest: sha256:abc123...
Status: pushed
latest: digest: sha256:abc123...
Status: pushed
```

> **📸 화면 확인:** ECR 콘솔에서 "my-ecs-task" 리포지토리가 생성되었고, 이미지가 정상적으로 업로드되었는지 확인하세요.

#### 2.3 Fargate 태스크 정의 파일 생성
```bash
# Fargate 태스크 정의 파일 생성
cat > task-definition.json <<EOF
{
    "family": "my-task-definition",
    "networkMode": "awsvpc",
    "containerDefinitions": [
        {
            "name": "my-container",
            "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-ecs-task:latest",
            "cpu": "256",
            "memory": "512",
            "essential": true,
            "portMappings": [
                {
                    "containerPort": 80,
                    "hostPort": 80
                }
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/my-ecs-task",
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "ecs"
                }
            }
        }
    ]
}
EOF
```

#### 2.4 Fargate 태스크 정의 등록
```bash
# Fargate 태스크 정의 등록
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

**예상 출력:**
```
{
    "taskDefinition": {
        "taskDefinitionArn": "arn:aws:ecs:us-east-1:123456789012:task-definition/my-task-definition:1",
        "family": "my-task-definition",
        "revision": 1,
        "volumes": [],
        "networkMode": "awsvpc",
        "requiresCompatibilities": [
            "FARGATE"
        ],
        "cpu": "256",
        "memory": "512",
        "registeredAt": "2023-09-15T12:34:56Z",
        "status": "ACTIVE",
        "placementConstraints": [],
        "taskRoleArn": "",
        "executionRoleArn": "arn:aws:iam::123456789012:role/ecs-Fargate-Role"
    }
}
```

> **💡 설명:** 태스크 정의는 Fargate 태스크가 실행될 구성 정보입니다. `networkMode`가 `awsvpc`로 설정되어야 하며, 로그 설정이 올바르게 구성되어야 합니다.

#### ✅ Step 2 완료 확인
다음이 보이면 Step 2가 완료된 것입니다:
- [ ] ECR 리포지토리가 생성되고 이미지가 푸시됨
- [ ] Fargate 태스크 정의가 등록되고 상태가 ACTIVE

---

### Step 3: ECS 서비스 배포 (약 10분)

#### 3.1 ECS 서비스 생성
```bash
# ECS 서비스 생성
aws ecs create-service --cluster MyECSCluster \
--service-name MyECSService \
--task-definition my-task-definition \
--desired-count 1 \
--launch-type FARGATE \
--network-configuration "awsvpcConfiguration={subnets=[subnet-12345678],securityGroups=[sg-12345678],assignPublicIp=TRUE}"
```

**예상 출력:**
```
{
    "service": {
        "serviceArn": "arn:aws:ecs:us-east-1:123456789012:service/MyECSCluster/MyECSService",
        "serviceName": "MyECSService",
        "clusterArn": "arn:aws:ecs:us-east-1:123456789012:cluster/MyECSCluster",
        "status": "ACTIVE",
        "desiredCount": 1,
        "runningCount": 0,
        "pendingCount": 1,
        "createdAt": 1694800000,
        "placementStrategy": [],
        "deploymentConfiguration": {
            "deploymentCircuitBreaker": {
                "enable": false,
                "rollbackOnFirstFailure": false
            },
            "maximumPercent": 200,
            "minimumHealthyPercent": 50
        },
        "roleArn": "arn:aws:iam::123456789012:role/ecs-Fargate-Role",
        "startedBy": "AWS",
        "stabilityStatus": "STABLE"
    }
}
```

> **📸 화면 확인:** ECS 콘솔에서 "MyECSService" 서비스가 생성되었고, 상태가 "ACTIVE"로 표시되며, 태스크가 실행 중인지 확인하세요.

#### ✅ Step 3 완료 확인
다음이 보이면 Step 3가 완료된 것입니다:
- [ ] ECS 서비스가 생성되고 상태가 ACTIVE
- [ ] 태스크가 실행 중으로 전환됨

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] ECS 클러스터 생성 및 Fargate 태스크 배포 완료
- [ ] ECR 이미지 등록 및 서비스 연결 완료
- [ ] ECS Anywhere 하이브리드 배포 환경 구성 완료

### 예상 최종 결과
```bash
# 서비스 상태 확인
aws ecs describe-services --cluster MyECSCluster --services MyECSService
```

**예상 출력:**
```
{
    "services": [
        {
            "serviceArn": "arn:aws:ecs:us-east-1:123456789012:service/MyECSCluster/MyECSService",
            "serviceName": "MyECSService",
            "clusterArn": "arn:aws:ecs:us-east-1:123456789012:cluster/MyECSCluster",
            "status": "ACTIVE",
            "desiredCount": 1,
            "runningCount": 1,
            "pendingCount": 0,
            "createdAt": 1694800000,
            "deploymentConfiguration": {
                "deploymentCircuitBreaker": {
                    "enable": false,
                    "rollbackOnFirstFailure": false
                },
                "maximumPercent": 200,
                "minimumHealthyPercent": 50
            },
            "roleArn": "arn:aws:iam::123456789012:role/ecs-Fargate-Role",
            "startedBy": "AWS",
            "stabilityStatus": "STABLE"
        }
    ]
}
```

---

## 🔧 트러블슈팅

### 문제 1: `InvalidParameterException` 오류
**증상:** `InvalidParameterException: The parameter taskDefinition is invalid` 오류 발생

**원인:** 태스크 정의 이름이 잘못 입력되었거나, 리소스가 존재하지 않음

**해결 방법:**
1. `aws ecs list-task-definitions` 명령어로 등록된 태스크 정의 목록 확인
2. `task-definition.json` 파일의 `family` 필드를 확인하고, `--task-definition` 파라미터에 올바른 이름 입력

### 문제 2: `AccessDenied` 오류
**증상:** `AccessDenied` 또는 `UnauthorizedAccess` 오류 발생

**해결 방법:**
1. IAM 사용자 권한 확인
2. `aws iam get-user` 명령어로 현재 사용자 확인
3. 필요한 정책 연결: `AmazonEC2ContainerRegistryFullAccess`, `AmazonECS_FullAccess` 추가

### 문제 3: Fargate 태스크 실행 실패
**증상:** 태스크 상태가 `STOPPED` 또는 `RUNNING`이 아닌 경우

**해결 방법:**
1. `aws ecs describe-services` 명령어로 서비스 상태 확인
2. `aws ecs describe-tasks` 명령어로 태스크 상태 확인
3. 로그 확인: CloudWatch Logs에서 `/ecs/my-ecs-task` 그룹 확인

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] ECS 클러스터 (`MyECSCluster`)
- [ ] ECR 리포지토리 (`my-ecs-task`)
- [ ] Fargate 태스크 서비스 (`MyECSService`)

### 리소스 정리 명령어
```bash
# 1. ECR 리포지토리 삭제
aws ecr delete-repository --repository-name my-ecs-task --force

# 2. ECS 서비스 삭제
aws ecs delete-service --cluster MyECSCluster --service MyECSService

# 3. ECS 클러스터 삭제
aws ecs delete-cluster --cluster MyECSCluster
```

### 정리 완료 확인
```bash
# 리소스가 모두 삭제되었는지 확인
aws ecr describe-repositories
aws ecs list-clusters
aws ecs list-services
```

---

## 📚 추가 학습 자료
- [AWS ECS 공식 문서](https://docs.aws.amazon.com/ecs/)
- [AWS ECR 공식 문서](https://docs.aws.amazon.com/ecr/)
- [AWS Fargate 최적화 가이드](https://aws.amazon.com/fargate/guides/)
- [AWS Copilot 사용 가이드](https://copilot-cli.github.io/)