# AWS-Certified-Solutions-Architect-Associate_Exam-Guide

  
버전 1.1 SAA-C03  1 | 페이지 
AWS Certified Solutions Architect - Associate(SAA-C03) 시험 안내서 
서론 
AWS Certified Solutions Architect - Associate(SAA-C03) 시험은 Solutions Architect 
역할을 수행하는 개인을 대상으로 합니다. 이 시험에서는 응시자가 AWS Well-Architected 
Framework 를 기반으로 솔루션을 설계할 수 있는지 확인합니다.  
또한 이 시험에서는 응시자가 다음과 같은 태스크를 완료할 수 있는지도 확인합니다. 
• 현재 비즈니스 요구 사항과 향후 예상되는 요구 사항을 충족하도록 AWS 서비스를 
통합하는 솔루션 설계 
• 안전하고 복원력이 뛰어나며 성능이 우수하고 비용에 최적화된 아키텍처 설계 
• 기존 솔루션 검토 및 개선 사항 결정 
대상 응시자 설명 
대상 응시자는 AWS 서비스를 사용하는 클라우드 솔루션을 설계한 1 년 이상의 실무 경험이 
있어야 합니다. 
부록을 참고하여 시험에 출제될 수 있는 기술 및 개념의 목록, 시험 범위에 해당하는 AWS 
서비스 및 기능의 목록, 시험 범위가 아닌 AWS 서비스 및 기능의 목록을 확인하시기 바랍니다. 
시험 콘텐츠 
답안 유형 
이 시험의 문항은 두 가지 유형으로 제공됩니다.  
• 선다형: 정답 1 개와 오답 3 개(정답 이외의 답)가 있습니다. 
• 복수 응답형: 5 개 이상의 응답 항목 중에 2 개 이상의 정답이 있습니다. 
문장을 가장 잘 완성하거나 질문에 대한 답으로 가장 적합한 응답을 하나 이상 선택합니다. 정답 
이외의 답 또는 오답은 지식이나 기술이 부족한 응시자가 선택할 가능성이 큰 응답 항목입니다. 
정답 이외의 답은 일반적으로 콘텐츠 영역에 부합하여 맞아 보이는 응답입니다. 
답을 하지 않은 문항은 오답으로 처리됩니다. 󳰜에 따른 불이익은 없습니다. 시험에는 점수에 
반영되는 50 개의 문항이 포함되어 있습니다. 

 
버전 1.1 SAA-C03  2 | 페이지 
채점되지 않는 콘텐츠 
시험에는 점수에 반영되지 않아 채점되지 않는 15 개의 문항이 포함되어 있습니다. AWS 는 
채점되지 않는 문항에 대한 응시자 성적 정보를 수집하여 추후 채점 대상 문항으로 사용할 수 
있도록 이러한 문항을 평가합니다. 이러한 채점되지 않는 질문은 시험에서 식별되지 않습니다.  
시험 결과 
AWS Certified Solutions Architect - Associate(SAA-C03) 시험은 합격 또는 불합격이 
결정되는 시험입니다. AWS 전문가가 자격증 분야 모범 사례 및 지침에 따라 설정한 최소 표준을 
기준으로 시험 점수를 매깁니다.  
시험 결과는 100~1,000 점의 변환 점수로 보고됩니다. 합격 최소 점수는 720 점입니다. 
응시자의 점수는 전반적인 시험 성적과 합격 여부를 보여줍니다. 변환 점수 모델은 난이도가 
조금씩 다를 수 있는 여러 시험 형식에 걸쳐 점수를 균등하게 조정하는 데 도움이 됩니다. 
점수 보고서에는 섹션 레벨별로 성적 분류표가 포함될 수 있습니다. 시험은 보상 점수 모델을 
사용하므로 각 섹션에서 합격 점수를 얻을 필요는 없으며, 전체 시험에만 합격하면 됩니다. 
시험의 섹션마다 특정 가중치가 적용되므로 일부 섹션은 다른 섹션보다 문항 수가 많습니다. 
분류표에는 응시자의 장단점을 강조하여 보여주는 일반 정보가 포함되어 있습니다. 섹션별 
피드백을 파악할 때 주의하시기 바랍니다.  
내용 개요 
이 시험 안내서에서는 시험의 가중치, 콘텐츠 도메인 및 태스크 설명 자료를 제공합니다. 이 
안내서에서 시험 내용의 전체 목록을 제공하지는 않습니다. 그러나 각 태스크 설명에 관한 추가 
맥락 정보를 사용하여 시험을 준비하는 데 참고할 수 있습니다.  
시험의 콘텐츠 도메인과 가중치는 다음과 같습니다. 
• 도메인 1: 보안 아키텍처 설계(채점 대상 콘텐츠의 30%) 
• 도메인 2: 복원력을 갖춘 아키텍처 설계(채점 대상 콘텐츠의 26%) 
• 도메인 3: 고성능 아키텍처 설계(채점 대상 콘텐츠의 24%) 
• 도메인 4: 비용에 최적화된 아키텍처 설계(채점 대상 콘텐츠의 20%) 
  

 
버전 1.1 SAA-C03  3 | 페이지 
도메인 1: 보안 아키텍처 설계 
태스크 설명 1.1: AWS 리소스에 대한 보안 액세스를 설계합니다.  
관련 지식: 
• 여러 계정에 대한 액세스 제어 및 관리 
• AWS 페더레이션 액세스 및 자격 증명 서비스(예: AWS Identity and Access 
Management[IAM], AWS IAM Identity Center[AWS Single Sign-On]) 
• AWS 글로벌 인프라(예: 가용 영역, AWS 리전) 
• AWS 보안 모범 실무(예: 최소 권한의 원칙) 
• AWS 공동 책임 모델 
관련 기술: 
• IAM 사용자 및 루트 사용자에게 AWS 보안 모범 실무 적용(예: 다중 인증[MFA]) 
• IAM 사용자, 그룹, 역할 및 정책을 포함하는 유연한 권한 부여 모델 설계 
• 역할 기반 액세스 제어 전략 설계(예: AWS Security Token Service[AWS STS], 
역할 전환, 교차 계정 액세스) 
• 여러 AWS 계정에 대한 보안 전략 설계(예: AWS Control Tower, 서비스 제어 
정책[SCP]) 
• AWS 서비스에 적합한 리소스 정책 사용 결정 
• 디렉터리 서비스를 IAM 역할과 연동할 시기 결정 
태스크 설명 1.2: 안전한 워크로드 및 애플리케이션을 설계합니다. 
관련 지식: 
• 애플리케이션 구성 및 보안 인증 정보의 보안 
• AWS 서비스 엔드포인트 
• AWS 에서 포트, 프로토콜 및 네트워크 트래픽 제어 
• 안전한 애플리케이션 액세스 
• 보안 서비스와 적합한 사용 사례(예: Amazon Cognito, Amazon GuardDuty, 
Amazon Macie) 
• AWS 외부의 위협 벡터(예: DDoS, SQL 명령어 삽입) 
관련 기술: 
• 보안 구성 요소(예: 보안 그룹, 라우팅 테이블, 네트워크 ACL, NAT 게이트웨이)로 
VPC 아키텍처 설계 
• 네트워크 분할 전략 결정(예: 퍼블릭 서브넷 및 프라이빗 서브넷 사용) 

 
버전 1.1 SAA-C03  4 | 페이지 
• 보안 애플리케이션에 AWS 서비스 통합(예: AWS Shield, AWS WAF, IAM Identity 
Center, AWS Secrets Manager) 
• AWS 클라우드와의 외부 네트워크 연결 보호(예: VPN, AWS Direct Connect) 
태스크 설명 1.3: 적합한 데이터 보안 제어를 결정합니다. 
관련 지식: 
• 데이터 액세스 및 거버넌스 
• 데이터 복구 
• 데이터 보존 및 분류 
• 암호화 및 적합한 키 관리 
관련 기술: 
• 규정 준수 요구 사항을 충족하도록 AWS 기술 조율 
• 저장 데이터 암호화(예: AWS Key Management Service[AWS KMS]) 
• 전송 중 데이터 암호화(예: TLS 를 사용하는 AWS Certificate Manager[ACM]) 
• 암호화 키에 대한 액세스 정책 구현 
• 데이터 백업 및 복제(replication) 구현 
• 데이터 액세스, 수명 주기 및 보호를 위한 정책 구현 
• 암호화 키 교체 및 인증서 갱신 
도메인 2: 복원력을 갖춘 아키텍처 설계  
태스크 설명 2.1: 확장 가능하고 느슨하게 결합된 아키텍처를 설계합니다. 
관련 지식: 
• API 생성 및 관리(예: Amazon API Gateway, REST API) 
• AWS Managed Services 와 적합한 사용 사례(예: AWS Transfer Family, Amazon 
Simple Queue Service[Amazon SQS], Secrets Manager) 
• 캐싱 전략 
• 마이크로서비스의 설계 원칙(예: 스테이트리스 워크로드와 스테이트풀 워크로드 
비교) 
• 이벤트 기반 아키텍처  
• 수평적 크기 조정 및 수직적 크기 조정 
• 엣지 액셀러레이터를 적절하게 사용하는 방법(예: 콘텐츠 전송 네트워크[CDN]) 
• 애플리케이션을 컨테이너로 마이그레이션하는 방법 
• 로드 밸런싱 개념(예: Application Load Balancer) 

 
버전 1.1 SAA-C03  5 | 페이지 
• 멀티 티어 아키텍처 
• 대기열 및 메시징 개념(예: 게시/구독) 
• 서버리스 기술 및 패턴(예: AWS Fargate, AWS Lambda) 
• 연관된 특성이 있는 스토리지 유형(예: 객체, 파일, 블록) 
• 컨테이너의 오케스트레이션(예: Amazon Elastic Container Service[Amazon 
ECS], Amazon Elastic Kubernetes Service[Amazon EKS]) 
• 읽기 전용 복제본 사용 시기  
• 워크플로 오케스트레이션(예: AWS Step Functions) 
관련 기술: 
• 요구 사항에 따라 이벤트 기반, 마이크로서비스 및/또는 멀티 티어 아키텍처 설계 
• 아키텍처 설계에 사용되는 구성 요소의 크기 조정 전략 결정 
• 요구 사항에 따라 느슨한 결합을 달성하는 데 필요한 AWS 서비스 결정 
• 컨테이너 사용 시기 결정  
• 서버리스 기술 및 패턴 사용 시기 결정 
• 요구 사항에 따라 적합한 컴퓨팅, 스토리지, 네트워킹 및 데이터베이스 기술 권장 
• 워크로드에 맞춰 특별히 구축된 AWS 서비스 사용 
태스크 설명 2.2: 고가용성 및/또는 내결함성 아키텍처를 설계합니다. 
관련 지식: 
• AWS 글로벌 인프라(예: 가용 영역, AWS 리전, Amazon Route 53) 
• AWS Managed Services 와 적합한 사용 사례(예: Amazon Comprehend, 
Amazon Polly) 
• 기본 네트워킹 개념(예: 라우팅 테이블) 
• 재해 복구(DR) 전략(예: 백업 및 복원, 파일럿 라이트, 웜 대기, 액티브-액티브 장애 
조치, RPO[복구 시점 목표], RTO[복구 시간 목표]) 
• 분산 설계 패턴 
• 장애 조치 전략  
• 변경 불가능한 인프라 
• 로드 밸런싱 개념(예: Application Load Balancer) 
• 프록시 개념(예: Amazon RDS Proxy) 
• 서비스 할당량 및 제한(예: 대기 환경에서 워크로드에 대한 서비스 할당량을 구성하는 
방법) 
• 스토리지 옵션 및 특성(예: 내구성, 복제(replication)) 
• 워크로드 가시성(예: AWS X-Ray) 

 
버전 1.1 SAA-C03  6 | 페이지 
관련 기술: 
• 인프라 무결성을 보장하기 위한 자동화 전략 결정 
• AWS 리전 또는 가용 영역 전체에서 고가용성 및/또는 내결함성 아키텍처를 
제공하는 데 필요한 AWS 서비스 결정 
• 비즈니스 요구 사항에 따라 지표를 파악하여 고가용성 솔루션 제공 
• 단일 장애 지점을 완화하기 위한 설계 구현 
• 데이터의 내구성과 가용성을 보장하기 위한 전략 구현(예: 백업) 
• 비즈니스 요구 사항을 충족하는 적합한 DR 전략 선택 
• 레거시 애플리케이션과 클라우드용으로 구축되지 않은 애플리케이션의 신뢰성을 
개선하는 AWS 서비스 사용(예: 애플리케이션 변경이 불가능한 경우) 
• 워크로드에 맞춰 특별히 구축된 AWS 서비스 사용 
도메인 3: 고성능 아키텍처 설계  
태스크 설명 3.1: 고성능 및/또는 확장 가능한 스토리지 솔루션을 결정합니다. 
관련 지식: 
• 비즈니스 요구 사항을 충족하는 하이브리드 스토리지 솔루션  
• 스토리지 서비스와 적합한 사용 사례(예: Amazon S3, Amazon Elastic File 
System[Amazon EFS], Amazon Elastic Block Store[Amazon EBS]) 
• 연관된 특성이 있는 스토리지 유형(예: 객체, 파일, 블록) 
관련 기술: 
• 성능 요구 사항을 충족하는 스토리지 서비스 및 구성 결정 
• 향후 요구 사항을 수용하도록 크기 조정 가능한 스토리지 서비스 결정 
태스크 설명 3.2: 고성능의 탄력적인 컴퓨팅 솔루션을 설계합니다. 
관련 지식: 
• AWS 컴퓨팅 서비스와 적합한 사용 사례(예: AWS Batch, Amazon EMR, Fargate)  
• AWS 글로벌 인프라 및 엣지 서비스에서 지원하는 분산 컴퓨팅 개념 
• 대기열 및 메시징 개념(예: 게시/구독) 
• 확장성 기능과 적합한 사용 사례(예: Amazon EC2 Auto Scaling, AWS Auto 
Scaling) 
• 서버리스 기술 및 패턴(예: Lambda, Fargate) 
• 컨테이너의 오케스트레이션(예: Amazon ECS, Amazon EKS) 
  

 
버전 1.1 SAA-C03  7 | 페이지 
관련 기술: 
• 구성 요소 크기를 독립적으로 조정할 수 있도록 워크로드 디커플링 
• 크기 조정 작업을 수행하기 위한 지표 및 조건 식별 
• 비즈니스 요구 사항을 충족하는 적합한 컴퓨팅 옵션 및 기능 선택(예: EC2 인스턴스 
유형) 
• 비즈니스 요구 사항을 충족하는 적합한 리소스 유형 및 크기 선택(예: Lambda 
메모리 양) 
태스크 설명 3.3: 고성능 데이터베이스 솔루션을 결정합니다. 
관련 지식: 
• AWS 글로벌 인프라(예: 가용 영역, AWS 리전) 
• 캐싱 전략 및 서비스(예: Amazon ElastiCache) 
• 데이터 액세스 패턴(예: 읽기 집약적 패턴과 쓰기 집약적 패턴 비교) 
• 데이터베이스 용량 계획(예: 용량 단위, 인스턴스 유형, 프로비저닝된 IOPS) 
• 데이터베이스 연결 및 프록시 
• 데이터베이스 엔진과 적합한 사용 사례(예: 이기종 마이그레이션, 동종 마이그레이션) 
• 데이터베이스 복제(replication)(예: 읽기 전용 복제본) 
• 데이터베이스 유형 및 서비스(예: 서버리스, 관계형과 비관계형 비교, 인 메모리) 
관련 기술: 
• 비즈니스 요구 사항을 충족하도록 읽기 전용 복제본 구성 
• 데이터베이스 아키텍처 설계 
• 적합한 데이터베이스 엔진 결정(예: MySQL 과 PostgreSQL 비교) 
• 적합한 데이터베이스 유형 결정(예: Amazon Aurora, Amazon DynamoDB) 
• 비즈니스 요구 사항을 충족하도록 캐싱 통합 
태스크 설명 3.4: 고성능 및/또는 확장 가능한 네트워크 아키텍처를 결정합니다. 
관련 지식: 
• 엣지 네트워킹 서비스와 적합한 사용 사례(예: Amazon CloudFront, AWS Global 
Accelerator)  
• 네트워크 아키텍처 설계 방법(예: 서브넷 티어, 라우팅, IP 주소 지정) 
• 로드 밸런싱 개념(예: Application Load Balancer) 
• 네트워크 연결 옵션(예: AWS VPN, Direct Connect, AWS PrivateLink) 
  

 
버전 1.1 SAA-C03  8 | 페이지 
관련 기술: 
• 다양한 아키텍처에 대한 네트워크 토폴로지 생성(예: 글로벌, 하이브리드, 멀티 티어)  
• 향후 요구 사항을 수용하도록 크기 조정 가능한 네트워크 구성 결정 
• 비즈니스 요구 사항을 충족하는 적합한 리소스 배치 결정 
• 적합한 로드 밸런싱 전략 선택  
태스크 설명 3.5: 고성능 데이터 수집 및 변환 솔루션을 결정합니다. 
관련 지식: 
• 데이터 분석 및 시각화 서비스와 적합한 사용 사례(예: Amazon Athena, AWS Lake 
Formation, Amazon QuickSight) 
• 데이터 수집 패턴(예: 빈도) 
• 데이터 전송 서비스와 적합한 사용 사례(예: AWS DataSync, AWS Storage 
Gateway)  
• 데이터 변환 서비스와 적합한 사용 사례(예: AWS Glue)  
• 수집 액세스 포인트에 대한 보안 액세스 
• 비즈니스 요구 사항을 충족하는 데 필요한 크기 및 속도 
• 스트리밍 데이터 서비스와 적합한 사용 사례(예: Amazon Kinesis) 
관련 기술: 
• 데이터 레이크 구축 및 보호 
• 데이터 스트리밍 아키텍처 설계  
• 데이터 전송 솔루션 설계 
• 시각화 전략 구현 
• 데이터 처리에 적합한 컴퓨팅 옵션 선택(예: Amazon EMR) 
• 수집에 적합한 구성 선택 
• 데이터 형식 변환(예: .csv 에서.parquet 으로 변환) 
도메인 4: 비용에 최적화된 아키텍처 설계  
태스크 설명 4.1: 비용에 최적화된 스토리지 솔루션을 설계합니다. 
관련 지식: 
• 액세스 옵션(예: 요청자 지불 객체 스토리지가 포함된 S3 버킷) 
• AWS 비용 관리 서비스 기능(예: 비용 할당 태그, 다중 계정 결제) 
• AWS 비용 관리 도구와 적합한 사용 사례(예: AWS Cost Explorer, AWS Budgets, 
AWS Cost and Usage Report) 

 
버전 1.1 SAA-C03  9 | 페이지 
• AWS 스토리지 서비스와 적합한 사용 사례(예: Amazon FSx, Amazon EFS, 
Amazon S3, Amazon EBS) 
• 백업 전략 
• 블록 스토리지 옵션(예: 하드 디스크 드라이브[HDD] 볼륨 유형, 솔리드 스테이트 
드라이브[SSD] 볼륨 유형) 
• 데이터 수명 주기 
• 하이브리드 스토리지 옵션(예: DataSync, Transfer Family, Storage Gateway) 
• 스토리지 액세스 패턴 
• 스토리지 계층화(예: 객체 스토리지의 콜드 계층화) 
• 연관된 특성이 있는 스토리지 유형(예: 객체, 파일, 블록) 
관련 기술: 
• 적합한 스토리지 전략 설계(예: Amazon S3 에 배치 업로드와 개별 업로드 비교) 
• 워크로드에 올바른 스토리지 크기 결정 
• 워크로드에 대한 데이터를 AWS 스토리지로 전송하는 가장 저렴한 방법 결정 
• 스토리지 자동 크기조정이 필요한 시점 결정  
• S3 객체 수명 주기 관리 
• 적합한 백업 및/또는 아카이브 솔루션 선택 
• 스토리지 서비스로의 데이터 마이그레이션에 적합한 서비스 선택 
• 적합한 스토리지 티어 선택  
• 스토리지에 올바른 데이터 수명 주기 선택 
• 워크로드에 가장 비용 효율적인 스토리지 서비스 선택 
태스크 설명 4.2: 비용에 최적화된 컴퓨팅 솔루션을 설계합니다. 
관련 지식: 
• AWS 비용 관리 서비스 기능(예: 비용 할당 태그, 다중 계정 결제) 
• AWS 비용 관리 도구와 적합한 사용 사례(예: Cost Explorer, AWS Budgets, AWS 
Cost and Usage Report) 
• AWS 글로벌 인프라(예: 가용 영역, AWS 리전) 
• AWS 구매 옵션(예: 스팟 인스턴스, 예약형 인스턴스, Savings Plans) 
• 분산 컴퓨팅 전략(예: 엣지 프로세싱) 
• 하이브리드 컴퓨팅 옵션(예: AWS Outposts, AWS Snowball Edge) 
• 인스턴스 유형, 패밀리 및 크기(예: 메모리 최적화, 컴퓨팅 최적화, 가상화) 
• 컴퓨팅 사용률 최적화(예: 컨테이너, 서버리스 컴퓨팅, 마이크로서비스) 
• 크기 조정 전략(예: 자동 크기 조정, 최대 절전 모드) 

 
버전 1.1 SAA-C03  10 | 페이지 
관련 기술: 
• 적합한 로드 밸런싱 전략 결정(예: Application Load Balancer[Layer 7]와 
Network Load Balancer[Layer 4]와 Gateway Load Balancer 비교) 
• 탄력적인 워크로드에 적합한 크기 조정 방법 및 전략 결정(예: 수평과 수직 비교, EC2 
최대 절전 모드) 
• 적합한 사용 사례로 비용 효율적인 AWS 컴퓨팅 서비스 결정(예: Lambda, Amazon 
EC2, Fargate) 
• 다양한 워크로드 클래스에 필요한 가용성 결정(예: 프로덕션 워크로드, 비프로덕션 
워크로드) 
• 워크로드에 적합한 인스턴스 패밀리 선택 
• 워크로드에 적합한 인스턴스 크기 선택 
태스크 설명 4.3: 비용에 최적화된 데이터베이스 솔루션을 설계합니다. 
관련 지식: 
• AWS 비용 관리 서비스 기능(예: 비용 할당 태그, 다중 계정 결제) 
• AWS 비용 관리 도구와 적합한 사용 사례(예: Cost Explorer, AWS Budgets, AWS 
Cost and Usage Report) 
• 캐싱 전략 
• 데이터 보존 정책 
• 데이터베이스 용량 계획(예: 용량 단위) 
• 데이터베이스 연결 및 프록시 
• 데이터베이스 엔진과 적합한 사용 사례(예: 이기종 마이그레이션, 동종 마이그레이션) 
• 데이터베이스 복제(replication)(예: 읽기 전용 복제본) 
• 데이터베이스 유형 및 서비스(예: 관계형과 비관계형 비교, Aurora, DynamoDB) 
관련 기술: 
• 적합한 백업 및 보존 정책 설계(예: 스냅샷 빈도) 
• 적합한 데이터베이스 엔진 결정(예: MySQL 과 PostgreSQL 비교) 
• 적합한 사용 사례로 비용 효율적인 AWS 데이터베이스 서비스 결정(예: 
DynamoDB 와 Amazon RDS 비교, 서버리스) 
• 비용 효율적인 AWS 데이터베이스 유형 결정(예: 시계열 형식, 열 형식) 
• 데이터베이스 스키마와 데이터를 다른 위치 및/또는 다른 데이터베이스 엔진으로 
마이그레이션 

 
버전 1.1 SAA-C03  11 | 페이지 
태스크 설명 4.4: 비용에 최적화된 네트워크 아키텍처를 설계합니다. 
관련 지식: 
• AWS 비용 관리 서비스 기능(예: 비용 할당 태그, 다중 계정 결제) 
• AWS 비용 관리 도구와 적합한 사용 사례(예: Cost Explorer, AWS Budgets, AWS 
Cost and Usage Report) 
• 로드 밸런싱 개념(예: Application Load Balancer) 
• NAT 게이트웨이(예: NAT 인스턴스 비용과 NAT 게이트웨이 비용 비교) 
• 네트워크 연결(예: 프라이빗 회선, 전용 회선, VPN) 
• 네트워크 라우팅, 토폴로지 및 피어링(예: AWS Transit Gateway, VPC 피어링) 
• 네트워크 서비스와 적합한 사용 사례(예: DNS) 
관련 기술: 
• 네트워크에 적합한 NAT 게이트웨이 유형 구성(예: 단일 공유 NAT 게이트웨이와 각 
가용 영역의 NAT 게이트웨이 비교) 
• 적합한 네트워크 연결 구성(예: Direct Connect 와 VPN 과 인터넷 비교) 
• 네트워크 전송 비용을 최소화하는 데 적합한 네트워크 경로 구성(예: 리전 간, 가용 
영역 간, 프라이빗과 퍼블릭 간, Global Accelerator, VPC 엔드포인트) 
• 콘텐츠 전송 네트워크(CDN) 및 엣지 캐싱에 대한 전략적 요구 사항 결정 
• 네트워크 최적화를 위한 기존 워크로드 검토  
• 적합한 제한 전략 선택  
• 네트워크 디바이스에 적합한 대역폭 할당 선택(예: 단일 VPN 과 복수 VPN 비교, 
Direct Connect 속도) 
  

 
버전 1.1 SAA-C03  12 | 페이지 
부록 
시험에 출제될 수 있는 기술 및 개념 
다음 목록에는 시험에 출제될 수 있는 기술 및 개념이 포함되어 있습니다. 이 목록에 모든 사항이 
포함된 것은 아니며 변경될 수 있습니다. 이 목록에 나와 있는 다음 항목의 배치와 순서가 
시험에서의 상대적 가중치 또는 중요도를 의미하지는 않습니다.  
• 컴퓨팅 
• 비용 관리 
• 데이터베이스 
• 재해 복구 
• 고성능 
• AWS 의 관리 및 거버넌스 
• 마이크로서비스 및 구성 요소 전송 
• 마이그레이션 및 데이터 전송 
• 네트워킹, 연결 및 콘텐츠 전송 
• 복원력 
• 보안 
• 서버리스 및 이벤트 기반 설계 원칙 
• 스토리지 
시험 범위에 포함되는 AWS 서비스 및 기능 
다음 목록에는 시험 범위에 해당하는 AWS 서비스 및 기능이 나와 있습니다. 이 목록에 모든 
사항이 포함된 것은 아니며 변경될 수 있습니다. AWS 제품 및 서비스는 주요 기능에 따라 
다음과 같은 카테고리로 분류됩니다. 
분석: 
• Amazon Athena 
• AWS Data Exchange 
• AWS Data Pipeline 
• Amazon EMR 
• AWS Glue 
• Amazon Kinesis 
• AWS Lake Formation 
• Amazon Managed Streaming for Apache Kafka(Amazon MSK) 

 
버전 1.1 SAA-C03  13 | 페이지 
• Amazon OpenSearch Service 
• Amazon QuickSight 
• Amazon Redshift 
애플리케이션 통합: 
• Amazon AppFlow 
• AWS AppSync 
• Amazon EventBridge 
• Amazon MQ 
• Amazon Simple Notification Service(Amazon SNS) 
• Amazon Simple Queue Service(Amazon SQS) 
• AWS Step Functions 
AWS 비용 관리: 
• AWS Budgets 
• AWS Cost and Usage Report 
• AWS Cost Explorer 
• Savings Plans 
컴퓨팅: 
• AWS Batch 
• Amazon EC2 
• Amazon EC2 Auto Scaling 
• AWS Elastic Beanstalk 
• AWS Outposts 
• AWS Serverless Application Repository 
• VMware Cloud on AWS 
• AWS Wavelength 
컨테이너: 
• Amazon ECS Anywhere 
• Amazon EKS Anywhere 
• Amazon EKS Distro 
• Amazon Elastic Container Registry(Amazon ECR) 
• Amazon Elastic Container Service(Amazon ECS) 

 
버전 1.1 SAA-C03  14 | 페이지 
• Amazon Elastic Kubernetes Service(Amazon EKS) 
데이터베이스: 
• Amazon Aurora 
• Amazon Aurora Serverless 
• Amazon DocumentDB(MongoDB 호환) 
• Amazon DynamoDB 
• Amazon ElastiCache 
• Amazon Keyspaces(for Apache Cassandra) 
• Amazon Neptune  
• Amazon Quantum Ledger Database(Amazon QLDB) 
• Amazon RDS 
• Amazon Redshift 
개발자 도구: 
• AWS X-Ray 
프런트 엔드 웹 및 모바일: 
• AWS Amplify 
• Amazon API Gateway 
• AWS Device Farm 
• Amazon Pinpoint 
Machine Learning: 
• Amazon Comprehend 
• Amazon Forecast 
• Amazon Fraud Detector 
• Amazon Kendra 
• Amazon Lex 
• Amazon Polly 
• Amazon Rekognition 
• Amazon SageMaker 
• Amazon Textract 
• Amazon Transcribe 
• Amazon Translate 

 
버전 1.1 SAA-C03  15 | 페이지 
AWS 의 관리 및 거버넌스: 
• AWS Auto Scaling 
• AWS CloudFormation 
• AWS CloudTrail 
• Amazon CloudWatch 
• AWS Command Line Interface(AWS CLI) 
• AWS Compute Optimizer 
• AWS Config 
• AWS Control Tower 
• AWS Health Dashboard 
• AWS License Manager 
• Amazon Managed Grafana 
• Amazon Managed Service for Prometheus 
• AWS Management Console 
• AWS Organizations 
• AWS Proton 
• AWS Service Catalog 
• AWS Systems Manager 
• AWS Trusted Advisor 
• AWS Well-Architected Tool 
미디어 서비스: 
• Amazon Elastic Transcoder 
• Amazon Kinesis Video Streams 
마이그레이션 및 전송: 
• AWS Application Discovery Service 
• AWS Application Migration Service 
• AWS Database Migration Service(AWS DMS) 
• AWS DataSync 
• AWS Migration Hub 
• AWS Snow Family 
• AWS Transfer Family 

 
버전 1.1 SAA-C03  16 | 페이지 
네트워킹 및 콘텐츠 전송: 
• AWS Client VPN 
• Amazon CloudFront 
• AWS Direct Connect 
• Elastic Load Balancing(ELB) 
• AWS Global Accelerator 
• AWS PrivateLink 
• Amazon Route 53 
• AWS Site-to-Site VPN 
• AWS Transit Gateway 
• Amazon VPC 
보안, 자격 증명 및 규정 준수: 
• AWS Artifact 
• AWS Audit Manager 
• AWS Certificate Manager(ACM) 
• AWS CloudHSM 
• Amazon Cognito 
• Amazon Detective 
• AWS Directory Service 
• AWS Firewall Manager 
• Amazon GuardDuty 
• AWS IAM Identity Center(AWS Single Sign-On) 
• AWS Identity and Access Management(IAM) 
• Amazon Inspector 
• AWS Key Management Service(AWS KMS) 
• Amazon Macie 
• AWS Network Firewall 
• AWS Resource Access Manager(AWS RAM) 
• AWS Secrets Manager 
• AWS Security Hub 
• AWS Shield 
• AWS WAF 

 
버전 1.1 SAA-C03  17 | 페이지 
서버리스: 
• AWS AppSync 
• AWS Fargate 
• AWS Lambda 
스토리지: 
• AWS Backup 
• Amazon Elastic Block Store(Amazon EBS) 
• Amazon Elastic File System(Amazon EFS) 
• Amazon FSx(모든 유형) 
• Amazon S3 
• Amazon S3 Glacier 
• AWS Storage Gateway 
시험 범위가 아닌 AWS 서비스 및 기능 
다음 목록에는 시험 범위가 아닌 AWS 서비스 및 기능이 나와 있습니다. 이 목록에 모든 사항이 
포함된 것은 아니며 변경될 수 있습니다. 시험의 대상 작업 역할과 전혀 관련이 없는 AWS 제품 
및 서비스는 다음 목록에서 제외됩니다. 
분석: 
• Amazon CloudSearch 
애플리케이션 통합: 
• Amazon Managed Workflows for Apache Airflow(Amazon MWAA) 
AR 및 VR: 
• Amazon Sumerian 
Blockchain: 
• Amazon Managed Blockchain 
컴퓨팅: 
• Amazon Lightsail 

 
버전 1.1 SAA-C03  18 | 페이지 
데이터베이스: 
• Amazon RDS on VMware 
개발자 도구: 
• AWS Cloud9 
• AWS Cloud Development Kit(AWS CDK) 
• AWS CloudShell 
• AWS CodeArtifact 
• AWS CodeBuild 
• AWS CodeCommit 
• AWS CodeDeploy 
• Amazon CodeGuru 
• AWS CodeStar 
• Amazon Corretto 
• AWS Fault Injection Simulator(AWS FIS) 
• AWS 도구 및 SDK 
프런트 엔드 웹 및 모바일: 
• Amazon Location Service 
게임 기술: 
• Amazon GameLift 
• Amazon Lumberyard 
사물 인터넷(IoT): 
• 모든 서비스 
Machine Learning: 
• Apache MXNet on AWS 
• Amazon Augmented AI(Amazon A2I) 
• AWS DeepComposer 
• AWS Deep Learning AMIs(DLAMI) 
• AWS Deep Learning Containers 
• AWS DeepLens 

 
버전 1.1 SAA-C03  19 | 페이지 
• AWS DeepRacer 
• Amazon DevOps Guru 
• Amazon Elastic Inference 
• Amazon HealthLake 
• AWS Inferentia 
• Amazon Lookout for Equipment 
• Amazon Lookout for Metrics 
• Amazon Lookout for Vision 
• Amazon Monitron 
• AWS Panorama 
• Amazon Personalize 
• PyTorch on AWS 
• Amazon SageMaker Data Wrangler 
• Amazon SageMaker Ground Truth 
• TensorFlow on AWS 
AWS 의 관리 및 거버넌스: 
• AWS Chatbot 
• AWS Console 모바일 애플리케이션 
• AWS Distro for OpenTelemetry 
• AWS OpsWorks 
미디어 서비스: 
• AWS Elemental Appliances and Software 
• AWS Elemental MediaConnect 
• AWS Elemental MediaConvert 
• AWS Elemental MediaLive 
• AWS Elemental MediaPackage 
• AWS Elemental MediaStore 
• AWS Elemental MediaTailor 
• Amazon Interactive Video Service(Amazon IVS) 
마이그레이션 및 전송: 
• 마이그레이션 평가기 

 
버전 1.1 SAA-C03  20 | 페이지 
네트워킹 및 콘텐츠 전송: 
• AWS App Mesh 
• AWS Cloud Map 
퀀텀 테크놀로지: 
• Amazon Braket 
로보틱스: 
• AWS RoboMaker 
인공위성: 
• AWS Ground Station 
설문 조사 
이 시험 안내서가 도움이 되었나요? 설문 조사에 참여하여 의견을 공유해 주시기 바랍니다. 
 