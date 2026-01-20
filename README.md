# AWS 학습 강의자료 생성기

LangGraph 기반 멀티 에이전트 시스템으로 AWS 학습 강의자료를 자동 생성합니다.

## 주요 기능

- **4주 커리큘럼 자동 생성**: AWS 기초부터 고급까지 체계적인 학습 계획
- **멀티 에이전트 시스템**: 6개의 전문 에이전트가 협력하여 콘텐츠 생성
- **RAG 지원**: 기존 문서를 참조하여 일관된 콘텐츠 생성
- **웹 검색 통합**: 최신 AWS 정보 자동 수집
- **MCP 서버**: 파일시스템, 웹검색, AWS API 연동
- **Gradio UI**: 직관적인 웹 인터페이스

## 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                         Gradio UI                                │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph Orchestrator                        │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    Supervisor Agent                          │ │
│  └─────────────────────────────────────────────────────────────┘ │
│         │           │           │           │           │        │
│         ▼           ▼           ▼           ▼           ▼        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐│
│  │Curriculum│ │ Content  │ │   Web    │ │   RAG    │ │  Review  ││
│  │ Designer │ │Generator │ │ Searcher │ │ Searcher │ │  Agent   ││
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘│
└─────────────────────────────────────────────────────────────────┘
         │                         │                    │
         ▼                         ▼                    ▼
┌─────────────┐           ┌─────────────┐       ┌─────────────┐
│   Ollama    │           │  ChromaDB   │       │ MCP Servers │
│  (qwen3:8b) │           │ (Vector DB) │       │             │
└─────────────┘           └─────────────┘       └─────────────┘
```

## 에이전트 구성

| 에이전트 | 역할 |
|---------|------|
| Supervisor | 워크플로우 조율 및 에이전트 라우팅 |
| Curriculum Designer | 주차별/일별 학습 계획 설계 |
| Content Generator | 마크다운 형식 강의자료 생성 |
| Web Searcher | 최신 AWS 정보 웹 검색 |
| RAG Searcher | 기존 문서에서 관련 정보 검색 |
| Reviewer | 생성된 콘텐츠 품질 검토 |

## 4주 커리큘럼

| 주차 | 주제 | 핵심 서비스 |
|------|------|-------------|
| Week 1 | AWS 기초 & 컴퓨팅 | IAM, EC2, VPC |
| Week 2 | 스토리지 & 데이터베이스 | S3, RDS, DynamoDB |
| Week 3 | 서버리스 & 컨테이너 | Lambda, API Gateway, ECS/EKS |
| Week 4 | 모니터링 & 아키텍처 | CloudWatch, CloudFormation, Well-Architected |

## 빠른 시작

### Docker로 실행 (권장)

```bash
# 1. 저장소 클론
git clone <repository-url>
cd aws-lecture-generator

# 2. 환경 변수 설정
cp .env.example .env

# 3. Docker Compose로 실행
docker-compose up --build

# 4. 브라우저에서 접속
# http://localhost:7860
```

### 로컬 실행

```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. Ollama 실행 (별도 터미널)
ollama serve

# 4. 모델 다운로드
ollama pull qwen2.5
ollama pull nomic-embed-text

# 5. ChromaDB 실행 (별도 터미널)
docker run -p 8000:8000 chromadb/chroma

# 6. 애플리케이션 실행
python -m src.main
```

## 사용 방법

### Gradio UI 사용

1. **커리큘럼 생성 탭**: 주차 수를 선택하고 커리큘럼 생성
2. **콘텐츠 생성 탭**: 특정 주차의 강의자료 생성
3. **전체 파이프라인 탭**: 4주 전체 강의자료 한 번에 생성
4. **RAG 관리 탭**: 문서 인덱싱 및 검색 테스트
5. **콘텐츠 미리보기 탭**: 생성된 콘텐츠 확인

### CLI 사용

```bash
# Gradio UI 실행 (기본)
python -m src.main

# 특정 주차 강의자료 생성
python -m src.main --generate --week 1

# 전체 강의자료 생성
python -m src.main --generate

# 문서 인덱싱
python -m src.main --index

# 문서 인덱싱 (특정 디렉토리)
python -m src.main --index --docs-dir ./my_docs
```

## 출력 구조

```
output/
├── curriculum.json              # 전체 커리큘럼 메타데이터
├── week1/
│   ├── overview.md             # 주간 개요
│   ├── day1/
│   │   ├── lecture.md          # 강의 내용
│   │   ├── practice.md         # 실습 가이드
│   │   └── quiz.md             # 퀴즈/복습 문제
│   ├── day2/
│   │   └── ...
│   └── ...
├── week2/
│   └── ...
├── week3/
│   └── ...
└── week4/
    └── ...
```

## 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| OLLAMA_HOST | Ollama 서버 주소 | http://localhost:11434 |
| OLLAMA_MODEL | 사용할 LLM 모델 | qwen2.5 |
| CHROMA_HOST | ChromaDB 서버 주소 | http://localhost:8000 |
| OUTPUT_DIR | 출력 디렉토리 | ./output |
| DATA_DIR | RAG 문서 디렉토리 | ./data/documents |

## 프로젝트 구조

```
aws-lecture-generator/
├── docker-compose.yml          # Docker Compose 설정
├── Dockerfile                  # 앱 Docker 이미지
├── requirements.txt            # Python 의존성
├── .env.example               # 환경 변수 예시
├── README.md                  # 이 파일
│
├── src/
│   ├── main.py                # 진입점
│   ├── config.py              # 설정 관리
│   │
│   ├── agents/                # 에이전트 구현
│   │   ├── base.py
│   │   ├── supervisor.py
│   │   ├── curriculum_designer.py
│   │   ├── content_generator.py
│   │   ├── web_searcher.py
│   │   ├── rag_searcher.py
│   │   └── reviewer.py
│   │
│   ├── graph/                 # LangGraph 워크플로우
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── workflow.py
│   │
│   ├── rag/                   # RAG 시스템
│   │   ├── embeddings.py
│   │   ├── vectorstore.py
│   │   └── retriever.py
│   │
│   ├── mcp/                   # MCP 서버
│   │   ├── filesystem_server.py
│   │   ├── web_search_server.py
│   │   └── aws_server.py
│   │
│   ├── tools/                 # LangChain 도구
│   │   ├── web_search.py
│   │   └── file_writer.py
│   │
│   └── ui/                    # Gradio UI
│       └── gradio_app.py
│
├── data/
│   ├── documents/             # RAG용 문서
│   └── chroma_db/             # ChromaDB 저장소
│
├── output/                    # 생성된 강의자료
│
└── tests/                     # 테스트
    ├── test_agents.py
    └── test_workflow.py
```

## 테스트

```bash
# 전체 테스트 실행
pytest

# 특정 테스트 실행
pytest tests/test_agents.py -v

# 커버리지 리포트
pytest --cov=src --cov-report=html
```

## 기술 스택

- **LLM**: Ollama (qwen2.5)
- **오케스트레이션**: LangGraph
- **Vector DB**: ChromaDB
- **UI**: Gradio
- **컨테이너**: Docker + Docker Compose
- **언어**: Python 3.11+

## 라이선스

MIT License
