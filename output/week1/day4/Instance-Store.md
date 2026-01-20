---

| [⬅️ EFS](./EFS.md) | [📑 Day 4 목차](./README.md) | [🏠 Week 1](../README.md) | [Security Groups ➡️](./Security-Groups.md) |

---

> **한 줄 정의:** Instance Store는 EC2 인스턴스의 고성능 임시 저장소를 위한 AWS의 임시 스토리지 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** EC2 인스턴스가 종료되면 데이터가 사라지는 경우가 많아 휴대용 데이터 저장이 어려웠습니다.  
  - 기존에는 로컬 디스크나 외부 저장소에 데이터를 복제해야 했으나, 데이터 일관성 유지가 어려웠습니다.  
- **문제 2:** 고성능 I/O 요구사항(예: DB 서버)에 맞는 스토리지 솔루션이 부족했습니다.  
  - EBS는 성능이 제한적이었고, S3는 로컬 접근이 불가능해 실시간 처리에 부적합했습니다.  
- **문제 3:** 임시 데이터 저장 시 EBS의 고정 비용이 발생해 비용 효율성이 떨어졌습니다.  
  - EBS 볼륨은 1시간당 $0.10 이상의 비용이 발생해 단기 사용 시 비용 부담이 컸습니다.  

**Instance Store로 해결:**
- **해결 1:** 인스턴스 종료 시 데이터가 사라지는 문제를 해결해 임시 데이터 저장에 최적화되었습니다.  
  - 인스턴스 종료 시 자동으로 데이터가 삭제되므로, 장기 저장이 필요 없는 경우에 적합합니다.  
- **해결 2:** 고성능 I/O 처리를 위한 최적화된 스토리지 구조로 DB 서버 등 실시간 처리 요구사항을 충족합니다.  
  - 인스턴스와 동일한 호스트에서 접근하므로, I/O 지연이 최소화됩니다.  
- **해결 3:** 단기 사용 시 EBS 대비 저비용으로 임시 저장소를 제공해 예산 절감 효과를 줍니다.  
  - 인스턴스 종료 시 스토리지 비용이 발생하지 않아, 단기 프로젝트에 적합합니다.  

### 비유로 이해하기
Instance Store는 사무실의 임시 작업 공간에 해당합니다. 예를 들어, 프로젝트가 끝나면 작업 공간을 해제하고 다른 팀이 사용할 수 있도록 합니다. 이처럼 Instance Store는 인스턴스가 종료되면 데이터를 자동으로 삭제해 임시 저장소로 활용되며, 장기 저장이 필요한 데이터는 EBS나 S3로 이동해야 합니다.  

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 임시 데이터 처리에 최적화된 스토리지 | 빅데이터 처리 시 중간 결과를 임시 저장해 메모리 부담을 줄임 |
| 시나리오 2 | 고성능 I/O 요구사항을 충족하는 서버 | Redis 캐싱 서버나 MySQL DB 서버로 인스턴스와 동일한 호스트에서 접근 |
| 시나리오 3 | 단기 프로젝트 및 테스트 환경 | CI/CD 파이프라인에서 임시 저장소로 사용해 비용을 절감 |

**이럴 때 Instance Store를 선택하세요:**
- ✅ **임시 데이터 저장이 필요한 경우**  
- ✅ **실시간 처리 및 고성능 I/O가 필수적인 서버 환경**  
- ✅ **단기 프로젝트 및 테스트 환경에서 비용 절감이 필요한 경우**  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ **장기 저장이 필요한 데이터 → EBS 또는 S3 사용**  
  - EBS는 볼륨 형식을 선택해 지속적인 저장을 가능하게 하며, S3는 대용량 데이터 저장에 적합합니다.  
- ❌ **데이터 일관성 유지가 필요한 경우 → EBS 또는 RDS 사용**  
  - EBS는 볼륨 복제와 스냅샷 기능을 통해 데이터 일관성을 보장하고, RDS는 관계형 데이터베이스로 일관성 유지에 최적화되어 있습니다.  

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **EC2** | Instance Store는 EC2 인스턴스의 디스크로 사용되며, 인스턴스 종료 시 자동으로 삭제됩니다. | EC2 → Instance Store (임시 저장소) → 애플리케이션 |
| **EBS** | 장기 저장이 필요한 데이터는 EBS로 이동해 데이터 일관성을 유지합니다. | EC2 → Instance Store (임시) + EBS (장기 저장) → 애플리케이션 |
| **Security Groups** | 네트워크 접근 제어를 통해 Instance Store의 접근 권한을 제한합니다. | EC2 → Security Groups (접근 제어) → Instance Store |

**자주 사용되는 아키텍처 패턴:**
```
User → EC2 (Instance Store) → 애플리케이션 → EBS (장기 저장)
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **Instance Store 자체 비용** | $0.00 (AWS Free Tier 포함) | 월 750시간 무료 (EC2 사용 시) |
| **인스턴스 종료 시 데이터 복구 비용** | $0.10~$0.50/GB (사용 시) | 12개월 무료 (EC2 프리티어 기준) |
| **데이터 전송 비용** | $0.09/GB (인터넷 전송) | 항상 무료 |

**비용 최적화 팁:**
1. 💡 **EC2 프리티어 활용:** 인스턴스 종료 시 데이터 복구 비용을 최소화하기 위해 프리티어 인스턴스를 우선 사용하세요.  
2. 💡 **데이터 전송 최소화:** 로컬 스토리지와 Instance Store 간 데이터 전송을 줄여 비용을 절감합니다.  
3. 💡 **장기 저장용 EBS 사용:** 임시 데이터는 Instance Store, 지속적인 데이터는 EBS로 분리해 비용 효율성을 극대화합니다.  

> **⚠️ 비용 주의:** 인스턴스 종료 시 데이터 복구 비용이 발생할 수 있으므로, 중요한 데이터는 EBS로 백업해야 합니다. 또한, 인스턴스 종료 후 데이터를 복구할 때는 별도의 비용이 발생하므로 주의해야 합니다.

## 📚 핵심 개념

### 개념 1: Instance Store의 기본 개념 및 중요성  
Instance Store는 AWS EC2 인스턴스에 직접 연결된 **로컬 스토리지**로, 인스턴스가 실행되는 호스트 머신의 물리적 디스크에 데이터를 저장하는 방식입니다. 이는 EBS(Elastic Block Store)와 달리 네트워크를 통해 접근하는 것이 아니라, 인스턴스와 직접 연결되어 **저지연, 고성능**의 I/O 성능을 제공합니다. Instance Store는 **일시적인 데이터**나 **고성능 요구사항**이 있는 작업에 최적화되어 있으며, 인스턴스가 종료되면 데이터가 **자동으로 삭제**되므로 **지속적인 데이터 보존**이 필요 없는 경우에 적합합니다.  

#### 왜 중요한가?  
- **성능 최적화**: 인스턴스와 직접 연결되어 I/O 지연이 최소화되어 고성능 애플리케이션에 적합합니다.  
- **비용 효율성**: EBS보다 저렴하게 고성능 스토리지를 제공합니다.  
- **일시적 데이터 저장**: 임시 작업 결과나 임시 파일 저장에 적합합니다.  

#### 세부 요소  
| 요소 | 설명 | 예시 |
|-----|-----|-----|
| **로컬 스토리지** | 인스턴스의 물리적 디스크에 데이터가 저장됩니다. | GPU 인스턴스에서 고성능 컴퓨팅에 사용 |
| **고성능 I/O** | 네트워크 지연이 없어 데이터 전송 속도가 빠릅니다. | 빅데이터 처리, 실시간 분석 작업 |
| **데이터 임시 저장** | 인스턴스 종료 시 데이터가 자동 삭제됩니다. | 임시 파일, 로그 데이터 저장 |

> **💡 Tip:** Instance Store는 **고성능이 필요하고 데이터 지속성이 필요하지 않은** 경우에만 사용하세요. 중요한 데이터는 EBS나 S3에 백업해야 합니다.

---

### 개념 2: Instance Store vs EBS의 차이  
Instance Store와 EBS는 모두 EC2 스토리지 옵션입니다. 두 서비스의 주요 차이점은 **데이터 저장 방식**, **성능**, **데이터 지속성** 등에서 나타납니다.  

#### 작동 원리  
1. **Instance Store**: 인스턴스와 직접 연결되어 데이터를 로컬 디스크에 저장합니다.  
2. **EBS**: 가상 네트워크를 통해 EC2 인스턴스에 EBS 볼륨을 마운트하여 데이터를 저장합니다.  
3. **데이터 지속성**: Instance Store는 인스턴스 종료 시 데이터가 삭제되지만, EBS는 볼륨이 유지되며 데이터가 지속됩니다.  

> **💡 Tip:** Instance Store는 **고성능이 필요하고 데이터 지속성이 필요하지 않은** 경우, EBS는 **데이터 지속성과 복구 가능성**이 중요한 시나리오에 적합합니다.

---

### 개념 3: Instance Store의 주요 특징 및 사용 사례  
Instance Store는 특정한 고성능 요구사항을 충족시키기 위해 설계된 스토리지 옵션으로, 다음과 같은 특징을 가지고 있습니다.  

#### 주요 특징  
1. **고성능 I/O**: 인스턴스와 직접 연결되어 네트워크 지연이 없어 I/O 성능이 뛰어납니다.  
2. **가격 효율성**: EBS보다 저렴한 가격으로 고성능 스토리지를 제공합니다.  
3. **일시적 데이터 저장**: 인스턴스 종료 시 데이터가 자동 삭제되어 임시 파일 저장에 적합합니다.  

> **💡 Tip:** Instance Store는 **고성능 컴퓨팅**, **임시 데이터 저장**, **GPU/TPU 기반 인스턴스**에서 주로 사용됩니다. 중요한 데이터는 EBS나 S3에 백업해야 합니다.

## 🖥️ AWS 콘솔에서 Instance Store 사용하기

### Step 1: Instance Store 서비스 접속  
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
   - IAM 계정으로 로그인 후, **EC2** 서비스로 이동합니다.  
2. 상단 검색창에서 "Instance Store"를 입력합니다.  
   - **Instance Store**는 EC2 서비스 내부에 포함되어 있으므로, "EC2"로 이동한 후 "Instance Store"를 검색합니다.  
3. 검색 결과에서 "Instance Store"를 클릭합니다.  

> **📸 화면 확인:** Instance Store 대시보드가 표시되면 정상입니다. 이 화면에서는 현재 사용 중인 EC2 인스턴스의 Instance Store 정보와 관리 옵션을 확인할 수 있습니다.  

---

### Step 2: [주요 작업 1 - 리소스 생성]  
1. **인스턴스 생성 및 Instance Store 부착**  
   - EC2 대시보드에서 **"Instances"** 탭을 클릭합니다.  
   - **"Launch Instance"** 버튼을 누르고, 원하는 AMI(예: Ubuntu)와 인스턴스 유형(예: `t2.micro`)을 선택합니다.  
   - **"Storage"** 섹션에서 **"Instance Store"** 옵션을 선택합니다.  
     - 인스턴스 유형에 따라 Instance Store 크기(예: 50GB)가 자동으로 설정됩니다.  
2. **Instance Store 설정**  
   - **"Configure Instance Details"**에서 Instance Store 타입(예: `ssd` 또는 `hdd`)을 선택합니다.  
   - **"Tags"** 섹션에서 리소스를 식별할 수 있는 태그(예: `Name: MyInstanceStore`)를 추가합니다.  
3. **리소스 생성 확인**  
   - **"Review and Launch"**를 클릭한 후, 키 페어를 생성하고 인스턴스를 시작합니다.  

> **📸 화면 확인:** 인스턴스 생성 후, **"Instances"** 탭에서 **"Storage"** 섹션을 확장하면 Instance Store 정보(크기, 상태)가 표시됩니다.  

---

### Step 3: [주요 작업 2 - 설정/구성]  
1. **Instance Store 볼륨 관리**  
   - 인스턴스를 선택한 후, **"Actions" > "Attach Volume"**를 클릭합니다.  
   - 연결할 볼륨을 선택하고, **"Attach"** 버튼을 누르면 볼륨이 인스턴스에 연결됩니다.  
2. **볼륨 설정 변경**  
   - **"Actions" > "Modify Volume"**를 통해 볼륨 크기(예: 100GB로 확장)를 변경할 수 있습니다.  
   - **"Actions" > "Delete Volume"**를 통해 볼륨을 삭제할 수 있지만, 인스턴스가 실행 중인 경우 **"Detached"** 상태로 변경해야 합니다.  
3. **볼륨 상태 모니터링**  
   - **"Volumes"** 탭에서 볼륨 상태(예: `in-use`, `available`)를 확인합니다.  
   - **"Events"** 섹션에서 볼륨 연결/해제 이력을 확인할 수 있습니다.  

> **⚠️ 주의:** Instance Store는 EC2 인스턴스와 함께 삭제됩니다. 볼륨을 영구적으로 저장하려면 **EBS**를 사용해야 합니다.  

---

### Step 4: 설정 확인 및 테스트  
1. **생성된 리소스 확인 방법**  
   - **"Instances"** 탭에서 인스턴스를 선택한 후, **"Storage"** 섹션을 확장해 Instance Store 크기와 상태를 확인합니다.  
2. ** 상태 확인 방법**  
   - **"Volumes"** 탭에서 볼륨 상태를 확인합니다.  
   - **"System Log"** 섹션에서 볼륨 연결/해제 이력을 확인할 수 있습니다.  
3. **정상 동작 테스트**  
   - 인스턴스에 SSH 접속 후, `/dev/xvdf` 또는 `/dev/xvdg` 경로에서 Instance Store 파일 시스템을 확인합니다.  
   - 예: `df -h` 명령어로 디스크 사용량을 확인합니다.  

> **💡 Tip:** Instance Store는 임시 저장소이므로, 중요한 데이터는 EBS로 이동해야 합니다.  
> **💡 Tip:** Instance Store 볼륨을 다른 인스턴스에 연결하려면 볼륨을 **"Detached"** 상태로 변경한 후, 다른 인스턴스에 연결해야 합니다.

## ⌨️ AWS CLI로 Instance Store 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

**⚠️ 주의:** Instance Store는 EC2 인스턴스에 직접 연결된 고성능 스토리지로, CLI로 별도 리소스를 관리할 수 없습니다. EC2 인스턴스 생성 시 Instance Store를 사용할 수 있습니다.  
**💡 Tip:** Instance Store는 EBS와 달리 영구 저장소가 아닙니다. 인스턴스 종료 시 데이터가 사라집니다.  

---

### 예제 1: Instance Store 리소스 조회
```bash
# [Instance Store 리소스 목록 조회]
aws ec2 describe-instances --filters "Name=tag-key,Values=InstanceStore" --query "Reservations[].Instances[].Tags[?Key=='InstanceStore']" --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| --filters | 필터링 조건 (예: 태그 기반 필터) | "Name=tag-key,Values=InstanceStore" |
| --query | JSON 결과 필터링 | "Reservations[].Instances[].Tags[?Key=='InstanceStore']" |
| --output | 출력 형식 | table, json, text |

**예상 출력:**
```
[
  {
    "Key": "InstanceStore",
    "Value": "root-volume"
  },
  {
    "Key": "InstanceStore",
    "Value": "data-volume"
  }
]
```

**💡 Tip:** Instance Store는 EC2 인스턴스의 부팅 디스크(예: /dev/sda1)로 사용되며, CLI로 직접 조회/관리할 수 없습니다.  

---

### 예제 2: Instance Store 리소스 생성
```bash
# [Instance Store 리소스 생성]
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --count 1 \
    --instance-type t2.micro \
    --key-name MyKeyPair \
    --security-group-ids sg-90a81c01 \
    --tag-specifications "ResourceType=instance,Tags=[{Key=InstanceStore,Value=root-volume}]"
```

**필수 옵션:**
- `--image-id`: AMI ID (예: Ubuntu)
- `--instance-type`: 인스턴스 타입 (예: t2.micro)
- `--tag-specifications`: Instance Store 태그 지정

**예상 출력:**
```json
{
    "Instances": [
        {
            "InstanceId": "i-1234567890abcdef0",
            "Tags": [
                {
                    "Key": "InstanceStore",
                    "Value": "root-volume"
                }
            ]
        }
    ]
}
```

**💡 Tip:** Instance Store는 인스턴스 생성 시 자동으로 생성되며, CLI로 별도 생성/삭제가 불가능합니다.  

---

### 예제 3: Instance Store 리소스 수정
```bash
# [Instance Store 리소스 수정]
aws ec2 create-tags \
    --resources i-1234567890abcdef0 \
    --tags "Key=InstanceStore,Value=data-volume"
```

**필수 옵션:**
- `--resources`: 인스턴스 ID
- `--tags`: 수정할 태그 (Key/Value)

**예상 출력:**
```json
{
    "Tags": [
        {
            "Key": "InstanceStore",
            "Value": "data-volume"
        }
    ]
}
```

**⚠️ 주의:** Instance Store는 인스턴스에 직접 연결된 디스크이므로, CLI로 디스크 크기/타입 수정은 불가능합니다.  

---

### 예제 4: Instance Store 리소스 삭제
```bash
# [Instance Store 리소스 삭제]
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# 삭제 확인
aws ec2 describe-instances --instance-ids i-1234567890abcdef0
```

**⚠️ 주의:** Instance Store는 인스턴스 종료 시 자동으로 삭제됩니다. 데이터는 복구 불가능합니다.  

---

### 자주 사용하는 명령어 정리
```bash
# 인스턴스 생성 (Instance Store 포함)
aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 --instance-type t2.micro --tag-specifications "ResourceType=instance,Tags=[{Key=InstanceStore,Value=root-volume}]"

# 인스턴스 조회 (Instance Store 태그 필터)
aws ec2 describe-instances --filters "Name=tag-key,Values=InstanceStore" --query "Reservations[].Instances[].Tags[?Key=='InstanceStore']"

# 태그 수정
aws ec2 create-tags --resources i-1234567890abcdef0 --tags "Key=InstanceStore,Value=data-volume"

# 인스턴스 종료 (Instance Store 삭제)
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

**💡 Tip:** Instance Store는 EC2 인스턴스의 부팅 디스크로 사용되며, CLI로 직접 관리할 수 없습니다. 데이터 백업은 EBS 스냅샷을 사용하세요.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 Instance Store 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **Instance Store vs EBS의 차이점**  
   - 설명: Instance Store는 인스턴스와 밀접하게 연결된 일시적 스토리지로, 데이터는 인스턴스 종료 시 소실됩니다. 반면 EBS는 지속성 스토리지로 볼륨을 분리해 재사용 가능합니다. 시험에서 이 두 서비스의 특성 차이를 묻는 경우가 많습니다.  
   - 키워드: `일시성`, `지속성`, `볼륨 분리`

2. **Instance Store의 제한사항 및 사용 시나리오**  
   - 설명: Instance Store는 데이터 손실 위험이 있으며, 고성능 컴퓨팅(예: 빅데이터 처리, 메모리 캐싱)에 적합합니다. 시험에서는 특정 작업에 Instance Store가 필요한 경우를 묻는 문제가 자주 출제됩니다.  
   - 키워드: `고성능`, `데이터 손실`, `임시 저장소`

3. **Instance Store의 비용 구조**  
   - 설명: Instance Store는 인스턴스 사용 시간에 따라 비용이 발생하며, EBS와 달리 볼륨 요금이 없습니다. 시험에서는 비용 효율성에 대한 비교 질문이 자주 등장합니다.  
   - 키워드: `인스턴스 기반 요금`, `볼륨 요금 없음`, `비용 효율성`

4. **Instance Store의 데이터 백업 및 복구 방법**  
   - 설명: Instance Store는 EBS 스냅샷과 달리 백업이 불가능하며, 데이터 손실 시 복구가 어렵습니다. 시험에서는 이 점을 강조하는 문제나 실무 사례가 등장합니다.  
   - 키워드: `백업 불가`, `데이터 손실`, `복구 어려움`

5. **Instance Store의 네트워크 및 성능 특성**  
   - 설명: Instance Store는 인스턴스와 직접 연결되어 고속 I/O 성능을 제공하지만, 네트워크 기반 스토리지(예: EFS)와 비교할 때 제한적입니다. 시험에서는 성능 vs. 지속성의 균형을 묻는 경우가 많습니다.  
   - 키워드: `고속 I/O`, `네트워크 기반`, `성능 균형`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | "Instance Store는 EBS보다 더 저렴하다"는 문장이 등장할 때 헷갈릴 수 있음 | **Instance Store는 인스턴스 사용 시간에 따라 요금이 발생하지만, EBS와 비교해 볼륨 요금이 없어 비용 효율적일 수 있음** |
| 함정 2 | "Instance Store는 인스턴스 종료 시 데이터를 보존한다"는 오류 | **Instance Store는 인스턴스 종료 시 데이터가 소실됨** |
| 함정 3 | "Instance Store는 EFS와 동일한 방식으로 데이터를 공유한다"는 오해 | **Instance Store는 인스턴스에 고유하게 할당되며, EFS처럼 다중 인스턴스 간 공유 불가능** |

#### 🔄 Instance Store vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | Instance Store | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| **용도** | 인스턴스에 고속 I/O가 필요한 일시적 데이터 저장 | EBS(지속성 스토리지), EFS(다중 인스턴스 공유) | **고성능 메모리 캐싱, 임시 데이터 저장 시** |
| **확장성** | 인스턴스 크기 제한으로 확장성 저하 | EBS(볼륨 확장 가능), EFS(스케일 아웃 지원) | **스케일 아웃이 필요한 경우 EBS/EFS 선택** |
| **비용** | 인스턴스 사용 시간에 따라 요금 발생 | EBS(볼륨 요금 + 데이터 전송 비용) | **단기 작업 시 Instance Store, 지속성 필요 시 EBS 선택** |
| **지연시간** | 높은 I/O 성능(예: 100MB/s 이상) | EFS(네트워크 지연 발생) | **고속 처리가 필수적일 때 Instance Store 선택** |

#### 📝 시험 대비 체크리스트
- [ ] Instance Store의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  (예: "인스턴스에 고속 I/O가 필요한 일시적 데이터 저장에 최적화된 스토리지")  
- [ ] Instance Store를 선택해야 하는 시나리오를 알고 있는가?  
  (예: 메모리 캐싱, 임시 데이터 저장, 고성능 컴퓨팅)  
- [ ] Instance Store의 제한사항/한계를 알고 있는가?  
  (예: 데이터 소실 위험, 인스턴스 종료 시 복구 불가, 네트워크 공유 불가)  
- [ ] Instance Store와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  (예: EBS는 지속성, EFS는 다중 인스턴스 공유)  
- [ ] Instance Store의 비용 구조를 이해하고 있는가?  
  (예: 인스턴스 사용 시간에 따라 요금, 볼륨 요금 없음)

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 Instance Store를 떠올리세요:  
> - **일시성** (데이터 소실 위험)  
> - **고속 I/O** (고성능 요구 시)  
> - **인스턴스 기반** (인스턴스와 밀접하게 연결됨)

---

| [⬅️ EFS](./EFS.md) | [📑 Day 4 목차](./README.md) | [🏠 Week 1](../README.md) | [Security Groups ➡️](./Security-Groups.md) |

---
