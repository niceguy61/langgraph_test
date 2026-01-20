# Week 4 Day 4 복습 퀴즈

## 객관식 (3문제)

### Q1. 다음 중 EC2 인스턴스의 CPU 사용량을 모니터링할 때 사용하는 CloudWatch 지표는 무엇인가요?  
- A) NetworkIn  
- B) CPUUtilization  
- C) DiskReadBytes  
- D) SystemErrors  

### Q2. CloudWatch Logs Insights에서 로그를 필터링할 때 사용하는 구문은 다음 중哪一个인가요?  
- A) `filter @message contains "error"`  
- B) `fields @timestamp, @message | filter @message like /error/`  
- C) `search "error" in @message`  
- D) `select * from logs where message = "error"`  

### Q3. X-Ray에서 샘플링 비율을 100%로 설정할 때, 어떤 상황에서 사용해야 하나요?  
- A) 개발 환경에서 테스트  
- B) 프로덕션 환경에서 전체 트레이스 수집  
- C) 로그 분석을 위한 샘플링  
- D) 비용 절감을 위한 제한적 수집  

## OX 문제 (2문제)

### Q4. CloudTrail은 S3에 로그를 저장하고, Athena을 통해 이를 분석할 수 있습니다.  
(O/X)  

### Q5. OpenSearch는 실시간 로그 검색 및 분석을 위해 설계된 서비스입니다.  
(O/X)  

---

## 정답

| 문제 | 정답 | 해설 |
|-----|------|---|
| Q1 | **B) CPUUtilization** | EC2 인스턴스의 CPU 사용량은 `CPUUtilization` 지표로 추적됩니다. 이 지표는 CPU 사용률을 % 단위로 표시하며, 알람 설정에 활용됩니다. |
| Q2 | **B) fields @timestamp, @message \| filter @message like /error/** | CloudWatch Logs Insights의 쿼리 구문은 `fields`로 필드 선택 후 `filter`로 조건을 걸 수 있습니다. 정규표현식 `/error/`는 로그 메시지에 "error" 키워드가 포함된 경우를 필터링합니다. |
| Q3 | **B) 프로덕션 환경에서 전체 트레이스 수집** | X-Ray의 샘플링 비율은 100%로 설정하면 모든 트레이스를 수집합니다. 이는 프로덕션 환경에서 성능 문제 진단이나 복잡한 트랜잭션 분석에 사용됩니다. |
| Q4 | **O** | CloudTrail은 S3에 로그를 저장하고, Athena은 S3에 저장된 로그를 SQL 쿼리로 분석할 수 있습니다. 이는 로그 분석을 위한 흔한 결합입니다. |
| Q5 | **O** | OpenSearch는 Elasticsearch 기반으로 설계된 검색 및 분석 서비스로, 실시간 로그 검색, 지연 없는 분석, 시각화 기능을 제공합니다. |