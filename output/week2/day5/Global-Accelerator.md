---

| [⬅️ Route 53](./Route-53.md) | [📑 Day 5 목차](./README.md) | [🏠 Week 2](../README.md) | [다음 Day ➡️](../../week3/day1/README.md) |

---

# Global Accelerator 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** Global Accelerator는 **전 세계 사용자에게 저지연 및 고성능의 애플리케이션 접근을 제공하기 위한 AWS의 글로벌 네트워크 최적화 서비스**입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 전 세계 사용자가 동일한 서버에 연결할 때 지연 시간이 길어지고, 특정 지역에서 성능 저하가 발생합니다. 예: 유럽 사용자가 미국 서버에 연결하면 데이터 전송 시간이 증가합니다.  
- **문제 2:** 애플리케이션의 가용성이 낮아지며, 서버 장애 시 사용자에게 즉각적인 대체 경로를 제공하지 못해 서비스 중단이 발생합니다.  
- **문제 3:** 고대역폭 데이터 전송 시 AWS 서비스의 고정 비용이 발생하며, 성능 최적화가 어려웠습니다.  

**Global Accelerator로 해결:**
- **해결 1:** AWS의 글로벌 네트워크를 통해 사용자에게 **최근접 서버로 트래픽을 자동으로 라우팅**해 지연 시간을 최소화합니다.  
- **해결 2:** **건강 상태 모니터링**을 통해 서버 장애 시 즉시 대체 경로로 트래픽을 전환해 서비스 가용성을 보장합니다.  
- **해결 3:** **데이터 전송 기반 과금**으로 사용량에 따라 비용을 조절해 예측 가능한 비용 구조를 제공합니다.  

### 비유로 이해하기
Global Accelerator는 **세계적인 고속도로 네트워크**를 생각해보세요. 사용자가 어떤 지역에 있든, 최적의 경로를 통해 빠르게 목적지에 도착합니다. 예를 들어, 유럽 사용자는 유럽 서버로, 아시아 사용자는 아시아 서버로 트래픽이 자동으로 분배되어 지연 시간이 줄어듭니다. 이처럼 **글로벌 네트워크의 최적화**를 통해 애플리케이션 성능을 극대화합니다.

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | **글로벌 웹 애플리케이션 운영** | 글로벌 사용자에게 저지연 서비스 제공 (예: 온라인 쇼핑몰) |
| 시나리오 2 | **재해 복구 및 고가용성 요구** | 서버 장애 시 자동 대체 경로 설정 (예: 클라우드 백업 시스템) |
| 시나리오 3 | **고대역폭 데이터 전송** | 대용량 파일 배포 또는 스트리밍 서비스 (예: 동영상 플랫폼) |

**이럴 때 Global Accelerator를 선택하세요:**
- ✅ **전 세계 사용자에게 일관된 성능 제공이 필요할 때**  
- ✅ **트래픽 분산 및 장애 대응이 필수적일 때**  
- ✅ **데이터 전송 비용 최적화가 필요한 경우**  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ **단일 지역 내 저지연이 필요할 때** → **AWS Direct Connect**  
- ❌ **캐시 기반 콘텐츠 전달이 필요할 때** → **CloudFront**  
- ❌ **DNS 라우팅이 필요할 때** → **Route 53**  

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **CloudFront** | **최종 사용자에게 캐시된 콘텐츠 전달** | User → CloudFront → Global Accelerator → Origin (S3/EC2) |
| **Route 53** | **DNS 라우팅 및 고가용성 설정** | User → Route 53 → Global Accelerator → Origin |
| **S3** | **원본 서버로 데이터 저장 및 배포** | Global Accelerator → S3 (CRR/SRR 설정) |

**자주 사용되는 아키텍처 패턴:**
```
User → CloudFront → Global Accelerator → S3 (CRR/SRR)
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **Accelerated Endpoint** | $0.10/월 (1개) | 12개월 무료 (최대 10개) |
| **Data Transfer** | $0.01/GB (미국 기준) | 12개월 무료 (최대 100GB) |
| **Health Check** | $0.001/월 (1개) | 항상 무료 |

**비용 최적화 팁:**
1. 💡 **프리티어 기간 동안 사용량을 극대화하세요** (12개월 무료 기간 동안 트래픽을 늘리면 비용 절감 효과가 큽니다).  
2. 💡 **데이터 전송량을 모니터링해 과다 사용을 방지하세요** (예: 데이터 전송량이 100GB를 초과하면 요금이 급증합니다).  
3. 💡 **Health Check 주기 및 기준을 최적화해 불필요한 검사를 줄이세요** (예: 1분 단위로 검사하는 대신 5분 단위로 설정).  

> **⚠️ 비용 주의:** **데이터 전송량이 예상치 못하게 증가할 경우 과금이 급격히 상승할 수 있습니다**. 특히, 특정 지역에서의 트래픽 증가 또는 대규모 파일 전송 시 주의해야 합니다.

## 📚 핵심 개념

### 개념 1: **Global Accelerator의 핵심 개념: 글로벌 가속화의 기초**
Global Accelerator는 AWS에서 제공하는 글로벌 트래픽 가속화 서비스로, 사용자의 요청을 최적의 위치에 있는 리소스로 빠르게 전달합니다. 이는 DNS 레벨에서 트래픽을 최적화해 지연 시간을 줄이고, 지리적으로 가까운 리전에서 서비스를 제공하여 사용자 경험을 개선합니다. 특히, CloudFront와 같은 CDN 서비스, S3 스토리지, Route 53 DNS 서비스 등과 연동해 전 세계 사용자에게 신속한 응답을 제공합니다.

#### 왜 중요한가?
- **지연 최소화**: 사용자의 요청을 가장 가까운 리전의 리소스로 전달해 응답 속도를 향상시킵니다.  
- **고가용성 보장**: 다중 리전에 리소스를 배치해 단일 지점 실패(SPOF)를 방지합니다.  
- **비용 효율성**: 트래픽을 최적화해 네트워크 대역폭 비용을 절감할 수 있습니다.  

#### 세부 요소
| 요소 | 설명 | 예시 |
|-----|------|---|
| **트래픽 라우팅** | 사용자의 요청을 최적의 리전으로 전달 | 유럽 사용자가 미국 리전의 S3 버킷에 접근 시, EU 리전으로 트래픽이 라우팅됨 |
| **DNS 기반 가속** | Route 53을 통해 DNS 레벨에서 최적의 엔드포인트 선택 | 사용자 요청을 기반으로 IP 주소를 동적으로 변경 |
| **CDN 연동** | CloudFront와 결합해 콘텐츠를 가까운 위치에서 제공 | 글로벌 사용자에게 동일한 콘텐츠를 지역별로 제공 |

> **💡 Tip:** Global Accelerator는 단일 리전에 집중하지 않고, 다중 리전의 리소스를 활용해 트래픽을 분산시켜 고가용성과 성능을 동시에 달성합니다.

---

### 개념 2: **전역 가속화의 핵심 요소: 리소스 배치와 트래픽 분산**
Global Accelerator는 사용자의 요청을 기반으로 리전을 선택하고, 해당 리전의 리소스로 트래픽을 전달합니다. 이 과정에서 S3, CloudFront, Route 53 등 다양한 서비스와의 협업이 필수적입니다. 예를 들어, S3 버킷이 여러 리전에 배치된 경우, Global Accelerator는 DNS 레벨에서 가장 가까운 리전을 선택해 응답 속도를 최적화합니다.

#### 작동 원리
1. **DNS 요청 처리**: Route 53을 통해 사용자의 요청을 기반으로 최적의 엔드포인트 선택  
2. **트래픽 전달**: 선택된 리전의 리소스(예: S3, EC2, CloudFront)로 트래픽을 라우팅  
3. **성능 최적화**: 다중 리전 간 트래픽 분산을 통해 네트워크 지연 최소화  

> **💡 Tip:** Global Accelerator는 단일 리전에 집중하지 않고, 다중 리전의 리소스를 활용해 트래픽을 분산시켜 고가용성과 성능을 동시에 달성합니다.

---

### 개념 3: **전역 가속화의 주요 특징**
Global Accelerator는 다양한 기능을 통해 글로벌 사용자에게 최적의 서비스를 제공합니다. 주요 특징은 다음과 같습니다:

1. **지연 최소화**: 사용자의 요청을 가장 가까운 리전의 리소스로 전달해 응답 속도를 향상시킵니다.  
2. **고가용성 보장**: 다중 리전에 리소스를 배치해 단일 지점 실패(SPOF)를 방지합니다.  
3. **비용 효율성**: 트래픽을 최적화해 네트워크 대역폭 비용을 절감할 수 있습니다.  

> **💡 Tip:** Global Accelerator는 단일 리전에 집중하지 않고, 다중 리전의 리소스를 활용해 트래픽을 분산시켜 고가용성과 성능을 동시에 달성합니다.

## 🖥️ AWS 콘솔에서 Global Accelerator 사용하기

### Step 1: Global Accelerator 서비스 접속
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
   - **AWS 계정 ID**와 **IAM 권한**이 활성화되어 있어야 합니다.  
2. 상단 검색창에서 "Global Accelerator"를 입력하고, 검색 결과에서 해당 서비스를 클릭합니다.  
   - **AWS 서비스 타일**이 표시된 후, "Global Accelerator"를 선택합니다.  

> **📸 화면 확인:** Global Accelerator 대시보드가 표시되면 정상입니다.  
> **💡 Tip:** 처음 접속 시 "Accelerator" 목록이 빈 상태일 수 있으므로, 리소스 생성 후 확인해야 합니다.

---

### Step 2: [주요 작업 1 - 리소스 생성]
1. **Accelerator 생성**  
   - "Create accelerator" 버튼을 클릭합니다.  
   - **Accelerator 이름**: 알파벳, 숫자, 하이픈(-)만 사용 가능합니다.  
   - **Region**: 전 세계에서 사용 가능한 리전 중 하나를 선택합니다 (예: us-east-1).  
   - **IP Address Type**: `IPv4` 또는 `IPv6`를 선택합니다.  
2. **Endpoints 추가**  
   - "Add endpoint" 버튼을 클릭하고, 다음 설정을 수행합니다:  
     - **Protocol**: TCP 또는 UDP (HTTP/HTTPS는 ALB/CloudFront와 연동)  
     - **Port**: 포트 번호를 입력합니다 (예: 80, 443).  
     - **Endpoint**: EC2 인스턴스, ALB, 또는 CloudFront 배포의 ARN을 입력합니다.  
3. **리소스 생성 확인**  
   - "Create" 버튼을 클릭하여 리소스를 생성합니다.  
   - 생성 후, "Accelerator" 목록에 새 리소스가 표시됩니다.  

> **📸 화면 확인:** "Create accelerator" 화면에서 설정값이 올바르게 입력되었는지 확인합니다.  
> **⚠️ 주의:** 생성된 Accelerator의 상태가 "ACTIVE"가 아닐 경우, 엔드포인트 설정이 잘못되었을 수 있습니다.

---

### Step 3: [주요 작업 2 - 설정/구성]
1. **Listener 구성**  
   - Accelerator 목록에서 특정 리소스를 선택하고, "Listeners" 탭을 클릭합니다.  
   - "Add listener" 버튼을 클릭하여 다음 설정을 수행합니다:  
     - **Protocol**: TCP/UDP/HTTP/HTTPS  
     - **Port**: 포트 번호를 입력합니다.  
     - **Default Action**: "Forward to"를 선택하고, 전달할 엔드포인트를 선택합니다.  
2. **Routing Rule 추가**  
   - "Rules" 탭에서 "Add rule" 버튼을 클릭하여 조건 기반 라우팅을 설정합니다.  
   - **Rule Condition**: IP 주소, 포트, 프로토콜 등을 기준으로 규칙을 정의합니다.  
   - **Action**: 전달할 엔드포인트를 선택합니다.  
3. **HTTPS 설정 (선택 사항)**  
   - "SSL/TLS" 탭에서 인증서를 업로드하고, 암호화 설정을 적용합니다.  
   - **Certificate**: AWS Certificate Manager(CM)에서 발급한 SSL 인증서를 연결합니다.  

> **⚠️ 주의:** HTTPS를 사용할 경우, 엔드포인트의 SSL 설정도 일치해야 합니다.  
> **💡 Tip:** CloudFront 배포와 연동 시, "HTTP" 프로토콜을 사용하고 "Forward to" 설정을 활용하세요.

---

### Step 4: 설정 확인 및 테스트
1. **리소스 상태 확인**  
   - Accelerator 목록에서 "Status" 컬럼을 확인합니다.  
   - **Status**: `ACTIVE`일 경우 정상적으로 작동 중입니다.  
2. **트래픽 테스트**  
   - `curl` 명령어를 사용해 외부에서 요청을 보내고, 응답 시간을 측정합니다.  
   - 예시:  
     ```bash
     curl -v https://<global-accelerator-dns-name>
     ```  
   - **DNS 이름**: Accelerator의 "DNS name"을 확인하고 테스트합니다.  
3. **CloudWatch 로그 확인**  
   - "Monitoring" 탭에서 요청 수, 지연 시간, 실패율 등을 확인합니다.  
   - **CloudWatch Metrics**: 트래픽 패턴을 분석하고 최적화에 활용합니다.  

> **📸 화면 확인:** "Monitor" 탭에서 트래픽 패턴을 확인하고, "Test" 버튼을 클릭해 직접 테스트합니다.  
> **💡 Tip:** 프리티어는 1년간 1개의 Accelerator를 무료로 제공합니다. 비용을 최소화하려면 적절한 리전과 리소스만 사용하세요.

## ⌨️ AWS CLI로 Global Accelerator 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

> **💡 Tip:** AWS CLI는 기본적으로 `us-east-1` 리전에서 실행됩니다. Global Accelerator 리소스는 생성 시 리전을 명시해야 합니다.

---

### 예제 1: Global Accelerator 리소스 조회
```bash
# [Global Accelerator 리소스 목록 조회]
aws globalaccelerator list-accelerators --query "[].AcceleratorArn" --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| `--query` | 결과 필터링 | `"[].AcceleratorArn"` |
| `--output` | 출력 형식 | `json`, `table`, `text` |

**예상 출력:**
```
| AcceleratorArn                                  |
|-------------------------------------------------|
| arn:aws:globalaccelerator::123456789012:accelerator/abcd1234 |
```

> **⚠️ 주의:** 리소스 목록은 생성한 리소스만 표시됩니다. 아직 생성하지 않은 경우 빈 테이블이 출력됩니다.

---

### 예제 2: Global Accelerator 리소스 생성
```bash
# [Global Accelerator 리소스 생성]
aws globalaccelerator create-accelerator \
    --name "example-accelerator" \
    --attributes Region=ap-northeast-1,IpAddressType=ipv4
```

**필수 옵션:**
- `--name`: 리소스 이름 (128자 이내)
- `--attributes`: 리전 및 IP 주소 유형 설정 (Region, IpAddressType)

**예상 출력:**
```json
{
    "Accelerator": {
        "AcceleratorArn": "arn:aws:globalaccelerator::123456789012:accelerator/abcd1234",
        "AcceleratorName": "example-accelerator",
        "Id": "abcd1234",
        "Region": "ap-northeast-1",
        "Status": "CREATING"
    }
}
```

> **💡 Tip:** `IpAddressType`은 `ipv4` 또는 `ipv6`로 설정 가능하며, 리전은 AWS 지원 리전만 지정해야 합니다.

---

### 예제 3: Global Accelerator 리소스 수정
```bash
# [Global Accelerator 리소스 수정]
aws globalaccelerator update-accelerator \
    --accelerator-id "abcd1234" \
    --attributes Region=ap-northeast-2,IpAddressType=ipv6
```

**필수 옵션:**
- `--accelerator-id`: 수정할 리소스 ID
- `--attributes`: 수정할 리전 및 IP 주소 유형

**예상 출력:**
```json
{
    "Accelerator": {
        "AcceleratorArn": "arn:aws:globalaccelerator::123456789012:accelerator/abcd1234",
        "AcceleratorName": "example-accelerator",
        "Id": "abcd1234",
        "Region": "ap-northeast-2",
        "Status": "UPDATING"
    }
}
```

> **⚠️ 주의:** 수정 시 리전 변경은 기존 엔드포인트 연결을 끊을 수 있으니 주의하세요.

---

### 예제 4: Global Accelerator 리소스 삭제
```bash
# [Global Accelerator 리소스 삭제]
aws globalaccelerator delete-accelerator --accelerator-id "abcd1234"

# 삭제 확인
aws globalaccelerator describe-accelerator --accelerator-id "abcd1234"
```

**예상 출력 (삭제 후):**
```json
{
    "Accelerator": {
        "AcceleratorArn": "arn:aws:globalaccelerator::123456789012:accelerator/abcd1234",
        "AcceleratorName": "example-accelerator",
        "Id": "abcd1234",
        "Region": "ap-northeast-2",
        "Status": "DELETING"
    }
}
```

> **⚠️ 주의:** 삭제는 되돌릴 수 없습니다. `--force` 옵션 없이 실행 시 최소 10분간 상태가 `DELETING`으로 유지됩니다.

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws globalaccelerator list-accelerators
aws globalaccelerator describe-accelerator --accelerator-id "id"

# 생성
aws globalaccelerator create-accelerator --name "name" --attributes Region=ap-northeast-1,IpAddressType=ipv4

# 수정
aws globalaccelerator update-accelerator --accelerator-id "id" --attributes Region=ap-northeast-2,IpAddressType=ipv6

# 삭제
aws globalaccelerator delete-accelerator --accelerator-id "id"
```

> **💡 Tip:** `aws globalaccelerator` 명령어는 리전을 명시하지 않으면 `us-east-1`에서 실행됩니다. 리전 변경 시 명시적으로 설정해야 합니다.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 Global Accelerator 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **Global Accelerator의 핵심 목적**:
   - 설명: **전 세계 사용자에게 저지연으로 애플리케이션 트래픽을 전달**하는 데 사용됩니다. 이는 ALB나 EC2 등 backend 서버에 직접 트래픽을 전달하는 대신 AWS의 글로벌 네트워크를 통해 최적 경로를 선택해 지연 시간을 최소화합니다.  
   - 키워드: `저지연`, `글로벌 네트워크`, `트래픽 최적화`

2. **Global Accelerator vs. CloudFront 비교**:
   - 설명: **CloudFront는 CDN**으로 콘텐츠를 캐시해 전달하지만, Global Accelerator는 **서버에 직접 트래픽을 전달**해 애플리케이션 성능을 개선합니다. 시험에서는 이 두 서비스의 **용도 및 기능 차이**를 구분하는 문제가 자주 출제됩니다.  
   - 키워드: `CDN`, `서버 트래픽 전달`, `콘텐츠 캐싱`

3. **Global Accelerator의 제한사항**:
   - 설명: **TCP/SSL 트래픽만 지원**하며, HTTP/2, WebSocket, TLS 1.2 이상은 제한됩니다. 또한, **서버 포트와 경로 기반 라우팅**만 가능해 특정 트래픽 유형은 처리하지 못합니다.  
   - 키워드: `TCP/SSL만 지원`, `HTTP/2 제한`, `포트 기반 라우팅`

4. **비용 구조 및 프리티어 활용**:
   - 설명: **프리티어는 1개의 가상 인스턴스와 1개의 액셀러레이터**를 제공하며, 실제 비용은 **트래픽량에 따라 계산됩니다**. 시험에서는 **비용 최적화 전략**과 **프리티어 한계**를 묻는 문제가 흔합니다.  
   - 키워드: `프리티어 한계`, `트래픽 기반 요금제`, `비용 최적화`

5. **Global Accelerator와 Route 53의 통합**:
   - 설명: **Route 53을 사용해 DNS 레코드를 설정**하고, Global Accelerator를 **backend로 연결**해 트래픽을 분배할 수 있습니다. 이는 **다중 지역 리전의 트래픽 균형**을 관리하는 데 유용합니다.  
   - 키워드: `DNS 레코드`, `backend 연결`, `지역 리전 균형`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | "Global Accelerator는 CDN 기능을 제공한다"고 잘못 기술할 수 있습니다. | **Global Accelerator는 CDN이 아닙니다. CloudFront가 CDN입니다.** |
| 함정 2 | "Global Accelerator는 모든 트래픽 유형을 지원한다"고 생각할 수 있습니다. | **TCP/SSL 트래픽만 지원하며, HTTP/2, WebSocket은 제한됩니다.** |
| 함정 3 | "Global Accelerator와 Route 53는 동일한 기능을 수행한다"고 오인할 수 있습니다. | **Route 53는 DNS 서비스로, Global Accelerator는 트래픽 전달 서비스입니다.** |

#### 🔄 Global Accelerator vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | Global Accelerator | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | **저지연 애플리케이션 트래픽 전달** | CloudFront (CDN), Route 53 (DNS) | **트래픽 최적화**가 필요한 경우 |
| 확장성 | **자동 확장 및 글로벌 네트워크 활용** | CloudFront (스케일링 자동화), Route 53 (DNS 확장성) | **대규모 트래픽 처리**가 필요한 경우 |
| 비용 | **트래픽량에 따라 요금제** | CloudFront (데이터 전송 기반), Route 53 (요금제 유형별) | **비용 최적화**를 중시하는 경우 |
| 지연시간 | **AWS 글로벌 네트워크 기반 최적 경로** | CloudFront (콘텐츠 캐싱), Route 53 (DNS 레코드 기반) | **저지연 성능**이 필수인 경우 |

#### 📝 시험 대비 체크리스트
- [ ] Global Accelerator의 핵심 목적을 한 문장으로 설명할 수 있는가?  
- [ ] Global Accelerator를 선택해야 하는 시나리오를 알고 있는가? (예: 저지연 애플리케이션)  
- [ ] Global Accelerator의 제한사항/한계를 알고 있는가? (TCP/SSL, HTTP/2 제한)  
- [ ] Global Accelerator와 비슷한 서비스(예: CloudFront, Route 53)의 차이점을 설명할 수 있는가?  
- [ ] Global Accelerator의 비용 구조를 이해하고 있는가? (트래픽량 기반 요금제)  

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 Global Accelerator를 떠올리세요:  
> - **저지연**  
> - **글로벌 트래픽 전달**  
> - **서버 트래픽 최적화**  
> - **TCP/SSL 전달**  
> - **비용 효율성**

---

| [⬅️ Route 53](./Route-53.md) | [📑 Day 5 목차](./README.md) | [🏠 Week 2](../README.md) | [다음 Day ➡️](../../week3/day1/README.md) |

---
