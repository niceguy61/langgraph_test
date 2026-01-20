---

| [⬅️ ELB](./ELB.md) | [📑 Day 5 목차](./README.md) | [🏠 Week 1](../README.md) | [Launch Templates ➡️](./Launch-Templates.md) |

---

> **한 줄 정의:** Auto Scaling은 AWS의 자동화된 확장 및 축소 기능을 제공하는 서비스입니다.

### 이 서비스가 해결하는 문제  
**기존의 문제점:**  
- **문제 1:** 수작업으로 인스턴스 수를 조절해야 하며, 트래픽 급증 시 가용성이 떨어지고 서비스 중단 위험이 있었습니다. 예를 들어, 블로그 서버는 하루 중 특정 시간대에 트래픽이 급증할 때 수작업으로 인스턴스를 추가해야 했습니다.  
- **문제 2:** 트래픽 변동이 예측되지 않아 인스턴스를 과도하게 유지해 비용이 증가하거나, 부족해 응답 지연이 발생했습니다. 예를 들어, 이벤트 기반 서비스는 트래픽 폭주 시 대응하지 못해 사용자 경험 저하가 발생했습니다.  
- **문제 3:** 인스턴스 수를 조절하는 데 시간이 걸려, 응답 속도가 느려지거나 시스템이 과부하 상태가 되었습니다. 예를 들어, 쇼핑몰의 프로모션 기간 동안 인스턴스 확장이 지연되어 요청이 거절되는 사례가 있었습니다.  

**Auto Scaling로 해결:**  
- **해결 1:** 트래픽 변화에 따라 자동으로 인스턴스를 추가/삭제해 가용성을 유지합니다. 예를 들어, ALB를 통해 트래픽이 증가하면 Auto Scaling이 즉시 인스턴스를 확장해 요청을 처리합니다.  
- **해결 2:** 정책을 설정해 비용을 최적화하고, 트래픽 감소 시 자동으로 인스턴스를 축소해 비용 절감이 가능합니다. 예를 들어, 하루 중 사용량이 낮은 시간대에 인스턴스를 자동으로 제거해 연간 비용을 절감할 수 있습니다.  
- **해결 3:** 인스턴스 확장/축소가 실시간으로 이루어져 응답 속도가 빠르고, 시스템 과부하를 방지합니다. 예를 들어, 클라우드 기반 게임 서버는 유저 수 변화에 따라 자동으로 인스턴스를 조절해 지연 없이 서비스합니다.  

### 비유로 이해하기  
Auto Scaling은 집 난방 시스템의 온도 조절 기능을 비유할 수 있습니다. 실내 온도가 낮으면 난방기(인스턴스)를 자동으로 켜고, 높으면 꺼서 항상 최적의 온도를 유지합니다. 마찬가지로, Auto Scaling은 트래픽 변화에 따라 자동으로 인스턴스를 조절해 시스템이 항상 안정적으로 작동하도록 합니다.  

---

## 🎯 주요 사용 시나리오 (When to Use)  

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 트래픽 급증 시 자동 확장이 필요한 서비스 | 블로그, SaaS 플랫폼, 이벤트 기반 앱 등 |
| 시나리오 2 | 비용 최적화를 위해 인스턴스 수를 조절 | 프로모션 기간, 저사양 시스템 운영, 쇼핑몰 등 |
| 시나리오 3 | 가용성 확보를 위한 동적 인스턴스 관리 | 게임 서버, 라우팅 서비스, 대규모 데이터 처리 시스템 등 |

**이럴 때 Auto Scaling을 선택하세요:**  
- ✅ **트래픽 변동성이 큰 서비스**  
- ✅ **비용을 최소화하면서도 가용성을 유지해야 하는 시스템**  
- ✅ **자동으로 인스턴스를 조절해 운영 부담을 줄이고자 하는 경우**  

**이럴 때는 다른 서비스를 고려하세요:**  
- ❌ **단일 인스턴스로 충분한 서비스** → EC2 단일 인스턴스 사용  
- ❌ **트래픽 변동이 없고 고정된 부하** → EC2 Reserved Instances  
- ❌ **단순한 랜딩 페이지 운영** → S3 + CloudFront  

---

## 🔗 연관 서비스 (Used Together With)  

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **EC2** | Auto Scaling 그룹에 인스턴스를 생성/관리 | User → ALB → Auto Scaling Group → EC2 |
| **CloudWatch** | 트래픽 메트릭을 모니터링해 조정 정책 트리거 | Auto Scaling Group → CloudWatch Metrics |
| **Route 53** | DNS 레코드를 통해 Auto Scaling 그룹을 연결 | User → Route 53 → ALB → Auto Scaling Group |

**자주 사용되는 아키텍처 패턴:**  
```
User → CloudFront → S3 (정적 자산)  
User → ALB → Auto Scaling Group → EC2 (동적 처리)  
User → Route 53 → ALB → Auto Scaling Group → EC2  
```  

---

## 💰 비용 구조 (Pricing)  

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **인스턴스 수동 조절 비용** | $0.01~$0.50/인스턴스/시간 | 월 750시간 무료 |
| **조정 정책 실행 비용** | $0.0001~$0.005/요청 | 12개월 무료 |
| **CloudWatch 메트릭 저장 비용** | $0.0001~$0.005/메트릭/시간 | 항상 무료 |

**비용 최적화 팁:**  
1. 💡 **트래픽 패턴 분석 후 조정 정책 설정:** 예측 가능한 트래픽을 기반으로 정책을 세분화해 비용을 절감합니다.  
2. 💡 **Launch Templates로 인스턴스 자동 최적화:** CPU/메모리 사용량에 맞춰 인스턴스 타입을 자동 조정해 비용을 절감합니다.  
3. 💡 **CloudWatch 알림 기능 활용:** 비정상적인 트래픽 패턴을 감지해 사전에 조정 정책을 실행해 비용을 줄입니다.  

> **⚠️ 비용 주의:** 트래픽 급증 시 과도한 인스턴스 확장으로 인해 예상치 못한 비용이 발생할 수 있습니다. 조정 정책의 기준을 정확히 설정하고, CloudWatch 알림을 통해 실시간 모니터링해야 합니다.

## 📚 핵심 개념

### 개념 1: Auto Scaling 그룹(Auto Scaling Group) 운영 원리  
Auto Scaling 그룹은 인스턴스를 자동으로 확장하거나 축소하는 기능을 제공하는 AWS 서비스로, 애플리케이션의 트래픽 변화에 따라 자원을 유동적으로 조정합니다. 이 그룹은 정책에 따라 CPU 사용률, 네트워크 트래픽, 요청 수 등 기준을 기반으로 인스턴스를 추가/삭제하며, 항상 일정한 수준의 가용성을 유지합니다.  
**왜 중요한가?**  
- **1. 자동화된 확장성**: 트래픽 증가 시 수동으로 인스턴스를 추가하는 번거로움을 제거합니다.  
- **2. 비용 최적화**: 트래픽 감소 시 자원을 줄여 비용을 절감할 수 있습니다.  
- **3. 고가용성 보장**: 항상 최소 인스턴스 수를 유지해 서비스 중단을 방지합니다.  

#### 세부 요소  
| 요소 | 설명 | 예시 |  
|-----|-----|-----|  
| **최소/최대 인스턴스 수** | 자동 확장 범위를 정의합니다. | 최소 2, 최대 10 |  
| **인스턴스 유형** | 사용할 EC2 인스턴스의 종류를 지정합니다. | `t2.micro` |  
| **负载 밸런서 연동** | ALB/NLB 등과 연결해 트래픽을 분산합니다. | ALB 연결 |  

> **💡 Tip:** ASG는 상태 검사 실패 시 인스턴스를 자동으로 교체해 가용성을 유지합니다.  

---

### 개념 2: 조정 정책(Scaling Policy) 타입 및 트리거 조건  
조정 정책은 Auto Scaling 그룹이 자원을 조정할 조건과 방식을 정의하는 규칙입니다. 주요 타입은 **확장 정책**(CPU 사용률, 요청 수 등 기준으로 인스턴스 추가), **축소 정책**(트래픽 감소 시 인스턴스 제거), **일정 시간 기반 정책**(정해진 시각에 자동 조정) 등입니다.  
**왜 중요한가?**  
- **1. 실시간 반응**: 트래픽 변화에 따라 즉시 자원을 조정해 성능을 보장합니다.  
- **2. 비용 효율성**: 과도한 자원 사용을 방지해 비용을 절감합니다.  
- **3. 예측 가능성**: 트래픽 패턴을 분석해 정책을 미리 설정할 수 있습니다.  

#### 작동 원리  
1. **트리거 조건 확인**: CPU 사용률이 70% 이상일 경우 확장 정책이 실행됩니다.  
2. **인스턴스 생성**: 정책에 따라 `t2.micro` 인스턴스를 자동으로 생성합니다.  
3. **재균형 처리**: 생성된 인스턴스를 ALB에 연결해 트래픽을 분산합니다.  

> **💡 Tip:** 정책을 설정할 때 **Cooldown 시간**을 설정해 과도한 조정을 방지하세요.  

---

### 개념 3: Launch Templates의 인스턴스 구성 정의 방법  
Launch Templates는 EC2 인스턴스 생성 시 사용하는 템플릿으로, 인스턴스 유형, 보안 그룹, 키 페어, 네트워크 설정 등을 미리 정의합니다. 이 템플릿은 Auto Scaling 그룹과 연동해 일관된 인스턴스 생성을 가능하게 합니다.  
**왜 중요한가?**  
- **1. 일관성 확보**: 모든 인스턴스가 동일한 설정으로 생성되어 관리가 용이합니다.  
- **2. 신속한 확장**: 템플릿을 기반으로 자동으로 인스턴스를 생성해 시간을 절약합니다.  
- **3. 보안 강화**: 미리 정의된 보안 그룹과 키 페어로 보안을 강화할 수 있습니다.  

#### 주요 특징  
1. ****템플릿 버전 관리**: 여러 버전의 템플릿을 관리해 기존 구성과 신규 구성이 혼동되지 않도록 합니다.  
2. ****동적 파라미터 지원**: `Launch Template`에서 변수를 사용해 인스턴스 설정을 유연하게 조정할 수 있습니다.  
3. ****Auto Scaling 연동**: ASG에서 템플릿을 선택해 인스턴스 생성 시 자동으로 적용됩니다.  

> **💡 Tip:** 템플릿을 수정하면 기존 인스턴스는 변경 사항을 반영하지 않으므로, 신규 인스턴스만 업데이트하세요.

## 🖥️ AWS 콘솔에서 Auto Scaling 사용하기

### Step 1: Auto Scaling 서비스 접속
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
   - AWS 계정 ID와 비밀번호를 입력해 로그인합니다.  
2. 상단 검색창에서 "Auto Scaling"을 입력하고, 검색 결과에서 "Auto Scaling"을 클릭합니다.  
   - "Auto Scaling" 서비스는 EC2 자동 확장 기능을 관리하는 대시보드입니다.  

> **📸 화면 확인:** Auto Scaling 대시보드가 표시되면 정상입니다.  
> **💡 Tip:** "Auto Scaling Group" 목록이 표시되며, 이는 생성한 자동 확장 그룹을 확인할 수 있는 메인 화면입니다.

---

### Step 2: [주요 작업 1 - 리소스 생성]
1. **Auto Scaling 그룹 생성**  
   - 대시보드 상단 "Create Auto Scaling Group" 버튼을 클릭합니다.  
   - **Launch Template 선택**: EC2 인스턴스의 스펙을 정의한 템플릿을 선택합니다.  
   - **VPC 및 서브넷**: 네트워크 설정을 입력합니다.  
   - **Minimum/Maximum/Desired Capacity**: 최소, 최대, 목표 인스턴스 수를 설정합니다.  
2. **스케일링 정책 설정**  
   - "Scaling Policies" 섹션에서 **Simple Scaling** 또는 **Dynamic Scaling**을 선택합니다.  
   - **Metric Type**: CPU 사용률, 네트워크 트래픽 등 기준을 설정합니다.  
   - **Cooldown Period**: 정책이 실행된 후 대기 시간을 입력합니다.  
3. **확인 및 생성**  
   - 설정 내용을 검토하고, "Create" 버튼을 클릭해 리소스를 생성합니다.  

> **📸 화면 확인:** "Auto Scaling Group" 목록에 생성된 그룹이 표시되며, "Launch Template"과 "Scaling Policies" 설정이 정확히 반영된 상태입니다.  
> **⚠️ 주의:** 리소스 생성 시 지역(Region) 설정을 반드시 확인하세요. 다른 지역에서 생성된 리소스는 접근할 수 없습니다.

---

### Step 3: [주요 작업 2 - 설정/구성]
1. **Health Check 설정**  
   - "Health Check" 섹션에서 **Target Group**을 선택합니다.  
   - **Health Check Protocol**: HTTP, HTTPS, TCP 등으로 설정합니다.  
   - **Health Check Path**: HTTP 테스트 경로를 입력합니다 (예: `/health`).  
2. **Target Group 연동**  
   - ELB(ELastic Load Balancing)와 Auto Scaling을 연동해 트래픽을 분배합니다.  
   - "Target Group"을 선택하고, **Health Check Timeout** 및 **Interval**을 설정합니다.  
3. **스케일링 정책 조정**  
   - "Scaling Policies"에서 **Step Scaling** 또는 **Scheduled Scaling**을 추가합니다.  
   - **Step Scaling**은 CPU 사용률 기준으로 인스턴스 수를 단계별로 조정합니다.  

> **⚠️ 주의:** 정책을 변경할 때는 기존 정책이 중단되지 않도록 **Replace Policy** 옵션을 사용하세요.  
> **💡 Tip:** "Scheduled Scaling"은 특정 시간대에 자동으로 인스턴스 수를 조정하는 데 유용합니다.

---

### Step 4: 설정 확인 및 테스트
1. **리소스 상태 확인**  
   - "Auto Scaling Group" 클릭 후 "Instances" 탭에서 생성된 인스턴스를 확인합니다.  
   - "Health Status"가 "healthy"로 표시되면 정상입니다.  
2. **스케일링 테스트**  
   - ELB에서 트래픽을 증가시켜 CPU 사용률을 70% 이상으로 올립니다.  
   - Auto Scaling 그룹이 자동으로 인스턴스를 증가시키는지 확인합니다.  
3. **CLI 명령어 확인**  
   - CLI로 설정을 검증할 수 있습니다:  
     ```bash
     aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names <group-name>
     ```  
   - "Scaling Policies"와 "Health Check" 설정이 정확히 반영되었는지 확인합니다.  

> **💡 Tip:** 프리티어(Free Tier) 사용 시, 최대 750시간의 EC2 인스턴스 사용이 가능합니다. 비용을 절약하기 위해 "Minimum Capacity"를 적절히 설정하세요.

## ⌨️ AWS CLI로 Auto Scaling 사용하기

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
AWS CLI를 사용하기 전에 버전을 확인해 최신 버전인지 확인합니다. 자격 증명이 정상적으로 설정되어 있는지 확인하고, 현재 리전을 확인해 리소스를 관리할 리전을 설정합니다.  

---

### 예제 1: Auto Scaling 리소스 조회
```bash
# Auto Scaling 그룹 목록 조회
aws autoscaling describe-auto-scaling-groups --query 'AutoScalingGroups[*].AutoScalingGroupName' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| `--query` | 필터링 조건 (예: `AutoScalingGroups[*].AutoScalingGroupName`) | `'AutoScalingGroups[*].AutoScalingGroupName'` |
| `--output` | 출력 형식 (json, table, text) | `table` |

**예상 출력:**
```
| AutoScalingGroupName |
|----------------------|
| example-group        |
| another-group        |
```

---

### 예제 2: Auto Scaling 그룹 생성
```bash
# Auto Scaling 그룹 생성
aws autoscaling create-auto-scaling-group \
    --auto-scaling-group-name "example-group" \
    --launch-template LaunchTemplateName=example-launch-template \
    --min-size 1 \
    --max-size 5 \
    --desired-capacity 2 \
    --vpc-zone-identifier subnet-12345678
```

**필수 옵션:**
- `--auto-scaling-group-name`: 그룹 이름
- `--launch-template`: 사용할 Launch Template 이름
- `--min-size`, `--max-size`: 최소/최대 인스턴스 수
- `--vpc-zone-identifier`: VPC 서브넷 ID (예: `subnet-12345678`)

**예상 출력:**
```json
{
    "AutoScalingGroup": {
        "AutoScalingGroupName": "example-group",
        "MinSize": 1,
        "MaxSize": 5,
        "DesiredCapacity": 2,
        "LaunchTemplate": {
            "LaunchTemplateName": "example-launch-template"
        }
    }
}
```

---

### 예제 3: Auto Scaling 그룹 수정
```bash
# Auto Scaling 그룹 수정 (최대 인스턴스 수 변경)
aws autoscaling update-auto-scaling-group \
    --auto-scaling-group-name "example-group" \
    --max-size 10
```

**설명:**  
`--auto-scaling-group-name`은 수정할 그룹 이름, `--max-size`는 최대 인스턴스 수를 변경합니다.  
기타 수정 가능한 옵션: `--min-size`, `--desired-capacity`, `--launch-template`, `--vpc-zone-identifier`.

---

### 예제 4: Auto Scaling 그룹 삭제
```bash
# Auto Scaling 그룹 삭제
aws autoscaling delete-auto-scaling-group \
    --auto-scaling-group-name "example-group" \
    --force-delete

# 삭제 확인
aws autoscaling describe-auto-scaling-groups --query 'AutoScalingGroups[*].AutoScalingGroupName' --output table
```

> **⚠️ 주의:** `--force-delete` 옵션을 사용하면 종속된 리소스(예: EC2 인스턴스)도 함께 삭제됩니다. 삭제 후에는 되돌릴 수 없습니다.  

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws autoscaling describe-auto-scaling-groups --query 'AutoScalingGroups[*].AutoScalingGroupName' --output table
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name "example-group" --output table

# 생성
aws autoscaling create-auto-scaling-group --auto-scaling-group-name "example-group" --launch-template LaunchTemplateName=example-launch-template --min-size 1 --max-size 5 --desired-capacity 2

# 수정
aws autoscaling update-auto-scaling-group --auto-scaling-group-name "example-group" --max-size 10

# 삭제
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name "example-group" --force-delete
```

**팁:**  
- `--query`를 사용해 필터링하여 필요한 정보만 출력  
- `--output table`을 사용해 가독성 있는 테이블 형식으로 결과 확인  
- `--force-delete`는 삭제 시 종속 리소스도 제거하므로 주의해야 합니다.  

--- 

**비용 관련 주의사항:**  
Auto Scaling 그룹은 인스턴스 생성/삭제 시 수수료가 발생합니다. 프리티어는 750시간(1년 기준) 제공되며, `--min-size 0`을 설정해 비용을 최소화할 수 있습니다.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 Auto Scaling 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **Auto Scaling 그룹(Auto Scaling Group) 운영 원리**:
   - 설명: Auto Scaling 그룹은 CPU 사용률, 네트워크 트래픽, 요청 수 등 기준으로 인스턴스를 자동으로 확장/축소합니다. 이는 단일 인스턴스의 고가용성 문제를 해결하고, 트래픽 폭주 시 신속히 자원을 확보하는 데 필수적입니다.  
   - 키워드: `Auto Scaling Group`, `인스턴스 풀`, `타겟 그룹`

2. **조정 정책(Scaling Policy) 타입 및 트리거 조건**:
   - 설명: `Scheduled Scaling`은 예약된 시간대에 자동 확장, `Dynamic Scaling`은 메트릭 기반 확장, `Simple Scaling`은 단일 메트릭 기준으로 간단한 확장입니다. 트리거 조건은 CPU 사용률, 요청 수, 상태 코드 등으로 설정할 수 있습니다.  
   - 키워드: `Scheduled Scaling`, `Dynamic Scaling`, `트리거 메트릭`

3. **대상 그룹( Target Group ) 구성 및 상태 검사**:
   - 설명: 대상 그룹은 ALB/NLB과 연결되어 인스턴스의 건강 상태를 모니터링합니다. 상태 검사는 HTTP/HTTPS, TCP, TCP+HTTP 등 다양한 프로토콜로 설정할 수 있으며, 불건전한 인스턴스는 자동으로 제외됩니다.  
   - 키워드: `Target Group`, `상태 검사`, `HTTP 프로토콜`

4. **ALB/NLB/GLB/CLB 차이점**:
   - 설명: ALB는 HTTP/HTTPS 트래픽 처리, NLB는 TCP/UDP 트래픽 처리, GLB는 다중 리전 간 트래픽 분산, CLB는 내부 네트워크용으로 사용됩니다. 시험에서는 각 런타임의 주요 기능과 사용 사례를 구분해야 합니다.  
   - 키워드: `ALB`, `NLB`, `GLB`, `CLB`

5. **Launch Templates의 인스턴스 구성 정의 방법**:
   - 설명: Launch Templates는 EC2 인스턴스의 스펙(예: CPU, 메모리, AMI)과 보안 그룹, 네트워크 설정 등을 미리 정의해 Auto Scaling 그룹에서 재사용됩니다. 이는 일관된 인스턴스 생성을 보장합니다.  
   - 키워드: `Launch Template`, `AMI`, `보안 그룹`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | ALB와 NLB의 차이를 혼동해 문제를 틀리기 | ALB는 HTTP/HTTPS 트래픽, NLB는 TCP/UDP 트래픽 처리에 사용됩니다. |
| 함정 2 | 상태 검사 실패 시 자동 제거가 아니라 수동 수동 수동 수동 | 상태 검사 실패 시 Auto Scaling은 자동으로 인스턴스를 제외합니다. |
| 함정 3 | 조정 정책을 설정하지 않아도 자동 확장이 가능하다고 생각 | Auto Scaling은 기본적으로 조정 정책이 필요하며, 설정되지 않으면 비활성 상태입니다. |

#### 🔄 Auto Scaling vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | Auto Scaling | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | 인스턴스 자동 확장 및 축소 | AWS Lambda(무 서버 아키텍처) | 리소스가 고정적이거나 스케일링이 필요할 때 |
| 확장성 | 실시간 메트릭 기반 확장 | DynamoDB Auto Scaling | 데이터베이스 용량 조절 시 |
| 비용 | 인스턴스 수에 따라 비용 발생 | AWS Fargate(컨테이너 실행) | CPU/메모리 사용률에 따른 비용 최적화 |
| 지연시간 | 인스턴스 생성/삭제 시간 | Lambda(서버리스) | 즉시 실행이 필요한 경우 |

#### 📝 시험 대비 체크리스트
- [ ] Auto Scaling의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  *예: "트래픽 변화에 따라 자동으로 인스턴스를 확장/축소하여 가용성을 유지합니다."*
- [ ] Auto Scaling를 선택해야 하는 시나리오를 알고 있는가?  
  *예: 트래픽 폭주 시 신속한 자원 확보가 필요한 웹 애플리케이션.*
- [ ] Auto Scaling의 제한사항/한계를 알고 있는가?  
  *예: 인스턴스 생성 시간, 최소/최대 인스턴스 수 제한, 메트릭 수집 지연.*
- [ ] Auto Scaling와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  *예: DynamoDB Auto Scaling은 데이터베이스 용량 조절, EC2 Auto Scaling은 인스턴스 수 조절.*
- [ ] Auto Scaling의 비용 구조를 이해하고 있는가?  
  *예: 인스턴스 수에 따라 비용 발생, 예약 인스턴스 할인 가능.*

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 Auto Scaling을 떠올리세요:  
> - **Auto Scaling Group**  
> - **Scaling Policy**  
> - **Target Group**  
> - **Launch Template**  
> - **Health Check**

---

| [⬅️ ELB](./ELB.md) | [📑 Day 5 목차](./README.md) | [🏠 Week 1](../README.md) | [Launch Templates ➡️](./Launch-Templates.md) |

---
