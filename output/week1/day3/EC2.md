---

| [⬅️ 이전 Day](../day2/README.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 1](../README.md) | [AMI ➡️](./AMI.md) |

---

> **한 줄 정의:** EC2는 클라우드 환경에서 가상 머신을 생성하고 관리하기 위한 AWS의 Compute 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**  
- **문제 1:** 물리 서버를 직접 구매해 운영해야 하며, 서버 수요에 따라 추가 비용이 발생하고 유지보수에 많은 시간이 소요되었습니다.  
- **문제 2:** 서버 수요가 급변할 경우, 미리 구입한 서버의 비용 낭비 또는 처리 능력 부족으로 인한 서비스 중단이 발생했습니다.  
- **문제 3:** 특정 운영체제나 소프트웨어를 설치해 운영해야 하며, 이에 대한 기술 역량이 필요했습니다.  

**EC2로 해결:**  
- **해결 1:** 클라우드 기반 가상 머신을 즉시 생성해 사용할 수 있어 물리 서버 구매 비용을 절감하고, 필요한 만큼만 자원을 사용합니다.  
- **해결 2:** 온디맨드, 예약, 스포트, 전용 등 다양한 구매 옵션을 통해 서버 수요에 유연하게 대응하고 비용을 최적화할 수 있습니다.  
- **해결 3:** AMI(Amazon Machine Image)를 활용해 기존 이미지를 복제해 사용하거나, 커스터마이징된 이미지를 직접 생성해 운영 가능합니다.  

### 비유로 이해하기  
EC2는 대형 주차장의 자동차 대여소를 생각해보세요. 차량을 직접 소유하지 않아도, 필요할 때마다 차량을 대여할 수 있으며, 사용 시간에 따라 비용을 지불합니다. 이처럼 EC2는 클라우드 환경에서 가상 머신을 즉석에서 생성해 사용할 수 있어, 물리 서버 구매와 운영의 복잡성을 해결합니다.  

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 웹 애플리케이션 호스팅 | 스타트업이 AWS EC2로 웹사이트를 운영하며, 트래픽 증가 시 자동으로 인스턴스를 확장합니다. |
| 시나리오 2 | 대규모 데이터 처리 | 데이터 분석 회사가 EC2 스포트 인스턴스를 사용해 대규모 데이터 처리 작업을 수행합니다. |
| 시나리오 3 | 개발/테스트 환경 | 개발 팀이 EC2 예약 인스턴스를 사용해 일정한 성능을 유지하면서 테스트 환경을 구축합니다. |

**이럴 때 EC2를 선택하세요:**  
- ✅ 상황 1: 웹 서버나 애플리케이션 서버를 빠르게 배포해야 할 때  
- ✅ 상황 2: 일시적인 처리 부담이 있을 때 (예: 데이터 분석, 대규모 파일 처리)  
- ✅ 상황 3: 고정된 성능 요구사항이 있을 때 (예: 24/7 운영)  

**이럴 때는 다른 서비스를 고려하세요:**  
- ❌ 상황 → 대안 서비스 추천: EBS가 아닌 S3를 사용해 임시 파일 저장 (S3는 스토리지 용도로 적합)  
- ❌ 상황 → 대안 서비스 추천: 데이터베이스 관리 시 RDS를 사용해 복잡한 설정을 줄임  

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **EBS** | 데이터 저장 및 복구 | EC2 → EBS → 애플리케이션 |
| **RDS** | 관계형 데이터베이스 관리 | EC2 → RDS → 애플리케이션 |
| **CloudFront** | 글로벌 콘텐츠 전송 | User → CloudFront → S3/EC2 |

**자주 사용되는 아키텍처 패턴:**  
```
User → CloudFront → S3 (정적 자산 저장)  
User → EC2 → RDS (동적 데이터 처리)  
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **온디맨드 인스턴스** | $0.015 / 시간 | 월 750시간 무료 |
| **예약 인스턴스** | $0.025 / 월 | 12개월 무료 |
| **스포트 인스턴스** | $0.008 / 시간 | 항상 무료 |

**비용 최적화 팁:**  
1. 💡 팁 1: 일시적인 처리 작업에 스포트 인스턴스를 사용해 비용을 50% 절감할 수 있습니다.  
2. 💡 팁 2: 연간 사용 예상 시 예약 인스턴스를 선택해 단위 시간당 비용을 30% 절감합니다.  
3. 💡 팁 3: 자동 확장(Auto Scaling)을 통해 인스턴스 수를 자동 조절해 비용을 최적화하세요.  

> **⚠️ 비용 주의:** 스포트 인스턴스는 가격 변동 시 인스턴스가 중단될 수 있으므로, 중요한 작업에는 사용을 자제해야 합니다.

## 📚 핵심 개념

### 개념 1: 인스턴스 유형  
EC2 인스턴스 유형은 컴퓨팅 성능, 메모리, 저장 공간, 네트워크 대역폭 등에 따라 분류된 가상 머신 템플릿입니다. 각 유형은 특정 작업에 최적화되어 있으며, 예를 들어 `t2.micro`는 경량 웹 서버에 적합하고, `c5.large`는 고성능 컴퓨팅 작업에 사용됩니다. 이 개념은 리소스 효율성과 비용 최적화를 위해 필수적입니다.  

#### 왜 중요한가?  
- **리소스 최적화**: 작업에 맞는 인스턴스 유형을 선택하면 CPU, 메모리 등 자원을 효율적으로 사용할 수 있습니다.  
- **비용 절감**: 과다한 자원을 사용하지 않으면 비용을 줄이고, 작업 요구에 따라 유연하게 확장할 수 있습니다.  

#### 세부 요소  
| 요소 | 설명 | 예시 |  
|-----|-----|-----|  
| 컴퓨팅 성능 | CPU 코어 수 및 속도를 기준으로 분류 | `c5.large` (고성능 컴퓨팅) |  
| 메모리 | RAM 용량을 기준으로 분류 | `r4.4xlarge` (대용량 메모리) |  
| 저장 공간 | 기본 저장 공간과 EBS 볼륨을 결합 | `gp2` (일반 저장) 또는 `io1` (고성능 저장) |  
| 네트워크 대역폭 | 데이터 전송 속도를 결정 | `m5.large` (고대역폭) |  

> **💡 Tip:** 웹 서버라면 `t2.micro`부터 시작해 성능을 점검하고, 데이터베이스 작업이라면 `db.m5.large` 같은 전용 DB 인스턴스를 사용하세요.  

---

### 개념 2: 구매 옵션(온디맨드/예약/스팟/전용)  
AWS에서 EC2 인스턴스를 사용하는 방식으로, 비용과 유연성을 균형 잡게 설계한 구매 모델입니다. 각 옵션은 사용 목적에 따라 최적화된 비용 효율성을 제공합니다.  

#### 작동 원리  
1. **온디맨드**: 즉시 사용할 수 있지만 단위 시간당 비용이 높습니다. 예를 들어, `t2.micro`는 시간당 $0.0125입니다.  
2. **예약**: 1년 기간 동안 고정된 요금으로 인스턴스를 예약하면, 단위 시간당 비용이 75% 감소합니다.  
3. **스팟**: 비용이 낮지만 인스턴스가 중단될 수 있는 방식입니다. 머신러닝 훈련이나 배포 시 사용이 적합합니다.  
4. **전용**: 특정 지역에만 할당된 인스턴스로, 보안과 고성능이 요구되는 경우에 사용합니다.  

> **💡 Tip:** 스팟 인스턴스는 비용 절감에 유리하지만, 작업 중단 시 데이터 손실 위험이 있으므로 백업을 필수적으로 수행하세요.  

---

### 개념 3: AMI (Amazon Machine Image)  
AMI는 EC2 인스턴스를 생성할 때 사용되는 기반 이미지로, 운영체제, 애플리케이션, 설정 등을 포함합니다. AMI는 일관된 환경을 제공하여 배포 속도를 높이고, 오류를 줄입니다.  

#### 주요 특징  
1. **일관성 보장**: 모든 인스턴스가 동일한 소프트웨어 및 설정을 사용하여 배포 시 오류를 방지합니다.  
2. **빠른 배포**: 이미 준비된 AMI를 기반으로 인스턴스를 생성하면 개발 시간을 절약할 수 있습니다.  
3. **유연한 구성**: 커스터마이징이 가능한 AMI를 사용해 특정 환경에 맞춤형 설정을 적용할 수 있습니다.  

> **💡 Tip:** `user-data`를 사용해 인스턴스 생성 시 자동으로 스크립트를 실행해 웹 서버를 구성할 수 있습니다. 예를 들어, `user-data`에 `#!/bin/bash && apt update && apt install -y apache2`를 입력하면 Apache 웹 서버가 자동으로 설치됩니다.  

---

### 🧾 실습 체크리스트  
1. AWS 콘솔에서 EC2 서비스로 이동하고 인스턴스 유형 선택  
2. 스팟 인스턴스 생성 시 비용 절감 효과 확인  
3. AMI에서 `user-data`를 사용해 웹 서버 자동 설치  
4. CLI 명령어로 인스턴스 생성 및 SSH 접속 테스트  
5. EBS 볼륨을 통해 데이터 저장 공간 확장 시도

## 🖥️ AWS 콘솔에서 EC2 사용하기

### Step 1: EC2 서비스 접속  
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
   - 로그인 후 **"EC2"**를 검색하고 서비스를 클릭합니다.  
2. EC2 대시보드에 도달하면, **"인스턴스"** 탭에서 리소스를 관리할 수 있습니다.  
   - **"Launch Instance"** 버튼을 클릭해 새로운 인스턴스를 생성할 수 있습니다.  

> **📸 화면 확인:** EC2 대시보드가 표시되고, "Launch Instance" 버튼이 보이는지 확인합니다.  

---

### Step 2: [주요 작업 1 - 리소스 생성]  
1. **인스턴스 생성**  
   - **"Launch Instance"** 버튼 클릭 후, **"Select an Amazon Machine Image (AMI)"** 섹션에서 기본 AMI(예: Ubuntu Server)를 선택합니다.  
   - **"Instance Type"**에서 **"t2.micro"**를 선택해 무료 프리티어를 사용할 수 있도록 합니다.  
2. **보안 그룹 설정**  
   - **"Configure Security Group"**에서 **"Add Rule"**을 클릭해 **SSH(22)** 및 **HTTP(80)** 포트를 허용합니다.  
   - **"Security Group"** 이름을 `allow-ssh-http`로 설정하고 저장합니다.  
3. **인스턴스 설정 확인**  
   - **"Review and Launch"** 단계에서 인스턴스 이름, 키 쌍, 네트워크 설정을 확인합니다.  
   - **"Launch"** 버튼을 클릭해 인스턴스를 생성합니다.  

> **📸 화면 확인:** "Launch Instance" 화면에서 인스턴스 설정이 정확하게 입력되었는지 확인하고, "Launch" 버튼을 클릭한 후 생성 완료 메시지가 표시되는지 확인합니다.  

---

### Step 3: [주요 작업 2 - 설정/구성]  
1. **인스턴스 메타데이터 설정**  
   - **"User Data"** 섹션에서 스크립트를 입력해 인스턴스 생성 시 자동으로 웹서버를 설정할 수 있습니다.  
     ```bash
     #!/bin/bash
     apt update && apt install -y apache2
     systemctl start apache2
     systemctl enable apache2
     ```
2. **EBS 볼륨 추가**  
   - **"Storage"** 섹션에서 **"Add New Volume"**을 클릭해 10GB EBS 볼륨을 추가합니다.  
   - 볼륨을 마운트하고, **"Mount Point"**를 `/var/www/html`로 설정합니다.  
3. **태그 설정**  
   - **"Tags"** 섹션에서 **"Key: Project"**, **"Value: WebServer"**를 추가해 리소스를 분류합니다.  

> **⚠️ 주의:** 보안 그룹 설정에서 SSH 및 HTTP 포트를 제대로 열지 않으면 인스턴스에 접근할 수 없으므로, 반드시 확인하세요.  

---

### Step 4: 설정 확인 및 테스트  
1. **인스턴스 상태 확인**  
   - **"Instances"** 탭에서 생성된 인스턴스를 선택해 **"State"**가 `running`인지 확인합니다.  
   - **"Public IP"**를 클릭해 인스턴스의 IP 주소를 확인합니다.  
2. **SSH 접속 및 웹서버 테스트**  
   - **SSH 클라이언트**(예: Terminal, PuTTY)를 사용해 인스턴스에 접속합니다.  
     ```bash
     ssh -i your-key.pem ubuntu@<public-ip>
     ```
   - **`curl http://localhost`** 명령어로 웹서버가 정상적으로 실행되는지 확인합니다.  
3. **HTTP 접근 테스트**  
   - 브라우저에서 인스턴스의 **Public IP**를 입력해 웹서버가 작동하는지 확인합니다.  

> **📸 화면 확인:** 인스턴스 상태가 `running`, SSH 접속 성공, 브라우저에서 웹 페이지가 표시되는지 확인합니다.  

---

### ✅ 실습 목표 달성  
- EC2 인스턴스 생성 및 SSH 접속  
- 웹서버(Apache) 자동 설정  
- EBS 볼륨 추가 및 마운트  
- 보안 그룹 및 태그 설정  

> **💡 Tip:** 프리티어 사용 시 **"t2.micro"** 인스턴스 유형을 선택해야 하며, 월간 사용량이 750시간 이내이면 무료입니다.  
> **⚠️ 주의:** 인스턴스를 종료하지 않으면 비용이 발생하므로, 테스트 후 반드시 종료하세요.

## ⌨️ AWS CLI로 EC2 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

**🔧 준비 사항:**  
AWS CLI를 사용하기 전에 `aws configure` 명령어로 액세스 키, 비밀번호, 리전, 출력 형식을 설정해야 합니다.  
예시:  
```bash
aws configure set aws_access_key_id YOUR_ACCESS_KEY
aws configure set aws_secret_access_key YOUR_SECRET_KEY
aws configure set region ap-northeast-2
aws configure set output json
```

---

### 예제 1: EC2 리소스 조회
```bash
# [EC2 인스턴스 목록 조회]
aws ec2 describe-instances --query 'Reservations[*].Instances[*].{InstanceId:InstanceId, State:State.Name}' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| `--query` | JSON 결과 필터링 | `'Reservations[*].Instances[*].{InstanceId:InstanceId, State:State.Name}'` |
| `--output` | 출력 형식 | `json`, `table`, `text` |

**예상 출력:**
```
|InstanceId | State |
|-----------|-------|
|i-12345678 | running|
|i-87654321 | stopped|
```

**💡 Tip:** `--query`를 사용해 특정 필드만 추출할 수 있습니다. 예: `Instances[*].InstanceId`로 인스턴스 ID만 조회.

---

### 예제 2: EC2 인스턴스 생성
```bash
# [EC2 인스턴스 생성]
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.micro \
    --key-name MyKeyPair \
    --security-group-ids sg-0abcdef12345678901 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Environment,Value=Dev}]'
```

**필수 옵션:**
- `--image-id`: AMI ID (예: `ami-0c55b159cbfafe1f0`)  
- `--instance-type`: 인스턴스 유형 (예: `t2.micro`)  
- `--key-name`: SSH 키 쌍 이름  
- `--security-group-ids`: 보안 그룹 ID  

**예상 출력:**
```json
{
    "Instances": [
        {
            "InstanceId": "i-1234567890abcdef0",
            "State": {
                "Name": "running"
            }
        }
    ]
}
```

**⚠️ 주의:** `--image-id`는 유효한 AMI ID여야 하며, `--key-name`은 사전에 생성한 키 쌍 이름과 일치해야 합니다.

---

### 예제 3: EC2 인스턴스 수정
```bash
# [인스턴스 태그 수정]
aws ec2 create-tags \
    --resources i-1234567890abcdef0 \
    --tags Key=Environment,Value=Prod

# [인스턴스 유형 변경 (중단 후)]
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 modify-instance-attribute --instance-id i-1234567890abcdef0 --instance-type t2.large
aws ec2 start-instances --instance-ids i-1234567890abcdef0
```

**🔧 주의사항:**  
- 인스턴스 유형 변경은 중단 후에만 가능합니다.  
- 태그 수정은 `create-tags` 명령어로 수행할 수 있습니다.

---

### 예제 4: EC2 인스턴스 삭제
```bash
# [인스턴스 종료]
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# [삭제 확인]
aws ec2 describe-instances --instance-ids i-1234567890abcdef0
```

**⚠️ 주의:**  
- `terminate-instances`는 즉시 인스턴스를 종료하고, 데이터는 손실될 수 있습니다.  
- 삭제 후 `describe-instances`로 상태를 확인할 수 있습니다.  

---

### 자주 사용하는 명령어 정리
```bash
# 조회
aws ec2 describe-instances --filters Name=tag:Environment,Values=Dev
aws ec2 describe-instances --instance-ids i-1234567890abcdef0

# 생성
aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 --instance-type t2.micro --key-name MyKeyPair

# 수정
aws ec2 create-tags --resources i-1234567890abcdef0 --tags Key=Environment,Value=Prod

# 삭제
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

**💡 Tip:** `--filters`를 사용해 특정 태그로 필터링할 수 있습니다. 예: `Name=tag:Environment,Values=Dev`로 개발 환경 인스턴스만 조회.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 EC2 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **인스턴스 유형 (Instance Types)**  
   - 설명: EC2의 성능, 메모리, CPU 등 하드웨어 사양을 결정하며, 특정 워크로드에 최적화된 타입(예: compute-optimized, memory-optimized)을 선택해야 합니다. 시험에서는 비용 효율성과 성능 요구사항을 고려한 타입 선택 방안을 평가합니다.  
   - 키워드: `Instance Types`, `Performance`, `Cost Optimization`

2. **구매 옵션 (Purchase Options: On-Demand/Reserved/Spot/Dedicated)**  
   - 설명: 비용 관리의 핵심입니다. 예약(Reserved)은 장기 사용 시 할인, 스포트(Spot)는 잔여 자원 활용, 전용(Dedicated)은 보안 요구사항을 충족하는 경우 선택합니다. 시험에서는 각 옵션의 장단점과 적절한 시나리오를 묻는 경우가 많습니다.  
   - 키워드: `On-Demand`, `Reserved Instances`, `Spot Instances`, `Dedicated Instances`

3. **AMI (Amazon Machine Image)**  
   - 설명: 인스턴스 생성 시 사용되는 템플릿으로, OS, 애플리케이션, 설정 등을 사전에 패킹해 효율적인 배포를 가능하게 합니다. 시험에서는 AMI의 구성 요소(예: EBS, S3)나 개인 AMI 생성 방법을 주요 포인트로 출제합니다.  
   - 키워드: `AMI`, `EBS`, `S3`, `Custom AMI`

4. **사용자 데이터 (User Data)**  
   - 설명: 인스턴스 생성 시 초기 설정을 자동화하는 데 사용됩니다. 예를 들어, SSH 키나 스크립트를 통해 자동 배포를 수행할 수 있습니다. 시험에서는 사용자 데이터와 인스턴스 메타데이터의 차이를 묻는 문제가 자주 출제됩니다.  
   - 키워드: `User Data`, `Instance Metadata`, `Auto-Deployment`

5. **인스턴스 메타데이터 (Instance Metadata)**  
   - 설명: 런타임 중 인스턴스의 정보(예: IP 주소, 보안 그룹)를 제공하며, 이는 네트워크 설정이나 구성 관리 도구에서 활용됩니다. 시험에서는 메타데이터의 접근 방법과 보안 관련 주의사항을 중심으로 출제됩니다.  
   - 키워드: `Instance Metadata`, `Metadata Endpoint`, `Security Group`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | "스팟 인스턴스는 항상 저렴한 비용"이라는 오해 | 스포트 인스턴스는 자원 가용성에 따라 가격이 변동하며, 중단 시 작업이 손실될 수 있음 |
| 함정 2 | "AMI는 항상 EBS 타입"이라고 생각 | AMI는 EBS, S3, 또는 파운데이션 타입으로 구성 가능하며, EBS는 스토리지 방식에 따라 달라짐 |
| 함정 3 | "사용자 데이터는 인스턴스 생성 후에만 접근 가능"이라고 생각 | 사용자 데이터는 인스턴스 생성 시 즉시 접근 가능하며, 메타데이터는 런타임 중에도 실시간으로 확인 가능 |

#### 🔄 EC2 vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | EC2 | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | 가상 머신 기반의 서버 실행 | Lambda (서버리스), Fargate (컨테이너) | 서버 자원 제어가 필요한 경우 |
| 확장성 | 수동/자동 확장 가능 | Lambda는 무한 확장, Fargate는 리소스 기반 확장 | 트래픽 변동성이 큰 경우 |
| 비용 | On-Demand/Reserved/Spot 옵션 | Lambda는 실행 시간 기반, Fargate는 CPU/메모리 기반 | 비용 구조가 복잡한 경우 |
| 지연시간 | 네트워크 지연 발생 가능 | Lambda/Fargate는 레이턴시 최소화 | 실시간 처리가 필요한 경우 |

#### 📝 시험 대비 체크리스트
- [ ] EC2의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  (예: "가상 머신을 생성하여 애플리케이션을 실행하는 컴퓨팅 서비스")
- [ ] EC2를 선택해야 하는 시나리오를 알고 있는가?  
  (예: 고성능 컴퓨팅, 장기 실행 작업, 커스터마이징이 필요한 경우)
- [ ] EC2의 제한사항/한계를 알고 있는가?  
  (예: 스포트 인스턴스 중단, 네트워크 지연, 자원 할당 제한)
- [ ] EC2와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  (예: EC2 vs Lambda: 서버 관리 필요 여부)
- [ ] EC2의 비용 구조를 이해하고 있는가?  
  (예: On-Demand vs Reserved의 할인 비율, 스포트 인스턴스의 가격 변동)

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 EC2를 떠올리세요:  
> - `Instance Types`  
> - `Purchase Options`  
> - `AMI`  
> - `User Data`  
> - `Instance Metadata`

---

| [⬅️ 이전 Day](../day2/README.md) | [📑 Day 3 목차](./README.md) | [🏠 Week 1](../README.md) | [AMI ➡️](./AMI.md) |

---
