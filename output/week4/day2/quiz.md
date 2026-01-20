# Week 4 Day 2 복습 퀴즈

## 객관식 (3문제)

### Q1. 다음 중 AWS KMS CMK 관리에 대한 올바른 설명은 무엇인가요?  
- A) CMK는 수동으로만 생성하고 관리할 수 있습니다.  
- B) CMK 회전은 AWS KMS에서 자동으로 수행됩니다.  
- C) CMK는 암호화 키를 저장하는 데 사용되지만 암호화 알고리즘을 제공하지 않습니다.  
- D) CMK는 AWS KMS 외부의 키 관리 시스템에서만 생성할 수 있습니다.  

### Q2. 봉투 암호화(Envelope Encryption) 메커니즘을 사용하는 AWS 서비스는 무엇인가요?  
- A) AWS CloudHSM  
- B) AWS KMS  
- C) AWS Secrets Manager  
- D) AWS Parameter Store  

### Q3. Secrets Manager에서 자동 교체 기능을 지원하는 것은 무엇인가요?  
- A) AWS ACM 인증서 자동화  
- B) AWS Parameter Store의 동적 파라미터  
- C) AWS Secrets Manager의 자동 교체 정책  
- D) AWS Macie의 데이터 스캔  

---

## OX 문제 (2문제)

### Q4. AWS CloudHSM은 하드웨어 보안 모듈(HSM)을 제공하는 서비스로, 암호화 키의 물리적 보호를 제공합니다. (O/X)  

### Q5. AWS ACM은 인증서를 자동으로 생성, 배포, 관리할 수 있으며, 이는 애플리케이션 통합에 용이합니다. (O/X)  

---

## 정답

| 문제 | 정답 | 해설 |
|-----|------|---|
| Q1 | **C** | KMS CMK는 암호화 키를 저장하는 데 사용되지만, 암호화 알고리즘 자체를 제공하지 않습니다. CMK 회전은 AWS KMS에서 자동/수동으로 수행 가능합니다. |
| Q2 | **B** | KMS는 봉투 암호화(Envelope Encryption)를 지원하며, 데이터 키를 암호화하여 저장하고 복호화 시 사용합니다. |
| Q3 | **C** | Secrets Manager는 자동 교체 정책을 통해 비밀 정보를 주기적으로 교체할 수 있습니다. |
| Q4 | **O** | CloudHSM은 하드웨어 기반의 HSM을 제공해 키의 물리적 보호와 보안성 강화를 지원합니다. |
| Q5 | **O** | ACM은 인증서 생성, 배포, 갱신을 자동화하여 애플리케이션과의 통합을 간소화합니다. |