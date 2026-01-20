# Week 3 Day 3 복습 퀴즈

## 객관식 (3문제)

### Q1. ElastiCache Redis와 Memcached의 주요 차이점은 무엇인가요?  
- A) Redis는 메모리 기반으로 데이터를 저장하지만 Memcached는 디스크 기반으로 저장  
- B) Redis는 데이터 구조 다양성을 지원하지만 Memcached는 단순 키-값 저장만 가능  
- C) Redis는 분산 클러스터를 지원하지만 Memcached는 단일 노드만 가능  
- D) Redis는 스토리지 확장이 불가능하지만 Memcached는 스토리지 확장이 가능  

### Q2. Amazon Redshift의 데이터 웨어하우스 아키텍처에서 "Compute Node"와 "Storage Node"의 역할은 무엇인가요?  
- A) Compute Node는 데이터 저장, Storage Node는 쿼리 처리  
- B) Compute Node는 쿼리 처리, Storage Node는 데이터 저장  
- C) Compute Node는 메타데이터 관리, Storage Node는 스토리지 확장  
- D) Compute Node는 스토리지 확장, Storage Node는 쿼리 처리  

### Q3. Neptune에서 SPARQL 쿼리로 특정 그래프의 데이터를 조회할 때 사용하는 키워드는 무엇인가요?  
- A) `WHERE`  
- B) `SELECT`  
- C) `GRAPH`  
- D) `MATCH`  

## OX 문제 (2문제)

### Q4. QLDB는 데이터의 불변성을 보장하며, 모든 트랜잭션 로그는 불변성 보장을 위해 암호화되어 저장됩니다.  
(O/X)  

### Q5. Timestream은 시간 시리즈 데이터를 처리할 때, 실시간 쿼리 및 분석을 위한 자동 스케일링 기능을 제공합니다.  
(O/X)  

---

## 정답

| 문제 | 정답 | 해설 |
|-----|------|---|
| Q1 | **B** | Redis는 리스트, 세트, 해시 등의 복잡한 데이터 구조를 지원하지만, Memcached는 단순 키-값 저장만 가능합니다. Redis는 Redis Modules를 통해 확장성도 제공합니다. |
| Q2 | **B** | Redshift는 Compute Node가 쿼리 처리 및 메모리 관리, Storage Node가 데이터 저장 및 병렬 처리를 담당합니다. |
| Q3 | **C** | Neptune의 SPARQL 쿼리에서 `GRAPH` 키워드는 특정 그래프의 데이터를 조회하는 데 사용됩니다. 예: `SELECT * FROM GRAPH 'graph1'` |
| Q4 | **O** | QLDB는 데이터의 불변성을 보장하며, 모든 트랜잭션 로그는 암호화되어 저장되어 데이터 무결성을 유지합니다. |
| Q5 | **O** | Timestream은 실시간 데이터 수집, 분석, 쿼리 처리를 위한 자동 스케일링과 높은 처리량을 지원합니다. |