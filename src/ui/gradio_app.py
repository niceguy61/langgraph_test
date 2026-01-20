"""Gradio UI for AWS Lecture Generator"""
import gradio as gr
import json
import asyncio
from typing import Dict, Any, Optional, Generator
from pathlib import Path

# nest_asyncio removed due to compatibility issues with newer uvicorn

from src.config import settings
from src.graph import run_workflow, stream_workflow, create_initial_state
from src.graph.workflow import compile_workflow
from src.agents import (
    CurriculumDesignerAgent,
    ContentGeneratorAgent,
    RAGSearcherAgent,
    ReviewerAgent
)
from src.rag import VectorStoreManager, CurriculumStore
from src.mcp import FileSystemMCPServer


# Initialize components
curriculum_agent = CurriculumDesignerAgent()
content_agent = ContentGeneratorAgent()
rag_agent = RAGSearcherAgent()
reviewer_agent = ReviewerAgent()
fs_server = FileSystemMCPServer()
vectorstore = VectorStoreManager()
curriculum_store = CurriculumStore()

# Curriculum file path
CURRICULUM_FILE = settings.paths.output_dir / "curriculum.json"


def load_existing_curriculum() -> tuple:
    """Load existing curriculum from file if exists"""
    try:
        if CURRICULUM_FILE.exists():
            with open(CURRICULUM_FILE, 'r', encoding='utf-8') as f:
                curriculum = json.load(f)
            curriculum_json = json.dumps(curriculum, ensure_ascii=False, indent=2)
            return curriculum_json, "기존 커리큘럼을 불러왔습니다.", curriculum
        return "", "저장된 커리큘럼이 없습니다.", {}
    except Exception as e:
        return "", f"커리큘럼 로드 오류: {e}", {}


async def generate_curriculum(weeks: int) -> tuple:
    """Generate curriculum for specified weeks"""
    try:
        state = {
            "request": f"{weeks}주 AWS 학습 커리큘럼 생성",
            "target_week": None if weeks == 4 else weeks
        }

        result = await curriculum_agent.execute(state)
        curriculum = result.get("curriculum", {})

        # Save curriculum
        await fs_server.save_curriculum(curriculum)

        # Index curriculum to ChromaDB
        try:
            index_result = curriculum_store.index_curriculum(curriculum)
            index_status = f"ChromaDB 인덱싱 완료: {index_result.get('indexed_days', 0)}개 일차"
        except Exception as idx_error:
            index_status = f"ChromaDB 인덱싱 실패: {idx_error}"

        # Format for display
        curriculum_json = json.dumps(curriculum, ensure_ascii=False, indent=2)

        return (
            curriculum_json,
            f"커리큘럼이 생성되었습니다! {index_status}",
            curriculum
        )

    except Exception as e:
        return (
            json.dumps({"error": str(e)}, ensure_ascii=False),
            f"오류 발생: {e}",
            {}
        )


async def index_curriculum_to_chromadb() -> str:
    """Index existing curriculum to ChromaDB"""
    try:
        if not CURRICULUM_FILE.exists():
            return "커리큘럼 파일이 존재하지 않습니다. 먼저 커리큘럼을 생성하세요."

        result = curriculum_store.index_curriculum()
        return f"""
커리큘럼 ChromaDB 인덱싱 완료!

- 인덱싱된 일차: {result.get('indexed_days', 0)}개
- 컬렉션 크기: {result.get('collection_count', 0)}
- 상태: {result.get('status', 'unknown')}
"""
    except Exception as e:
        return f"인덱싱 오류: {e}"


async def verify_content_against_curriculum(week: int = None) -> str:
    """Verify generated content against curriculum"""
    try:
        report = await reviewer_agent.full_verification_report(week)
        stats = report.get('statistics', {})
        results = report.get('results', [])

        output = f"""
## 📊 커리큘럼 대비 콘텐츠 검증 결과

### 통계
| 항목 | 값 |
|------|---|
| 총 일수 | {stats.get('total', 0)} |
| ✅ 완료 | {stats.get('complete', 0)} |
| ⚠️ 부분 완료 | {stats.get('partial', 0)} |
| ❌ 미완료 | {stats.get('incomplete', 0)} |
| 🚫 누락 | {stats.get('missing', 0)} |
| 완료율 | {stats.get('completion_rate', 0):.1f}% |

### 상세 결과
"""
        for r in results:
            status_icon = {
                'COMPLETE': '✅',
                'PARTIAL': '⚠️',
                'INCOMPLETE': '❌',
                'MISSING': '🚫'
            }.get(r.get('status'), '❓')

            week_num = r.get('week', '?')
            day_num = r.get('day', '?')
            day_title = r.get('day_title', '')
            message = r.get('message', '')

            output += f"\n**{status_icon} Week {week_num} Day {day_num}**: {day_title}\n"
            output += f"- 상태: {r.get('status')}\n"

            if r.get('expected_services'):
                output += f"- 예상 서비스: {', '.join(r.get('expected_services', []))}\n"
            if r.get('found_services'):
                output += f"- 발견된 서비스: {', '.join(r.get('found_services', []))}\n"
            if r.get('missing_services'):
                output += f"- ⚠️ 누락된 서비스: {', '.join(r.get('missing_services', []))}\n"
            output += f"- 메시지: {message}\n"

        return output

    except Exception as e:
        return f"검증 오류: {e}"


async def search_curriculum(query: str) -> str:
    """Search curriculum in ChromaDB"""
    try:
        results = curriculum_store.search_by_service(query, n_results=5)

        if not results:
            return "검색 결과가 없습니다."

        output = f"## '{query}' 검색 결과\n\n"
        for r in results:
            meta = r.get('metadata', {})
            output += f"### Week {meta.get('week')} Day {meta.get('day')}: {meta.get('day_title')}\n"
            output += f"- 주차 주제: {meta.get('week_title')}\n"
            output += f"- 핵심 서비스: {meta.get('core_services')}\n"
            output += f"- 토픽: {meta.get('topics')}\n\n"

        return output

    except Exception as e:
        return f"검색 오류: {e}"


async def generate_day_content(
    week: int,
    day: int
) -> tuple:
    """Generate content for a specific day"""
    try:
        # Load curriculum from file automatically
        if not CURRICULUM_FILE.exists():
            return (
                "커리큘럼 파일이 없습니다. 먼저 '커리큘럼 생성' 탭에서 커리큘럼을 생성하세요.",
                json.dumps({"error": "curriculum not found"}, ensure_ascii=False),
                ""
            )

        with open(CURRICULUM_FILE, "r", encoding="utf-8") as f:
            curriculum = json.load(f)

        # Create week structure
        await fs_server.create_week_structure(week)

        # Get week and day data
        week_data = None
        day_data = None
        for w in curriculum.get("weeks", []):
            if w.get("week") == week:
                week_data = w
                for d in w.get("days", []):
                    if d.get("day") == day:
                        day_data = d
                        break
                break

        if not day_data:
            return (
                f"Week {week} Day {day} 데이터를 커리큘럼에서 찾을 수 없습니다.",
                json.dumps({"error": "day not found"}, ensure_ascii=False),
                ""
            )

        services = day_data.get("core_services", [])
        day_title = day_data.get("title", "")

        # Search for existing context
        rag_result = await rag_agent.execute({
            "curriculum": curriculum,
            "target_week": week,
            "target_day": day
        })
        rag_context = rag_result.get("rag_context", "")

        # Generate content
        state = {
            "curriculum": curriculum,
            "target_week": week,
            "target_day": day,
            "rag_context": rag_context,
            "web_context": ""
        }

        result = await content_agent.execute(state)
        content = result.get("generated_content", {})

        # Save content
        saved = await content_agent.save_content(content)
        generated_files = list(saved.values())

        # Get output summary
        summary = {
            "week": week,
            "day": day,
            "title": day_title,
            "services": services,
            "files_generated": len(generated_files)
        }

        return (
            f"Week {week} Day {day} ({day_title}) 콘텐츠가 생성되었습니다!\n서비스: {', '.join(services)}",
            json.dumps(summary, ensure_ascii=False, indent=2),
            "\n".join(generated_files)
        )

    except Exception as e:
        return (
            f"오류 발생: {e}",
            json.dumps({"error": str(e)}, ensure_ascii=False),
            ""
        )


async def generate_week_content(
    week: int,
    progress: gr.Progress = None
) -> tuple:
    """Generate content for a specific week - supports new per-service structure"""
    try:
        # Load curriculum from file automatically
        if not CURRICULUM_FILE.exists():
            return (
                "커리큘럼 파일이 없습니다. 먼저 '커리큘럼 생성' 탭에서 커리큘럼을 생성하세요.",
                json.dumps({"error": "curriculum not found"}, ensure_ascii=False),
                ""
            )

        with open(CURRICULUM_FILE, "r", encoding="utf-8") as f:
            curriculum = json.load(f)

        # Create week structure
        await fs_server.create_week_structure(week)

        # Search for existing context
        if progress:
            progress(0.1, desc="기존 자료 검색 중...")

        rag_result = await rag_agent.execute({
            "curriculum": curriculum,
            "target_week": week
        })
        rag_context = rag_result.get("rag_context", "")

        # Get week data for README generation
        week_data = None
        for w in curriculum.get("weeks", []):
            if w.get("week") == week:
                week_data = w
                break

        # Generate content for each day
        generated_files = []
        days = 5

        for day in range(1, days + 1):
            # Get day data and services
            day_data = None
            if week_data:
                for d in week_data.get("days", []):
                    if d.get("day") == day:
                        day_data = d
                        break

            services = day_data.get("core_services", []) if day_data else []
            services_str = ", ".join(services[:2])

            if progress:
                progress(0.1 + (day / days) * 0.8, desc=f"Day {day} ({services_str}...) 생성 중...")

            state = {
                "curriculum": curriculum,
                "target_week": week,
                "target_day": day,
                "rag_context": rag_context,
                "web_context": ""
            }

            result = await content_agent.execute(state)
            content = result.get("generated_content", {})

            # Save content
            saved = await content_agent.save_content(content)
            generated_files.extend(saved.values())

        # Generate and save Week README
        if week_data:
            week_readme = content_agent._generate_week_readme(week, week_data, days)
            week_readme_path = settings.paths.output_dir / f"week{week}" / "README.md"
            week_readme_path.parent.mkdir(parents=True, exist_ok=True)
            week_readme_path.write_text(week_readme, encoding="utf-8")
            generated_files.append(str(week_readme_path))

        if progress:
            progress(1.0, desc="완료!")

        # Get output summary
        summary = await fs_server.get_output_summary()

        return (
            f"Week {week} 콘텐츠가 생성되었습니다! (서비스별 파일 생성)",
            json.dumps(summary, ensure_ascii=False, indent=2),
            "\n".join(generated_files)
        )

    except Exception as e:
        return (
            f"오류 발생: {e}",
            json.dumps({"error": str(e)}, ensure_ascii=False),
            ""
        )


def run_full_pipeline_sync() -> Generator:
    """Run the full lecture generation pipeline (sync generator for Gradio)"""
    try:
        yield "## 🚀 전체 파이프라인 시작\n\n4주 AWS 학습 강의자료를 생성합니다..."

        results = []
        total_weeks = 4
        days_per_week = 5

        # Step 1: Generate curriculum
        yield "## 📋 Step 1: 커리큘럼 생성 중...\n\n4주 커리큘럼을 설계하고 있습니다..."

        try:
            curriculum_result = asyncio.run(curriculum_agent.execute({
                "request": "4주 AWS 학습 커리큘럼 생성",
                "target_week": None
            }))
            curriculum = curriculum_result.get("curriculum", {})

            # Save curriculum
            asyncio.run(fs_server.save_curriculum(curriculum))

            # Generate and save main README
            course_readme = content_agent._generate_course_readme(curriculum)
            readme_path = settings.paths.output_dir / "README.md"
            readme_path.write_text(course_readme, encoding="utf-8")

            results.append("### ✅ 커리큘럼 생성 완료\n커리큘럼이 성공적으로 생성되었습니다.")
            yield "\n\n".join(results) + f"\n\n```json\n{json.dumps(curriculum, ensure_ascii=False, indent=2)[:1500]}...\n```"

        except Exception as e:
            yield f"## ❌ 커리큘럼 생성 실패\n\n오류: {e}"
            return

        # Step 2: Generate content for each week
        for week in range(1, total_weeks + 1):
            yield "\n\n".join(results) + f"\n\n## 📚 Step 2.{week}: Week {week} 콘텐츠 생성 중..."

            try:
                # Create week directory structure
                asyncio.run(fs_server.create_week_structure(week))

                # Get RAG context for the week
                rag_result = asyncio.run(rag_agent.execute({
                    "curriculum": curriculum,
                    "target_week": week
                }))
                rag_context = rag_result.get("rag_context", "")

                # Get week data for README generation
                week_data = None
                for w in curriculum.get("weeks", []):
                    if w.get("week") == week:
                        week_data = w
                        break

                # Generate content for each day of the week
                for day in range(1, days_per_week + 1):
                    # Get services for this day
                    day_data = None
                    if week_data:
                        for d in week_data.get("days", []):
                            if d.get("day") == day:
                                day_data = d
                                break

                    services = day_data.get("core_services", []) if day_data else []
                    services_str = ", ".join(services[:3])
                    if len(services) > 3:
                        services_str += f" 외 {len(services)-3}개"

                    yield "\n\n".join(results) + f"\n\n## 📚 Week {week}, Day {day} 콘텐츠 생성 중...\n\n서비스: {services_str}\n\n서비스별 강의자료, 실습 가이드, 퀴즈를 작성하고 있습니다..."

                    state = {
                        "curriculum": curriculum,
                        "target_week": week,
                        "target_day": day,
                        "rag_context": rag_context,
                        "web_context": ""
                    }

                    content_result = asyncio.run(content_agent.execute(state))
                    content = content_result.get("generated_content", {})

                    # Save content
                    saved = asyncio.run(content_agent.save_content(content))

                    # Count generated service files
                    service_count = len([k for k in saved.keys() if not k.endswith(('_readme', '_practice', '_quiz'))])

                    results.append(f"### ✅ Week {week} Day {day} 완료\n- 서비스 파일: {service_count}개\n- 총 생성 파일: {len(saved)}개")
                    yield "\n\n".join(results[-10:])

                # Generate and save Week README
                if week_data:
                    week_readme = content_agent._generate_week_readme(week, week_data, days_per_week)
                    week_readme_path = settings.paths.output_dir / f"week{week}" / "README.md"
                    week_readme_path.parent.mkdir(parents=True, exist_ok=True)
                    week_readme_path.write_text(week_readme, encoding="utf-8")

                results.append(f"### 🎉 Week {week} 전체 완료!")
                yield "\n\n".join(results[-10:])

            except Exception as e:
                results.append(f"### ⚠️ Week {week} 오류: {e}")
                yield "\n\n".join(results[-10:])
                continue

        # Final summary
        yield "\n\n".join(results[-10:]) + "\n\n## 📊 최종 결과 집계 중..."

        try:
            summary = asyncio.run(fs_server.get_output_summary())
            final_result = f"""

---

## ✅ 전체 파이프라인 완료!

### 생성된 콘텐츠 요약
```json
{json.dumps(summary, ensure_ascii=False, indent=2)}
```

### 출력 구조
```
output/
├── README.md                    # 전체 과정 목차
├── curriculum.json              # 커리큘럼 데이터
├── week1/
│   ├── README.md               # Week 1 목차
│   ├── day1/
│   │   ├── README.md           # Day 1 서비스 인덱스
│   │   ├── IAM.md              # 서비스별 강의
│   │   ├── EC2.md              # 서비스별 강의
│   │   ├── practice.md         # 실습 가이드
│   │   └── quiz.md             # 복습 퀴즈
│   └── ...
├── week2/
│   └── ...
└── ...
```

### 각 서비스 파일 구성
- 📌 핵심 목적 (What & Why)
- 🎯 주요 사용 시나리오 (When to Use)
- 🔗 연관 서비스 (Used Together With)
- 💰 비용 구조 (Pricing)
- 📚 핵심 개념
- 🖥️ AWS 콘솔 가이드
- ⌨️ AWS CLI 가이드
- 🎯 SAA-C03 시험 포인트
"""
        except Exception as summary_error:
            final_result = f"""

---

## ✅ 전체 파이프라인 완료!

파이프라인 실행이 완료되었습니다.
(요약 로드 오류: {summary_error})

### 출력 위치
- 전체 목차: `output/README.md`
- 커리큘럼: `output/curriculum.json`
- Week 1-4 강의자료: `output/week1/` ~ `output/week4/`
"""

        yield "\n\n".join(results[-5:]) + final_result

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        yield f"## ❌ 오류 발생\n\n**오류 메시지:** {e}\n\n**상세 내용:**\n```\n{error_details}\n```"


async def index_documents(directory: str) -> str:
    """Index documents into vector store"""
    try:
        dir_path = Path(directory) if directory else settings.paths.data_dir

        result = vectorstore.ingest_documents(dir_path)

        return f"""
문서 인덱싱 완료!

- 로드된 문서: {result.get('documents_loaded', 0)}개
- 생성된 청크: {result.get('chunks_created', 0)}개
- 상태: {result.get('status', 'unknown')}
"""
    except Exception as e:
        return f"인덱싱 오류: {e}"


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file"""
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        return "\n\n".join(text_parts)
    except Exception as e:
        return f"PDF 추출 오류: {e}"


def upload_documents(files) -> str:
    """Upload and save documents to data directory"""
    if not files:
        return "파일을 선택해주세요."

    try:
        data_dir = settings.paths.data_dir
        data_dir.mkdir(parents=True, exist_ok=True)

        uploaded_files = []
        pdf_converted = []

        for file in files:
            file_path = Path(file) if isinstance(file, str) else Path(file.name if hasattr(file, 'name') else file)
            filename = file_path.name
            suffix = file_path.suffix.lower()

            source_path = file if isinstance(file, str) else (file.name if hasattr(file, 'name') else str(file))

            if suffix == '.pdf':
                # PDF -> Markdown 변환
                text_content = extract_text_from_pdf(source_path)
                if text_content.startswith("PDF 추출 오류"):
                    uploaded_files.append(f"{filename} (오류)")
                    continue

                # PDF를 마크다운으로 저장
                md_filename = file_path.stem + ".md"
                dest_path = data_dir / md_filename
                md_content = f"# {file_path.stem}\n\n{text_content}"
                dest_path.write_text(md_content, encoding='utf-8')
                uploaded_files.append(md_filename)
                pdf_converted.append(filename)

            elif suffix in ['.md', '.txt']:
                # 텍스트 파일 직접 복사
                dest_path = data_dir / filename
                with open(source_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                dest_path.write_text(content, encoding='utf-8')
                uploaded_files.append(filename)

            else:
                uploaded_files.append(f"{filename} (지원하지 않는 형식)")

        result = f"""
파일 업로드 완료!

업로드된 파일:
{chr(10).join(['- ' + f for f in uploaded_files])}
"""
        if pdf_converted:
            result += f"""
PDF 변환됨:
{chr(10).join(['- ' + f + ' -> ' + Path(f).stem + '.md' for f in pdf_converted])}
"""
        result += f"""
저장 위치: {data_dir}

이제 '문서 인덱싱' 버튼을 클릭하여 벡터 DB에 저장하세요.
"""
        return result

    except Exception as e:
        return f"업로드 오류: {e}"


def list_indexed_files() -> str:
    """List files in data directory"""
    try:
        data_dir = settings.paths.data_dir
        if not data_dir.exists():
            return "문서 디렉토리가 비어있습니다."

        files = list(data_dir.rglob("*.md"))
        if not files:
            return "마크다운 파일이 없습니다."

        file_list = []
        for f in files:
            rel_path = f.relative_to(data_dir)
            size = f.stat().st_size
            file_list.append(f"- {rel_path} ({size:,} bytes)")

        return f"총 {len(files)}개 파일:\n" + "\n".join(file_list)

    except Exception as e:
        return f"오류: {e}"


async def search_rag(query: str) -> str:
    """Search indexed documents"""
    try:
        from src.rag import RAGRetriever
        retriever = RAGRetriever(vectorstore)

        context = retriever.retrieve_with_context(query, k=5)
        return context

    except Exception as e:
        return f"검색 오류: {e}"


async def preview_content(week: int, day: int, content_type: str) -> str:
    """Preview generated content - supports new per-service structure"""
    try:
        file_path = f"week{week}/day{day}/{content_type}.md"
        result = await fs_server.read_file(file_path)

        if "error" in result:
            return f"파일을 찾을 수 없습니다: {file_path}"

        return result.get("content", "내용 없음")

    except Exception as e:
        return f"미리보기 오류: {e}"


async def list_day_services(week: int, day: int) -> list:
    """List available service files for a specific day"""
    try:
        day_dir = settings.paths.output_dir / f"week{week}" / f"day{day}"
        if not day_dir.exists():
            return ["README", "practice", "quiz"]

        files = list(day_dir.glob("*.md"))
        service_names = []
        for f in files:
            name = f.stem
            if name not in ["README", "practice", "quiz"]:
                service_names.append(name)

        # Add standard files at the beginning
        return ["README", "practice", "quiz"] + sorted(service_names)

    except Exception as e:
        return ["README", "practice", "quiz"]


def create_app() -> gr.Blocks:
    """Create the Gradio application"""

    with gr.Blocks(
        title="AWS 강의자료 생성기"
    ) as app:

        gr.Markdown("""
        # AWS 학습 강의자료 생성기

        LangGraph 기반 멀티 에이전트 시스템으로 AWS 학습 자료를 자동 생성합니다.
        """)

        with gr.Tabs():

            # Tab 1: Curriculum Generation
            with gr.Tab("커리큘럼 생성"):
                with gr.Row():
                    with gr.Column(scale=1):
                        weeks_slider = gr.Slider(
                            minimum=1,
                            maximum=4,
                            value=4,
                            step=1,
                            label="주차 수"
                        )
                        with gr.Row():
                            generate_curriculum_btn = gr.Button(
                                "커리큘럼 생성",
                                variant="primary"
                            )
                            load_curriculum_btn = gr.Button(
                                "저장된 커리큘럼 불러오기",
                                variant="secondary"
                            )

                    with gr.Column(scale=2):
                        curriculum_status = gr.Textbox(
                            label="상태",
                            interactive=False
                        )
                        curriculum_output = gr.Code(
                            label="커리큘럼 JSON",
                            language="json",
                            lines=20
                        )

                curriculum_state = gr.State({})

                generate_curriculum_btn.click(
                    fn=lambda w: asyncio.run(generate_curriculum(w)),
                    inputs=[weeks_slider],
                    outputs=[curriculum_output, curriculum_status, curriculum_state]
                )

                load_curriculum_btn.click(
                    fn=load_existing_curriculum,
                    outputs=[curriculum_output, curriculum_status, curriculum_state]
                )

            # Tab 2: Content Generation
            with gr.Tab("콘텐츠 생성"):
                gr.Markdown("""
                > **참고**: 저장된 커리큘럼(curriculum.json)을 자동으로 불러옵니다.
                > 커리큘럼이 없으면 먼저 위의 **커리큘럼 생성** 탭에서 생성하세요.
                """)
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("#### 일별 콘텐츠 생성 (권장)")
                        week_select = gr.Dropdown(
                            choices=[1, 2, 3, 4],
                            value=1,
                            label="주차 선택"
                        )
                        day_select = gr.Dropdown(
                            choices=[1, 2, 3, 4, 5],
                            value=1,
                            label="일차 선택"
                        )
                        with gr.Row():
                            generate_day_btn = gr.Button(
                                "일별 콘텐츠 생성",
                                variant="primary"
                            )
                            generate_week_btn = gr.Button(
                                "주차 전체 생성",
                                variant="secondary"
                            )

                    with gr.Column(scale=2):
                        content_status = gr.Textbox(
                            label="상태",
                            interactive=False
                        )
                        content_summary = gr.Code(
                            label="생성 요약",
                            language="json",
                            lines=10
                        )
                        generated_files = gr.Textbox(
                            label="생성된 파일",
                            lines=10
                        )

                generate_day_btn.click(
                    fn=lambda w, d: asyncio.run(generate_day_content(w, d)),
                    inputs=[week_select, day_select],
                    outputs=[content_status, content_summary, generated_files]
                )

                generate_week_btn.click(
                    fn=lambda w: asyncio.run(generate_week_content(w)),
                    inputs=[week_select],
                    outputs=[content_status, content_summary, generated_files]
                )

            # Tab 3: Full Pipeline
            with gr.Tab("전체 파이프라인"):
                gr.Markdown("""
                전체 4주 강의자료를 한 번에 생성합니다.
                """)

                run_pipeline_btn = gr.Button(
                    "전체 파이프라인 실행",
                    variant="primary",
                    size="lg"
                )
                pipeline_output = gr.Markdown(
                    label="실행 로그"
                )

                run_pipeline_btn.click(
                    fn=run_full_pipeline_sync,
                    outputs=[pipeline_output]
                )

            # Tab 4: RAG Management
            with gr.Tab("RAG 관리"):
                gr.Markdown("""
                ### RAG (Retrieval-Augmented Generation) 문서 관리

                PDF, 마크다운(.md), 텍스트(.txt) 파일을 업로드하여 강의 생성 시 참조 자료로 활용할 수 있습니다.
                PDF 파일은 자동으로 텍스트를 추출하여 마크다운으로 변환됩니다.
                """)

                with gr.Row():
                    with gr.Column():
                        gr.Markdown("#### 1. 문서 업로드")
                        file_upload = gr.File(
                            label="문서 파일 업로드 (PDF, MD, TXT)",
                            file_count="multiple",
                            file_types=[".md", ".txt", ".pdf"],
                            type="filepath"
                        )
                        upload_btn = gr.Button("파일 업로드", variant="secondary")
                        upload_result = gr.Textbox(
                            label="업로드 결과",
                            lines=6,
                            interactive=False
                        )

                        gr.Markdown("#### 2. 문서 인덱싱")
                        doc_dir = gr.Textbox(
                            label="문서 디렉토리 (비워두면 기본 경로)",
                            placeholder="기본: ./data/documents",
                            value=""
                        )
                        with gr.Row():
                            index_btn = gr.Button("문서 인덱싱", variant="primary")
                            list_btn = gr.Button("파일 목록")
                        index_result = gr.Textbox(
                            label="인덱싱 결과",
                            lines=8,
                            interactive=False
                        )

                    with gr.Column():
                        gr.Markdown("#### 3. RAG 검색 테스트")
                        search_query = gr.Textbox(
                            label="검색어",
                            placeholder="예: AWS EC2 인스턴스 생성 방법"
                        )
                        search_btn = gr.Button("검색", variant="primary")
                        search_result = gr.Markdown(
                            label="검색 결과"
                        )

                upload_btn.click(
                    fn=upload_documents,
                    inputs=[file_upload],
                    outputs=[upload_result]
                )

                index_btn.click(
                    fn=lambda d: asyncio.run(index_documents(d)),
                    inputs=[doc_dir],
                    outputs=[index_result]
                )

                list_btn.click(
                    fn=list_indexed_files,
                    outputs=[index_result]
                )

                search_btn.click(
                    fn=lambda q: asyncio.run(search_rag(q)),
                    inputs=[search_query],
                    outputs=[search_result]
                )

            # Tab 5: Curriculum Verification
            with gr.Tab("커리큘럼 검증"):
                gr.Markdown("""
                ### 커리큘럼 기반 콘텐츠 검증

                생성된 콘텐츠가 커리큘럼에 정의된 서비스들을 올바르게 다루고 있는지 검증합니다.
                """)

                with gr.Row():
                    with gr.Column():
                        gr.Markdown("#### 1. 커리큘럼 ChromaDB 인덱싱")
                        index_curriculum_btn = gr.Button(
                            "커리큘럼 인덱싱",
                            variant="primary"
                        )
                        index_curriculum_result = gr.Textbox(
                            label="인덱싱 결과",
                            lines=6,
                            interactive=False
                        )

                        gr.Markdown("#### 2. 커리큘럼 검색")
                        curriculum_search_query = gr.Textbox(
                            label="서비스명 또는 토픽 검색",
                            placeholder="예: EC2, Lambda, VPC..."
                        )
                        curriculum_search_btn = gr.Button("검색", variant="secondary")

                    with gr.Column():
                        gr.Markdown("#### 3. 콘텐츠 검증")
                        verify_week_select = gr.Dropdown(
                            choices=["전체", 1, 2, 3, 4],
                            value="전체",
                            label="검증할 주차"
                        )
                        verify_btn = gr.Button(
                            "커리큘럼 대비 콘텐츠 검증",
                            variant="primary"
                        )

                curriculum_search_result = gr.Markdown(label="검색 결과")
                verify_result = gr.Markdown(label="검증 결과")

                index_curriculum_btn.click(
                    fn=lambda: asyncio.run(index_curriculum_to_chromadb()),
                    outputs=[index_curriculum_result]
                )

                curriculum_search_btn.click(
                    fn=lambda q: asyncio.run(search_curriculum(q)),
                    inputs=[curriculum_search_query],
                    outputs=[curriculum_search_result]
                )

                verify_btn.click(
                    fn=lambda w: asyncio.run(verify_content_against_curriculum(
                        None if w == "전체" else int(w)
                    )),
                    inputs=[verify_week_select],
                    outputs=[verify_result]
                )

            # Tab 6: Content Preview
            with gr.Tab("콘텐츠 미리보기"):
                gr.Markdown("""
                ### 생성된 콘텐츠 미리보기

                서비스별 강의자료, README, 실습 가이드, 퀴즈를 미리볼 수 있습니다.
                """)

                with gr.Row():
                    preview_week = gr.Dropdown(
                        choices=[1, 2, 3, 4],
                        value=1,
                        label="주차"
                    )
                    preview_day = gr.Dropdown(
                        choices=[1, 2, 3, 4, 5],
                        value=1,
                        label="일차"
                    )
                    preview_type = gr.Textbox(
                        label="파일명 (서비스명 또는 README/practice/quiz)",
                        value="README",
                        placeholder="예: README, practice, quiz, IAM, EC2..."
                    )
                    preview_btn = gr.Button("미리보기", variant="primary")

                with gr.Row():
                    refresh_files_btn = gr.Button("파일 목록 새로고침", variant="secondary")
                    available_files = gr.Textbox(
                        label="사용 가능한 파일",
                        interactive=False,
                        placeholder="파일 목록을 새로고침하세요"
                    )

                preview_content_output = gr.Markdown(
                    label="콘텐츠"
                )

                preview_btn.click(
                    fn=lambda w, d, t: asyncio.run(preview_content(w, d, t)),
                    inputs=[preview_week, preview_day, preview_type],
                    outputs=[preview_content_output]
                )

                refresh_files_btn.click(
                    fn=lambda w, d: ", ".join(asyncio.run(list_day_services(w, d))),
                    inputs=[preview_week, preview_day],
                    outputs=[available_files]
                )

            # Tab 7: Settings
            with gr.Tab("설정"):
                gr.Markdown("""
                ### 현재 설정

                - **LLM**: Ollama (qwen2.5)
                - **Vector DB**: ChromaDB
                - **출력 경로**: ./output
                """)

                with gr.Row():
                    with gr.Column():
                        ollama_host = gr.Textbox(
                            label="Ollama Host",
                            value=settings.ollama.host
                        )
                        ollama_model = gr.Textbox(
                            label="Ollama Model",
                            value=settings.ollama.model
                        )

                    with gr.Column():
                        chroma_host = gr.Textbox(
                            label="ChromaDB Host",
                            value=settings.chroma.host
                        )
                        output_dir = gr.Textbox(
                            label="출력 디렉토리",
                            value=str(settings.paths.output_dir)
                        )

        return app


def launch_app():
    """Launch the Gradio application"""
    app = create_app()
    app.launch(
        server_name=settings.gradio.server_name,
        server_port=settings.gradio.server_port,
        share=settings.gradio.share,
        theme=gr.themes.Soft()
    )


if __name__ == "__main__":
    launch_app()
