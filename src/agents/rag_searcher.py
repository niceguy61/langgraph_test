"""RAG Searcher Agent - Searches existing documents and curriculum"""
from typing import Any, Dict, List, Optional

from .base import BaseAgent
from src.rag import RAGRetriever, VectorStoreManager, CurriculumStore


class RAGSearcherAgent(BaseAgent):
    """Agent responsible for searching existing documents and curriculum via RAG"""

    def __init__(self, vectorstore_manager: VectorStoreManager = None):
        super().__init__(
            name="rag_searcher",
            description="RAG 검색 에이전트 - 커리큘럼 및 기존 문서에서 관련 정보 검색",
            temperature=0.3
        )
        self.vectorstore_manager = vectorstore_manager or VectorStoreManager()
        self.retriever = RAGRetriever(self.vectorstore_manager)
        self.curriculum_store = CurriculumStore()

    @property
    def system_prompt(self) -> str:
        return """당신은 AWS 학습 자료 검색 전문가입니다.

당신의 역할:
1. 기존 학습 자료에서 관련 정보를 찾습니다
2. 검색된 문서의 관련성을 평가합니다
3. 핵심 정보를 추출하여 제공합니다

검색 원칙:
- 정확한 정보 우선
- 컨텍스트 고려
- 중복 제거
- 관련성 순위화"""

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute RAG search based on current context"""

        curriculum = state.get("curriculum", {})
        target_week = state.get("target_week")
        search_query = state.get("search_query", "")

        # Generate search queries
        queries = self._generate_queries(curriculum, target_week, search_query)

        # Perform RAG search
        all_contexts = []
        for query in queries:
            context = self.retriever.retrieve_with_context(query, k=3)
            if context and "관련 문서를 찾을 수 없습니다" not in context:
                all_contexts.append(context)

        # Combine and summarize
        combined_context = await self._synthesize_context(all_contexts, curriculum)

        return {
            "rag_context": combined_context,
            "rag_queries": queries,
            "completed_tasks": state.get("completed_tasks", []) + ["rag_search"],
            "current_step": "rag_searched"
        }

    def _generate_queries(
        self,
        curriculum: Dict,
        target_week: int = None,
        base_query: str = ""
    ) -> List[str]:
        """Generate search queries based on context"""

        queries = []

        if base_query:
            queries.append(base_query)

        if target_week:
            # Find week data
            week_data = None
            weeks = curriculum.get("weeks", [])
            for w in weeks:
                if w.get("week") == target_week:
                    week_data = w
                    break

            if not week_data and curriculum.get("week") == target_week:
                week_data = curriculum

            if week_data:
                # Add queries based on week topics
                title = week_data.get("title", "")
                if title:
                    queries.append(title)

                services = week_data.get("services", [])
                for service in services:
                    queries.append(f"AWS {service}")

                # Add queries from days
                for day in week_data.get("days", []):
                    topics = day.get("topics", [])
                    for topic in topics[:2]:
                        queries.append(topic)

        if not queries:
            queries = ["AWS 기초", "클라우드 컴퓨팅"]

        return queries[:5]  # Limit queries

    async def _synthesize_context(
        self,
        contexts: List[str],
        curriculum: Dict
    ) -> str:
        """Synthesize multiple RAG contexts into a coherent summary"""

        if not contexts:
            return "기존 자료에서 관련 정보를 찾을 수 없습니다."

        combined = "\n\n---\n\n".join(contexts)

        # If combined context is short enough, return as is
        if len(combined) < 2000:
            return combined

        # Summarize using LLM
        template = self.get_prompt_template("""
다음 검색된 문서들을 분석하고 핵심 정보를 요약해주세요.

검색된 문서:
{contexts}

커리큘럼 컨텍스트:
{curriculum}

다음 형식으로 요약해주세요:

## 관련 기존 자료 요약
- 핵심 내용 1
- 핵심 내용 2

## 활용 가능한 정보
- 재사용 가능한 예제
- 참고할 설명

요약:""")

        summary = await self.invoke_with_template(
            template,
            contexts=combined[:3000],
            curriculum=str(curriculum)[:500]
        )

        return summary

    async def index_documents(self, directory: str = None) -> Dict[str, Any]:
        """Index documents into vector store"""

        from pathlib import Path
        from src.config import settings

        dir_path = Path(directory) if directory else settings.paths.data_dir

        result = self.vectorstore_manager.ingest_documents(dir_path)

        return {
            "status": result.get("status"),
            "documents_indexed": result.get("documents_loaded", 0),
            "chunks_created": result.get("chunks_created", 0)
        }

    async def get_week_context(self, week: int) -> str:
        """Get all relevant context for a specific week"""

        documents = self.retriever.get_week_documents(week)

        if not documents:
            return f"Week {week}에 대한 기존 자료가 없습니다."

        context_parts = []
        for doc in documents:
            context_parts.append(
                f"[{doc.metadata.get('filename', 'Unknown')}]\n{doc.page_content[:500]}"
            )

        return "\n\n---\n\n".join(context_parts)

    async def get_curriculum_day_info(self, week: int, day: int) -> Optional[Dict]:
        """커리큘럼에서 특정 일차 정보 조회"""
        return self.curriculum_store.get_day_info(week, day)

    async def get_day_services_from_curriculum(self, week: int, day: int) -> List[str]:
        """커리큘럼에서 특정 일차의 서비스 목록 조회"""
        return self.curriculum_store.get_day_services(week, day)

    async def search_curriculum_by_service(self, service: str) -> List[Dict]:
        """서비스명으로 커리큘럼 검색"""
        return self.curriculum_store.search_by_service(service)

    async def validate_content(self, week: int, day: int, content_files: Dict[str, str]) -> Dict:
        """콘텐츠가 커리큘럼과 일치하는지 검증"""
        return self.curriculum_store.validate_content_against_curriculum(week, day, content_files)

    async def index_curriculum(self, curriculum: Dict = None) -> Dict[str, Any]:
        """커리큘럼을 ChromaDB에 인덱싱"""
        return self.curriculum_store.index_curriculum(curriculum)

    async def get_curriculum_context_for_generation(self, week: int, day: int) -> str:
        """콘텐츠 생성을 위한 커리큘럼 컨텍스트 조회"""
        day_info = self.curriculum_store.get_day_info(week, day)

        if not day_info:
            return f"Week {week} Day {day}에 대한 커리큘럼 정보가 없습니다."

        metadata = day_info.get('metadata', {})
        content = day_info.get('content', '')

        context = f"""
## 커리큘럼 정보 (Week {week} Day {day})

**제목:** {metadata.get('day_title', 'N/A')}
**주차 주제:** {metadata.get('week_title', 'N/A')}

### 핵심 서비스
{metadata.get('core_services', 'N/A')}

### 다루는 토픽
{metadata.get('topics', 'N/A')}

### 핵심 개념
{metadata.get('key_concepts', 'N/A')}

---
{content}
"""
        return context
