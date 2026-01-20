# Week 1 Day 5 실습 가이드  
**고가용성 & 확장성: ELB, Auto Scaling, Launch Templates 실습**  

---

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
- [ ] **ELB(로드 밸런서) 기본 구성** (ALB 생성 및 테스트)  
- [ ] **Auto Scaling 그룹 설정** (스케일링 정책 및 인스턴스 자동 확장)  
- [ ] **Launch Template 사용** (인스턴스 구성 정의 및 Auto Scaling 연동)  

## ⏱️ 예상 소요 시간  
- 전체 실습: 약 30-45분  
- Step 1: 약 10분  
- Step 2: 약 15분  
- Step 3: 약 10분  
- 리소스 정리: 약 5분  

---

## 📝 실습 단계  

### Step 1: **ALB(애플리케이션 로드 밸런서) 생성** (약 10분)  

#### 1.1 **AWS 콘솔에서 ALB 생성**  
1. [AWS 콘솔](https://console.aws.amazon.com/) 접속 후 **EC2** 서비스로 이동  
2. 좌측 메뉴에서 **Load Balancers** → **Create Load Balancer** 클릭  
3. **Application Load Balancer** 선택  
4. **Name** 입력 (예: `MyALB`)  
5. **VPC** 선택 (기본 VPC 사용)  
6. **Subnets** 선택 (공개 서브넷 2개 선택)  
7. **Security Groups** 선택 (기본 SG 사용)  
8. **Listeners** 설정:  
   - 포트 80 → HTTP → **Action** → **Forward to target group**  
9. **Create** 클릭  

> **📸 화면 확인:** **Load Balancers** 목록에 생성된 ALB 이름이 표시되면 정상입니다.  

#### 1.2 **Target Group 구성**  
1. **Load Balancers** → 생성된 ALB 클릭  
2. **Target Groups** → **Create Target Group**  
3. **Name** 입력 (예: `MyTG`)  
4. **Protocol** → HTTP, **Port** → 80  
5. **VPC** 선택 (동일 VPC)  
6. **Health Check Path** → `/health`  
7. **Create** 클릭  

> **💡 설명:** Target Group은 로드 밸런서가 트래픽을 분배할 대상 인스턴스 목록입니다.  
> **Health Check**는 인스턴스 상태를 모니터링하는 기능으로, 비정상 시 트래픽을 제외합니다.  

#### ✅ Step 1 완료 확인  
- [ ] ALB 목록에 `MyALB` 생성됨  
- [ ] Target Group 목록에 `MyTG` 생성됨  

---

### Step 2: **Auto Scaling 그룹 설정** (약 15분)  

#### 2.1 **Launch Template 생성**  
```bash
# CLI 명령어로 Launch Template 생성
aws ec2 create-launch-template \
  --launch-template-name MyLaunchTemplate \
  --version-description "Initial version" \
  --launch-template-data '{"InstanceType": "t2.micro", "KeyName": "my-key", "SecurityGroups": ["launch-permissions"], "SubnetId": "subnet-12345678", "ImageId": "ami-0c55b159cbfafe1f0"}'
```

> **💡 설명:**  
> - `InstanceType`: t2.micro (무료 티어 지원)  
> - `KeyName`: 사전 생성한 키 쌍 이름  
> - `SecurityGroups`: 기본 보안 그룹 사용  
> - `SubnetId`: ALB과 동일한 VPC의 공개 서브넷  
> - `ImageId`: Amazon Linux 2 AMI  

#### 2.2 **Auto Scaling 그룹 생성**  
1. **EC2** → **Auto Scaling** → **Create Auto Scaling Group**  
2. **Name** 입력 (예: `MyASGroup`)  
3. **Launch Template** 선택: `MyLaunchTemplate`  
4. **Min/Max/Desired Capacity** 설정: 1/2/1  
5. **Load Balancer** 선택: `MyALB`  
6. **Health Check** 설정:  
   - **Health Check Type** → EC2  
   - **Health Check Port** → 80  
   - **Health Check Path** → `/health`  
7. **Create** 클릭  

> **📸 화면 확인:** Auto Scaling 그룹이 생성되고, 상태가 `In Service`로 변경되면 정상입니다.  

#### ✅ Step 2 완료 확인  
- [ ] Auto Scaling 그룹 `MyASGroup` 생성됨  
- [ ] ALB에 인스턴스가 연결됨 (Health Check 상태 확인)  

---

### Step 3: **스케일링 정책 설정** (약 10분)  

#### 3.1 **CloudWatch 알림 기반 스케일링**  
1. **CloudWatch** → **Alarms** → **Create Alarm**  
2. **Name** 입력 (예: `MyScaleOutAlarm`)  
3. **Metric** → **EC2** → **CPUUtilization**  
4. **Dimensions** → `MyASGroup`  
5. **Threshold** → 70, **Period** → 5분, **Evaluation Periods** → 2  
6. **Actions** → **Scale out**  
   - **Auto Scaling Group** → `MyASGroup`  
   - **Desired Capacity** → 3  
7. **Create** 클릭  

#### 3.2 **CLI 명령어로 스케일링 정책 추가**  
```bash
# 스케일링 정책 생성
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name MyASGroup \
  --policy-name MyScaleOutPolicy \
  --scaling-policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration '{"PredefinedMetricSpecification": {"PredefinedMetricType": "CPUUtilization"}, "TargetValue": 70}'
```

> **💡 설명:**  
> - **TargetTrackingScaling**은 CPU 사용률이 70%를 넘으면 자동으로 인스턴스를 확장합니다.  
> - **PredefinedMetricType**은 AWS가 제공하는 메트릭을 기준으로 합니다.  

#### ✅ Step 3 완료 확인  
- [ ] CPUUtilization이 70% 이상일 경우 인스턴스가 자동으로 확장됨  
- [ ] Auto Scaling 그룹의 **Desired Capacity**가 3으로 변경됨  

---

## ✅ 실습 완료 확인  

### 최종 확인 체크리스트  
- [ ] ALB가 정상적으로 동작함  
- [ ] Auto Scaling 그룹이 인스턴스를 자동으로 확장함  
- [ ] Launch Template가 정확히 정의됨  

### 예상 최종 결과  
```bash
# 인스턴스 상태 확인
aws ec2 describe-instances --filters "Name=tag:AutoScalingGroup,Values=MyASGroup"
```

**예상 출력:**  
```
{
  "Reservations": [
    {
      "Instances": [
        {
          "InstanceId": "i-1234567890abcdef0",
          "State": {"Name": "running"},
          "Tags": [{"Key": "AutoScalingGroup", "Value": "MyASGroup"}]
        }
      ]
    }
  ]
}
```

---

## 🔧 트러블슈팅  

### 문제 1: **"AccessDenied" 오류 발생**  
**증상:** `aws` 명령어 실행 시 `AccessDenied` 오류  
**원인:** IAM 사용자 권한 부족  
**해결 방법:**  
1. IAM 사용자 권한 확인:  
   ```bash
   aws iam get-user
   ```
2. 필요한 정책 추가:  
   ```bash
   aws iam attach-user-policy --user-name my-user --policy-arn arn:aws:iam::123456789012:policy/AmazonEC2FullAccess
   ```

### 문제 2: **Target Group 상태가 "healthy"가 아님**  
**증상:** 인스턴스가 health check 실패  
**원인:** 키 쌍 설정 오류 또는 포트 차단  
**해결 방법:**  
1. EC2 인스턴스에 `curl http://localhost:80/health` 실행  
2. 보안 그룹에서 포트 80을 허용  

### 문제 3: **스케일링 정책이 동작하지 않음**  
**증상:** CPU 사용률이 70% 이상임에도 인스턴스 추가 안됨  
**원인:** CloudWatch 알림 설정 오류  
**해결 방법:**  
1. CloudWatch 알림 확인:  
   ```bash
   aws cloudwatch describe-alarms --alarm-name MyScaleOutAlarm
   ```
2. 알림이 활성화되었는지 확인  

---

## 🧹 리소스 정리 (필수!)  

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!  
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.  

### 정리할 리소스 목록  
- [ ] ALB (`MyALB`)  
- [ ] Target Group (`MyTG`)  
- [ ] Auto Scaling 그룹 (`MyASGroup`)  
- [ ] Launch Template (`MyLaunchTemplate`)  

### 리소스 정리 명령어  
```bash
# 1. ALB 삭제
aws elb delete-load-balancer --load-balancer-name MyALB

# 2. Target Group 삭제
aws elb delete-target-group --target-group-arn arn:aws:elasticloadbalancing:region:account:targetgroup/MyTG/1234567890123456

# 3. Auto Scaling 그룹 삭제
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name MyASGroup --force-delete

# 4. Launch Template 삭제
aws ec2 delete-launch-template --launch-template-name MyLaunchTemplate
```

### 정리 완료 확인  
```bash
# 리소스가 모두 삭제되었는지 확인
aws ec2 describe-launch-templates
aws autoscaling describe-auto-scaling-groups
```

---

## 📚 추가 학습 자료  
- [AWS 공식 ELB 문서](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/)  
- [Auto Scaling 정책 설정 가이드](https://docs.aws.amazon.com/autoscaling/ec2/userguide/autoscaling-policies.html)  
- [Launch Template 사용법](https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_CreateLaunchTemplate.html)