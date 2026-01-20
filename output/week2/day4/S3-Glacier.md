---

| [⬅️ S3](./S3.md) | [📑 Day 4 목차](./README.md) | [🏠 Week 2](../README.md) | [다음 Day ➡️](../day5/README.md) |

---

# S3 Glacier 완전 정복

## 📌 핵심 목적 (What & Why)

> **한 줄 정의:** S3 Glacier는 장기 보존 및 저비용으로 데이터를 저장하기 위한 AWS의 대규모 객체 스토리지 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- **문제 1:** 데이터 저장 시 고비용이 발생했습니다. 기존 S3 Standard는 1TB당 월 $15 이상의 비용이 들었고, 장기 보존에 적합하지 않았습니다.  
- **문제 2:** 데이터 보안성 부족으로 중요한 정보가 해킹 위험에 처했습니다. 암호화 기능이 제한적이었고, 접근 제어 설정이 복잡했습니다.  
- **문제 3:** 데이터 관리가 복잡했습니다. 버전 관리, 삭제 보호, 접근 권한 설정 등이 분리되어 있어 운영 효율성이 떨어졌습니다.  

**S3 Glacier로 해결:**
- **해결 1:** **저비용 저장**을 제공합니다. S3 Glacier는 1TB당 월 $0.0045의 저렴한 가격으로 장기 보존이 가능하며, 데이터 접근이 필요할 때만 비용이 발생합니다.  
- **해결 2:** **강력한 암호화 및 접근 제어**를 지원합니다. SSE-KMS, 버킷 정책, ACL 등을 통해 데이터 보안을 강화하고, MFA Delete로 오직 인증된 사용자만 삭제가 가능합니다.  
- **해결 3:** **스마트한 데이터 관리**를 가능하게 합니다. 버전 관리, Object Lock, Lifecycle 정책 등을 통해 데이터 변경 내역을 추적하고, 오래된 데이터는 자동으로 이동 또는 삭제할 수 있습니다.  

### 비유로 이해하기
S3 Glacier는 은행의 안전통장처럼 생각해보세요. 중요한 문서나 자산은 통장에 보관하고, 필요할 때만 찾아보는 방식입니다. 데이터는 저비용으로 저장되며, 암호화와 접근 제어로 보안성을 확보하고, 오래된 데이터는 자동으로 이동하거나 삭제될 수 있습니다. 이렇게 데이터는 안전하게 보존되면서도 비용은 최소화됩니다.

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | **장기 보존이 필요한 데이터 저장** | 금융 기관이 7년 이상 보관해야 하는 고객 계약서 저장 |
| 시나리오 2 | **법적/규제 준수를 위한 데이터 보존** | 의료 기관이 HIPAA 규정에 따라 환자 정보를 10년간 보관 |
| 시나리오 3 | **디스크라우드 복구 및 백업** | 서버 가상화 환경에서 데이터 백업 및 재해 복구 목적으로 사용 |

**이럴 때 S3 Glacier를 선택하세요:**
- ✅ **데이터 접근 빈도가 낮은 경우** (월 1회 이하)  
- ✅ **장기 보존이 필수적인 법적/규제 데이터 저장 시**  
- ✅ **데이터 복구 시 비용을 최소화해야 하는 경우**  

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ **실시간 데이터 접근이 필요한 경우** → **S3 Standard** 사용 (S3 Glacier는 1~5일 이내 데이터 접근에 최적화됨)  
- ❌ **고성능 데이터 처리가 필요한 경우** → **S3 Intelligent-Tiering** 사용 (데이터 접근 빈도에 따라 자동 조정됨)  
- ❌ **저비용이 아닌 고성능 저장이 필요한 경우** → **S3 One Zone-Infrequent Access** 사용 (단일 존에 저장되며, 접근 비용이 낮음)

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| **AWS KMS** | 암호화 키 관리 및 SSE-KMS 암호화 지원 | S3 Glacier → AWS KMS → 데이터 암호화 |
| **S3 Lifecycle Policies** | 자동 데이터 이동 및 삭제 정책 관리 | S3 Glacier → Lifecycle 정책 → S3 Glacier로 이동 |
| **CloudFront** | 데이터 전송 비용 절감 및 성능 최적화 | User → CloudFront → S3 Glacier |

**자주 사용되는 아키텍처 패턴:**
```
User → CloudFront → S3 Glacier (데이터 복구 시)  
User → S3 Glacier (데이터 보존 시)  
S3 Glacier → AWS KMS (암호화 키 관리)  
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| **Storage** | $0.0045/GB/월 (Glacier) | 월 5GB 무료 (12개월) |
| **Data Retrieval** | $0.02/GB (초기 10TB까지 무료) | 10TB 이하 무료 |
| **Data Transfer** | $0.02/GB (인터넷 전송) | 10TB 이하 무료 |

**비용 최적화 팁:**
1. 💡 **Lifecycle 정책 활용**하여 S3 Glacier로 자동 이동: 데이터 접근 빈도가 낮은 경우 자동 이동해 비용 절감  
2. 💡 **데이터 압축** 적용: 파일 크기를 줄여 저장 및 전송 비용을 절감  
3. 💡 **데이터 복구 시간 최소화** 위해 암호화 해제 후 복구: 암호화 해제 후 데이터 복구 시 추가 비용이 발생하지 않도록 주의  

> **⚠️ 비용 주의:** **데이터 복구 시 Retrieval 요금**이 발생할 수 있습니다. 예를 들어, 10TB 이상 데이터를 복구하면 $0.02/GB의 요금이 부과되므로, 복구 전에 비용 계산을 반드시 확인해야 합니다.

## 📚 핵심 개념

### 개념 1: 버킷 정책(Bucket Policy)
S3 Glacier 버킷에 대한 액세스 제어를 정의하는 정책입니다. AWS Identity and Access Management(IAM) 정책 형식을 사용하여 특정 사용자, 그룹, 서비스에 대한 권한을 설정합니다. 이 정책은 S3 버킷과 연결되어 데이터에 대한 접근 권한을 제어하며, 보안 규정 준수(예: GDPR, HIPAA)를 지원하는 데 중요한 역할을 합니다.  

#### 왜 중요한가?
- **권한 관리의 표준화**: 모든 사용자에게 동일한 접근 권한을 부여하는 대신, 특정 조건에 따라 접근을 제어할 수 있습니다.  
- **보안 규정 준수**: 데이터 접근 권한을 명확히 정의하여 법적 요구사항을 충족할 수 있습니다.  

#### 세부 요소
| 요소 | 설명 | 예시 |
|-----|-----|-----|
| **Principal** | 권한을 부여받는 사용자 또는 역할 | `Principal": {"AWS": "arn:aws:iam::123456789012:role/MyRole"}` |
| **Action** | 수행할 수 있는 작업 (예: `s3:GetObject`) | `"Action": "s3:GetObject"` |
| **Resource** | 권한이 적용되는 리소스(버킷 또는 객체) | `"Resource": "arn:aws:s3:::my-bucket"` |
| **Condition** | 추가 조건 (예: IP 주소, 시간대) | `"Condition": {"IpAddress": {"aws:SourceIp": "192.0.2.0/24"}}` |

> **💡 Tip:** 버킷 정책은 IAM 역할을 통해 관리하는 것이 보안적으로 더 안전합니다. 예를 들어, EC2 인스턴스에 IAM 역할을 부여해 S3 접근을 제어할 수 있습니다.

---

### 개념 2: 암호화(SSE-KMS)
S3 Glacier에서 데이터를 암호화하기 위한 **Server-Side Encryption with AWS Key Management Service (SSE-KMS)** 기능입니다. AWS KMS를 사용해 데이터를 암호화하고, 키 관리를 통해 보안성을 높입니다. 이 기능은 데이터 유출 방지, 보안 규정 준수(예: SOC 2, ISO 27001)에 필수적입니다.  

#### 작동 원리
1. **암호화 요청**: 사용자가 S3에 객체를 업로드할 때, 암호화 요청이 생성됩니다.  
2. **KMS 키 요청**: S3는 AWS KMS에 암호화 키를 요청합니다.  
3. **데이터 암호화 및 저장**: KMS가 키를 제공한 후, S3는 데이터를 암호화하여 S3 Glacier에 저장합니다.  

> **💡 Tip:** 암호화된 데이터는 AWS KMS의 키 관리 정책에 따라 복호화 가능하며, 키의 접근 권한을 제어해 보안을 강화할 수 있습니다.

---

### 개념 3: 버전 관리(Versioning)
S3 Glacier에서 **버전 관리**는 동일한 객체에 대해 여러 버전을 저장하여 데이터를 복구할 수 있도록 합니다. 이 기능은 실수로 삭제된 데이터를 복원하거나, 이전 버전의 데이터를 참조하는 데 필수적입니다.  

#### 주요 특징
1. **버전 활성화**: 버전 관리를 활성화하면 모든 객체 변경이 새 버전으로 저장됩니다.  
2. **버전 ID**: 각 객체는 고유한 버전 ID로 식별되며, 이 ID를 통해 특정 버전을 선택적으로 접근할 수 있습니다.  
3. **버전 관리 정책**: 삭제 정책(예: `DeleteMarker` 생성)을 설정해 데이터 삭제 시 복구 가능성을 유지합니다.  

> **💡 Tip:** 버전 관리는 데이터 보호의 핵심 기능으로, 중요한 데이터에 항상 활성화되어야 합니다. 예를 들어, 고객 정보나 기업 내부 문서는 버전 관리를 통해 보호할 수 있습니다.

## 🖥️ AWS 콘솔에서 S3 Glacier 사용하기

### Step 1: S3 Glacier 서비스 접속  
1. AWS Management Console에 로그인합니다  
   - URL: https://console.aws.amazon.com  
2. 상단 검색창에서 **"S3 Glacier"**를 입력하고, **"S3 Glacier"**를 클릭합니다.  
   - **S3 Glacier**는 S3 서비스의 일부로, S3 버킷의 데이터를 Glacier 스토리지 클래스로 이동할 수 있는 기능입니다.  
3. S3 Glacier 대시보드에서 **"S3 버킷"**을 선택하여 작업을 시작합니다.  

> **📸 화면 확인:** S3 Glacier 대시보드에서 "S3 버킷" 탭이 표시되면 정상입니다.  

---

### Step 2: [주요 작업 1 - 리소스 생성]  
1. **S3 버킷 생성**  
   - **"Create bucket"** 버튼을 클릭합니다.  
   - **버킷 이름**을 입력하고, **리전**을 선택합니다.  
     - 예: `my-glacier-bucket` 및 `us-east-1`  
   - **버킷 정책**을 생성할지 선택합니다.  
2. **버전 관리 활성화**  
   - 버킷 생성 후, **"Properties"** > **"Versioning"** 메뉴에서 **"Enable versioning"**을 선택합니다.  
   - 버전 관리는 데이터 복구 및 변경 사항 추적에 필수적입니다.  
3. **암호화 설정**  
   - **"Permissions"** > **"Bucket Policy"**에서 **SSE-S3** 또는 **SSE-KMS**를 선택합니다.  
   - 예: `aws:awsResourceAccessManager`를 사용한 정책을 적용합니다.  

> **📸 화면 확인:** 버킷 생성 후 "Properties" 탭에서 버전 관리 및 암호화 옵션을 확인하세요.  

---

### Step 3: [주요 작업 2 - 설정/구성]  
1. **버킷 정책 설정**  
   - **"Permissions"** > **"Bucket Policy"**에서 **JSON 형식**의 정책을 입력합니다.  
   - 예:  
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Deny",
           "Principal": "*",
           "Action": "s3:PutObject",
           "Resource": "arn:aws:s3:::my-glacier-bucket/*"
         }
       ]
     }
     ```  
2. **ACL 설정**  
   - **"Permissions"** > **"Access Control"**에서 **"Block public access"** 옵션을 활성화합니다.  
   - ACL을 통해 특정 사용자에게만 접근 권한을 부여할 수 있습니다.  
3. **MFA Delete 활성화**  
   - **"Permissions"** > **"Versioning"**에서 **"Enable MFA Delete"**를 선택합니다.  
   - MFA Delete는 삭제 작업 시 MFA 장치 입력이 필요하여 실수 방지에 유용합니다.  

> **⚠️ 주의:** MFA Delete를 활성화하면 버킷 삭제 시 MFA 인증이 필수입니다.  

---

### Step 4: 설정 확인 및 테스트  
1. **생성된 리소스 확인**  
   - **S3 Console**에서 버킷 이름을 검색해 생성된 버킷을 확인합니다.  
   - 버킷 이름, 리전, 버전 관리, 암호화 설정이 올바르게 적용되었는지 확인합니다.  
2. **암호화 상태 확인**  
   - **"Properties"** > **"Encryption"** 탭에서 **SSE-S3** 또는 **SSE-KMS**가 활성화되었는지 확인합니다.  
3. **테스트 데이터 업로드**  
   - **"Upload"** 버튼을 클릭해 객체를 업로드하고, **"GetObject"** 명령어로 데이터를 다운로드해 암호화가 제대로 작동하는지 테스트합니다.  

> **💡 Tip:** AWS CLI를 사용해 설정을 확인할 수 있습니다.  
```bash
aws s3api get-bucket-encryption --bucket my-glacier-bucket
```  

---

### 📋 체크리스트: S3 Glacier 설정 완료 여부  
- [ ] S3 버킷 생성 완료  
- [ ] 버전 관리 활성화 완료  
- [ ] SSE-S3/SSE-KMS 암호화 설정 완료  
- [ ] 버킷 정책 및 ACL 설정 완료  
- [ ] MFA Delete 활성화 완료  
- [ ] 객체 업로드 및 암호화 테스트 완료  

> **💰 비용 주의사항:** S3 Glacier는 **저비용 저장**을 위한 서비스이지만, **데이터 복구 비용**이 발생할 수 있습니다. 프리티어는 12개월 동안 15GB 무료 제공됩니다.

## ⌨️ AWS CLI로 S3 Glacier 사용하기

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
AWS CLI를 사용하기 전에는 최소한의 설정이 필요합니다. `aws --version`은 CLI 버전을 확인하고, `sts get-caller-identity`는 현재 사용자 권한을 확인합니다. 리전은 S3 버킷 생성 시 지역 설정에 영향을 줄 수 있으므로 반드시 확인해야 합니다.

---

### 예제 1: S3 Glacier 리소스 조회
```bash
# S3 버킷 목록 조회 (Glacier 스토리지 클래스 포함)
aws s3api list-buckets --query 'Buckets[*].BucketName' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| `--query` | JSON 응답에서 특정 필드 추출 | `'Buckets[*].BucketName'` |
| `--output` | 출력 형식 (json, table, text) | `table` |

**예상 출력:**
```
| BucketName      |
|-----------------|
| my-glacier-bucket |
| another-bucket  |
```

**팁:**  
`list-buckets`는 현재 AWS 계정에 속한 모든 버킷을 표시합니다. Glacier 스토리지 클래스는 버킷 생성 시 설정해야 합니다.

---

### 예제 2: S3 Glacier 리소스 생성
```bash
# Glacier 스토리지 클래스로 버킷 생성
aws s3api create-bucket \
    --bucket my-glacier-bucket \
    --region ap-northeast-2 \
    --storage-class glacier
```

**필수 옵션:**
- `--bucket`: 생성할 버킷 이름
- `--region`: 리전 (예: `ap-northeast-2`)
- `--storage-class`: 스토리지 클래스 (Glacier, DeepArchive 등)

**예상 출력:**
```json
{
    "Location": "https://my-glacier-bucket.s3.ap-northeast-2.amazonaws.com/"
}
```

**주의사항:**  
Glacier 스토리지 클래스는 데이터 접근이 느리며, 복구 시간이 길 수 있습니다. 데이터 복구 시 추가 비용이 발생할 수 있습니다.

---

### 예제 3: S3 Glacier 버킷 정책 설정
```bash
# 버킷 정책 설정 (S3 Glacier 접근 제한)
aws s3api put-bucket-policy \
    --bucket my-glacier-bucket \
    --policy file://policy.json
```

**policy.json 예시:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "GlacierAccess",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-glacier-bucket/*",
            "Condition": {
                "StringNotLike": {
                    "aws:arn": "arn:aws:s3:::my-glacier-bucket"
                }
            }
        }
    ]
}
```

**설명:**  
버킷 정책은 데이터 접근 권한을 제어합니다. Glacier 버킷은 일반적으로 내부 사용자만 접근하도록 제한해야 합니다. `StringNotLike` 조건은 특정 ARN만 허용합니다.

---

### 예제 4: S3 암호화 및 버전 관리 설정
```bash
# SSE-S3 암호화 및 버전 관리 활성화
aws s3api put-bucket-encryption \
    --bucket my-glacier-bucket \
    --server-side-encryption-configuration '{
        "Rules": [
            {
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "AES256"
                }
            }
        ]
    }'

aws s3api put-bucket-versioning \
    --bucket my-glacier-bucket \
    --versioning-configuration Status=Enabled
```

**설명:**  
- `put-bucket-encryption`은 데이터를 암호화합니다. `SSE-S3`는 AWS 관리 암호화를 사용합니다.
- `put-bucket-versioning`은 버전 관리를 활성화해 변경 사항을 추적합니다.

---

### 예제 5: MFA Delete 및 Object Lock 설정
```bash
# MFA Delete 활성화
aws s3api put-bucket-mfa-delete \
    --bucket my-glacier-bucket \
    --mfa-delete-configuration '{
        "Enabled": true
    }'

# Object Lock 설정
aws s3api put-bucket-object-lock \
    --bucket my-glacier-bucket \
    --object-lock-configuration '{
        "ObjectLockEnabled": {
            "Enabled": true,
            "Rule": {
                "DefaultRetention": {
                    "Mode": "Governance",
                    "Days": 30
                }
            }
        }
    }'
```

**설명:**  
- MFA Delete는 삭제 시 MFA 인증이 필요해 오류 방지에 유용합니다.
- Object Lock은 데이터를 영구히 보호해 복구 불가능한 상태로 설정합니다.

---

### 자주 사용하는 명령어 정리
```bash
# 버킷 생성
aws s3api create-bucket --bucket my-bucket --region us-east-1 --storage-class glacier

# 버킷 정책 설정
aws s3api put-bucket-policy --bucket my-bucket --policy file://policy.json

# 암호화 설정
aws s3api put-bucket-encryption --bucket my-bucket --server-side-encryption-configuration '{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}'

# 버전 관리 활성화
aws s3api put-bucket-versioning --bucket my-bucket --versioning-configuration Status=Enabled

# MFA Delete 활성화
aws s3api put-bucket-mfa-delete --bucket my-bucket --mfa-delete-configuration '{"Enabled": true}'

# Object Lock 설정
aws s3api put-bucket-object-lock --bucket my-bucket --object-lock-configuration '{"ObjectLockEnabled": {"Enabled": true, "Rule": {"DefaultRetention": {"Mode": "Governance", "Days": 30}}}}'
```

---

> **⚠️ 주의:** Glacier 스토리지 클래스는 데이터 접근이 느리며, 복구 시 추가 비용이 발생합니다. 중요한 데이터는 DeepArchive나 Standard 클래스를 고려하세요.  
> **💡 Tip:** 프리티어는 5GB까지 무료로 사용 가능합니다. Glacier 사용 시 비용을 점검하고, 필요한 경우 S3 Glacier Deep Archive로 전환하세요.

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 S3 Glacier 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **S3 Glacier의 저장 클래스로 활용되는 용도**  
   - 설명: S3 Glacier는 **저빈도 액세스 데이터**에 최적화된 저장 클래스로, 장기 보관 및 비용 효율성을 강조합니다. 시험에서 **"저비용, 높은 저장 용량"**을 요구하는 문제에 자주 등장합니다.  
   - 키워드: `저비용`, `저빈도 액세스`, `장기 보관`

2. **Lifecycle 정책을 통한 자동 이동**  
   - 설명: S3 Glacier는 **Lifecycle 정책**을 통해 S3 Standard에서 Glacier로 자동 이동할 수 있어, 데이터 관리 효율성을 높입니다. 시험에서 **"데이터 이동 전략"** 또는 **"비용 최적화"** 관련 문제에 자주 등장합니다.  
   - 키워드: `Lifecycle 정책`, `자동 이동`, `비용 최적화`

3. **데이터 복구 시간(Recovery Time)의 차이**  
   - 설명: Glacier는 **Standard, Expedited, Bulk** 세 가지 복구 옵션을 제공하지만, 시험에서 **"복구 시간과 비용의 균형"**을 묻는 문제가 자주 출제됩니다. 예: "Expedited 복구는 어떤 경우에 사용해야 하나요?"  
   - 키워드: `복구 시간`, `Expedited`, `Bulk`

4. **S3 Glacier의 비용 구조**  
   - 설명: Glacier는 **스토리지 비용 + 복구 비용**으로 구성되며, 시험에서 **"비용 계산"**이나 **"프리티어 활용"** 관련 문제에 자주 등장합니다. 예: "Glacier의 복구 비용은 어떤 요소에 따라 달라지나요?"  
   - 키워드: `비용 계산`, `복구 비용`, `프리티어`

5. **S3 Glacier와 S3 Deep Archive의 차이**  
   - 설명: 시험에서 **"저비용 저장 클래스의 비교"**를 묻는 문제가 자주 출제됩니다. 예: "Deep Archive와 Glacier의 주요 차이점은 무엇인가요?"  
   - 키워드: `Deep Archive`, `복구 시간`, `비용 비교`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | "S3 Glacier는 실시간 액세스를 위한 저장 클래스입니다." → **틀린 설명** | Glacier는 **저빈도 액세스**를 위한 저장 클래스입니다. |
| 함정 2 | "Glacier의 복구 시간은 항상 길다." → **부분적으로 맞지만, 복구 옵션에 따라 달라진다** | **Expedited** 복구 옵션은 3~5시간, **Standard**는 3~12시간, **Bulk**는 5~10일이 걸린다. |
| 함정 3 | "Glacier는 데이터 복구 시 별도 비용이 없다." → **오답** | 복구 시 **데이터 크기 × 복구 옵션 요금**이 추가된다. |

#### 🔄 S3 Glacier vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | S3 Glacier | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| **용도** | **저빈도 액세스 데이터** 저장 | S3 Standard(일반 액세스), S3 One Zone, S3 Deep Archive(최저 비용) | **비용 효율성**과 **데이터 접근 빈도**에 따라 선택 |
| **확장성** | **AWS 전체 글로벌 배포** | S3 Standard(전역), S3 One Zone(지역) | **데이터 접근 빈도**에 따라 확장성 차이 |
| **비용** | **저비용** (스토리지 + 복구 비용) | Deep Archive(더 저비용), S3 Standard(고비용) | **장기 보관** 시 Deep Archive 선택, **실시간 액세스** 시 Standard 선택 |
| **지연시간** | **복구 시간 차이 큼** (Expedited/Standard/Bulk) | S3 Standard(즉시), S3 One Zone(지역) | **데이터 복구 시간**과 **비용 균형** 고려 |

#### 📝 시험 대비 체크리스트
- [ ] S3 Glacier의 핵심 목적을 한 문장으로 설명할 수 있는가?  
  → **저비용, 저빈도 액세스 데이터 저장**  
- [ ] S3 Glacier를 선택해야 하는 시나리오를 알고 있는가?  
  → **장기 보관, 비용 효율성, 액세스 빈도가 낮은 데이터**  
- [ ] S3 Glacier의 제한사항/한계를 알고 있는가?  
  → **복구 시간이 길고, 복구 비용이 추가된다**  
- [ ] S3 Glacier와 비슷한 서비스의 차이점을 설명할 수 있는가?  
  → **Deep Archive는 더 저비용, Standard는 실시간 액세스**  
- [ ] S3 Glacier의 비용 구조를 이해하고 있는가?  
  → **스토리지 비용 + 복구 비용(옵션에 따라)**  

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 S3 Glacier를 떠올리세요:  
> - **저비용**, **저빈도 액세스**, **장기 보관**, **복구 시간**, **비용 효율성**

---

| [⬅️ S3](./S3.md) | [📑 Day 4 목차](./README.md) | [🏠 Week 2](../README.md) | [다음 Day ➡️](../day5/README.md) |

---
