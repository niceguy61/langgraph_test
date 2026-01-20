---

| [⬅️ 이전 Day](../../week3/day5/README.md) | [📑 Day 1 목차](./README.md) | [🏠 Week 4](../README.md) | [EKS ➡️](./EKS.md) |

---

# ECS 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** ECS는 Docker 컨테이너를 관리하고 배포하기 위한 AWS의 컨테이너 오케스트레이션 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 컨테이너 환경에서 수동으로 서비스 배포 및 관리해야 하며, 리소스 분배, 네트워킹, 로깅 등의 복잡한 작업이 필요했습니다.  
  예: Docker를 직접 사용할 때는 컨테이너 상태 모니터링, 자동 확장, 네트워크 설정 등을 수동으로 관리해야 했습니다.  

- **문제 2:** 클라우드 환경에서 컨테이너를 확장할 때 리소스를 예측할 수 없어 비용 과다 사용 또는 성능 저하가 발생했습니다.  
  예: 트래픽 증가 시 수동으로 인스턴스를 추가해야 하거나, 리소스 사용량이 불균형하게 증가했습니다.  

- **문제 3:** 컨테이너 이미지의 보안 및 접근 제어 관리가 복잡했습니다.  
  예: 다수의 개발자 및 서비스가 이미지를 사용할 때, IAM 정책을 수동으로 설정하고 관리해야 했습니다.  

**ECS로 해결:**
- **해결 1:** ECS는 컨테이너를 클러스터화해 자동으로 리소스 분배, 네트워킹, 로깅을 처리합니다.  
  예: Fargate를 사용하면 컨테이너 실행 시 네트워크, 보안 그룹 등을 자동으로 설정해 줍니다.  

- **해결 2:** ECS는 자동 확장 기능으로 트래픽 증가 시 리소스를 자동으로 조절해 비용을 최적화합니다.  
  예: ECS 서비스에서 CPU/메모리 사용량을 기준으로 태스크를 자동으로 확장해 줍니다.  

- **해결 3:** ECR(Amazon Elastic Container Registry)와 IAM 정책을 결합해 이미지의 보안 및 접근 제어를 간편하게 관리합니다.  
  예: 특정 사용자 그룹에게만 이미지 접근 권한을 부여할 수 있으며, 정책을 클러스터 전체에 적용할 수 있습니다.  

### 비유로 이해하기
ECS는 레스토랑 주방을 운영하는 주방장입니다. 각 요리(컨테이너)가 필요한 재료(리소스)와 조리 시간(태스크)을 정해두고, 주방장이 요리 순서를 조율하며 요리를 준비하고 나열합니다. 주방장은 요리가 완료되면 서버에게 전달하고, 필요 시 인력(리소스)을 추가해 효율적으로 운영합니다. 이처럼 ECS는 컨테이너를 효율적으로 조율하고 관리해줍니다.  

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 마이크로서비스 아키텍처에서 서비스를 관리하고 확장 | 금융 기업이 실시간 거래 처리 시스템을 구축해 ECS로 서비스를 관리 |
| 시나리오 2 | 배치 처리 작업을 자동화하고 리소스를 효율적으로 활용 | 데이터 분석 회사가 매일 밤 대량의 데이터를 처리하는 작업을 ECS로 자동화 |
| 시나리오 3 | 하이브리드 클라우드 환경에서 컨테이너를 운영 | 기업이 온프레미스 서버와 AWS 클라우드를 결합해 ECS Anywhere로 서비스 운영 |

**이럴 때 ECS를 선택하세요:**
- ✅ **컨테이너 오케스트레이션이 필요한 경우**  
- ✅ **자동 확장 및 리소스 최적화가 필요한 경우**  
- ✅ **하이브리드 클라우드 환경에서 컨테이너를 운영해야 할 때**  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ **Kubernetes를 기반으로 클러스터를 운영해야 할 때** → **EKS(Amazon EKS)** 추천 (Kubernetes 기반)  
- ❌ **서버리스 방식으로 빠르게 배포해야 할 때** → **App Runner** 추천 (서버리스 컨테이너 실행)  
- ❌ **저비용으로 단일 컨테이너 실행이 필요한 경우** → **Fargate** 추천 (지불 방식 유연)  

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **ECR** | 컨테이너 이미지를 저장하고 관리 | ECS → ECR → 컨테이너 실행 |
| **EKS** | Kubernetes 기반 클러스터를 운영 | EKS → ECS 서비스 통합 (예: EKS 클러스터에서 ECS 태스크 실행) |
| **App Runner** | 서버리스 방식으로 빠르게 배포 | App Runner → ECS 클러스터로 컨테이너 전달 |

**자주 사용되는 아키텍처 패턴:**
```
User → CloudFront → S3 → ECS → ECR → Fargate
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **ECS 클러스터 관리** | $0.000125/월 (Fargate 기준) | 월 12개월 무료 |
| **ECR 이미지 저장소** | $0.025/GB/월 | 월 12GB 무료 |
| **Fargate 태스크 실행** | $0.035/시간 (Linux) | 항상 무료 (단, 리소스 사용량 기준) |

**비용 최적화 팁:**
1. 💡 **Fargate를 사용해 수동 인스턴스 관리 비용 절감**  
   Fargate는 인스턴스 관리 없이 컨테이너 실행이 가능해 리소스 비용을 절감합니다.  
2. 💡 **클러스터 크기 최적화**  
   필요하지 않은 태스크를 제거하거나, 태스크 수를 줄여 리소스 사용량을 줄입니다.  
3. 💡 **ECR 이미지 최소화 및 압축**  
   이미지 크기를 줄이면 저장 비용과 전송 비용을 절감할 수 있습니다.  

> **⚠️ 비용 주의:** 데이터 전송 비용이나 ECR 이미지 저장 비용이 예상치 못하게 증가할 수 있습니다.  
  예: 대용량 이미지를 저장하거나, 데이터 전송량이 많은 경우 추가 비용이 발생할 수 있습니다.

## 📚 핵심 개념

### 개념 1: ECS 클러스터 구성 및 관리  
AWS ECS(Elastic Container Service)는 컨테이너화된 애플리케이션을 실행하고 관리하는 서비스입니다. 클러스터는 ECS에서 리소스를 분배하고 관리하는 기본 단위로, **EC2 호스트**, **Fargate** 등의 실행 환경을 포함합니다. 클러스터는 서비스와 태스크 단위로 구성되며, 태스크는 특정 컨테이너 이미지를 실행하는 작업을 나타냅니다.  

#### 왜 중요한가?  
- **확장성**: 클러스터를 통해 수천 개의 컨테이너를 유연하게 관리할 수 있습니다.  
- **자원 최적화**: EC2 호스트나 Fargate를 통해 CPU, 메모리 자원을 효율적으로 할당합니다.  

#### 세부 요소  
| 요소 | 설명 | 예시 |  
|-----|-----|-----|  
| 클러스터 유형 | EC2 호스트 기반 또는 Fargate 기반으로 구분 | `EC2` 클러스터는 EC2 인스턴스를 사용, `Fargate` 클러스터는 AWS 관리 호스트를 사용 |  
| 태스크 정의 | 컨테이너 이미지, 포트, 환경 변수 등을 정의 | `task-definition.json` 파일로 컨테이너 실행 조건 설정 |  
| 서비스 | 태스크를 지속적으로 실행하는 데 사용 | `ecs service` 명령어로 태스크를 자동으로 유지 |  

> **💡 Tip:** 클러스터 생성 시 `Fargate`를 선택하면 자동으로 리소스 관리를 위한 설정이 완료됩니다.  

---

### 개념 2: EKS 컨트롤 플레인 및 노드 그룹  
EKS(Elastic Kubernetes Service)는 Kubernetes 클러스터를 AWS에서 관리하는 서비스입니다. **컨트롤 플레인**은 Kubernetes의 핵심 구성 요소(예: API Server, Scheduler, etcd)로, 클러스터의 전체 상태를 관리합니다. **노드 그룹**은 EC2 인스턴스를 사용하여 실행되는 워커 노드 집합으로, 애플리케이션을 실행하는 데 사용됩니다.  

#### 작동 원리  
1. **컨트롤 플레인 생성**: AWS가 API Server, etcd 등 Kubernetes 핵심 컴포넌트를 관리합니다.  
2. **노드 그룹 설정**: 사용자가 EC2 인스턴스를 선택하거나 자동 생성하여 워커 노드를 구성합니다.  
3. **자동 확장**: 노드 그룹은 CPU/메모리 사용량에 따라 자동으로 스케일링됩니다.  

> **💡 Tip:** 노드 그룹을 생성할 때 `Auto Scaling Group`을 사용하면 트래픽 증가 시 자동으로 인스턴스를 추가할 수 있습니다.  

---

### 개념 3: Fargate 자동 확장 및 리소스 관리  
Fargate는 ECS의 관리형 컨테이너 실행 환경으로, 사용자가 EC2 인스턴스를 직접 관리할 필요가 없습니다. Fargate는 **리소스 자동 할당**, **스크래치 저장소**, **자동 확장** 등의 기능을 제공하여 애플리케이션 실행을 간소화합니다.  

#### 주요 특징  
1. **Pay-per-use**: 사용한 자원에만 요금이 청구되며, 비용 최적화에 유리합니다.  
2. **자동 확장**: 트래픽 증가 시 Fargate가 자동으로 실행 중인 태스크를 확장합니다.  
3. **스크래치 저장소**: 임시 파일 저장을 위한 메모리 공간을 제공하며, 종료 시 데이터가 삭제됩니다.  

> **💡 Tip:** Fargate를 사용할 때는 `Task Definition`에서 메모리와 CPU를 명확히 설정해 리소스 과다 사용을 방지하세요.  

--- 

### 개념 4: ECR 이미지 보안 및 IAM 정책  
ECR(Elastic Container Registry)는 Docker 이미지를 저장하고 관리하는 서비스로, **이미지 보안**과 **IAM 정책**을 통해 접근 제어를 제공합니다. ECR은 AWS KMS를 사용해 이미지 암호화를 지원하며, IAM 정책을 통해 특정 사용자가 특정 이미지에 접근할 수 있는 권한을 정의합니다.  

#### 왜 중요한가?  
- **보안 강화**: IAM 정책을 통해 이미지 접근 권한을 제한하여 내부 악성 사용자 방지.  
- **암호화**: KMS를 사용해 이미지 데이터를 암호화하여 데이터 유출 방지.  

#### 세부 요소  
| 요소 | 설명 | 예시 |  
|-----|-----|-----|  
| IAM 정책 | 사용자/그룹의 ECR 접근 권한 정의 | `aws iam attach-role-policy` 명령어로 정책 부착 |  
| KMS 암호화 | 이미지 데이터를 암호화하여 보안 강화 | `aws ecr put-image` 명령어로 암호화된 이미지 저장 |  

> **💡 Tip:** ECR에 저장된 이미지는 기본적으로 공개적으로 접근 가능하므로, `aws ecr put-image` 명령어를 사용할 때 `--image-tag`를 설정해 보안을 강화하세요.  

---

### 개념 5: ECS Anywhere 하이브리드 배포  
ECS Anywhere는 EC2 클러스터와 Fargate 클러스터를 결합해 **하이브리드 배포**를 가능하게 하는 기능입니다. EC2 인스턴스에서 실행되는 애플리케이션과 Fargate에서 실행되는 애플리케이션을 동일한 클러스터에서 관리할 수 있어, 네트워크, 로그, 모니터링 등에 대한 통일성을 제공합니다.  

#### 주요 특징  
1. **하이브리드 운영**: EC2와 Fargate를 병행해 사용할 수 있어 유연한 환경 구성.  
2. **리소스 최적화**: EC2 인스턴스를 직접 관리하면서도 Fargate의 자동 확장을 활용.  
3. **일관된 모니터링**: AWS CloudWatch를 통해 EC2와 Fargate의 리소스 사용량을 통합 모니터링.  

> **💡 Tip:** ECS Anywhere를 사용할 때는 EC2 인스턴스의 네트워크 설정을 정확히 확인해 애플리케이션 연결 오류를 방지하세요.

## 🖥️ AWS 콘솔에서 ECS 사용하기

### Step 1: ECS 서비스 접속
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
   - 로그인 후, 상단 메뉴에서 **Services**를 클릭하고 "ECS"를 검색합니다.  
2. 검색 결과에서 "ECS"를 클릭하여 대시보드로 이동합니다.  
   - **ECS 클러스터**, **서비스**, **태스크** 등 주요 리소스가 표시됩니다.  

> **📸 화면 확인:** ECS 대시보드가 표시되면 정상입니다.  
> **💡 Tip:** 처음 접속 시 "Clusters" 탭이 자동으로 열립니다.  

---

### Step 2: [주요 작업 1 - 리소스 생성]  
#### 1. ECS 클러스터 생성  
1. 왼쪽 메뉴에서 **Clusters** → **Create cluster** 클릭  
2. **Cluster type**에서 **Fargate**를 선택  
   - **EC2**는 EC2 인스턴스를 직접 관리하는 방식, **Fargate**는 AWS가 자동으로 인프라를 관리합니다.  
3. **Cluster name**을 입력하고, **Task execution role**을 선택합니다.  
   - 기본적으로 **ecsTaskExecutionRole**이 생성되지만, **Custom ARN**을 선택해 사용자 정의 역할을 지정할 수 있습니다.  
4. **VPC**를 선택하고, **Create** 버튼 클릭  

> **⚠️ 주의:** Fargate 사용 시 **Task execution role**이 필수입니다. 역할이 없으면 태스크가 실행되지 않습니다.  

#### 2. 태스크 정의 생성  
1. **Task Definitions** → **Create new task definition** 클릭  
2. **Task template**에서 **Fargate**를 선택  
3. **Container**를 추가하고, **Image**를 `httpd:latest` 또는 ECR 이미지로 입력  
4. **CPU/ Memory** 값을 설정하고, **Create** 버튼 클릭  

> **📸 화면 확인:** "Task Definition" 생성 화면에서 이미지와 리소스 설정이 정확히 입력되었는지 확인  

---

### Step 3: [주요 작업 2 - 설정/구성]  
#### 1. 서비스 생성  
1. **Services** → **Create service** 클릭  
2. **Cluster**를 선택하고, **Task definition**을 생성한 태스크 정의로 지정  
3. **Service name**을 입력하고, **Launch type**을 **Fargate**로 설정  
4. **Desired count**를 1로 설정하고, **Create** 버튼 클릭  

#### 2. 네트워크 설정  
1. 생성된 서비스를 클릭 후 **Network settings** 탭에서 **Public IP**를 활성화  
   - 외부에서 태스크에 접근할 수 있도록 설정해야 합니다.  
2. **Security groups**를 확인하고, 필요한 포트(예: 80)를 열어줍니다.  

> **⚠️ 주의:** Fargate 태스크는 VPC 내에서 실행되므로, **Security group**과 **Subnet** 설정이 정확해야 합니다.  

---

### Step 4: 설정 확인 및 테스트  
#### 1. 리소스 확인  
1. **Clusters** 탭에서 생성한 클러스터를 클릭  
2. **Tasks** 탭에서 태스크가 **RUNNING** 상태인지 확인  
   - **RUNNING** 상태가 아닐 경우, **Logs** 탭에서 오류를 확인합니다.  

#### 2. 태스크 로그 확인  
1. **Tasks** 탭에서 특정 태스크를 클릭  
2. **Logs** 탭에서 **CloudWatch Logs**로 이동  
3. **/var/log/httpd/access.log** 파일을 확인해 HTTP 요청이 정상적으로 처리되는지 확인  

#### 3. 외부 접근 테스트  
1. **Public IP**가 할당된 클러스터에서 **HTTP** 요청을 보내고, 응답이 정상인지 확인  
   - 예: `curl http://<public-ip>:80` 명령어 사용  

> **💡 Tip:** Fargate는 인프라 관리 부담을 줄이지만, **비용이 발생**합니다. 프리티어 사용 시 1년간 125시간까지 무료입니다.  
> **⚠️ 주의:** ECR 이미지를 사용할 경우, **ECR 리포지토리**를 연결해 이미지 레지스트리 설정을 확인하세요.  

--- 

### ✅ 실무 팁  
- **Fargate**는 EC2 대비 더 많은 관리 작업이 필요하지 않지만, **VPC 설정**은 필수입니다.  
- **ECR** 이미지 사용 시, **Task Definition**에서 이미지 URI를 `aws_account_id.dkr.ecr.region.amazonaws.com/repo:tag` 형식으로 입력해야 합니다.  
- **ECS Anywhere**는 EC2 없이 Fargate를 사용할 수 있도록 지원하지만, **AWS Graviton2** 인스턴스에서만 작동합니다.

## ⌨️ AWS CLI로 ECS 사용하기

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
- AWS CLI가 최신 버전 (2.0 이상) 설치되어야 합니다.
- AWS IAM 사용자 권한이 ECS 관련 작업 수행 권한을 포함해야 합니다.
- ECR 리포지토리 및 Fargate 서비스 사용을 위한 리전 설정이 완료되어야 합니다.

---

### 예제 1: ECS 클러스터 목록 조회
```bash
# ECS 클러스터 목록 조회
aws ecs list-clusters --query "clusters[]" --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| `--query` | JSON 결과 필터링 (예: `clusters[]`로 클러스터 목록 추출) | `"clusters[]"` |
| `--output` | 출력 형식 (table: 테이블 형식, json: JSON 형식) | `table` |

**예상 출력:**
```
CLUSTER_NAME     STATUS
my-cluster       ACTIVE
```

**팁:**  
- `--query`를 사용해 특정 필드만 추출할 수 있습니다.  
- `--output json`으로 전체 JSON 응답을 확인할 수 있습니다.

---

### 예제 2: ECS 클러스터 생성
```bash
# Fargate용 클러스터 생성
aws ecs create-cluster \
    --cluster-name "my-fargate-cluster" \
    --service-role "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole"
```

**필수 옵션:**
- `--cluster-name`: 클러스터 이름 (예: `my-fargate-cluster`)
- `--service-role`: Fargate 작업 실행을 위한 IAM 역할 ARN  
  (예: `arn:aws:iam::<account-id>:role/ecsTaskExecutionRole`)

**예상 출력:**
```json
{
    "cluster": {
        "clusterArn": "arn:aws:ecs:region:account-id:cluster/my-fargate-cluster",
        "clusterName": "my-fargate-cluster",
        "status": "ACTIVE"
    }
}
```

**주의사항:**  
- Fargate 클러스터 생성 시 `service-role`이 필수입니다.  
- IAM 역할은 `AmazonECSTaskExecutionRolePolicy` 정책을 포함해야 합니다.

---

### 예제 3: ECS 태스크 정의 생성 (Fargate)
```bash
# Fargate 태스크 정의 생성
aws ecs register-task-definition \
    --family "my-fargate-task" \
    --network-mode "awsvpc" \
    --cpu "256" \
    --memory "512" \
    --container-definitions '[{"name": "my-container", "image": "my-ecr-repo:latest", "cpu": "256", "memory": "512", "essential": true, "logConfiguration": [{"logDriver": "awslogs", "options": {"awslogs-group": "/ecs/my-fargate-task", "awslogs-region": "region", "awslogs-stream-prefix": "ecs"}}]}]'
```

**필수 옵션:**
- `--family`: 태스크 정의 가족 이름 (예: `my-fargate-task`)
- `--network-mode`: `awsvpc` (Fargate 사용 시 필수)
- `--cpu`/`--memory`: 컨테이너 리소스 할당량
- `--container-definitions`: JSON 형식의 컨테이너 정의 (ECR 이미지, 로그 설정 포함)

**팁:**  
- `--container-definitions`는 JSON 형식으로 전달해야 합니다.  
- 로그 설정 시 `awslogs` 드라이버를 사용해 CloudWatch 로그에 연결할 수 있습니다.

---

### 예제 4: ECS 태스크 실행 (Fargate)
```bash
# Fargate 태스크 실행
aws ecs run-task \
    --cluster "my-fargate-cluster" \
    --task-definition "my-fargate-task" \
    --launch-type "FARGATE" \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-12345678],securityGroups=[sg-12345678],assignPublicIp=TRUE}"
```

**필수 옵션:**
- `--cluster`: 생성한 클러스터 이름 (`my-fargate-cluster`)
- `--task-definition`: 등록한 태스크 정의 이름 (`my-fargate-task`)
- `--launch-type`: `FARGATE`로 지정 (Fargate 사용 시 필수)
- `--network-configuration`: VPC 설정 (subnet, security group 등 포함)

**예상 출력:**
```json
{
    "tasks": [
        {
            "taskArn": "arn:aws:ecs:region:account-id:task/my-fargate-task/1234567890abcdef",
            "lastStatus": "PROVISIONING"
        }
    ]
}
```

**주의사항:**  
- `--network-configuration`에서 `subnets`와 `securityGroups`는 생성한 VPC 설정을 기반으로 지정해야 합니다.  
- 태스크 실행 시 `RUNNING` 상태로 전환되면 정상적으로 작동합니다.

---

### 자주 사용하는 명령어 정리
```bash
# 클러스터 조회
aws ecs list-clusters
aws ecs describe-clusters --cluster-arns "arn:aws:ecs:region:account-id:cluster/my-fargate-cluster"

# 태스크 정의 관리
aws ecs register-task-definition --family my-task --container-definitions '[{"name": "my-container", "image": "my-ecr-repo:latest"}]'
aws ecs describe-task-definition --task-definition my-task

# 태스크 실행/관리
aws ecs run-task --cluster my-cluster --task-definition my-task --launch-type FARGATE
aws ecs describe-tasks --cluster my-cluster --tasks "arn:aws:ecs:region:account-id:task/my-task/1234567890abcdef"
```

**비용 주의사항:**  
- Fargate는 `per vCPU` 기준으로 요금이 청구됩니다.  
- `AWS Free Tier`는 1개의 Fargate 클러스터 및 256 vCPU/1024 MB 메모리 사용 시 1년간 무료입니다.  
- ECR 리포지토리 생성 후, `AWS Free Tier`로 500MB까지 무료로 이미지 저장 가능합니다.

**추천 실습:**  
1. ECR에 이미지 업로드 (aws ecr get-login --region region)  
2. Fargate 클러스터 생성  
3. 태스크 정의 등록 및 태스크 실행  
4. CloudWatch 로그 확인 (aws logs describe-log-groups)  
5. 태스크 종료 (aws ecs stop-task --task "arn:aws:ecs:region:account-id:task/my-task/1234567890abcdef")

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 ECS 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **ECS 클러스터 구성 및 관리**  
   - 설명: ECS 클러스터는 컨테이너 작업을 관리하는 기초 구조로, EC2 호스팅 및 Fargate 자동 확장 시 고정된 리소스 할당 방식을 이해해야 합니다. 시험에서 클러스터 타입 선택(예: EC2 vs Fargate)에 대한 분석 문제가 자주 출제됩니다.  
   - 키워드: `클러스터 타입`, `리소스 할당`, `EC2`, `Fargate`

2. **Fargate 자동 확장 및 리소스 관리**  
   - 설명: Fargate는 서버리스 방식으로 리소스를 자동으로 확장하지만, CPU/메모리 사용량 기반의 스크알링 및 태스크 최대 수 제한을 반드시 파악해야 합니다. 시험에서는 Fargate의 유연성과 한계를 비교하는 문제가 자주 등장합니다.  
   - 키워드: `서버리스`, `스케일링`, `리소스 제한`, `태스크 수`

3. **ECR 이미지 보안 및 IAM 정책**  
   - 설명: ECR에서 이미지 저장소의 접근 제어(IAM 정책)와 스캔 기능(예: AWS ECR Image Scanning)은 보안 사고 예방에 핵심입니다. 시험에서는 ECR의 보안 설정과 공개/사용자 권한 관리 문제를 다룹니다.  
   - 키워드: `IAM 정책`, `이미지 스캔`, `공개 저장소`, `사용자 권한`

4. **ECS Anywhere 하이브리드 배포**  
   - 설명: ECS Anywhere는 온프레미스 서버와 클라우드 간의 하이브리드 배포를 지원하며, 이는 네트워크 설정 및 리소스 통합 관리의 복잡성을 시험에서 평가합니다. 시험에서는 랜섬웨어 방지와 같은 보안 관련 사례가 자주 등장합니다.  
   - 키워드: `하이브리드`, `네트워크 통합`, `온프레미스`, `보안 정책`

5. **EKS 컨트롤 플레인 및 노드 그룹**  
   - 설명: EKS는 Kubernetes를 기반으로 하며, 컨트롤 플레인의 고가용성과 노드 그룹 관리 방식은 클러스터 구성 시 필수 사항입니다. 시험에서는 EKS의 확장성과 ECS의 비교 문제를 포함합니다.  
   - 키워드: `컨트롤 플레인`, `노드 그룹`, `Kubernetes`, `확장성`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | ECS 클러스터 타입 선택 시 EC2 vs Fargate의 구분이 모호함 | Fargate는 서버리스로 리소스 자동 확장, EC2는 수동 리소스 할당 |
| 함정 2 | ECR 이미지 스캔 기능의 활성화 여부를 묻는 문제에서 기본 설정 오인 | 기본적으로 스캔 기능은 활성화되어 있으나, 정책 설정 필요 |
| 함정 3 | ECS Anywhere의 온프레미스 서버 요구사항을 오해 | 호스트 기반 서버가 필요하며, AWS 기존 인프라와 통합 필요 |

#### 🔄 ECS vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | ECS | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| **용도** | EC2/EC2 Auto Scaling, Fargate 서버리스 | EKS(Kubernetes), Fargate, ECR, App Runner | EC2/EC2 Auto Scaling: 고정 리소스, Fargate: 서버리스, EKS: Kubernetes 기반, App Runner: 단순 애플리케이션 |
| **확장성** | Fargate 자동 확장, EC2 수동 확장 | EKS: Kubernetes의 빌드인 확장성, App Runner: 서버리스 자동 확장 | 리소스 자동 확장 필요 시 Fargate/App Runner, Kubernetes 기반 시 EKS |
| **비용** | EC2 리소스 비용 + Fargate 스크알링 요금 | EKS: 관리 비용, Fargate: 리소스 기반 요금, App Runner: 요청 기반 요금 | 고정 리소스 필요 시 EC2, 서버리스 필요 시 Fargate/App Runner |
| **지연시간** | Fargate: 빠른 스타트, EC2: 리소스 기반 지연 | EKS: 빌드 시간, App Runner: 요청 처리 시간 | 저지연 처리 필요 시 Fargate, 복잡한 애플리케이션 시 EKS |

#### 📝 시험 대비 체크리스트
- [ ] ECS의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  (예: "컨테이너 작업을 관리하고 확장 가능한 클러스터 환경 제공")
- [ ] ECS를 선택해야 하는 시나리오를 알고 있는가?  
  (예: EC2 자원 제어 필요, Fargate 자동 확장 필요, 하이브리드 배포 필요)
- [ ] ECS의 제한사항/한계를 알고 있는가?  
  (예: EC2 자원 관리 복잡성, Fargate 리소스 제한, ECR 이미지 스캔 설정 필요)
- [ ] ECS와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  (예: EKS는 Kubernetes 기반, App Runner는 단순 애플리케이션 실행)
- [ ] ECS의 비용 구조를 이해하고 있는가?  
  (예: EC2 리소스 비용 + Fargate 스크알링 요금, ECR 이미지 스캔 설정 영향)

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 ECS를 떠올리세요:  
> - **클러스터 타입** (EC2, Fargate)  
> - **리소스 자동 확장** (Fargate)  
> - **이미지 보안** (ECR)  
> - **하이브리드 배포** (ECS Anywhere)  
> - **컨트롤 플레인** (EKS)

---

| [⬅️ 이전 Day](../../week3/day5/README.md) | [📑 Day 1 목차](./README.md) | [🏠 Week 4](../README.md) | [EKS ➡️](./EKS.md) |

---
