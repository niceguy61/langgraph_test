---

| [⬅️ 이전 Day](../day4/README.md) | [📑 Day 5 목차](./README.md) | [🏠 Week 1](../README.md) | [Auto Scaling ➡️](./Auto-Scaling.md) |

---

# ELB 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** ELB는 **고가용성 및 확장성**을 위한 AWS의 **로드 밸런서** 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 단일 EC2 인스턴스에 모든 트래픽을 집중시켜 **단일 고장점(Single Point of Failure)**을 초래합니다. 예를 들어, 인스턴스가 다운되면 전체 서비스가 중단됩니다.
- **문제 2:** 트래픽 증가 시 수동으로 인스턴스를 추가해야 하며, **스케일링을 자동화할 수 없습니다.** 이로 인해 지연 시간이 길어지고 고객 불만이 발생할 수 있습니다.
- **문제 3:** 트래픽 분배가 불균형해지면 일부 서버에 과도한 부하가 가해져 **성능 저하**나 **서비스 중단** 위험이 있습니다.

**ELB로 해결:**
- **해결 1:** ALB/NLB/GLB 등 다양한 로드 밸런서 유형을 통해 **다중 인스턴스에 트래픽을 균일하게 분배**해 단일 고장점 문제를 해결합니다.
- **해결 2:** Auto Scaling과 연동해 **트래픽 변화에 따라 자동으로 인스턴스 수를 조절**해 시스템이 유동적으로 확장됩니다.
- **해결 3:** 상태 검사와 대상 그룹을 통해 **건강한 인스턴스만 트래픽을 처리**하고, 비정상 인스턴스는 자동으로 배제해 서비스 가용성을 보장합니다.

### 비유로 이해하기
ELB는 도로 교통을 관리하는 **도로교통청** 같은 역할을 합니다. 예를 들어, 특정 구간의 교통 혼잡이 발생하면 트래픽을 다른 길로 분배해 차량 이동을 원활하게 합니다. 마찬가지로 ELB는 사용자 요청을 여러 EC2 인스턴스에 균형 있게 분배해 서버 부하를 줄이고, 단일 서버 고장 시 다른 서버로 트래픽을 이동시켜 서비스 중단을 방지합니다.

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 대규모 트래픽을 처리해야 할 때 | 온라인 쇼핑몰의 할인 이벤트 기간에 트래픽을 분산해 서비스 안정성 확보 |
| 시나리오 2 | 고가용성을 요구하는 시스템 | 클라우드 서버에서 24/7 운영하는 애플리케이션의 높은 가용성 보장 |
| 시나리오 3 | 동적인 스케일링이 필요한 환경 | 사용자 수가 시간에 따라 급변하는 SaaS 플랫폼의 자동 확장/축소 |

**이럴 때 ELB를 선택하세요:**
- ✅ **트래픽이 급증하거나 감소하는 환경**에서 실시간으로 인스턴스 수를 조절해야 할 때
- ✅ **고가용성과 서비스 중단 없는 운영**이 필수적인 시스템에서
- ✅ **다양한 서버 유형(예: EC2, Lambda)과 혼합 배포**가 필요한 복잡한 아키텍처에서

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ **단일 서버에서 처리 가능한 작은 규모 서비스** → EC2 또는 Lambda로 대체
- ❌ **고정된 인스턴스 수로 운영** → Auto Scaling 없이 ELB 사용
- ❌ **트래픽이 매우 낮은 경우** → AWS의 무료 서비스(예: Lambda)로 대체

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **Auto Scaling** | 인스턴스 수를 자동으로 조절해 ELB의 스케일링 정책을 실행 | ELB → Auto Scaling Group → EC2 인스턴스 |
| **Target Group** | ELB가 트래픽을 전달할 대상 서버 그룹을 정의 | ELB → Target Group → EC2 인스턴스 |
| **CloudFront** | CDN을 통해 ELB 전에 트래픽을 가속화해 대역폭 절약 | CloudFront → ELB → EC2 인스턴스 |

**자주 사용되는 아키텍처 패턴:**
```
User → CloudFront → ELB → Auto Scaling Group → EC2 인스턴스
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **ALB(NLB) 사용량** | $0.025/시간(ALB) ~ $0.025/시간(NLB) | 월 120시간 무료 |
| **상태 검사 요청** | $0.005/요청 | 12개월 무료 |
| **대상 그룹 기능 사용** | $0.005/요청 | 항상 무료 |

**비용 최적화 팁:**
1. 💡 **프리티어 활용:** 12개월간 무료로 ALB/NLB를 사용해 비용을 절감하세요.
2. 💡 **트래픽 분석:** AWS CloudWatch를 통해 트래픽 패턴을 분석해 과도한 인스턴스 수를 줄이세요.
3. 💡 **적절한 ELB 유형 선택:** ALB는 HTTP/HTTPS, NLB는 TCP/UDP 트래픽에 적합하며, 사용 사례에 맞게 선택해 비용을 줄이세요.

> **⚠️ 비용 주의:** **트래픽이 급증**하거나 **대규모 인스턴스 그룹**이 필요한 경우, 예상치 못한 비용이 발생할 수 있으므로 **CloudWatch를 활용한 모니터링**과 **Auto Scaling 정책 최적화**가 필수적입니다.

## 📚 핵심 개념

### 개념 1: **ELB의 타입 차이 (ALB/NLB/GLB/CLB)**
ELB(ELastic Load Balancer)는 네트워크 트래픽을 백엔드 인스턴스에 분배하는 기능을 제공하지만, **ALB( Application Load Balancer ), NLB( Network Load Balancer ), GLB( Global Accelerator ), CLB( Classic Load Balancer )**는 각각 다른 목적과 기능을 가진 타입입니다.  
ALB는 HTTP/HTTPS 트래픽을 처리하고, URL 기반의 요청 분배가 가능하며, 애플리케이션 레벨에서 트래픽을 관리합니다. NLB는 TCP/UDP 트래픽을 처리하고, 고가용성 네트워크 환경에서 고성능이 필요할 때 사용됩니다. GLB는 글로벌 트래픽을 최적화해 지역별 리전에 따라 트래픽을 분배하며, 지연 시간을 최소화합니다. CLB는 기존 클래식 ELB의 기능을 유지하지만, AWS에서 **2021년 12월에 폐지**되었습니다.  

#### 왜 중요한가?
- **업무 목적에 맞는 타입 선택**: ALB는 웹 애플리케이션, NLB는 랜섬웨어 방지, GLB는 글로벌 사용자 대응, CLB는 호환성 유지가 필요할 때 사용  
- **비용 효율성**: GLB는 데이터 전송 비용을 절감하고, ALB는 애플리케이션 로직에 적합한 트래픽 관리 가능  

#### 세부 요소
| 요소 | 설명 | 예시 |
|-----|-----|-----|
| **ALB** | HTTP/HTTPS 트래픽 처리, URL 기반 분배 | 웹 애플리케이션에 URL 경로별 요청 분배 |
| **NLB** | TCP/UDP 트래픽 처리, 고성능 네트워크 | 랜섬웨어 방지, 대규모 데이터 전송 |
| **GLB** | 글로벌 트래픽 최적화, 지역 리전 분배 | 글로벌 사용자에게 지역별 서버로 트래픽 전달 |
| **CLB** | 기존 ELB 기능 유지, 2021년 폐지 | 호환성 유지용으로 사용 (더 이상 권장되지 않음) |

> **💡 Tip:** 신규 프로젝트에서는 **ALB 또는 GLB**를 선택하고, CLB는 유지보수 목적으로만 사용하세요.  

---

### 개념 2: **대상 그룹( Target Group ) 구성 및 상태 검사**
대상 그룹은 ELB가 트래픽을 분배할 대상 인스턴스를 관리하는 논리적 그룹입니다. 상태 검사는 대상 인스턴스의 건강 상태를 확인하여 고가용성 보장합니다.  
대상 그룹을 구성할 때는 **포트**, **프로토콜**, **건강 체크 경로** 등을 정의해야 합니다. 상태 검사는 **HTTP/HTTPS** 또는 **TCP** 기반으로 수행되며, 실패 시 트래픽이 다른 인스턴스로 전환됩니다.  

#### 작동 원리
1. **대상 인스턴스 등록**: EC2 인스턴스를 대상 그룹에 등록하고, 포트와 프로토콜을 설정합니다.  
2. **건강 체크 수행**: ELB가 설정된 경로(예: `/health` URL) 또는 포트(예: 8080)를 주기적으로 점검합니다.  
3. **트래픽 전환**: 상태가 "UNHEALTHY"인 인스턴스는 트래픽에서 제외되고, 다른 건강한 인스턴스로 전환됩니다.  

> **💡 Tip:** 상태 검사 주기는 기본적으로 5초, 최대 10초로 설정할 수 있습니다. 고가용성 요구가 높은 시스템에서는 **HTTP 상태 코드**를 기준으로 검사를 조정하세요.  

---

### 개념 3: **Auto Scaling 그룹(Auto Scaling Group) 운영 원리**
Auto Scaling 그룹은 자동으로 인스턴스 수를 조절해 트래픽 변화에 유연하게 대응합니다. **조정 정책(Scaling Policy)**은 CPU 사용률, 네트워크 트래픽 등 특정 조건이 발생할 때 인스턴스를 추가/삭제하는 규칙입니다.  
Auto Scaling은 **Launch Templates**와 연동되어 인스턴스 구성(예: CPU/메모리, OS, 스토리지)을 일관되게 관리합니다. 이는 자동화된 확장성과 비용 효율성을 제공합니다.  

#### 주요 특징
1. ****자동 확장**: 트래픽 증가 시 인스턴스를 자동으로 추가해 요청 처리 능력을 확장합니다.  
2. ****동적 조정**: CPU 사용률, 네트워크 대역폭 등 실시간 지표에 따라 인스턴스 수를 조절합니다.  
3. ****Launch Templates 통합**: 인스턴스 스펙을 일관되게 정의해 리소스 관리 효율성을 높입니다.  

> **💡 Tip:** 조정 정책은 **CloudWatch 알람**과 연동해 특정 임계값을 초과할 때만 실행되도록 설정하세요. 비용 절감을 위해 **예약 인스턴스**와 결합하여 사용하세요.

## 🖥️ AWS 콘솔에서 ELB 사용하기

### Step 1: ELB 서비스 접속  
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
   - 로그인 후 **Services** 메뉴에서 **ELB**를 검색합니다  
2. 검색 결과에서 **ELB**를 클릭해 대시보드로 이동합니다  
   - **ELB**는 **Elastic Load Balancing**의 약자로, 네트워크 트래픽을 인스턴스 그룹에 분산하는 서비스입니다  
   - 대시보드에는 **Load Balancers**, **Target Groups**, **Health Checks** 등의 리소스 목록이 표시됩니다  

> **📸 화면 확인:** ELB 대시보드가 표시되면 정상입니다. **Load Balancers** 탭에서 생성한 리소스를 확인할 수 있습니다  

---

### Step 2: [주요 작업 1 - 리소스 생성]  
1. **Load Balancer 생성**  
   - **Actions > Create Load Balancer** 버튼을 클릭합니다  
   - **Classic Load Balancer (CLB)**, **Application Load Balancer (ALB)**, **Network Load Balancer (NLB)** 중 선택합니다  
     - **CLB**: HTTP/HTTPS 트래픽 처리 (Legacy)  
     - **ALB**: HTTP/HTTPS/UDP 트래픽 처리 (사용자 친화적)  
     - **NLB**: TCP/UDP 트래픽 처리 (저지연 환경)  
   - **VPC**, **Subnets**, **Security Groups**를 선택해 네트워크 설정을 구성합니다  
2. **Listener 구성**  
   - **Protocols** (HTTP/HTTPS) 및 **Port** (80/443)를 설정합니다  
   - **Default Action**에서 **Forward to Target Group**를 선택합니다  
3. **Target Group 생성**  
   - **Create Target Group** 버튼을 클릭해 **Health Check** 설정을 구성합니다  
     - **Protocol**: HTTP/HTTPS  
     - **Port**: 애플리케이션 포트 (예: 8080)  
     - **Path**: 상태 검사 경로 (예: `/health`)  
     - **Timeout**: 5초로 설정  

> **📸 화면 확인:** **Target Group** 생성 후 **Health Check** 설정이 제대로 입력되었는지 확인합니다  

---

### Step 3: [주요 작업 2 - 설정/구성]  
1. **Target Group 연결**  
   - 생성한 **Target Group**을 **Load Balancer**에 연결합니다  
   - **Actions > Edit** → **Target Group** 선택 → **Attach** 버튼 클릭  
2. **Health Check 조정**  
   - **Health Check** 설정을 수정할 수 있습니다  
   - **Interval**, **Timeout**, **Unhealthy Threshold**, **Healthy Threshold** 값을 조정해 인스턴스 상태를 정확히 감지합니다  
3. **Auto Scaling 연동**  
   - **Auto Scaling Group (ASG)**과 **Target Group**을 연결해 자동 확장 기능을 활성화합니다  
   - **Actions > Attach to Auto Scaling Group** → ASG 선택 → **Attach**  

> **⚠️ 주의:** 상태 검사 설정이 잘못되면 인스턴스가 정상적으로 작동하더라도 **Unhealthy**로 판단될 수 있습니다. 애플리케이션의 실제 포트와 경로를 정확히 입력해야 합니다  

---

### Step 4: 설정 확인 및 테스트  
1. **리소스 상태 확인**  
   - **ELB 대시보드**에서 **Load Balancers** 목록을 확인합니다  
   - **Status**가 **Active**인지, **Health Check** 상태가 **Healthy**인지 확인합니다  
2. **트래픽 테스트**  
   - **ELB DNS 이름**을 브라우저에 입력해 트래픽이 정상적으로 분산되는지 확인합니다  
   - **HTTP 상태 코드 200**이 반환되면 정상입니다  
3. **CLI로 상태 확인**  
   - CLI 명령어로 상태를 확인할 수 있습니다  
     ```bash
     aws elbv2 describe-load-balancers --load-balancer-arns <ELB_ARN>
     aws elbv2 describe-target-health --target-group-arn <TARGET_GROUP_ARN>
     ```  
   - **Describe Load Balancers** 명령어로 생성된 리소스 목록을 확인할 수 있습니다  

> **💡 Tip:** AWS Free Tier은 1개의 **ALB** 및 1개의 **Target Group**을 제공합니다. 프리티어 사용 시, 1년간 무료로 사용할 수 있습니다.

## ⌨️ AWS CLI로 ELB 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

> **💡 Tip:** AWS CLI를 사용하기 전에 `aws configure` 명령어로 액세스 키, 시크릿 키, 리전, 스토리지 클래스를 설정해야 합니다.  
> **⚠️ 주의:** CLI 명령어 실행 전에 `--region` 파라미터를 명시적으로 지정하는 것이 안전합니다.

---

### 예제 1: ELB 리소스 조회
```bash
# [ELB 리소스 목록 조회]
aws elbv2 list-load-balancers --query '[].LoadBalancerName' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| `--query` | 결과 필터링 | `'[].LoadBalancerName'` |
| `--output` | 출력 형식 | `json`, `table`, `text` |

**예상 출력:**
```
| LoadBalancerName |
|------------------|
| example-elb      |
| another-elb      |
```

> **💡 Tip:** `--query`를 사용해 특정 필드만 출력하거나, `--output json`으로 전체 JSON 데이터를 확인할 수 있습니다.

---

### 예제 2: ELB 리소스 생성
```bash
# [ELB 생성]
aws elbv2 create-load-balancer \
    --name "example-elb" \
    --subnets subnet-12345678 subnet-87654321 \
    --security-groups sg-12345678 \
    --type application
```

**필수 옵션:**
- `--name`: ELB 이름 (예: `example-elb`)
- `--subnets`: VPC 서브넷 목록 (예: `subnet-12345678`)
- `--security-groups`: 보안 그룹 (예: `sg-12345678`)
- `--type`: `application` (ALB) 또는 `network` (NLB)

**예상 출력:**
```json
{
    "LoadBalancers": [
        {
            "LoadBalancerName": "example-elb",
            "LoadBalancerArn": "arn:aws:elasticloadbalancing:region:account-id:loadbalancer/example-elb",
            "DNSName": "example-elb.region.elb.amazonaws.com",
            "VpcId": "vpc-12345678"
        }
    ]
}
```

> **💡 Tip:** `--type`을 `network`로 설정하면 NLB를 생성할 수 있습니다.  
> **⚠️ 주의:** 서브넷과 보안 그룹은 VPC 설정과 일치해야 합니다.

---

### 예제 3: ELB 리소스 수정
```bash
# [ELB 속성 수정]
aws elbv2 update-load-balancer-attributes \
    --load-balancer-arn arn:aws:elasticloadbalancing:region:account-id:loadbalancer/example-elb \
    --attributes "AccessLogs.S3BucketName=example-bucket"
```

**수정 가능한 속성 예시:**
- `AccessLogs.S3BucketName`
- `AccessLogs.S3Prefix`
- `IdleTimeoutTimeoutSeconds`
- `CrossZoneLoadBalancing.Enabled`

> **💡 Tip:** `--attributes`는 JSON 형식의 키-값 쌍을 전달해야 합니다.

---

### 예제 4: ELB 리소스 삭제
```bash
# [ELB 삭제]
aws elbv2 delete-load-balancer \
    --load-balancer-arn arn:aws:elasticloadbalancing:region:account-id:loadbalancer/example-elb

# 삭제 확인
aws elbv2 describe-load-balancers --load-balancer-arns arn:aws:elasticloadbalancing:region:account-id:loadbalancer/example-elb
```

**예상 출력 (삭제 후):**
```
{
    "LoadBalancers": []
}
```

> **⚠️ 주의:** 삭제된 리소스는 복구 불가능합니다. 삭제 전에 `describe-load-balancers`로 상태를 확인하세요.

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws elbv2 list-load-balancers
aws elbv2 describe-load-balancers --load-balancer-arns "arn"

# 생성
aws elbv2 create-load-balancer --name "name" --subnets "subnet" --security-groups "sg" --type "application"

# 수정
aws elbv2 update-load-balancer-attributes --load-balancer-arn "arn" --attributes "key=value"

# 삭제
aws elbv2 delete-load-balancer --load-balancer-arn "arn"
```

> **💡 Tip:** CLI로 ELB를 관리하면 자동화 스크립트 작성과 비용 최적화에 유리합니다.  
> **⚠️ 주의:** `--load-balancer-arn` 파라미터는 리소스 삭제 시 필수입니다.  

---

### CLI 사용 시 주의사항
| 항목 | 설명 |
|-----|-|
| **비용 관리** | ELB는 요청 수에 따라 요금이 발생하므로, `--idle-timeout`을 적절히 설정해 비용을 절감하세요. |
| **프리티어 활용** | ALB/NLB 생성 시 `--type application` 또는 `--type network`로 기본 사양으로 생성해 무료 사용 기간을 활용하세요. |
| **오류 대처** | `InvalidSubnetID` 또는 `InvalidSecurityGroup` 오류가 발생하면 VPC 설정을 다시 확인하세요. |

> **💡 Tip:** AWS CLI는 자동화 스크립트 작성에 매우 유용하며, `aws configure set region`으로 리전을 변경해 다양한 환경에서 테스트할 수 있습니다.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 ELB 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **포인트 1**: ALB/NLB/GLB/CLB 차이점  
   - 설명: ELB의 주요 유형인 Application Load Balancer(ALB), Network Load Balancer(NLB), Gateway Load Balancer(GLB), Classic Load Balancer(CLB)는 트래픽 처리 방식과 사용 시나리오에서 근본적인 차이가 존재합니다. ALB는 HTTP/HTTPS 기반의 애플리케이션 레벨 밸런싱, NLB는 TCP/UDP 레벨의 네트워크 레벨 밸런싱, GLB는 글로벌 트래픽 분산, CLB는 전통적인 스탠다드 레벨 밸런싱을 제공합니다. 이 차이를 이해하지 못하면 시험에서 혼동하게 됩니다.  
   - 키워드: `트래픽 레벨`, `HTTP/HTTPS`, `TCP/UDP`, `글로벌 밸런싱`, `클래식 밸런싱`

2. **포인트 2**: 대상 그룹( Target Group ) 구성 및 상태 검사  
   - 설명: 대상 그룹은 ELB가 연결할 인스턴스를 관리하는 핵심 구성 요소로, 상태 검사는 서비스 가용성과 트러블슈팅에 필수적입니다. 상태 검사 실패 시 자동으로 트래픽을 제외시키는 "Health Check" 메커니즘은 AWS에서 높이 평가하는 핵심 개념입니다.  
   - 키워드: `상태 검사`, `건강 상태`, `대상 그룹`, `트래픽 제외`, `자동 복구`

3. **포인트 3**: Auto Scaling 그룹(Auto Scaling Group) 운영 원리  
   - 설명: ELB는 Auto Scaling 그룹과 연동되어 트래픽 증가 시 자동으로 인스턴스를 확장하고, 감소 시 축소합니다. 이 연동은 시스템의 가용성과 비용 효율성을 동시에 보장하며, 시험에서 자주 묻는 "ELB와 Auto Scaling의 상호작용"을 이해하는 것이 필수적입니다.  
   - 키워드: `자동 확장`, `인스턴스 조정`, `트래픽 동적 관리`, `가용성 보장`

4. **포인트 4**: 조정 정책(Scaling Policy) 타입 및 트리거 조건  
   - 설명: Auto Scaling 정책은 CPU 사용률, 네트워크 트래픽, ELB의 연결 수 등 다양한 메트릭을 기반으로 트리거됩니다. "Target Tracking Scaling Policy"와 "Scheduled Scaling Policy"는 시험에서 자주 비교되는 개념으로, 각각의 동작 방식과 사용 시나리오를 정확히 구분해야 합니다.  
   - 키워드: `트래픽 메트릭`, `타겟 트래킹`, `정기적 조정`, `트리거 조건`, `자원 최적화`

5. **포인트 5**: Launch Templates의 인스턴스 구성 정의 방법  
   - 설명: Launch Template는 Auto Scaling 그룹에 인스턴스를 생성할 때 사용하는 템플릿으로, 인스턴스 유형, 보안 그룹, 볼륨 설정 등을 정의합니다. 이는 ELB와 Auto Scaling의 통합 운영에서 필수적인 구성 요소로, 시험에서 인스턴스 자동화 설정을 묻는 경우 반드시 포함됩니다.  
   - 키워드: `인스턴스 템플릿`, `자동화 구성`, `보안 그룹`, `볼륨 설정`, `일관성 관리`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | ALB와 NLB의 차이를 혼동해 "트래픽 레벨"을 잘못 판단 | ALB는 HTTP/HTTPS 레벨, NLB는 TCP/UDP 레벨로 처리 |
| 함정 2 | 상태 검사 실패 시 "트래픽 제외"가 아닌 "트래픽 전달"로 오해 | 상태 검사 실패 시 자동으로 트래픽을 제외시킴 |
| 함정 3 | Auto Scaling 정책의 "Target Tracking"과 "Scheduled"를 혼동 | Target Tracking은 실시간 메트릭 기반, Scheduled는 정기적 조정 |
| 함정 4 | Launch Template가 Auto Scaling 그룹과 무관하다고 오인 | Launch Template는 인스턴스 생성 시 필수적인 구성 요소 |
| 함정 5 | GLB와 Classic Load Balancer의 목적을 혼동 | GLB는 글로벌 트래픽 분산, CLB는 전통적 레벨 밸런싱 |

#### 🔄 ELB vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | ELB | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | 웹 애플리케이션/네트워크 트래픽 분산 | Route 53 (DNS), CloudFront (CDN) | 트래픽 분산/가용성 확보가 필수적일 때 |
| 확장성 | 자동 확장 및 트래픽 동적 관리 | Auto Scaling + EC2 | 인스턴스 수동/자동 조정이 필요할 때 |
| 비용 | 고정 비용 + 사용량 기반 요금 | AWS Lambda (함수 기반) | 트래픽 패턴이 예측 가능하거나 비용 효율성이 중요할 때 |
| 지연시간 | ALB는 HTTP/HTTPS 최적화, NLB는 네트워크 지연 최소화 | AWS Global Accelerator | 글로벌 트래픽 지연 최소화가 필수적일 때 |

#### 📝 시험 대비 체크리스트
- [ ] ELB의 핵심 목적을 한 문장으로 설명할 수 있는가?  
- [ ] ELB를 선택해야 하는 시나리오를 알고 있는가? (예: 트래픽 분산, 자동 확장)  
- [ ] ELB의 제한사항/한계를 알고 있는가? (예: 특정 프로토콜 지원 제한)  
- [ ] ELB와 비슷한 서비스의 차이점을 설명할 수 있는가? (예: ALB vs NLB)  
- [ ] ELB의 비용 구조를 이해하고 있는가? (예: 고정 비용 + 사용량 요금)  

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 ELB를 떠올리세요:  
> - `트래픽 분산`  
> - `상태 검사`  
> - `자동 확장`  
> - `대상 그룹`  
> - `가용성 보장`

---

| [⬅️ 이전 Day](../day4/README.md) | [📑 Day 5 목차](./README.md) | [🏠 Week 1](../README.md) | [Auto Scaling ➡️](./Auto-Scaling.md) |

---
