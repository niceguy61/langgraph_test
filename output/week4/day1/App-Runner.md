---

| [⬅️ ECR](./ECR.md) | [📑 Day 1 목차](./README.md) | [🏠 Week 4](../README.md) | [Copilot ➡️](./Copilot.md) |

---

# App Runner 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** App Runner는 컨테이너화된 애플리케이션을 쉽게 배포할 수 있도록 하는 AWS의 **서버리스 컨테이너 오케스트레이션 서비스**입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** ECS 클러스터 구성, Fargate 태스크 관리, ECR 이미지 보안 설정 등 복잡한 인프라 관리가 필요했습니다. 개발자는 컨테이너 이미지 생성, 네트워크 설정, 리소스 할당 등 모든 단계를 직접 관리해야 했습니다.  
- **문제 2:** ECS Anywhere를 활용한 하이브리드 배포 시, 온프레미스 서버와 클라우드 간의 통합 및 보안 설정이 복잡했습니다.  
- **문제 3:** EKS 컨트롤 플레인 및 노드 그룹 관리 시, 클러스터 확장, 자동 스케일링, IAM 정책 설정 등 고도화된 지식이 필요했습니다.  

**App Runner로 해결:**
- **해결 1:** App Runner는 ECS 클러스터, Fargate, ECR, EKS 등 복잡한 인프라를 추상화해 제공합니다. 개발자는 코드만 작성하면 자동으로 컨테이너가 실행됩니다.  
- **해결 2:** 하이브리드 배포 시 온프레미스 서버와의 통신을 자동으로 설정하고, 네트워크 보안을 최적화해 제공합니다.  
- **해결 3:** EKS를 사용하는 경우, App Runner는 자동으로 클러스터 생성, 노드 그룹 관리, IAM 정책 설정을 수행해 운영 부담을 줄입니다.  

### 비유로 이해하기
**App Runner는 요리사의 역할을 하는 서비스입니다.**  
개발자는 "레시피(코드)"만 작성하면, App Runner는 재료(컨테이너 이미지), 조리 방법(리소스 설정), 식탁 준비(네트워크 설정) 등을 모두 알아서 처리해 줍니다. 이로 인해 개발자는 애플리케이션의 기능에 집중할 수 있습니다.  

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | **마이크로서비스 아키텍처**에서 빠르게 배포하고 확장해야 할 경우 | eShopOnContainers 프로젝트에서 App Runner로 마이크로서비스 배포 |
| 시나리오 2 | **CI/CD 파이프라인 통합**을 원하는 경우 | GitHub Actions를 통해 App Runner에 배포 자동화 |
| 시나리오 3 | **하이브리드 클라우드 배포**를 고려하는 경우 | AWS 온프레미스 서버와 App Runner로 통합된 DB 서버 운영 |

**이럴 때 App Runner를 선택하세요:**
- ✅ **사용자 친화적인 배포**가 필요한 경우  
- ✅ **인프라 관리 부담을 줄이고자 할 때**  
- ✅ **하이브리드 클라우드 환경에서 운영을 원할 때**  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ **고성능 GPU 리소스가 필요한 경우** → **EC2 GPU 인스턴스**  
- ❌ **고도화된 네트워크 정책이 필요한 경우** → **VPC, AWS WAF**  
- ❌ **장기적인 인프라 관리가 필요한 경우** → **EKS, ECS 클러스터 직접 운영**  

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **ECR** | 컨테이너 이미지 저장소로 사용 | App Runner → ECR → Fargate |
| **CloudFront** | CDN을 통해 애플리케이션 전달 | User → CloudFront → App Runner |
| **RDS** | 데이터베이스 서버로 연동 | App Runner → RDS → Application Layer |

**자주 사용되는 아키텍처 패턴:**
```
User → CloudFront → App Runner → RDS
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **Compute Hours** | $0.0996 / hour | 월 120 hours 무료 |
| **Memory Usage** | $0.000043 / GB-hour | 12개월 무료 |
| **Data Transfer** | $0.09 / GB | 항상 무료 |

**비용 최적화 팁:**
1. 💡 **프리티어 활용:** 12개월 동안 무료로 사용 가능하므로, 초기 테스트에 적합합니다.  
2. 💡 **자동 확장 설정:** 트래픽 피크 시 자동으로 리소스 확장해 과다 사용을 방지합니다.  
3. 💡 **요청량 모니터링:** CloudWatch를 통해 실제 사용량을 분석해 비용 절감 전략 수립.  

> **⚠️ 비용 주의:** 고성능 애플리케이션은 트래픽 증가로 인해 예상치 못한 비용이 발생할 수 있습니다. **CloudFront 캐싱** 및 **요청량 제한 설정**으로 비용을 최소화해야 합니다.

## 📚 핵심 개념

### 개념 1: ECS 클러스터 구성 및 관리  
ECS( Elastic Container Service ) 클러스터는 컨테이너 작업을 실행하고 관리하는 AWS의 컨테이너 오케스트레이션 서비스입니다. 클러스터는 작업(task)을 실행할 EC2 인스턴스나 Fargate 호스팅 환경을 포함하며, 서비스(service)로 구성된 작업을 자동으로 스케줄링합니다. App Runner는 ECS 클러스터와 연동하여 컨테이너 애플리케이션을 배포하고, 자동 확장 및 리소스 관리를 통해 효율적인 운영을 지원합니다.  

#### 왜 중요한가?  
- **App Runner의 기반이 되는 인프라**  
  App Runner는 ECS 클러스터를 기반으로 애플리케이션을 실행하므로, 클러스터의 구성 방식과 관리 방법은 App Runner의 성능과 안정성에 직접적으로 영향을 미칩니다.  
- **리소스 최적화**  
  ECS 클러스터는 자동 스케일링과 리소스 할당을 통해 비용 효율성을 높이고, App Runner의 가상 머신 또는 Fargate 환경에서의 작업 실행을 간소화합니다.  

#### 세부 요소  
| 요소 | 설명 | 예시 |
|-----|------|---|
| **클러스터** | 컨테이너 작업을 실행하는 EC2 인스턴스 또는 Fargate 호스팅 환경 | `default` 클러스터 또는 `custom` 클러스터 |
| **작업 정의(Task Definition)** | 작업 실행에 필요한 컨테이너 이미지, 포트, 환경 변수 등을 정의한 템플릿 | `app-runner-task-definition.json` |
| **서비스(Service)** | 작업을 스케줄링하고 상태를 모니터링하는 데 사용 | `app-runner-service`로 작업을 자동 확장 |
| **리소스 정책(Resource Policy)** | 클러스터가 사용할 CPU/메모리 리소스의 제한을 설정 | `cpu: 256`, `memory: 512MB` |

> **💡 Tip:** App Runner는 ECS 클러스터를 기반으로 하므로, 클러스터의 리소스 제한을 설정해 과도한 비용을 방지해야 합니다. 예를 들어, Fargate 환경에서는 작업당 메모리/CPU를 미리 정의해 성능 최적화를 도모할 수 있습니다.

---

### 개념 2: EKS 컨트롤 플레인 및 노드 그룹  
EKS(Elastic Kubernetes Service)는 AWS에서 제공하는 관리형 Kubernetes 클러스터 서비스로, 컨트롤 플레인(control plane)과 노드 그룹(node groups)으로 구성됩니다. 컨트롤 플레인은 클러스터의 상태를 관리하고, 노드 그룹은 실제 컨테이너 작업을 실행하는 컴퓨팅 자원입니다. App Runner는 EKS를 통해 Kubernetes 기반 애플리케이션을 호스팅할 수 있으며, 자동 확장 및 리소스 관리를 통해 유연한 운영이 가능합니다.  

#### 작동 원리  
1. **컨트롤 플레인 초기화**  
   EKS는 AWS Managed Control Plane을 통해 Kubernetes API 서버, etcd, kubelet 등을 자동으로 구성합니다.  
2. **노드 그룹 생성 및 확장**  
   사용자는 EC2 노드 그룹을 생성하거나 Fargate를 사용해 Kubernetes 노드를 관리하며, 작업 증가 시 자동으로 노드를 확장합니다.  
3. **리소스 할당 및 작업 실행**  
   Kubernetes는 작업을 노드 그룹에 할당하고, App Runner는 이를 통해 컨테이너 애플리케이션을 실행합니다.  

> **💡 Tip:** EKS를 사용할 경우, App Runner의 컨테이너 작업은 Kubernetes의 자동 확장 기능을 활용해 트래픽 증가에 대응할 수 있습니다. 또한, Fargate를 선택하면 노드 관리 부담을 줄일 수 있습니다.

---

### 개념 3: Fargate 자동 확장 및 리소스 관리  
Fargate는 AWS에서 제공하는 관리형 컨테이너 실행 환경으로, 사용자가 인프라를 직접 관리하지 않아도 컨테이너 작업을 실행할 수 있습니다. App Runner는 Fargate를 통해 자동 확장 및 리소스 할당을 통해 트래픽 변화에 유연하게 대응할 수 있습니다. Fargate는 작업당 CPU/메모리 리소스를 정의하고, 필요 시 자동으로 작업을 확장해 성능을 최적화합니다.  

#### 주요 특징  
1. ****자동 확장(Auto Scaling)**  
   트래픽 증가 시 Fargate는 작업을 자동으로 확장해 성능을 유지하며, 트래픽 감소 시 작업을 축소해 비용을 절감합니다.  
2. ****Pay-As-You-Go 요금제**  
   작업당 리소스를 정의하고, 실제 사용량에 따라 요금이 청구됩니다. 비용을 최소화할 수 있습니다.  
3. ****노드 관리 없음**  
   사용자는 인프라를 직접 설정하지 않아도 Fargate가 자동으로 작업을 실행하고 리소스를 할당합니다.  

> **💡 Tip:** Fargate를 사용할 경우, App Runner의 컨테이너 작업은 리소스를 자동으로 최적화해 비용 절감과 성능 균형을 동시에 달성할 수 있습니다. 예를 들어, `cpu: 128`, `memory: 256MB`를 정의해 작업을 효율적으로 실행할 수 있습니다.

## 🖥️ AWS 콘솔에서 App Runner 사용하기

### Step 1: App Runner 서비스 접속  
1. **AWS Management Console 로그인**  
   - [https://console.aws.amazon.com](https://console.aws.amazon.com)으로 이동하여 AWS 계정에 로그인합니다.  
   - 로그인 후, 상단 메뉴에서 **"Services"**를 클릭하고 "App Runner"를 검색합니다.  

2. **App Runner 대시보드 열기**  
   - 검색 결과에서 **"App Runner"**를 클릭하면 대시보드가 표시됩니다.  
   - **AWS CLI**를 사용하는 경우, `aws apprunner list-services` 명령어로 서비스 목록을 확인할 수 있습니다.  

> **📸 화면 확인:** App Runner 대시보드가 표시되면 정상입니다. 왼쪽 메뉴에서 "Create service"를 클릭해 리소스 생성을 시작합니다.  

---

### Step 2: 리소스 생성 (App Runner 서비스 생성)  
1. **서비스 생성 화면 열기**  
   - "Create service" 버튼을 클릭하여 새 서비스를 생성합니다.  
   - **서비스 이름**: `my-app-runner-service` 등 원하는 이름 입력.  
   - **Description**: 서비스 설명을 입력합니다.  

2. **코드 저장소 선택**  
   - **Code repository**: GitHub, Bitbucket, AWS CodeCommit 등에서 코드 저장소를 선택합니다.  
   - **Branch**: 브랜치를 선택하거나, **Branch auto-detection**을 활성화해 자동 감지할 수 있습니다.  

3. **Compute platform 선택**  
   - **Fargate**를 선택해 App Runner가 Fargate를 사용하도록 설정합니다.  
   - Fargate는 ECS 클러스터에서 실행되며, App Runner가 이를 자동으로 관리합니다.  

> **📸 화면 확인:** "Create service" 화면에서 "Create" 버튼을 클릭해 서비스를 생성합니다.  

---

### Step 3: 설정 및 구성 (Fargate 태스크 배포)  
1. **ECS 클러스터 생성**  
   - App Runner는 Fargate를 사용하므로, ECS 클러스터는 자동으로 생성됩니다.  
   - **ECS 클러스터 이름**: `my-fargate-cluster` 형식으로 자동 생성됩니다.  

2. **ECR 리포지토리 연결**  
   - App Runner는 ECR(Amazon ECR)에서 이미지를 가져옵니다.  
   - **ECR 리포지토리**: GitHub Actions 또는 AWS CodeBuild를 통해 이미지를 빌드하고 ECR에 푸시해야 합니다.  

3. **Fargate 태스크 구성**  
   - App Runner는 Fargate 태스크를 자동으로 생성하고, 태스크는 ECS 클러스터에서 실행됩니다.  
   - **CPU/메모리**: App Runner UI에서 자동으로 최적화된 설정이 적용됩니다.  

> **⚠️ 주의:** Fargate 태스크는 ECS 클러스터에 종속되므로, ECS 클러스터가 삭제되면 Fargate 태스크도 함께 삭제됩니다.  

---

### Step 4: 설정 확인 및 테스트  
1. **생성된 리소스 확인**  
   - **App Runner 서비스**: 대시보드에서 서비스 이름을 클릭해 상태와 로그를 확인합니다.  
   - **ECS 클러스터**: **Services > ECS** 메뉴에서 생성된 클러스터를 확인합니다.  

2. **Fargate 태스크 상태 확인**  
   - **ECS Console**: "Tasks" 탭에서 태스크가 "RUNNING" 상태인지 확인합니다.  
   - **App Runner 로그**: "Logs" 탭에서 배포 과정의 로그를 확인합니다.  

3. **정상 동작 테스트**  
   - App Runner 서비스의 **URL**을 클릭해 애플리케이션을 직접 테스트합니다.  
   - **HTTP 테스트**: `curl https://<service-url>` 명령어로 응답 코드를 확인합니다.  

> **💡 Tip:** 프리티어는 750시간의 무료 사용량을 제공하므로, 테스트용으로 사용할 수 있습니다.  

---

### 📊 서비스 비교 및 가격 요약  
| 서비스         | 기능 설명                          | 비용 관리 방법               |  
|----------------|-----------------------------------|------------------------------|  
| App Runner     | Fargate 기반 컨테이너 배포          | AWS Cost Explorer 활용       |  
| ECS            | Fargate 태스크 실행 환경           | ECS 클러스터 관리            |  
| ECR            | 컨테이너 이미지 저장소             | ECR 리포지토리 관리          |  
| Fargate        | ECS 클러스터에서 실행되는 컴퓨팅    | 자동 스케일링 및 수요 기반 요금 |  

> **📌 주의:** Fargate는 AWS 프리티어에서 750시간까지 무료로 사용 가능합니다.

## ⌨️ AWS CLI로 App Runner 사용하기

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
AWS CLI를 사용하기 전에 버전을 확인하고, IAM 자격 증명이 정상적으로 설정되었는지, 그리고 현재 리전이 올바른지 확인해야 합니다.  
- `aws sts get-caller-identity` 명령어는 현재 사용자의 AWS 계정 ID, 유저명, 리전 정보를 확인합니다.  
- `aws configure get region`은 현재 설정된 리전을 확인합니다. App Runner는 리전에 따라 서비스가 제공되므로 정확한 리전 설정이 필수적입니다.

---

### 예제 1: App Runner 리소스 조회
```bash
# App Runner 서비스 목록 조회
aws apprunner list-services --query '[].ServiceArn' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|-----|--------|
| `--query '[].ServiceArn'` | 서비스 ARN 필터링 | `arn:aws:apprunner:us-east-1:123456789012:service/example-service` |
| `--output table` | 테이블 형식으로 출력 | `Status: active` |

**예상 출력:**
```
| ServiceArn                                           |
|------------------------------------------------------|
| arn:aws:apprunner:us-east-1:123456789012:service/... |
```

**팁:**  
`--query` 옵션을 사용해 특정 필드만 출력할 수 있으며, `--output json`으로 JSON 형식으로도 결과를 받아볼 수 있습니다.

---

### 예제 2: App Runner 리소스 생성
```bash
# App Runner 서비스 생성
aws apprunner create-service \
    --service-name "example-service" \
    --source-configuration "RepositoryUrl=https://github.com/example/repo,ImageConfiguration={ImageDigest=sha256:abc123}"
```

**필수 옵션:**
- `--service-name`: 서비스 이름 (예: `example-service`)
- `--source-configuration`: 소스 구성 (ECR 이미지 또는 GitHub 리포지토리 URL)

**예상 출력:**
```json
{
    "ServiceArn": "arn:aws:apprunner:us-east-1:123456789012:service/example-service",
    "Status": "ACTIVE"
}
```

**비용 주의사항:**  
- App Runner는 기본적으로 1개월간 $300 미만의 무료 트라이얼 제공 (AWS Free Tier)  
- ECR 이미지 저장소는 50GB 무료 제공  
- Fargate 태스크는 125,000초 (약 34시간) 무료 제공

---

### 예제 3: App Runner 리소스 수정
```bash
# App Runner 서비스 수정
aws apprunner update-service \
    --service-arn "arn:aws:apprunner:us-east-1:123456789012:service/example-service" \
    --configuration "ImageConfiguration={ImageDigest=sha256:xyz789}"
```

**옵션 설명:**  
- `--service-arn`: 수정할 서비스의 ARN  
- `--configuration`: 수정할 구성 (이미지 레이블 변경 등)

**팁:**  
App Runner 서비스 수정 시, `--configuration` 파라미터를 통해 이미지 레이블, 메타데이터 등을 변경할 수 있습니다.

---

### 예제 4: App Runner 리소스 삭제
```bash
# App Runner 서비스 삭제
aws apprunner delete-service --service-arn "arn:aws:apprunner:us-east-1:123456789012:service/example-service"

# 삭제 확인
aws apprunner describe-service --service-arn "arn:aws:apprunner:us-east-1:123456789012:service/example-service"
```

> **⚠️ 주의:** 삭제는 되돌릴 수 없습니다. 삭제 후에는 서비스 복구가 불가능합니다.  
> **🚨 확인 필수:** 삭제 전에 `describe-service` 명령어로 상태를 확인하세요.

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws apprunner list-services
aws apprunner describe-service --service-arn "arn:aws:apprunner:us-east-1:123456789012:service/..."

# 생성
aws apprunner create-service --service-name "example-service" --source-configuration "RepositoryUrl=https://github.com/example/repo"

# 수정
aws apprunner update-service --service-arn "arn:aws:apprunner:us-east-1:123456789012:service/..." --configuration "ImageConfiguration={ImageDigest=sha256:abc123}"

# 삭제
aws apprunner delete-service --service-arn "arn:aws:apprunner:us-east-1:123456789012:service/..."
```

**체크리스트:**  
- [ ] AWS CLI 버전 확인  
- [ ] IAM 자격 증명 설정  
- [ ] 리전 설정 확인  
- [ ] 서비스 생성 시 ECR 또는 GitHub 리포지토리 URL 제공  
- [ ] 삭제 전 서비스 상태 확인  
- [ ] 무료 트라이얼 기간 내 사용 여부 확인

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 App Runner 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **포인트 1**: **App Runner의 자동 확장 및 리소스 관리**  
   - 설명: App Runner는 CPU/메모리 사용량에 따라 자동으로 컴퓨팅 자원을 확장/축소해 비용 효율성을 극대화합니다. 이는 AWS에서 자동화된 컨테이너 서비스 운영의 핵심 개념으로, 시험에서 자동 확장 기능의 작동 방식과 리소스 관리 메커니즘을 묻는 경우가 많습니다.  
   - 키워드: `자동 확장`, `리소스 관리`

2. **포인트 2**: **App Runner의 소스 코드 통합 및 CI/CD 지원**  
   - 설명: App Runner는 GitHub, Bitbucket 등과 연동해 코드 변경 시 자동으로 배포를 수행합니다. 이는 DevOps 프로세스의 자동화와 CI/CD 파이프라인 구축에 대한 이해를 묻는 문제에 직접적으로 연결됩니다.  
   - 키워드: `CI/CD`, `소스 코드 통합`

3. **포인트 3**: **App Runner의 서버리스 아키텍처와 관리 부담 최소화**  
   - 설명: App Runner는 사용자가 컨테이너 관리, 네트워크 설정, 로드밸런서 운영 등 복잡한 관리 작업을 하지 않아도 서비스를 운영할 수 있도록 설계되었습니다. 이는 서버리스 서비스의 핵심 가치인 "0 마이그레이션" 개념을 시험에서 강조하는 주제입니다.  
   - 키워드: `서버리스`, `관리 부담`

4. **포인트 4**: **App Runner의 비용 최적화 구조**  
   - 설명: App Runner는 사용량 기반 요금제로, 실시간으로 필요한 자원만 결제하며, 과다 사용 시 비용 절감 효과가 있습니다. 이는 AWS 서비스 중에서 "비용 관리"와 "사용량 기반 요금제"를 묻는 시험 문제의 핵심 포인트입니다.  
   - 키워드: `사용량 기반 요금제`, `비용 최적화`

5. **포인트 5**: **App Runner의 네트워크 설정 및 보안 고려사항**  
   - 설명: App Runner는 VPC 통신을 지원하며, 네트워크 보안 정책(예: 방화벽 규칙)을 설정할 수 있습니다. 이는 서비스 보안과 네트워크 관리에 대한 이해를 묻는 시험 문제의 핵심 내용입니다.  
   - 키워드: `VPC`, `네트워크 보안`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | "App Runner는 Fargate와 동일한 기능을 가진다"는 문장으로 혼동하게 만듭니다. | App Runner는 Fargate와 달리 사용자가 컨테이너를 직접 관리하지 않으며, 자동 확장 기능이 포함되어 있습니다. |
| 함정 2 | "App Runner는 AWS Lambda와 같은 서버리스 서비스이지만, 코드 실행 환경을 직접 조정할 수 없다"는 문장으로 혼동하게 만듭니다. | App Runner는 코드 실행 환경을 제한적으로 커스터마이징할 수 있지만, Lambda처럼 완전한 서버리스 아키텍처가 아닙니다. |
| 함정 3 | "App Runner는 ECR 이미지 사용이 필수적이다"는 문장으로 혼동하게 만듭니다. | App Runner는 ECR 이미지 사용이 선택사항이며, Dockerfile을 직접 생성해 사용할 수 있습니다. |

#### 🔄 App Runner vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | App Runner | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | 빠른 프로토타입 배포 및 CI/CD 통합 | ECS/Fargate | 자동화된 배포 및 관리가 필요할 때 |
| 확장성 | 자동 확장, 사용량 기반 | 수동 확장, 고정 리소스 | 스케일링 자동화가 필수적일 때 |
| 비용 | 사용량 기반 요금제 | 고정 비용 또는 수동 리소스 관리 | 비용 최적화가 우선시될 때 |
| 지연시간 | 내장된 로드밸런서로 저지연 | 외부 로드밸런서 필요 | 저지연 서비스가 요구될 때 |

#### 📝 시험 대비 체크리스트
- [ ] App Runner의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  → "컨테이너 애플리케이션을 자동화된 방식으로 배포하고 관리하는 서버리스 서비스입니다."
- [ ] App Runner를 선택해야 하는 시나리오를 알고 있는가?  
  → CI/CD 통합, 빠른 프로토타입 배포, 비용 최적화가 필요한 경우
- [ ] App Runner의 제한사항/한계를 알고 있는가?  
  → 커스터마이징 제한, 고성능 요구 시 Fargate로 전환 필요
- [ ] App Runner와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  → App Runner는 자동화, Fargate는 수동 관리, ECS는 클러스터 기반 관리
- [ ] App Runner의 비용 구조를 이해하고 있는가?  
  → 사용량 기반 요금제, 과다 사용 시 비용 절감 효과

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 App Runner를 떠올리세요:  
> - **서버리스**  
> - **CI/CD 통합**  
> - **자동 확장**  
> - **비용 최적화**  
> - **VPC 통신**

---

| [⬅️ ECR](./ECR.md) | [📑 Day 1 목차](./README.md) | [🏠 Week 4](../README.md) | [Copilot ➡️](./Copilot.md) |

---
