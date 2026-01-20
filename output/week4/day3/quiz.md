# Week 4 Day 3 복습 퀴즈

## 객관식 (3문제)

### Q1. 다음 중 GuardDuty의 주요 기능은 무엇인가요?  
- A) 네트워크 장비의 물리적 보안 검사  
- B) 머신러닝 기반의 위협 탐지 및 분석  
- C) 클라우드 리소스의 자동화된 백업 관리  
- D) 사용자 활동 로그의 실시간 분석  

### Q2. Security Hub가 통합하는 주요 보안 데이터 소스는 무엇인가요?  
- A) AWS Lambda, DynamoDB  
- B) CloudTrail, GuardDuty, Inspector  
- C) S3 버킷, VPC 설정  
- D) EC2 인스턴스, RDS 데이터베이스  

### Q3. Config Rules의 주요 목적은 무엇인가요?  
- A) 서버의 성능 최적화  
- B) 자동화된 보안 정책 적용 및 준수 검증  
- C) 데이터베이스 백업 자동화  
- D) 네트워크 트래픽 분석  

## OX 문제 (2문제)

### Q4. CloudTrail은 모든 AWS API 호출과 사용자 활동을 로그로 기록합니다. (O/X)  
### Q5. Detective는 자동으로 발생한 위협을 식별하고, 사용자에게 경고를 제공합니다. (O/X)  

---

## 정답

| 문제 | 정답 | 해설 |
|-----|------|---|
| Q1 | **B** | GuardDuty는 머신러닝 기반의 위협 탐지, 악성 활동 감지, 악성 소프트웨어 분석을 수행합니다. |
| Q2 | **B** | Security Hub는 GuardDuty, Inspector, CloudTrail, AWS WAF 등의 데이터를 통합하여 보안 위험을 분류하고 관리합니다. |
| Q3 | **B** | Config Rules는 AWS 자동화된 보안 정책을 적용하고, 리소스가 규정에 부합하는지 실시간으로 검증합니다. |
| Q4 | **O** | CloudTrail은 모든 AWS API 호출, 사용자 활동, IAM 정책 변경 등을 로그로 기록하여 보안 분석에 활용됩니다. |
| Q5 | **O** | Detective는 자동으로 발생한 위협을 식별하고, 사용자에게 시각화된 보고서와 경고를 제공합니다. |