"""Reviewer Agent - Reviews and validates generated content"""
from typing import Any, Dict, List
from pathlib import Path

from .base import BaseAgent
from src.rag import CurriculumStore
from src.config import settings


class ReviewerAgent(BaseAgent):
    """Agent responsible for reviewing and validating generated content against curriculum"""

    def __init__(self):
        super().__init__(
            name="reviewer",
            description="리뷰 에이전트 - 커리큘럼 기반 콘텐츠 품질 및 일치성 검토",
            temperature=0.3
        )
        self.curriculum_store = CurriculumStore()

    @property
    def system_prompt(self) -> str:
        return """당신은 AWS 교육 콘텐츠 품질 검토 전문가입니다.

당신의 역할:
1. 생성된 강의자료의 정확성을 검증합니다
2. 내용의 완성도와 일관성을 평가합니다
3. 개선 사항을 구체적으로 제안합니다
4. 최종 품질 점수를 부여합니다

검토 기준:
- 기술적 정확성 (AWS 서비스 설명이 정확한가)
- 학습 효과성 (이해하기 쉬운가)
- 구조적 완성도 (체계적으로 구성되었는가)
- 실용성 (실무에 적용 가능한가)
- 최신성 (최신 AWS 정보를 반영했는가)

평가 척도:
- 우수 (90-100): 수정 없이 사용 가능
- 양호 (70-89): 사소한 수정 필요
- 보통 (50-69): 부분적 수정 필요
- 미흡 (0-49): 대폭 수정 필요"""

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Review generated content"""

        generated_content = state.get("generated_content", {})
        curriculum = state.get("curriculum", {})

        reviews = {}
        overall_scores = []

        for key, content in generated_content.items():
            review = await self._review_content(key, content, curriculum)
            reviews[key] = review

            if "overall_score" in review:
                overall_scores.append(review["overall_score"])

        # Calculate average score
        avg_score = sum(overall_scores) / len(overall_scores) if overall_scores else 0

        # Determine if content needs revision
        needs_revision = avg_score < 70

        return {
            "reviews": reviews,
            "average_score": avg_score,
            "needs_revision": needs_revision,
            "completed_tasks": state.get("completed_tasks", []) + ["review"],
            "current_step": "reviewed"
        }

    async def _review_content(
        self,
        content_key: str,
        content: Any,
        curriculum: Dict
    ) -> Dict[str, Any]:
        """Review a single piece of content"""

        # Extract content text
        if isinstance(content, dict):
            content_text = "\n\n".join([
                f"### {k}\n{v[:500]}..." if len(str(v)) > 500 else f"### {k}\n{v}"
                for k, v in content.items()
            ])
        else:
            content_text = str(content)[:2000]

        template = self.get_prompt_template("""
다음 AWS 학습 콘텐츠를 검토하고 평가해주세요.

콘텐츠 키: {content_key}

콘텐츠:
{content}

커리큘럼 정보:
{curriculum}

다음 형식으로 평가해주세요 (JSON 형식):

{{
    "accuracy_score": 0-100,
    "clarity_score": 0-100,
    "completeness_score": 0-100,
    "practicality_score": 0-100,
    "overall_score": 0-100,
    "strengths": ["강점 1", "강점 2"],
    "improvements": ["개선사항 1", "개선사항 2"],
    "critical_issues": ["심각한 문제 (있는 경우)"],
    "recommendation": "통과/수정필요/재작성필요"
}}

검토 결과 JSON:""")

        response = await self.invoke_with_template(
            template,
            content_key=content_key,
            content=content_text,
            curriculum=str(curriculum)[:500]
        )

        return self._parse_review_json(response)

    def _parse_review_json(self, response: str) -> Dict[str, Any]:
        """Parse review JSON from LLM response"""
        import json

        try:
            start = response.find('{')
            end = response.rfind('}') + 1

            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")

        # Return default review if parsing fails
        return {
            "accuracy_score": 70,
            "clarity_score": 70,
            "completeness_score": 70,
            "practicality_score": 70,
            "overall_score": 70,
            "strengths": ["콘텐츠 생성됨"],
            "improvements": ["자동 파싱 실패로 수동 검토 필요"],
            "critical_issues": [],
            "recommendation": "수정필요",
            "raw_response": response[:500]
        }

    async def generate_improvement_suggestions(
        self,
        content: str,
        review: Dict[str, Any]
    ) -> str:
        """Generate detailed improvement suggestions"""

        template = self.get_prompt_template("""
다음 콘텐츠와 검토 결과를 바탕으로 구체적인 개선 방안을 제시해주세요.

콘텐츠:
{content}

검토 결과:
{review}

다음 형식으로 개선 방안을 제시해주세요:

## 우선순위 높은 개선 사항
1. 개선 사항 1
   - 현재 상태: ...
   - 개선 방안: ...
   - 예시: ...

2. 개선 사항 2
   ...

## 추가 권장 사항
- 권장 1
- 권장 2

개선 방안:""")

        suggestions = await self.invoke_with_template(
            template,
            content=content[:1500],
            review=str(review)
        )

        return suggestions

    async def validate_aws_accuracy(self, content: str) -> Dict[str, Any]:
        """Validate AWS-specific technical accuracy"""

        template = self.get_prompt_template("""
다음 AWS 관련 콘텐츠의 기술적 정확성을 검증해주세요.

콘텐츠:
{content}

다음 항목을 확인하고 JSON으로 결과를 반환하세요:

{{
    "service_names_correct": true/false,
    "pricing_info_current": true/false,
    "cli_commands_valid": true/false,
    "best_practices_aligned": true/false,
    "security_recommendations_valid": true/false,
    "issues_found": ["문제 1", "문제 2"],
    "corrections_needed": ["수정 1", "수정 2"]
}}

검증 결과 JSON:""")

        response = await self.invoke_with_template(
            template,
            content=content[:2000]
        )

        return self._parse_review_json(response)

    async def validate_against_curriculum(
        self,
        week: int,
        day: int,
        content_files: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """콘텐츠가 커리큘럼과 일치하는지 검증"""
        if content_files is None:
            # 파일 시스템에서 콘텐츠 로드
            content_files = await self._load_content_files(week, day)

        return self.curriculum_store.validate_content_against_curriculum(week, day, content_files)

    async def _load_content_files(self, week: int, day: int) -> Dict[str, str]:
        """특정 일차의 콘텐츠 파일들 로드"""
        content_dir = settings.paths.output_dir / f"week{week}" / f"day{day}"
        content = {}

        if not content_dir.exists():
            return content

        for md_file in content_dir.glob("*.md"):
            try:
                content[md_file.stem] = md_file.read_text(encoding='utf-8')
            except Exception as e:
                print(f"파일 로드 오류 {md_file}: {e}")

        return content

    async def full_verification_report(self, target_week: int = None) -> Dict[str, Any]:
        """전체 또는 특정 주차 검증 리포트 생성"""
        results = []
        curriculum_info = self.curriculum_store.get_all_curriculum_info()

        weeks_to_check = [target_week] if target_week else range(1, 5)

        for week in weeks_to_check:
            for day in range(1, 6):
                content_files = await self._load_content_files(week, day)

                if not content_files:
                    results.append({
                        'week': week,
                        'day': day,
                        'status': 'MISSING',
                        'message': f'Week{week}/Day{day} 콘텐츠가 존재하지 않습니다.'
                    })
                    continue

                validation = await self.validate_against_curriculum(week, day, content_files)
                results.append(validation)

        # 통계 계산
        total = len(results)
        complete = sum(1 for r in results if r.get('status') == 'COMPLETE')
        partial = sum(1 for r in results if r.get('status') == 'PARTIAL')
        incomplete = sum(1 for r in results if r.get('status') == 'INCOMPLETE')
        missing = sum(1 for r in results if r.get('status') == 'MISSING')

        return {
            'statistics': {
                'total': total,
                'complete': complete,
                'partial': partial,
                'incomplete': incomplete,
                'missing': missing,
                'completion_rate': (complete / total * 100) if total > 0 else 0
            },
            'results': results
        }

    async def get_missing_services_report(self, week: int = None) -> List[Dict]:
        """누락된 서비스 리포트"""
        report = await self.full_verification_report(week)
        missing_services = []

        for result in report['results']:
            if result.get('missing_services'):
                missing_services.append({
                    'week': result.get('week'),
                    'day': result.get('day'),
                    'day_title': result.get('day_title', ''),
                    'missing': result.get('missing_services', [])
                })

        return missing_services
