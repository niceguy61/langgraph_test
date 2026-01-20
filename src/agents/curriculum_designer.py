"""Curriculum Designer Agent - Designs the course structure"""
import json
from typing import Any, Dict, List, Optional

from .base import BaseAgent
from src.config import settings


class CurriculumDesignerAgent(BaseAgent):
    """Agent responsible for designing the curriculum structure"""

    def __init__(self):
        super().__init__(
            name="curriculum_designer",
            description="커리큘럼 설계 에이전트 - 주차별/일별 학습 계획 수립",
            temperature=0.5
        )

    @property
    def system_prompt(self) -> str:
        return """당신은 AWS 교육 커리큘럼 전문 설계자입니다.

당신의 역할:
1. 체계적인 AWS 학습 커리큘럼을 설계합니다
2. 주차별(Week), 일별(Day) 학습 구조를 정의합니다
3. 각 세션의 학습 목표와 핵심 내용을 명시합니다
4. 난이도를 점진적으로 조절합니다

커리큘럼 설계 원칙:
- 기초에서 심화로 점진적 진행
- 이론과 실습의 균형
- 실무 적용 가능한 예제 포함
- 각 주차별 명확한 학습 목표

출력 형식은 반드시 JSON으로 제공하세요."""

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Design the curriculum structure"""

        week_config = settings.curriculum.week_topics
        total_weeks = settings.curriculum.total_weeks
        days_per_week = settings.curriculum.days_per_week

        # Get specific week if requested, otherwise generate full curriculum
        target_week = state.get("target_week")

        if target_week:
            curriculum = await self._design_week(target_week, week_config)
        else:
            curriculum = await self._design_full_curriculum(week_config, total_weeks, days_per_week)

        return {
            "curriculum": curriculum,
            "completed_tasks": state.get("completed_tasks", []) + ["curriculum_design"],
            "current_step": "curriculum_designed"
        }

    async def _design_full_curriculum(
        self,
        week_config: Dict,
        total_weeks: int,
        days_per_week: int
    ) -> Dict[str, Any]:
        """Design the complete curriculum based on pre-defined SAA structure"""

        # 상세 일별 설정이 있으면 그대로 활용
        weeks = []
        for week_num in range(1, total_weeks + 1):
            week_info = week_config.get(week_num, {})
            days_config = week_info.get("days", {})

            days = []
            for day_num in range(1, days_per_week + 1):
                day_info = days_config.get(day_num, {})

                if day_info:
                    # 미리 정의된 일별 설정 사용
                    days.append({
                        "day": day_num,
                        "title": day_info.get("title", f"Day {day_num}"),
                        "core_services": day_info.get("services", []),
                        "topics": day_info.get("topics", []),
                        "key_concepts": await self._generate_key_concepts(day_info.get("services", []), day_info.get("topics", [])),
                        "practice": await self._generate_practice_summary(day_info.get("services", [])),
                        "practice_goal": await self._generate_practice_goal(day_info.get("services", [])),
                        "duration_hours": 2
                    })
                else:
                    # 없으면 LLM으로 생성
                    days.append(await self._design_day_with_llm(week_num, day_num, week_info))

            weeks.append({
                "week": week_num,
                "title": week_info.get("title", f"Week {week_num}"),
                "description": week_info.get("description", ""),
                "learning_objectives": await self._generate_week_objectives(week_info),
                "core_services": week_info.get("services", []),
                "days": days
            })

        return {
            "title": "AWS Solutions Architect Associate (SAA-C03) 학습 과정",
            "total_weeks": total_weeks,
            "days_per_week": days_per_week,
            "total_services": len(settings.curriculum.saa_services),
            "weeks": weeks
        }

    async def _generate_key_concepts(self, services: list, topics: list) -> list:
        """Generate key concepts for services"""
        if not services:
            return []

        template = self.get_prompt_template("""
다음 AWS 서비스와 주제에 대해 SAA 시험에서 꼭 알아야 할 핵심 개념 3-5개를 나열하세요.

서비스: {services}
주제: {topics}

JSON 배열로만 응답하세요 (설명 없이):
["개념1", "개념2", "개념3"]

핵심 개념:""")

        response = await self.invoke_with_template(
            template,
            services=", ".join(services),
            topics=", ".join(topics) if topics else "일반"
        )

        try:
            # JSON 배열 추출
            start = response.find('[')
            end = response.rfind(']') + 1
            if start != -1 and end > start:
                return json.loads(response[start:end])
        except:
            pass

        return [f"{services[0]} 기본 개념" if services else "AWS 기본 개념"]

    async def _generate_practice_summary(self, services: list) -> str:
        """Generate practice summary"""
        if not services:
            return "AWS 콘솔 실습"

        return f"{', '.join(services[:2])} 서비스 콘솔 및 CLI 실습"

    async def _generate_practice_goal(self, services: list) -> str:
        """Generate practice goal"""
        if not services:
            return "AWS 서비스 기본 사용법 익히기"

        service = services[0]
        goals = {
            "IAM": "IAM 사용자와 역할을 생성하고 최소 권한 정책 적용",
            "EC2": "EC2 인스턴스를 생성하고 SSH로 접속하여 웹서버 구성",
            "VPC": "퍼블릭/프라이빗 서브넷이 있는 VPC 구성",
            "S3": "S3 버킷 생성 및 버킷 정책, 암호화 설정",
            "RDS": "Multi-AZ RDS 인스턴스 생성 및 읽기 전용 복제본 구성",
            "Lambda": "Lambda 함수 생성 및 API Gateway 연동",
            "ECS": "ECS 클러스터 생성 및 Fargate 태스크 배포",
            "CloudWatch": "CloudWatch 대시보드 및 경보 설정",
        }
        return goals.get(service, f"{service} 기본 구성 및 설정")

    async def _generate_week_objectives(self, week_info: dict) -> list:
        """Generate week learning objectives"""
        services = week_info.get("services", [])
        title = week_info.get("title", "")

        template = self.get_prompt_template("""
다음 AWS 학습 주차에 대한 학습 목표 3개를 작성하세요.

주차 제목: {title}
다루는 서비스: {services}

JSON 배열로만 응답하세요:
["목표1", "목표2", "목표3"]

학습 목표:""")

        response = await self.invoke_with_template(
            template,
            title=title,
            services=", ".join(services)
        )

        try:
            start = response.find('[')
            end = response.rfind(']') + 1
            if start != -1 and end > start:
                return json.loads(response[start:end])
        except:
            pass

        return [f"{title} 핵심 개념 이해", f"{services[0] if services else 'AWS'} 실습 완료", "모범 사례 적용"]

    async def _design_day_with_llm(self, week: int, day: int, week_info: dict) -> dict:
        """Design a day using LLM when no pre-defined config exists"""
        template = self.get_prompt_template("""
Week {week} Day {day}의 커리큘럼을 설계하세요.

주차 정보:
- 제목: {week_title}
- 서비스: {services}

JSON으로 응답:
{{
    "day": {day},
    "title": "일차 제목",
    "core_services": ["서비스1"],
    "topics": ["토픽1", "토픽2"],
    "key_concepts": ["개념1", "개념2"],
    "practice": "실습 설명",
    "practice_goal": "실습 목표",
    "duration_hours": 2
}}

Day {day} JSON:""")

        response = await self.invoke_with_template(
            template,
            week=week,
            day=day,
            week_title=week_info.get("title", f"Week {week}"),
            services=", ".join(week_info.get("services", []))
        )

        return self._parse_curriculum_json(response)

    async def _design_week(self, week: int, week_config: Dict) -> Dict[str, Any]:
        """Design a specific week's curriculum"""

        week_info = week_config.get(week, {})

        template = self.get_prompt_template("""
Week {week} 커리큘럼을 상세히 설계해주세요.

주제: {title}
핵심 서비스: {services}
설명: {description}

5일간의 학습 계획을 다음 JSON 형식으로 출력하세요:
{{
    "week": {week},
    "title": "{title}",
    "description": "{description}",
    "services": {services},
    "learning_objectives": ["목표1", "목표2", "목표3"],
    "days": [
        {{
            "day": 1,
            "title": "일차 제목",
            "topics": ["주제1", "주제2"],
            "key_concepts": ["개념1", "개념2"],
            "practice": "실습 내용 설명",
            "quiz_topics": ["퀴즈 주제1", "퀴즈 주제2"],
            "duration_hours": 2
        }}
    ],
    "weekly_project": "주간 프로젝트 설명"
}}

Week {week} 커리큘럼 JSON:""")

        response = await self.invoke_with_template(
            template,
            week=week,
            title=week_info.get("title", f"Week {week}"),
            services=week_info.get("services", []),
            description=week_info.get("description", "")
        )

        return self._parse_curriculum_json(response)

    def _parse_curriculum_json(self, response: str) -> Dict[str, Any]:
        """Parse curriculum JSON from LLM response"""
        try:
            # Try to find JSON in the response
            start = response.find('{')
            end = response.rfind('}') + 1

            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")

        # Return a default structure if parsing fails
        return {
            "error": "Failed to parse curriculum",
            "raw_response": response[:500]
        }
