"""Web Searcher Agent - Searches for latest AWS information"""
from typing import Any, Dict, List, Optional
import httpx
from bs4 import BeautifulSoup
import asyncio

from .base import BaseAgent


class WebSearcherAgent(BaseAgent):
    """Agent responsible for web search and information gathering"""

    def __init__(self):
        super().__init__(
            name="web_searcher",
            description="웹 검색 에이전트 - 최신 AWS 정보 수집",
            temperature=0.3
        )
        self.search_results: List[Dict] = []

    @property
    def system_prompt(self) -> str:
        return """당신은 AWS 관련 정보를 웹에서 검색하고 요약하는 전문가입니다.

당신의 역할:
1. AWS 관련 최신 정보를 검색합니다
2. 검색 결과를 분석하고 관련성을 평가합니다
3. 핵심 정보를 요약하여 제공합니다

검색 원칙:
- AWS 공식 문서 우선
- 최신 정보 확인
- 신뢰할 수 있는 출처 선호
- 실무에 유용한 정보 위주"""

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute web search based on current context"""

        curriculum = state.get("curriculum", {})
        target_week = state.get("target_week")
        search_query = state.get("search_query", "")

        # Generate search queries based on context
        queries = await self._generate_search_queries(curriculum, target_week, search_query)

        # Perform searches
        all_results = []
        for query in queries[:3]:  # Limit to 3 queries
            results = await self._search(query)
            all_results.extend(results)

        # Summarize results
        summary = await self._summarize_results(all_results, curriculum)

        return {
            "web_context": summary,
            "web_search_results": all_results,
            "completed_tasks": state.get("completed_tasks", []) + ["web_search"],
            "current_step": "web_searched"
        }

    async def _generate_search_queries(
        self,
        curriculum: Dict,
        target_week: Optional[int],
        base_query: str
    ) -> List[str]:
        """Generate relevant search queries"""

        if base_query:
            return [base_query]

        queries = []

        # Extract topics from curriculum
        if target_week:
            week_data = None
            for w in curriculum.get("weeks", []):
                if w.get("week") == target_week:
                    week_data = w
                    break

            if week_data:
                services = week_data.get("services", [])
                for service in services[:3]:
                    queries.append(f"AWS {service} tutorial 2024")
                    queries.append(f"AWS {service} best practices")

        if not queries:
            queries = [
                "AWS getting started guide 2024",
                "AWS free tier services",
                "AWS certification learning path"
            ]

        return queries

    async def _search(self, query: str) -> List[Dict]:
        """Perform web search using DuckDuckGo HTML"""

        results = []

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Use DuckDuckGo HTML search
                url = "https://html.duckduckgo.com/html/"
                response = await client.post(
                    url,
                    data={"q": query},
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                )

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    for result in soup.select('.result')[:5]:
                        title_elem = result.select_one('.result__title')
                        snippet_elem = result.select_one('.result__snippet')
                        link_elem = result.select_one('.result__url')

                        if title_elem:
                            results.append({
                                "title": title_elem.get_text(strip=True),
                                "snippet": snippet_elem.get_text(strip=True) if snippet_elem else "",
                                "url": link_elem.get_text(strip=True) if link_elem else "",
                                "query": query
                            })

        except Exception as e:
            print(f"Search error: {e}")
            results.append({
                "title": "Search failed",
                "snippet": str(e),
                "url": "",
                "query": query
            })

        return results

    async def _summarize_results(
        self,
        results: List[Dict],
        curriculum: Dict
    ) -> str:
        """Summarize search results using LLM"""

        if not results:
            return "웹 검색 결과가 없습니다."

        results_text = "\n\n".join([
            f"제목: {r['title']}\n내용: {r['snippet']}\nURL: {r['url']}"
            for r in results[:10]
        ])

        template = self.get_prompt_template("""
다음 웹 검색 결과를 분석하고 AWS 학습에 유용한 정보를 요약해주세요.

검색 결과:
{results}

커리큘럼 컨텍스트:
{curriculum}

다음 형식으로 요약해주세요:

## 주요 발견 사항
- 발견 1
- 발견 2

## 학습에 활용할 정보
- 정보 1
- 정보 2

## 참고 링크
- [제목](URL)

요약:""")

        summary = await self.invoke_with_template(
            template,
            results=results_text,
            curriculum=str(curriculum)[:500]
        )

        return summary

    async def search_aws_docs(self, service: str) -> str:
        """Search AWS official documentation"""

        # AWS docs search endpoint
        query = f"site:docs.aws.amazon.com {service}"
        results = await self._search(query)

        if results:
            return "\n".join([
                f"- {r['title']}: {r['snippet'][:100]}..."
                for r in results[:5]
            ])

        return f"AWS {service} 공식 문서를 찾을 수 없습니다."
