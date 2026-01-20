# Week 1 Day 1 복습 퀴즈

## 객관식 (3문제)

### Q1. AWS 리전(Region)과 가용성 존(Availability Zone)의 차이점은 무엇인가요?  
- A) 리전은 AWS의 글로벌 인프라스트럭처이며, AZ는 리전 내의 지역  
- B) 리전은 단일 데이터센터, AZ는 여러 데이터센터로 구성됨  
- C) 리전은 지역별로 서비스를 제공하고, AZ는 특정 국가에 집중됨  
- D) 리전은 서비스 가용성 보장, AZ는 데이터 저장 용도  

### Q2. EC2 인스턴스에서 AWS 자원에 접근할 수 있는 권한을 부여할 때, 다음 중 가장 적절한 IAM 리소스는 무엇인가요?  
- A) IAM 사용자  
- B) IAM 그룹  
- C) IAM 역할  
- D) IAM 정책  

### Q3. 다음 중 Managed Policy와 Inline Policy의 차이점을 올바르게 설명한 것은 무엇인가요?  
- A) Managed Policy는 AWS에서 제공하는 표준 정책, Inline Policy는 사용자 정의 정책  
- B) Managed Policy는 사용자 정의 정책, Inline Policy는 AWS에서 제공하는 정책  
- C) Managed Policy는 특정 리소스에 적용, Inline Policy는 모든 리소스에 적용  
- D) Managed Policy는 고정적, Inline Policy는 동적으로 변경 가능  

## OX 문제 (2문제)

### Q4. MFA는 모든 AWS 계정에서 자동으로 활성화되어야 하며, 모든 IAM 사용자에게 적용됩니다.  
(O/X)  

### Q5. AWS Organizations는 여러 AWS 계정을 하나의 조직으로 통합하여 관리하는 서비스입니다.  
(O/X)  

---

## 정답

| 문제 | 정답 | 해설 |
|-----|------|---|
| Q1 | **C** | 리전은 글로벌 지역을 기준으로 한 AWS 서비스 지역, AZ는 리전 내의 고가용성 데이터센터 그룹입니다. |
| Q2 | **C** | EC2 인스턴스는 서비스 역할(Role)을 통해 IAM 권한을 부여받습니다. 사용자는 직접 자원에 접근할 수 없습니다. |
| Q3 | **A** | Managed Policy는 AWS가 제공하는 표준 정책(예: `AmazonS3ReadOnlyAccess`), Inline Policy는 특정 리소스에 직접 정의한 정책입니다. |
| Q4 | **X** | MFA는 기본적으로 비활성화되며, 보안 정책에 따라 선택적으로 설정해야 합니다. |
| Q5 | **O** | AWS Organizations는 기업용으로 여러 AWS 계정을 통합 관리하고, 통일된 정책을 적용할 수 있습니다. |