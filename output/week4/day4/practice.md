# Week 4 Day 4 실습 가이드

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
- [ ] **CloudWatch 대시보드 생성 및 경보 설정**  
- [ ] **CloudWatch Logs Insights로 로그 분석**  
- [ ] **X-Ray로 서비스 추적**  
- [ ] **Athena로 S3 로그 분석**  
- [ ] **OpenSearch로 로그 검색 및 분석**

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분  
- Step 1: 약 10분  
- Step 2: 약 15분  
- Step 3: 약 10분  
- 리소스 정리: 약 5분  

---

## 📝 실습 단계

### Step 1: CloudWatch 지표/경보 설정 (약 10분)

#### 1.1 CloudWatch 지표 생성  
**AWS 콘솔에서:**  
1. 상단 메뉴에서 **CloudWatch** 클릭  
2. 좌측 메뉴에서 **Metrics** → **Create Metric** 선택  
3. **Namespace** 입력: `CustomNamespace`  
4. **Dimensions**에 `Environment=Production` 입력  
5. **Metric Name** 입력: `CustomMetric`  
6. **Value Type** 선택: `Count`  
7. **Create Metric** 클릭  

> **📸 화면 확인:** **Metrics** 탭에 `CustomNamespace`와 `CustomMetric`이 생성되었는지 확인  

**CLI 명령어:**  
```bash
aws cloudwatch put-metric-data --namespace CustomNamespace --metric-name CustomMetric --value 1 --dimensions Environment=Production
```

**예상 출력:**  
```
{
  "Labels": [
    "CustomNamespace/CustomMetric"
  ]
}
```

> **💡 설명:** 이 명령어는 `CustomNamespace` 네임스페이스에 `CustomMetric` 지표를 생성합니다. `Environment` 차원을 `Production`으로 설정합니다.

#### 1.2 경보 설정  
**AWS 콘솔에서:**  
1. **CloudWatch** → **Alarms** → **Create Alarm** 선택  
2. **Namespace** 선택: `CustomNamespace`  
3. **Metric** 선택: `CustomMetric`  
4. **Statistic** 선택: `Average`  
5. **Period** 입력: `5 minutes`  
6. **Evaluation Periods** 입력: `1`  
7. **Threshold** 입력: `1`  
8. **Alarm Name** 입력: `CustomAlarm`  
9. **Actions**에 **Email** 추가: `your-email@example.com`  
10. **Create Alarm** 클릭  

> **📸 화면 확인:** **Alarms** 탭에 `CustomAlarm`이 생성되었는지 확인  

**CLI 명령어:**  
```bash
aws cloudwatch put-metric-alarm --alarm-name CustomAlarm --metric-name CustomMetric --namespace CustomNamespace --statistic Average --period 300 --evaluation-periods 1 --threshold 1 --dimensions Environment=Production --alarm-actions arn:aws:sns:us-east-1:123456789012:your-sns-topic
```

#### ✅ Step 1 완료 확인  
- [ ] **CloudWatch Metrics**에 `CustomNamespace/CustomMetric` 생성  
- [ ] **CloudWatch Alarms**에 `CustomAlarm` 생성  

---

### Step 2: CloudWatch Logs Insights 및 X-Ray 설정 (약 15분)

#### 2.1 CloudWatch Logs Insights 사용  
**AWS 콘솔에서:**  
1. **CloudWatch** → **Logs** → **Logs Insights** 선택  
2. **Query** 입력:  
   ```sql
   fields @timestamp, @message
   | filter @message like /ERROR/
   | sort @timestamp desc
   | limit 10
   ```
3. **Run Query** 클릭  
4. **Results** 확인  

> **📸 화면 확인:** 로그에서 `ERROR` 키워드가 포함된 항목이 정렬되어 표시되는지 확인  

**CLI 명령어:**  
```bash
aws logs get-log-events --log-group-name /var/log/syslog --log-stream-name my-stream --start-time 1630000000000 --end-time 1630100000000 --output json
```

#### 2.2 X-Ray 추적 설정  
**AWS 콘솔에서:**  
1. **X-Ray** → **Create New Trace** 선택  
2. **Service Name** 입력: `MyService`  
3. **Trace ID** 입력: `1234567890abcdef`  
4. **Create Trace** 클릭  

> **📸 화면 확인:** **Trace Graph**에서 추적 흐름이 시각화되어 있는지 확인  

**CLI 명령어:**  
```bash
aws xray put-trace-segment --trace-id 1234567890abcdef --segment my-segment
```

#### ✅ Step 2 완료 확인  
- [ ] **CloudWatch Logs Insights**에서 로그 분석 완료  
- [ ] **X-Ray**에서 추적 생성 완료  

---

### Step 3: Athena 및 OpenSearch 로그 분석 (약 10분)

#### 3.1 Athena로 S3 로그 분석  
**AWS 콘솔에서:**  
1. **Athena** → **Query Editor** 선택  
2. **Database** 선택: `awslogs`  
3. **Query** 입력:  
   ```sql
   SELECT * FROM awslogs.aws_cloudfront_logs
   WHERE log_status = '404'
   LIMIT 10
   ```
4. **Run Query** 클릭  

> **📸 화면 확인:** S3에 저장된 로그에서 `404` 오류가 포함된 항목이 표시되는지 확인  

**CLI 명령어:**  
```bash
aws athena start-query-execution --query-string "SELECT * FROM awslogs.aws_cloudfront_logs WHERE log_status = '404'" --result-configuration "OutputLocation= s3://your-bucket-name/athena-output/"
```

#### 3.2 OpenSearch로 로그 검색  
**AWS 콘솔에서:**  
1. **OpenSearch** → **Dashboard** → **Discover** 선택  
2. **Index** 선택: `cloudfront-logs-*`  
3. **Query** 입력: `log_status: "404"`  
4. **Search** 클릭  

> **📸 화면 확인:** OpenSearch에서 `404` 오류가 포함된 로그가 검색되는지 확인  

**CLI 명령어:**  
```bash
aws opensearchserverless get-logs --log-type "cloudfront-logs"
```

#### ✅ Step 3 완료 확인  
- [ ] **Athena**에서 S3 로그 분석 완료  
- [, ] **OpenSearch**에서 로그 검색 완료  

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트  
- [ ] CloudWatch 대시보드 및 경보 생성 완료  
- [ ] CloudWatch Logs Insights로 로그 분석 완료  
- [ ] X-Ray 추적 설정 완료  
- [ ] Athena로 S3 로그 분석 완료  
- [ ] OpenSearch로 로그 검색 완료  

### 예상 최종 결과  
```bash
# 결과 확인 명령어
aws cloudwatch describe-alarms --alarm-names CustomAlarm
aws logs describe-log-groups --log-group-name /var/log/syslog
aws xray list-traces --trace-id 1234567890abcdef
```

**예상 출력:**  
```
{
  "Alarms": [
    {
      "AlarmName": "CustomAlarm",
      "StateValue": "OK"
    }
  ]
}
```

---

## 🔧 트러블슈팅

### 문제 1: **"AccessDenied" 오류**
**증상:** `AccessDenied` 또는 `UnauthorizedAccess` 오류  
**원인:** IAM 사용자 권한 부족  
**해결 방법:**  
1. IAM 사용자 권한 확인  
2. 필요한 정책 연결  
```bash
# 현재 사용자 권한 확인
aws sts get-caller-identity
```

### 문제 2: **CloudWatch Logs Insights 쿼리 오류**  
**증상:** 쿼리 실행 시 오류 발생  
**원인:** 잘못된 쿼리 구문  
**해결 방법:**  
```bash
# 정확한 쿼리 구문 확인
aws logs get-log-events --log-group-name /var/log/syslog --log-stream-name my-stream --start-time 1630000000000 --end-time 1630100000000 --output json
```

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!  
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록  
- [ ] CloudWatch Metric  
- [ ] CloudWatch Alarm  
- [ ] X-Ray Trace  
- [ ] Athena Query Result  
- [ ] OpenSearch Log Index  

### 리소스 정리 명령어  
```bash
# 1. CloudWatch Metric 삭제
aws cloudwatch delete-metric --namespace CustomNamespace --metric-name CustomMetric

# 2. CloudWatch Alarm 삭제
aws cloudwatch delete-alarms --alarm-names CustomAlarm

# 3. X-Ray Trace 삭제
aws xray delete-trace --trace-id 1234567890abcdef

# 4. Athena Query Result 삭제
aws s3 rm s3://your-bucket-name/athena-output/

# 5. OpenSearch Log Index 삭제
aws opensearchserverless delete-logs --log-type "cloudfront-logs"
```

### 정리 완료 확인  
```bash
# 리소스가 모두 삭제되었는지 확인
aws cloudwatch describe-alarms --alarm-names CustomAlarm
aws logs describe-log-groups --log-group-name /var/log/syslog
```

---

## 📚 추가 학습 자료  
- [AWS CloudWatch 공식 문서](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_GetStarted.html)  
- [X-Ray 튜토리얼](https://docs.aws.amazon.com/xray/latest/devguide/xray-introduction.html)  
- [Athena 사용 가이드](https://docs.aws.amazon.com/athena/latest/ug/what-is-athena.html)  
- [OpenSearch 서버리스 문서](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is-opensearch.html)