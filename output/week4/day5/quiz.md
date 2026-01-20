# Week 4 Day 5 복습 퀴즈

## 객관식 (3문제)

### Q1. 다음 중 CloudFormation에서 중첩 스택(Nested Stack)을 생성하는 방법은 무엇인가요?  
- A) `AWS::CloudFormation::Stack` 리소스를 사용하여 외부 스택에서 내부 스택을 참조  
- B) `AWS::CloudFormation::Resource`를 사용하여 스택 내부 리소스 정의  
- C) `AWS::CloudFormation::Output`을 통해 스택 출력값을 전달  
- D) `AWS::CloudFormation::Parameter`를 사용하여 파라미터 전달  

### Q2. AWS CDK의 주요 장점은 무엇인가요?  
- A) 템플릿 기반 인프라 정의  
- B) 코드 기반 인프라 정의 및 자동화된 배포  
- C) CLI를 통한 인프라 관리  
- D) 비용 최적화 기능 제공  

### Q3. Systems Manager의 State Manager 주요 기능은 무엇인가요?  
- A) 서버 가상화 관리  
- B) 시스템 구성 자동화 및 모니터링  
- C) 데이터베이스 백업 관리  
- D) 네트워크 보안 정책 관리  

## OX 문제 (2문제)

### Q4. Well-Architected Framework의 6대 원칙은 보안, 비용, 성능, 신뢰성, 운영 우수성, 지속 가능성으로 구성됩니다.  
(O / X)  

### Q5. Reserved Instances는 모든 경우에서 가장 저비용 인프라 옵션입니다.  
(O / X)  

---

## 정답

| 문제 | 정답 | 해설 |
|-----|------|---|
| Q1 | **A** | 중첩 스택은 `AWS::CloudFormation::Stack` 리소스를 사용해 외부 스택에서 내부 스택을 참조하는 방식으로 생성됩니다. |
| Q2 | **B** | CDK는 TypeScript/Python/Java로 인프라를 코드로 정의하고, 자동화된 배포와 관리를 지원합니다. |
| Q3 | **B** | State Manager는 시스템 구성 자동화(예: 패치 관리, 소프트웨어 설치), 모니터링, 보고 기능을 제공합니다. |
| Q4 | **O** | 6대 원칙은 보안, 비용 최적화, 성능, 신뢰성, 운영 우수성, 지속 가능성입니다. |
| Q5 | **X** | Reserved Instances는 장기 사용 시 비용 효율적이지만, 단기 사용 시 Spot Instance나 On-Demand가 더 저렴할 수 있습니다. |