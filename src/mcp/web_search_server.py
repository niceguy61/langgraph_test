"""Web Search MCP Server for searching AWS-related information"""
import os
from typing import Any, Dict, List, Optional
import httpx
from bs4 import BeautifulSoup
import asyncio


class WebSearchMCPServer:
    """MCP Server for web search operations"""

    def __init__(self, tavily_api_key: Optional[str] = None):
        self.tavily_api_key = tavily_api_key or os.getenv("TAVILY_API_KEY")
        self.search_history: List[Dict] = []

    # MCP Tool: search_web
    async def search_web(
        self,
        query: str,
        num_results: int = 5,
        search_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Search the web for information

        Args:
            query: Search query
            num_results: Number of results to return
            search_type: Type of search (general, aws_docs, tutorial)

        Returns:
            Search results
        """
        # Modify query based on search type
        if search_type == "aws_docs":
            query = f"site:docs.aws.amazon.com {query}"
        elif search_type == "tutorial":
            query = f"{query} tutorial guide"

        # Try Tavily API first if available
        if self.tavily_api_key:
            results = await self._search_tavily(query, num_results)
            if results.get("results"):
                return results

        # Fallback to DuckDuckGo
        return await self._search_duckduckgo(query, num_results)

    async def _search_tavily(self, query: str, num_results: int) -> Dict[str, Any]:
        """Search using Tavily API"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.tavily_api_key,
                        "query": query,
                        "max_results": num_results,
                        "include_answer": True
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "query": query,
                        "answer": data.get("answer", ""),
                        "results": [
                            {
                                "title": r.get("title", ""),
                                "url": r.get("url", ""),
                                "content": r.get("content", "")[:500]
                            }
                            for r in data.get("results", [])
                        ],
                        "source": "tavily"
                    }

        except Exception as e:
            print(f"Tavily search error: {e}")

        return {"results": [], "error": "Tavily search failed"}

    async def _search_duckduckgo(self, query: str, num_results: int) -> Dict[str, Any]:
        """Search using DuckDuckGo HTML"""
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
                        url_elem = result.select_one('.result__url')

                        if title_elem:
                            results.append({
                                "title": title_elem.get_text(strip=True),
                                "url": url_elem.get_text(strip=True) if url_elem else "",
                                "content": snippet_elem.get_text(strip=True) if snippet_elem else ""
                            })

                    return {
                        "query": query,
                        "results": results,
                        "source": "duckduckgo"
                    }

        except Exception as e:
            print(f"DuckDuckGo search error: {e}")

        return {"query": query, "results": [], "error": "Search failed"}

    # MCP Tool: search_aws_documentation
    async def search_aws_documentation(
        self,
        service: str,
        topic: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search AWS official documentation

        Args:
            service: AWS service name (e.g., EC2, S3, Lambda)
            topic: Specific topic within the service

        Returns:
            Documentation search results
        """
        query = f"AWS {service}"
        if topic:
            query += f" {topic}"

        return await self.search_web(query, num_results=5, search_type="aws_docs")

    # MCP Tool: fetch_page_content
    async def fetch_page_content(self, url: str) -> Dict[str, Any]:
        """
        Fetch and extract content from a web page

        Args:
            url: URL to fetch

        Returns:
            Extracted page content
        """
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }
                )

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Remove script and style elements
                    for script in soup(["script", "style", "nav", "header", "footer"]):
                        script.decompose()

                    # Get text content
                    text = soup.get_text(separator='\n', strip=True)

                    # Clean up whitespace
                    lines = [line.strip() for line in text.splitlines() if line.strip()]
                    content = '\n'.join(lines)

                    # Get title
                    title = soup.title.string if soup.title else ""

                    return {
                        "url": url,
                        "title": title,
                        "content": content[:5000],  # Limit content length
                        "content_length": len(content),
                        "status": "success"
                    }

                return {
                    "url": url,
                    "error": f"HTTP {response.status_code}",
                    "status": "failed"
                }

        except Exception as e:
            return {
                "url": url,
                "error": str(e),
                "status": "failed"
            }

    # MCP Tool: search_aws_tutorials
    async def search_aws_tutorials(
        self,
        service: str,
        level: str = "beginner"
    ) -> Dict[str, Any]:
        """
        Search for AWS tutorials

        Args:
            service: AWS service name
            level: Skill level (beginner, intermediate, advanced)

        Returns:
            Tutorial search results
        """
        query = f"AWS {service} {level} tutorial step by step"
        return await self.search_web(query, num_results=5, search_type="tutorial")

    # MCP Tool: search_aws_pricing
    async def search_aws_pricing(self, service: str) -> Dict[str, Any]:
        """
        Search for AWS pricing information

        Args:
            service: AWS service name

        Returns:
            Pricing information results
        """
        query = f"site:aws.amazon.com {service} pricing"
        return await self.search_web(query, num_results=3)

    # MCP Tool: search_aws_best_practices
    async def search_aws_best_practices(
        self,
        service: str,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for AWS best practices

        Args:
            service: AWS service name
            category: Specific category (security, performance, cost, etc.)

        Returns:
            Best practices search results
        """
        query = f"AWS {service} best practices"
        if category:
            query += f" {category}"

        return await self.search_web(query, num_results=5, search_type="aws_docs")

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get MCP tool definitions for this server"""
        return [
            {
                "name": "search_web",
                "description": "Search the web for information",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "num_results": {"type": "integer", "description": "Number of results"},
                        "search_type": {
                            "type": "string",
                            "enum": ["general", "aws_docs", "tutorial"],
                            "description": "Type of search"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "search_aws_documentation",
                "description": "Search AWS official documentation",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service": {"type": "string", "description": "AWS service name"},
                        "topic": {"type": "string", "description": "Specific topic"}
                    },
                    "required": ["service"]
                }
            },
            {
                "name": "fetch_page_content",
                "description": "Fetch and extract content from a web page",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "URL to fetch"}
                    },
                    "required": ["url"]
                }
            },
            {
                "name": "search_aws_tutorials",
                "description": "Search for AWS tutorials",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service": {"type": "string", "description": "AWS service name"},
                        "level": {
                            "type": "string",
                            "enum": ["beginner", "intermediate", "advanced"],
                            "description": "Skill level"
                        }
                    },
                    "required": ["service"]
                }
            },
            {
                "name": "search_aws_best_practices",
                "description": "Search for AWS best practices",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service": {"type": "string", "description": "AWS service name"},
                        "category": {
                            "type": "string",
                            "enum": ["security", "performance", "cost", "reliability"],
                            "description": "Category"
                        }
                    },
                    "required": ["service"]
                }
            }
        ]
