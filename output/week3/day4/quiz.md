# Week 3 Day 4 복습 퀴즈

## 객관식 (3문제)

### Q1. 다음 중 Lambda 함수의 실행 역할에 대한 설명으로 옳은 것은?  
- A) Lambda 함수는 실행 역할을 통해 S3 버킷에 접근할 수 있다  
- B) 실행 역할은 EC2 인스턴스에서만 생성할 수 있다  
- C) 실행 역할이 없으면 Lambda 함수는 모든 AWS 서비스에 접근할 수 있다  
- D) 실행 역할은 AWS Identity and Access Management(IAM) 정책을 통해 생성된다  

### Q2. VPC 내 Lambda 함수를 배포할 때 필요한 조건은 무엇인가요?  
- A) Lambda 함수는 반드시 공개_subnet에서 실행해야 한다  
- B) VPC 내 Lambda 함수는 NAT 게이트웨이를 필수적으로 사용해야 한다  
- C) Lambda 함수는 VPC를 구성할 때 항상 전용_subnet만 선택해야 한다  
- D) VPC 내 Lambda 함수는 AWS Lambda의 고정 IP 주소를 사용해야 한다  

### Q3. Lambda@Edge의 주요 사용 사례로 옳은 것은?  
- A) 사용자 요청을 기반으로 S3 버킷의 데이터를 실시간으로 변환하는 경우  
- B) CloudFront에 연결하여 글로벌 CDN에서 HTTP 요청을 처리하는 경우  
- C) Lambda 함수를 EC2 인스턴스에 배포하여 실시간 데이터 처리하는 경우  
- D) AWS API Gateway를 통해 REST API를 생성하는 경우  

## OX 문제 (2문제)

### Q4. API Gateway REST API는 HTTP 메서드(GET, POST 등)를 지원하지만, WebSocket API는 실시간 양방향 통신을 지원한다.  
(O/X)  

### Q5. Lambda 계층은 AWS Lambda의 측정 저장소에 저장되며, S3 버킷에 직접 저장할 수 없다.  
(O/X)  

---

## 정답

| 문제 | 정답 | 해설 |
|-----|------|---|
| Q1 | **A** | Lambda 실행 역할은 IAM 정책을 통해 생성되며, S3 접근 권한을 부여하는 역할로 사용됩니다. B는 EC2와 무관하고, C는 실행 역할이 없으면 접근 권한이 없으며, D는 실행 역할 생성은 IAM 정책을 기반으로 합니다. |
| Q2 | **B** | VPC 내 Lambda는 전용_subnet에서 실행되며, NAT 게이트웨이를 통해 외부 네트워크에 접근해야 합니다. 공개_subnet은 사용할 수 없으며, 전용_subnet만 선택해야 합니다. |
| Q3 | **B** | Lambda@Edge는 CloudFront와 통합되어 글로벌 CDN에서 HTTP 요청을 처리합니다. A는 S3 변환 기능은 Lambda@Edge가 아닌 다른 서비스가 제공하며, C는 EC2와 관련이 없고, D는 API Gateway와 무관합니다. |
| Q4 | **O** | REST API는 HTTP 메서드를 지원하고, WebSocket API는 실시간 양방향 통신을 위한 기능입니다. |
| Q5 | **O** | Lambda 계층은 AWS Lambda의 측정 저장소에 저장되며, S3 버킷에 직접 저장할 수 없습니다. |