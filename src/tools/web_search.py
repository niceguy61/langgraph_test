"""Web Search Tool for LangChain agents"""
from typing import Optional, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import httpx
from bs4 import BeautifulSoup


class WebSearchInput(BaseModel):
    """Input schema for web search"""
    query: str = Field(description="Search query")
    num_results: int = Field(default=5, description="Number of results to return")


class WebSearchTool(BaseTool):
    """Tool for searching the web"""

    name: str = "web_search"
    description: str = "Search the web for information. Use this when you need to find current information about AWS services, tutorials, or best practices."
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str, num_results: int = 5) -> str:
        """Synchronous search execution"""
        import asyncio
        return asyncio.run(self._arun(query, num_results))

    async def _arun(self, query: str, num_results: int = 5) -> str:
        """Async search execution using DuckDuckGo"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://html.duckduckgo.com/html/",
                    data={"q": query},
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }
                )

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    results = []

                    for result in soup.select('.result')[:num_results]:
                        title_elem = result.select_one('.result__title')
                        snippet_elem = result.select_one('.result__snippet')

                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                            results.append(f"- {title}: {snippet}")

                    if results:
                        return "\n".join(results)
                    return "No results found"

                return f"Search failed with status {response.status_code}"

        except Exception as e:
            return f"Search error: {e}"


class AWSDocsSearchTool(BaseTool):
    """Tool for searching AWS documentation specifically"""

    name: str = "aws_docs_search"
    description: str = "Search AWS official documentation. Use this when you need accurate AWS service information."
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str, num_results: int = 5) -> str:
        """Synchronous search"""
        import asyncio
        return asyncio.run(self._arun(query, num_results))

    async def _arun(self, query: str, num_results: int = 5) -> str:
        """Search AWS docs"""
        modified_query = f"site:docs.aws.amazon.com {query}"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://html.duckduckgo.com/html/",
                    data={"q": modified_query},
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }
                )

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    results = []

                    for result in soup.select('.result')[:num_results]:
                        title_elem = result.select_one('.result__title')
                        snippet_elem = result.select_one('.result__snippet')
                        url_elem = result.select_one('.result__url')

                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                            url = url_elem.get_text(strip=True) if url_elem else ""
                            results.append(f"[{title}]({url})\n{snippet}")

                    if results:
                        return "\n\n".join(results)
                    return "No AWS documentation found"

                return f"Search failed with status {response.status_code}"

        except Exception as e:
            return f"AWS docs search error: {e}"
