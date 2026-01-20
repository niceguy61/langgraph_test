"""Supervisor Agent - Orchestrates the multi-agent workflow"""
from typing import Any, Dict, Literal
from langchain_core.prompts import ChatPromptTemplate

from .base import BaseAgent


class SupervisorAgent(BaseAgent):
    """Supervisor agent that routes tasks to appropriate agents"""

    AGENT_OPTIONS = [
        "curriculum_designer",
        "content_generator",
        "web_searcher",
        "rag_searcher",
        "reviewer",
        "FINISH"
    ]

    def __init__(self):
        super().__init__(
            name="supervisor",
            description="총괄 에이전트 - 커리큘럼 기반 워크플로우 조율 및 에이전트 라우팅",
            temperature=0.3  # Lower temperature for more consistent routing
        )

    @property
    def system_prompt(self) -> str:
        return """당신은 AWS 학습 강의자료 생성 시스템의 총괄 관리자입니다.

당신의 역할:
1. 사용자 요청을 분석하고 적절한 에이전트에게 작업을 할당합니다
2. 각 에이전트의 작업 결과를 검토하고 다음 단계를 결정합니다
3. 커리큘럼을 기준으로 콘텐츠가 올바르게 생성되었는지 확인합니다
4. 전체 워크플로우가 완료되면 FINISH를 반환합니다

사용 가능한 에이전트:
- curriculum_designer: 커리큘럼 구조 설계 (주차별/일별 학습 계획) - ChromaDB에 커리큘럼 인덱싱
- content_generator: 커리큘럼 기반 강의 콘텐츠 마크다운 생성
- web_searcher: 최신 AWS 정보 웹 검색
- rag_searcher: ChromaDB에서 커리큘럼 정보 및 기존 문서 검색
- reviewer: 생성된 콘텐츠가 커리큘럼과 일치하는지 검증

작업 순서 가이드:
1. 새 강의 생성 요청 → curriculum_designer (커리큘럼 생성 및 ChromaDB 인덱싱)
2. 커리큘럼 완성 후 → rag_searcher (커리큘럼에서 해당 일차 정보 조회)
3. 추가 정보 필요시 → web_searcher
4. 콘텐츠 생성 준비 완료 → content_generator (커리큘럼의 core_services 기반)
5. 콘텐츠 생성 완료 → reviewer (커리큘럼 대비 검증)
6. 검증 통과 또는 수정 완료 → FINISH

중요: 콘텐츠는 반드시 커리큘럼의 core_services에 정의된 서비스들을 다뤄야 합니다.

반드시 다음 에이전트 이름 중 하나만 정확히 반환하세요:
{agent_options}"""

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the next agent to call based on current state"""

        template = self.get_prompt_template("""
현재 상태:
- 요청: {request}
- 현재 단계: {current_step}
- 완료된 작업: {completed_tasks}
- 마지막 결과: {last_result}

다음에 호출할 에이전트를 결정하세요.
반드시 다음 중 하나만 반환: {agent_options}

선택한 에이전트:""")

        response = await self.invoke_with_template(
            template,
            request=state.get("request", ""),
            current_step=state.get("current_step", "시작"),
            completed_tasks=", ".join(state.get("completed_tasks", [])),
            last_result=str(state.get("last_result", "없음"))[:500],
            agent_options=", ".join(self.AGENT_OPTIONS)
        )

        # Parse the response to get agent name
        next_agent = self._parse_agent_response(response)

        return {
            "next_agent": next_agent,
            "supervisor_reasoning": response
        }

    def _parse_agent_response(self, response: str) -> str:
        """Parse the LLM response to extract agent name"""
        response = response.strip().lower()

        for agent in self.AGENT_OPTIONS:
            if agent.lower() in response:
                return agent

        # Default to FINISH if no valid agent found
        return "FINISH"

    def get_routing_decision(
        self,
        state: Dict[str, Any]
    ) -> Literal["curriculum_designer", "content_generator", "web_searcher", "rag_searcher", "reviewer", "FINISH"]:
        """Synchronous routing decision for LangGraph edges"""
        next_agent = state.get("next_agent", "FINISH")

        if next_agent in self.AGENT_OPTIONS:
            return next_agent

        return "FINISH"
