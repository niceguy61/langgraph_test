# Week 3 Day 5 복습 퀴즈

## 객관식 (3문제)

### Q1. 다음 중 AWS Step Functions의 주요 기능은 무엇인가요?  
- A) 메시지 전달을 위한 토픽 기반 브로커  
- B) 상태 머신을 기반으로 작업 흐름을 자동화하는 오케스트레이션  
- C) 실시간 데이터 스트리밍을 위한 파티셔닝 기능  
- D) 로그 수집 및 분석을 위한 서비스  

### Q2. EventBridge에서 이벤트 패턴을 정의할 때 필수적으로 포함해야 하는 요소는 무엇인가요?  
- A) `source`, `resources`, `detail`  
- B) `account`, `region`, `timestamp`  
- C) `detail-type`, `event-id`, `version`  
- D) `subject`, `message`, `payload`  

### Q3. SQS FIFO 큐와 표준 큐의 주요 차이점은 무엇인가요?  
- A) FIFO는 메시지 순서 보장, 표준 큐는 메시지 중복 허용  
- B) FIFO는 메시지 중복 허용, 표준 큐는 메시지 순서 보장  
- C) FIFO는 메시지 전달 속도가 더 느림  
- D) FIFO는 모든 메시지를 동일한 큐에 저장  

## OX 문제 (2문제)

### Q4. Kinesis Data Streams는 실시간 데이터 분석을 위해 데이터를 파티셔닝하는 샤드를 사용합니다.  
(O)  
(X)  

### Q5. SNS는 토픽 기반의 메시지 전달 서비스로, 수신자에게 메시지를 즉시 전달합니다.  
(O)  
(X)  

---

## 정답

| 문제 | 정답 | 해설 |
|-----|------|---|
| Q1 | B | Step Functions은 상태 머신을 기반으로 작업 흐름을 자동화하여 복잡한 작업을 단순화합니다. |
| Q2 | A | EventBridge의 이벤트 패턴은 `source`, `resources`, `detail` 필드를 통해 이벤트를 필터링합니다. |
| Q3 | A | SQS FIFO 큐는 메시지 순서 보장 및 중복 제거 기능을 제공하지만, 표준 큐는 순서 보장이 없습니다. |
| Q4 | O | Kinesis Data Streams는 데이터를 샤드로 분산하여 확장성과 파티셔닝을 지원합니다. |
| Q5 | O | SNS는 토픽 기반으로 메시지를 수신자에게 즉시 전달하는 일방향 통신 방식입니다. |