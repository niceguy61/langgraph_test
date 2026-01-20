# Week 1 Day 2 복습 퀴즈

## 객관식 (3문제)

### Q1. 다음 중 IAM 역할을 EC2 인스턴스에 위임할 때 trust 정책에서 `Principal` 필드에 해당하는 서비스는 무엇인가요?  
- A) `ec2.amazonaws.com`  
- B) `lambda.amazonaws.com`  
- C) `sns.amazonaws.com`  
- D) `s3.amazonaws.com`  

### Q2. STS 서비스를 사용해 임시 자격 증명을 생성할 때, 다음 중 올바른 CLI 명령어는 무엇인가요?  
- A) `aws sts get-federationToken`  
- B) `aws sts get-session-token`  
- C) `aws sts assume-role`  
- D) `aws sts get-credentials`  

### Q3. 다음 중 서비스 연결 역할(Service Linked Role)을 자동으로 생성하는 AWS 서비스는 무엇인가요?  
- A) S3  
- B) RDS  
- C) Lambda  
- D) EC2  

## OX 문제 (2문제)

### Q4. 권한 경계(Permission Boundary)는 IAM 엔터티의 권한을 제한하는 정책으로, 해당 정책은 IAM 정책보다 더 엄격할 수 있습니다.  
- O  
- X  

### Q5. AWS Organizations에서 SCP(Service Control Policy)는 조직 내 모든 계정에 적용되며, 계정별 정책을 무시합니다.  
- O  
- X  

---

## 정답

| 문제 | 정답 | 해설 |
|-----|------|---|
| Q1 | **A) `ec2.amazonaws.com`** | IAM 역할의 trust 정책에서 `Principal` 필드는 역할을 사용할 서비스를 지정합니다. EC2 인스턴스는 `ec2.amazonaws.com`로 인증됩니다. |
| Q2 | **C) `aws sts assume-role`** | `assume-role` 명령어는 STS를 통해 역할을 가정하고 임시 자격 증명을 생성합니다. |
| Q3 | **A) S3** | S3 버킷 생성 시 자동으로 `AWSServiceRoleForS3`라는 서비스 연결 역할이 생성됩니다. |
| Q4 | **X** | 권한 경계는 IAM 정책과 동일한 권한 범위를 가질 수 있으며, IAM 정책보다 더 엄격할 수 없습니다. |
| Q5 | **O** | SCP는 조직 내 모든 계정에 강제 적용되며, 계정별 정책은 SCP의 제약을 무시할 수 없습니다. |