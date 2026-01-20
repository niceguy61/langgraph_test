"""Content Generator Agent - Creates lecture content in Markdown"""
from typing import Any, Dict, Optional
from pathlib import Path

from .base import BaseAgent
from src.config import settings


class ContentGeneratorAgent(BaseAgent):
    """Agent responsible for generating lecture content in Markdown"""

    def __init__(self):
        super().__init__(
            name="content_generator",
            description="콘텐츠 생성 에이전트 - 마크다운 형식 강의자료 작성",
            temperature=0.7
        )

    @property
    def system_prompt(self) -> str:
        return """당신은 AWS 교육 콘텐츠 전문 작성자입니다.

당신의 역할:
1. 체계적이고 이해하기 쉬운 AWS 학습 자료를 작성합니다
2. 마크다운 형식으로 깔끔하게 구조화합니다
3. 실습 예제와 코드 스니펫을 포함합니다
4. 핵심 개념을 명확하게 설명합니다
5. 각 서비스의 Overview를 충분히 상세하게 작성합니다

콘텐츠 작성 원칙:
- 한국어로 작성
- 초보자도 이해할 수 있는 상세한 설명
- 각 AWS 서비스가 무엇인지, 왜 필요한지, 어떤 문제를 해결하는지 명확히 설명
- 실무에 적용 가능한 예제 (최소 3개 이상)
- AWS 콘솔 및 CLI 사용법 모두 포함 (스크린샷 설명 포함)
- 비용 관련 주의사항 및 프리티어 활용법 명시
- 각 섹션은 최소 300자 이상으로 충분히 설명

마크다운 구조:
- H1: 강의 제목
- H2: 주요 섹션
- H3: 세부 주제
- 코드 블록: AWS CLI 명령어, 코드 예제
- 표: 서비스 비교, 가격 정보, 옵션 설명
- 팁/경고: 중요 사항 강조 (> **💡 Tip:** 또는 > **⚠️ 주의:** 형식)
- 체크리스트: 단계별 확인 사항"""

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate lecture content"""

        curriculum = state.get("curriculum", {})
        target_week = state.get("target_week")
        target_day = state.get("target_day")
        rag_context = state.get("rag_context", "")
        web_context = state.get("web_context", "")

        generated_content = {}

        if target_week and target_day:
            # Generate specific day content
            content = await self._generate_day_content(
                curriculum, target_week, target_day, rag_context, web_context
            )
            generated_content[f"week{target_week}_day{target_day}"] = content
        elif target_week:
            # Generate all content for a week
            week_data = self._get_week_data(curriculum, target_week)
            if week_data:
                for day_data in week_data.get("days", []):
                    day_num = day_data.get("day", 1)
                    content = await self._generate_day_content(
                        curriculum, target_week, day_num, rag_context, web_context
                    )
                    generated_content[f"week{target_week}_day{day_num}"] = content
        else:
            # Generate overview
            content = await self._generate_overview(curriculum)
            generated_content["overview"] = content

        return {
            "generated_content": generated_content,
            "completed_tasks": state.get("completed_tasks", []) + ["content_generation"],
            "current_step": "content_generated"
        }

    def _get_week_data(self, curriculum: Dict, week: int) -> Optional[Dict]:
        """Extract week data from curriculum"""
        weeks = curriculum.get("weeks", [])
        for w in weeks:
            if w.get("week") == week:
                return w
        return curriculum if curriculum.get("week") == week else None

    async def _generate_overview(self, curriculum: Dict) -> Dict[str, str]:
        """Generate course overview markdown"""

        template = self.get_prompt_template("""
다음 커리큘럼에 대한 과정 개요(overview.md)를 작성해주세요.

커리큘럼 정보:
{curriculum}

다음 내용을 포함하세요:
1. 과정 소개
2. 학습 목표
3. 사전 요구사항
4. 주차별 개요
5. 학습 방법 가이드

마크다운 형식으로 작성:""")

        overview_md = await self.invoke_with_template(
            template,
            curriculum=str(curriculum)[:2000]
        )

        return {
            "type": "overview",
            "content": overview_md
        }

    async def _generate_day_content(
        self,
        curriculum: Dict,
        week: int,
        day: int,
        rag_context: str = "",
        web_context: str = ""
    ) -> Dict[str, Any]:
        """Generate content for a specific day - per-service file approach"""

        week_data = self._get_week_data(curriculum, week)
        day_data = None

        if week_data:
            for d in week_data.get("days", []):
                if d.get("day") == day:
                    day_data = d
                    break

        # Get services for this day
        services = day_data.get("core_services", []) if day_data else ["AWS"]

        # Calculate previous/next navigation
        prev_link, next_link = self._get_nav_links(curriculum, week, day)

        # Generate per-service content files
        service_files = {}
        for idx, service in enumerate(services):
            service_content = await self._generate_service_content(
                week, day, service, day_data, rag_context,
                prev_service=services[idx-1] if idx > 0 else None,
                next_service=services[idx+1] if idx < len(services)-1 else None,
                prev_day_link=prev_link,
                next_day_link=next_link
            )
            # 파일명에 사용할 수 있도록 서비스 이름 정리
            safe_name = service.replace(" ", "-").replace("/", "-")
            service_files[safe_name] = service_content

        # Generate day README (index)
        day_readme = self._generate_day_readme(week, day, day_data, services, prev_link, next_link)

        # Generate practice guide
        practice = await self._generate_practice(week, day, day_data)

        # Generate quiz
        quiz = await self._generate_quiz(week, day, day_data)

        return {
            "week": week,
            "day": day,
            "services": services,
            "service_files": service_files,
            "readme": day_readme,
            "practice": practice,
            "quiz": quiz
        }

    def _get_nav_links(self, curriculum: Dict, week: int, day: int) -> tuple:
        """Get previous and next day navigation links"""
        total_weeks = curriculum.get("total_weeks", 4)
        days_per_week = curriculum.get("days_per_week", 5)

        # Previous
        if day > 1:
            prev_link = f"../day{day-1}/README.md"
        elif week > 1:
            prev_link = f"../../week{week-1}/day{days_per_week}/README.md"
        else:
            prev_link = None

        # Next
        if day < days_per_week:
            next_link = f"../day{day+1}/README.md"
        elif week < total_weeks:
            next_link = f"../../week{week+1}/day1/README.md"
        else:
            next_link = None

        return prev_link, next_link

    def _generate_day_readme(
        self,
        week: int,
        day: int,
        day_data: Optional[Dict],
        services: list,
        prev_link: Optional[str],
        next_link: Optional[str]
    ) -> str:
        """Generate README for the day with index and navigation"""
        title = day_data.get("title", f"Day {day}") if day_data else f"Day {day}"
        topics = day_data.get("topics", []) if day_data else []

        # Navigation bar
        nav = "---\n\n"
        nav += "| "
        nav += f"[⬅️ 이전]({prev_link})" if prev_link else "⬅️ 이전"
        nav += " | "
        nav += f"[🏠 Week {week} 목차](../README.md)"
        nav += " | "
        nav += f"[📚 전체 목차](../../README.md)"
        nav += " | "
        nav += f"[➡️ 다음]({next_link})" if next_link else "➡️ 다음"
        nav += " |\n"

        readme = f"""# Week {week} Day {day}: {title}

{nav}

---

## 📋 오늘의 학습 내용

| 순서 | 서비스 | 파일 |
|-----|-------|------|
"""
        for idx, service in enumerate(services, 1):
            safe_name = service.replace(" ", "-").replace("/", "-")
            readme += f"| {idx} | {service} | [{service}.md](./{safe_name}.md) |\n"

        readme += f"""
## 📚 학습 주제

"""
        for topic in topics:
            readme += f"- {topic}\n"

        readme += f"""

## 📝 실습 및 퀴즈

| 유형 | 파일 |
|-----|------|
| 실습 가이드 | [practice.md](./practice.md) |
| 복습 퀴즈 | [quiz.md](./quiz.md) |

{nav}
"""
        return readme

    async def _generate_service_content(
        self,
        week: int,
        day: int,
        service: str,
        day_data: Optional[Dict],
        rag_context: str,
        prev_service: Optional[str],
        next_service: Optional[str],
        prev_day_link: Optional[str],
        next_day_link: Optional[str]
    ) -> str:
        """Generate complete content for a single service"""

        # Navigation header
        nav_header = self._generate_service_nav(
            service, prev_service, next_service, prev_day_link, next_day_link, week, day
        )

        # Generate each section
        overview = await self._generate_service_overview(week, day, service, day_data)
        concepts = await self._generate_service_concepts(week, day, service, day_data, rag_context)
        console_guide = await self._generate_service_console(week, day, service, day_data)
        cli_guide = await self._generate_service_cli(week, day, service, day_data)
        exam_points = await self._generate_service_exam_points(week, day, service, day_data)

        # Navigation footer (same as header)
        nav_footer = nav_header

        content = f"""{nav_header}

{overview}

{concepts}

{console_guide}

{cli_guide}

{exam_points}

{nav_footer}
"""
        return content

    def _generate_service_nav(
        self,
        service: str,
        prev_service: Optional[str],
        next_service: Optional[str],
        prev_day_link: Optional[str],
        next_day_link: Optional[str],
        week: int,
        day: int
    ) -> str:
        """Generate navigation bar for service file"""
        nav = "---\n\n"
        nav += "| "

        # Previous service or previous day
        if prev_service:
            safe_prev = prev_service.replace(" ", "-").replace("/", "-")
            nav += f"[⬅️ {prev_service}](./{safe_prev}.md)"
        elif prev_day_link:
            nav += f"[⬅️ 이전 Day]({prev_day_link})"
        else:
            nav += "⬅️ 시작"

        nav += " | "
        nav += f"[📑 Day {day} 목차](./README.md)"
        nav += " | "
        nav += f"[🏠 Week {week}](../README.md)"
        nav += " | "

        # Next service or next day
        if next_service:
            safe_next = next_service.replace(" ", "-").replace("/", "-")
            nav += f"[{next_service} ➡️](./{safe_next}.md)"
        elif next_day_link:
            nav += f"[다음 Day ➡️]({next_day_link})"
        else:
            nav += "끝 ➡️"

        nav += " |\n\n---"
        return nav

    async def _generate_service_overview(
        self,
        week: int,
        day: int,
        service: str,
        day_data: Optional[Dict]
    ) -> str:
        """Generate service overview section with purpose, scenarios, related services, cost"""
        # Extract structured data from day_data
        topics = day_data.get("topics", []) if day_data else []
        key_concepts = day_data.get("key_concepts", []) if day_data else []
        practice_goal = day_data.get("practice_goal", "") if day_data else ""

        topics_str = "\n".join([f"- {t}" for t in topics]) if topics else "없음"
        concepts_str = "\n".join([f"- {c}" for c in key_concepts]) if key_concepts else "없음"

        template = self.get_prompt_template("""
# {service} 완전 정복

## 📌 핵심 목적 (What & Why)

{service} 서비스에 대한 Overview를 작성해주세요.

서비스 정보:
- 서비스명: {service}
- 학습 주제(topics):
{topics}
- 핵심 개념(key_concepts):
{concepts}
- 실습 목표: {practice_goal}

다음 구조로 마크다운을 작성하세요 (이 섹션만):

> **한 줄 정의:** {service}는 _____를 위한 AWS의 _____ 서비스입니다.

### 이 서비스가 해결하는 문제
**기존의 문제점:**
- 문제 1: 구체적 설명 (기존에는 어떻게 했는지)
- 문제 2: 구체적 설명
- 문제 3: 구체적 설명

**{service}로 해결:**
- 해결 1: 어떻게 해결되는지
- 해결 2: 어떻게 해결되는지
- 해결 3: 어떻게 해결되는지

### 비유로 이해하기
[일상생활의 비유를 들어 {service}를 쉽게 설명 - 최소 200자]

---

## 🎯 주요 사용 시나리오 (When to Use)

| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 언제 {service}를 선택하는지 | 실제 기업/서비스 사례 |
| 시나리오 2 | 언제 {service}를 선택하는지 | 실제 기업/서비스 사례 |
| 시나리오 3 | 언제 {service}를 선택하는지 | 실제 기업/서비스 사례 |

**이럴 때 {service}를 선택하세요:**
- ✅ 상황 1
- ✅ 상황 2
- ✅ 상황 3

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ 상황 → 대안 서비스 추천 (이유 포함)
- ❌ 상황 → 대안 서비스 추천 (이유 포함)

---

## 🔗 연관 서비스 (Used Together With)

| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| 서비스 A | 왜 함께 사용하는지 | 예: {service} → 서비스 A → ... |
| 서비스 B | 왜 함께 사용하는지 | 예: ... |
| 서비스 C | 왜 함께 사용하는지 | 예: ... |

**자주 사용되는 아키텍처 패턴:**
```
[간단한 아키텍처 다이어그램을 텍스트로 표현]
예: User → CloudFront → S3
```

---

## 💰 비용 구조 (Pricing)

| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| 항목 1 | $X.XX / 단위 | 월 XXX 무료 |
| 항목 2 | $X.XX / 단위 | 12개월 무료 |
| 항목 3 | $X.XX / 단위 | 항상 무료 |

**비용 최적화 팁:**
1. 💡 팁 1: 구체적인 비용 절감 방법
2. 💡 팁 2: 구체적인 비용 절감 방법
3. 💡 팁 3: 구체적인 비용 절감 방법

> **⚠️ 비용 주의:** 예상치 못한 비용이 발생할 수 있는 상황 설명

---

Overview 마크다운:""")

        return await self.invoke_with_template(
            template,
            service=service,
            topics=topics_str,
            concepts=concepts_str,
            practice_goal=practice_goal if practice_goal else "실습 목표 없음",
            day_data=str(day_data) if day_data else "정보 없음"
        )

    async def _generate_service_concepts(
        self,
        week: int,
        day: int,
        service: str,
        day_data: Optional[Dict],
        rag_context: str = ""
    ) -> str:
        """Generate service core concepts section"""
        # Extract structured data from day_data
        topics = day_data.get("topics", []) if day_data else []
        key_concepts = day_data.get("key_concepts", []) if day_data else []

        topics_str = "\n".join([f"- {t}" for t in topics]) if topics else "없음"
        concepts_str = "\n".join([f"- {c}" for c in key_concepts]) if key_concepts else "없음"

        template = self.get_prompt_template("""
{service}의 핵심 개념 섹션을 작성해주세요.

서비스: {service}
학습 주제(topics):
{topics}
핵심 개념(key_concepts):
{concepts}
참고 자료: {rag_context}

다음 구조로 마크다운을 작성하세요 (이 섹션만):

## 📚 핵심 개념

### 개념 1: [{service}의 핵심 개념명]
개념에 대한 상세한 설명 (최소 300자)

#### 왜 중요한가?
- 이유 1: 상세 설명
- 이유 2: 상세 설명

#### 세부 요소
| 요소 | 설명 | 예시 |
|-----|------|-----|
| 요소1 | 설명 | 예시 |
| 요소2 | 설명 | 예시 |
| 요소3 | 설명 | 예시 |

> **💡 Tip:** 실무에서 이 개념이 어떻게 활용되는지

### 개념 2: [두 번째 핵심 개념명]
개념에 대한 상세한 설명 (최소 300자)

#### 작동 원리
1. 단계 1 설명
2. 단계 2 설명
3. 단계 3 설명

> **💡 Tip:** 실무 활용 팁

### 개념 3: [세 번째 핵심 개념명]
개념에 대한 상세한 설명 (최소 300자)

#### 주요 특징
1. **특징 1**: 상세 설명 (2-3문장)
2. **특징 2**: 상세 설명 (2-3문장)
3. **특징 3**: 상세 설명 (2-3문장)

---

핵심 개념 마크다운:""")

        return await self.invoke_with_template(
            template,
            service=service,
            topics=topics_str,
            concepts=concepts_str,
            rag_context=rag_context[:800] if rag_context else "없음"
        )

    async def _generate_service_console(
        self,
        week: int,
        day: int,
        service: str,
        day_data: Optional[Dict]
    ) -> str:
        """Generate AWS Console guide section for the service"""
        # Extract structured data from day_data
        topics = day_data.get("topics", []) if day_data else []
        practice_goal = day_data.get("practice_goal", "") if day_data else ""

        topics_str = "\n".join([f"- {t}" for t in topics]) if topics else "없음"

        template = self.get_prompt_template("""
{service}의 AWS 콘솔 사용법 섹션을 작성해주세요.

서비스: {service}
학습 주제(topics):
{topics}
실습 목표: {practice_goal}

다음 구조로 마크다운을 작성하세요 (이 섹션만):

## 🖥️ AWS 콘솔에서 {service} 사용하기

### Step 1: {service} 서비스 접속
1. AWS Management Console에 로그인합니다
   - URL: https://console.aws.amazon.com
2. 상단 검색창에서 "{service}"을 검색합니다
3. 검색 결과에서 "{service}"을 클릭합니다

> **📸 화면 확인:** {service} 대시보드가 표시되면 정상입니다

### Step 2: [주요 작업 1 - 리소스 생성]
1. 상세 단계 1
   - 클릭할 버튼/메뉴 설명
   - 입력해야 할 값 설명
2. 상세 단계 2
   - 설정 옵션 설명
3. 상세 단계 3
   - 확인 사항

> **📸 화면 확인:** [확인해야 할 화면 요소]

### Step 3: [주요 작업 2 - 설정/구성]
1. 상세 단계 1
2. 상세 단계 2
3. 상세 단계 3

> **⚠️ 주의:** [이 단계에서 주의할 점]

### Step 4: 설정 확인 및 테스트
1. 생성된 리소스 확인 방법
2. 상태 확인 방법
3. 정상 동작 테스트 방법

---

콘솔 가이드 마크다운:""")

        return await self.invoke_with_template(
            template,
            service=service,
            topics=topics_str,
            practice_goal=practice_goal if practice_goal else "실습 목표 없음"
        )

    async def _generate_service_cli(
        self,
        week: int,
        day: int,
        service: str,
        day_data: Optional[Dict]
    ) -> str:
        """Generate AWS CLI guide section for the service"""
        # Extract structured data from day_data
        topics = day_data.get("topics", []) if day_data else []
        practice_goal = day_data.get("practice_goal", "") if day_data else ""

        topics_str = "\n".join([f"- {t}" for t in topics]) if topics else "없음"

        template = self.get_prompt_template("""
{service}의 AWS CLI 사용법 섹션을 작성해주세요.

서비스: {service}
학습 주제(topics):
{topics}
실습 목표: {practice_goal}

다음 구조로 마크다운을 작성하세요 (이 섹션만):

## ⌨️ AWS CLI로 {service} 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

### 예제 1: {service} 리소스 조회
```bash
# [{service} 리소스 목록 조회]
aws [서비스명] list-[리소스] --query '[].Name' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| --query | 결과 필터링 | '[].Name' |
| --output | 출력 형식 | json, table, text |

**예상 출력:**
```
출력 예시를 여기에
```

### 예제 2: {service} 리소스 생성
```bash
# [{service} 리소스 생성]
aws [서비스명] create-[리소스] \\
    --name "example-name" \\
    --option1 value1 \\
    --option2 value2
```

**필수 옵션:**
- `--name`: 리소스 이름
- `--option1`: 옵션 설명

**예상 출력:**
```json
{{
    "ResourceId": "example-id",
    "Status": "creating"
}}
```

### 예제 3: {service} 리소스 수정
```bash
# [{service} 리소스 수정]
aws [서비스명] update-[리소스] \\
    --resource-id "id" \\
    --new-value "value"
```

### 예제 4: {service} 리소스 삭제
```bash
# [{service} 리소스 삭제]
aws [서비스명] delete-[리소스] --resource-id "id"

# 삭제 확인
aws [서비스명] describe-[리소스] --resource-id "id"
```

> **⚠️ 주의:** 삭제는 되돌릴 수 없습니다. 신중하게 실행하세요.

### 자주 사용하는 명령어 정리
```bash
# 조회
aws [서비스] list-[리소스]
aws [서비스] describe-[리소스] --id "id"

# 생성/수정/삭제
aws [서비스] create-[리소스] --name "name"
aws [서비스] update-[리소스] --id "id" --option "value"
aws [서비스] delete-[리소스] --id "id"
```

---

CLI 가이드 마크다운:""")

        return await self.invoke_with_template(
            template,
            service=service,
            topics=topics_str,
            practice_goal=practice_goal if practice_goal else "실습 목표 없음"
        )

    async def _generate_service_exam_points(
        self,
        week: int,
        day: int,
        service: str,
        day_data: Optional[Dict]
    ) -> str:
        """Generate SAA exam key points section for the service"""
        template = self.get_prompt_template("""
{service}의 AWS SAA-C03 시험 핵심 포인트 섹션을 작성해주세요.

서비스: {service}
Day 정보: {day_data}

다음 구조로 마크다운을 작성하세요 (이 섹션만):

## 🎯 SAA-C03 시험 핵심 포인트

### 시험에서 자주 출제되는 {service} 포인트

#### 📌 핵심 출제 포인트 TOP 5
1. **포인트 1**:
   - 설명: 왜 이것이 시험에 중요한지
   - 키워드: `키워드1`, `키워드2`

2. **포인트 2**:
   - 설명: 왜 이것이 시험에 중요한지
   - 키워드: `키워드1`, `키워드2`

3. **포인트 3**:
   - 설명: 왜 이것이 시험에 중요한지
   - 키워드: `키워드1`, `키워드2`

4. **포인트 4**:
   - 설명: 왜 이것이 시험에 중요한지
   - 키워드: `키워드1`, `키워드2`

5. **포인트 5**:
   - 설명: 왜 이것이 시험에 중요한지
   - 키워드: `키워드1`, `키워드2`

#### ⚠️ 시험에서 자주 나오는 함정
| 함정 유형 | 설명 | 올바른 답변 |
|----------|------|------------|
| 함정 1 | 어떻게 헷갈리게 하는지 | 정답 포인트 |
| 함정 2 | 어떻게 헷갈리게 하는지 | 정답 포인트 |
| 함정 3 | 어떻게 헷갈리게 하는지 | 정답 포인트 |

#### 🔄 {service} vs 비슷한 서비스 비교 (시험 단골!)
| 비교 항목 | {service} | 대안 서비스 | 선택 기준 |
|----------|----------|-----------|----------|
| 용도 | {service}의 용도 | 대안의 용도 | 이럴 때 선택 |
| 확장성 | 특징 | 특징 | 이럴 때 선택 |
| 비용 | 특징 | 특징 | 이럴 때 선택 |
| 지연시간 | 특징 | 특징 | 이럴 때 선택 |

#### 📝 시험 대비 체크리스트
- [ ] {service}의 핵심 목적을 한 문장으로 설명할 수 있는가?
- [ ] {service}를 선택해야 하는 시나리오를 알고 있는가?
- [ ] {service}의 제한사항/한계를 알고 있는가?
- [ ] {service}와 비슷한 서비스의 차이점을 설명할 수 있는가?
- [ ] {service}의 비용 구조를 이해하고 있는가?

#### 💡 시험 팁
> **키워드 매칭:** 문제에서 이런 키워드가 나오면 {service}를 떠올리세요:
> - 키워드 1
> - 키워드 2
> - 키워드 3

---

시험 포인트 마크다운:""")

        return await self.invoke_with_template(
            template,
            service=service,
            day_data=str(day_data) if day_data else "정보 없음"
        )

    async def _generate_lecture_overview(
        self,
        week: int,
        day: int,
        day_data: Optional[Dict]
    ) -> str:
        """Generate lecture overview section"""
        services = day_data.get("core_services", []) if day_data else []
        services_str = ", ".join(services) if services else "AWS 서비스"

        template = self.get_prompt_template("""
Week {week}, Day {day}의 서비스 Overview 섹션을 작성해주세요.

**오늘 다룰 핵심 서비스: {services}**

일차 정보:
{day_data}

다음 구조로 마크다운을 작성하세요 (이 섹션만 작성):

# Week {week} Day {day}: [주제에 맞는 제목]

## 📋 학습 목표
이 강의를 완료하면 다음을 할 수 있습니다:
- [ ] 목표 1 (구체적으로)
- [ ] 목표 2 (구체적으로)
- [ ] 목표 3 (구체적으로)

---

(⚠️ 아래부터 각 서비스별로 섹션을 작성하세요. 오늘 다루는 서비스 각각에 대해 작성합니다.)

## 🔍 [서비스명] 완전 정복

### 📌 핵심 목적 (What & Why)
> **한 줄 정의:** [서비스명]은 _____를 위한 AWS의 _____ 서비스입니다.

**이 서비스가 해결하는 문제:**
- 문제 1: 구체적 설명 (기존에는 어떻게 했는지 → 이 서비스로 어떻게 해결되는지)
- 문제 2: 구체적 설명
- 문제 3: 구체적 설명

**비유로 이해하기:**
[일상생활의 비유를 들어 서비스를 쉽게 설명] (최소 200자)

### 🎯 주요 사용 시나리오 (When to Use)
| 시나리오 | 설명 | 구체적 예시 |
|---------|------|-----------|
| 시나리오 1 | 언제 이 서비스를 선택하는지 | 실제 사례 |
| 시나리오 2 | 언제 이 서비스를 선택하는지 | 실제 사례 |
| 시나리오 3 | 언제 이 서비스를 선택하는지 | 실제 사례 |

**이럴 때 선택하세요:**
- ✅ 상황 1
- ✅ 상황 2
- ✅ 상황 3

**이럴 때는 다른 서비스를 고려하세요:**
- ❌ 상황 → 대안 서비스 추천

### 🔗 연관 서비스 (Used Together With)
| 연관 서비스 | 연동 목적 | 일반적인 아키텍처 |
|------------|---------|-----------------|
| 서비스 A | 왜 함께 사용하는지 | 예: [서비스명] → 서비스 A → ... |
| 서비스 B | 왜 함께 사용하는지 | 예: ... |
| 서비스 C | 왜 함께 사용하는지 | 예: ... |

**자주 사용되는 아키텍처 패턴:**
```
[간단한 아키텍처 다이어그램을 텍스트로 표현]
예: User → CloudFront → S3 (정적 웹사이트)
예: User → ALB → EC2 → RDS
```

### 💰 비용 구조 (Pricing)
| 과금 항목 | 요금 | 프리티어 |
|----------|-----|---------|
| 항목 1 | $X.XX / 단위 | 월 XXX 무료 |
| 항목 2 | $X.XX / 단위 | 12개월 무료 |
| 항목 3 | $X.XX / 단위 | 항상 무료 |

**비용 최적화 팁:**
1. 💡 팁 1: 구체적인 비용 절감 방법
2. 💡 팁 2: 구체적인 비용 절감 방법
3. 💡 팁 3: 구체적인 비용 절감 방법

> **⚠️ 비용 주의:** 예상치 못한 비용이 발생할 수 있는 상황 설명

### 📝 주요 특징 및 기능
1. **특징 1**: 상세 설명 (2-3문장)
2. **특징 2**: 상세 설명 (2-3문장)
3. **특징 3**: 상세 설명 (2-3문장)
4. **특징 4**: 상세 설명 (2-3문장)

---

Overview 마크다운:""")

        return await self.invoke_with_template(
            template,
            week=week,
            day=day,
            services=services_str,
            day_data=str(day_data) if day_data else "정보 없음"
        )

    async def _generate_lecture_concepts(
        self,
        week: int,
        day: int,
        day_data: Optional[Dict],
        rag_context: str = ""
    ) -> str:
        """Generate lecture core concepts section"""
        template = self.get_prompt_template("""
Week {week}, Day {day}의 핵심 개념 섹션을 작성해주세요.

일차 정보:
{day_data}

참고 자료:
{rag_context}

다음 구조로 마크다운을 작성하세요 (이 섹션만 작성):

## 📚 핵심 개념

### 개념 1: [핵심 개념명]
개념에 대한 상세한 설명 (최소 300자)

#### 왜 중요한가?
- 이유 1
- 이유 2

#### 세부 요소
| 요소 | 설명 | 예시 |
|-----|------|-----|
| 요소1 | 설명 | 예시 |
| 요소2 | 설명 | 예시 |

> **💡 Tip:** 실무에서 이 개념이 어떻게 활용되는지

### 개념 2: [핵심 개념명]
개념에 대한 상세한 설명 (최소 300자)

#### 작동 원리
1. 단계 1 설명
2. 단계 2 설명
3. 단계 3 설명

> **💡 Tip:** 실무 활용 팁

### 개념 3: [핵심 개념명]
개념에 대한 상세한 설명 (최소 300자)

---

핵심 개념 마크다운:""")

        return await self.invoke_with_template(
            template,
            week=week,
            day=day,
            day_data=str(day_data) if day_data else "정보 없음",
            rag_context=rag_context[:800] if rag_context else "없음"
        )

    async def _generate_lecture_console(
        self,
        week: int,
        day: int,
        day_data: Optional[Dict]
    ) -> str:
        """Generate AWS Console guide section"""
        template = self.get_prompt_template("""
Week {week}, Day {day}의 AWS 콘솔 사용법 섹션을 작성해주세요.

일차 정보:
{day_data}

다음 구조로 마크다운을 작성하세요 (이 섹션만 작성):

## 🖥️ AWS 콘솔에서 사용하기

### Step 1: 서비스 접속
1. AWS Management Console에 로그인합니다
   - URL: https://console.aws.amazon.com
2. 상단 검색창에서 "[서비스명]"을 검색합니다
3. 검색 결과에서 "[서비스명]"을 클릭합니다

> **📸 화면 확인:** 서비스 대시보드가 표시되면 정상입니다

### Step 2: [주요 작업 1]
1. 상세 단계 1
   - 클릭할 버튼/메뉴 설명
   - 입력해야 할 값 설명
2. 상세 단계 2
3. 상세 단계 3

> **📸 화면 확인:** [확인해야 할 화면 요소]

### Step 3: [주요 작업 2]
1. 상세 단계 1
2. 상세 단계 2
3. 상세 단계 3

> **⚠️ 주의:** [이 단계에서 주의할 점]

### Step 4: 설정 확인
1. 생성된 리소스 확인 방법
2. 상태 확인 방법

---

콘솔 가이드 마크다운:""")

        return await self.invoke_with_template(
            template,
            week=week,
            day=day,
            day_data=str(day_data) if day_data else "정보 없음"
        )

    async def _generate_lecture_cli(
        self,
        week: int,
        day: int,
        day_data: Optional[Dict]
    ) -> str:
        """Generate AWS CLI guide section"""
        template = self.get_prompt_template("""
Week {week}, Day {day}의 AWS CLI 사용법 섹션을 작성해주세요.

일차 정보:
{day_data}

다음 구조로 마크다운을 작성하세요 (이 섹션만 작성):

## ⌨️ AWS CLI로 사용하기

### 사전 준비
```bash
# AWS CLI 버전 확인
aws --version

# AWS 자격 증명 확인
aws sts get-caller-identity

# 현재 리전 확인
aws configure get region
```

### 예제 1: [기본 조회]
```bash
# [조회 명령어 설명]
aws [서비스] [명령] --query '[쿼리]' --output table
```

**옵션 설명:**
| 옵션 | 설명 | 예시 값 |
|-----|------|--------|
| --query | 결과 필터링 | '[].Name' |
| --output | 출력 형식 | json, table, text |

**예상 출력:**
```
출력 예시
```

### 예제 2: [리소스 생성]
```bash
# [생성 명령어 설명]
aws [서비스] create-[리소스] \\
    --name "example-name" \\
    --option1 value1 \\
    --option2 value2
```

**필수 옵션:**
- `--name`: 리소스 이름 (영문, 숫자, 하이픈 사용)
- `--option1`: 옵션 설명

**예상 출력:**
```json
{{
    "ResourceId": "example-id",
    "Status": "creating"
}}
```

### 예제 3: [리소스 수정/업데이트]
```bash
# [수정 명령어 설명]
aws [서비스] update-[리소스] \\
    --resource-id "id" \\
    --new-value "value"
```

### 예제 4: [리소스 삭제]
```bash
# [삭제 명령어 설명]
aws [서비스] delete-[리소스] --resource-id "id"

# 삭제 확인
aws [서비스] describe-[리소스] --resource-id "id"
```

> **⚠️ 주의:** 삭제는 되돌릴 수 없습니다. 신중하게 실행하세요.

---

CLI 가이드 마크다운:""")

        return await self.invoke_with_template(
            template,
            week=week,
            day=day,
            day_data=str(day_data) if day_data else "정보 없음"
        )

    async def _generate_lecture_best_practices(
        self,
        week: int,
        day: int,
        day_data: Optional[Dict]
    ) -> str:
        """Generate cost and best practices section"""
        template = self.get_prompt_template("""
Week {week}, Day {day}의 비용 및 베스트 프랙티스 섹션을 작성해주세요.

일차 정보:
{day_data}

다음 구조로 마크다운을 작성하세요 (이 섹션만 작성):

## 💰 비용 및 프리티어

### 요금 구조
| 항목 | 요금 | 단위 | 프리티어 |
|-----|------|-----|---------|
| 항목1 | $X.XXX | 시간당/GB당 | 월 XXX 무료 |
| 항목2 | $X.XXX | 요청당 | 월 XXX 무료 |
| 항목3 | $X.XXX | GB당 | 12개월 무료 |

### 프리티어 활용 팁
1. **팁 1**: 구체적인 비용 절감 방법
2. **팁 2**: 구체적인 비용 절감 방법
3. **팁 3**: 구체적인 비용 절감 방법

### 비용 모니터링
```bash
# AWS Cost Explorer로 비용 확인
aws ce get-cost-and-usage \\
    --time-period Start=2024-01-01,End=2024-01-31 \\
    --granularity MONTHLY \\
    --metrics "BlendedCost"
```

> **⚠️ 주의:** 프리티어 한도 초과 시 요금이 청구됩니다!

## ⚠️ 주의사항 및 베스트 프랙티스

### 보안 베스트 프랙티스
1. **최소 권한 원칙**: 필요한 권한만 부여
2. **암호화 활성화**: 저장 데이터와 전송 데이터 암호화
3. **로깅 활성화**: CloudTrail로 API 호출 기록

### 성능 최적화
1. **팁 1**: 구체적인 성능 개선 방법
2. **팁 2**: 구체적인 성능 개선 방법

### 일반적인 실수와 해결법
| 실수 | 원인 | 해결 방법 |
|-----|------|----------|
| 실수 1 | 원인 설명 | 해결 방법 설명 |
| 실수 2 | 원인 설명 | 해결 방법 설명 |
| 실수 3 | 원인 설명 | 해결 방법 설명 |

## 📝 요약

### 오늘 배운 핵심 내용
1. **핵심 1**: 한 줄 요약
2. **핵심 2**: 한 줄 요약
3. **핵심 3**: 한 줄 요약

### 핵심 명령어 정리
```bash
# 조회
aws [서비스] list-[리소스]

# 생성
aws [서비스] create-[리소스] --name "name"

# 삭제
aws [서비스] delete-[리소스] --id "id"
```

## ➡️ 다음 학습
다음 시간에는 [다음 주제]에 대해 학습합니다.

---

비용/베스트프랙티스 마크다운:""")

        return await self.invoke_with_template(
            template,
            week=week,
            day=day,
            day_data=str(day_data) if day_data else "정보 없음"
        )

    async def _generate_lecture(
        self,
        week: int,
        day: int,
        day_data: Optional[Dict],
        rag_context: str,
        web_context: str
    ) -> str:
        """Generate lecture markdown (legacy - full version)"""

        template = self.get_prompt_template("""
Week {week}, Day {day} 강의 자료를 작성해주세요.

일차 정보:
{day_data}

참고 자료 (RAG):
{rag_context}

최신 정보 (웹):
{web_context}

⚠️ 중요: 각 섹션을 충분히 상세하게 작성하세요. 초보자가 읽어도 완전히 이해할 수 있도록 설명해야 합니다.

다음 구조로 마크다운을 작성하세요:

# Week {week} Day {day}: [제목]

## 📋 학습 목표
이 강의를 완료하면 다음을 할 수 있습니다:
- [ ] 목표 1 (구체적으로)
- [ ] 목표 2 (구체적으로)
- [ ] 목표 3 (구체적으로)

## 🔍 서비스 Overview

### 이 서비스는 무엇인가요?
[서비스명]이 무엇인지 초보자도 이해할 수 있게 상세히 설명합니다.
비유를 들어 설명하고, 왜 이 서비스가 필요한지 설명합니다.

### 왜 이 서비스를 사용하나요?
- 해결하는 문제 1: 구체적 설명
- 해결하는 문제 2: 구체적 설명
- 해결하는 문제 3: 구체적 설명

### 실제 사용 사례
| 사용 사례 | 설명 | 적합한 상황 |
|----------|------|------------|
| 사례 1 | 설명 | 상황 |
| 사례 2 | 설명 | 상황 |
| 사례 3 | 설명 | 상황 |

### 주요 특징
1. **특징 1**: 상세 설명 (최소 2-3문장)
2. **특징 2**: 상세 설명 (최소 2-3문장)
3. **특징 3**: 상세 설명 (최소 2-3문장)

## 📚 핵심 개념

### [개념 1]
개념에 대한 상세한 설명 (최소 200자 이상)
- 하위 개념 1
- 하위 개념 2

> **💡 Tip:** 실무에서 이 개념이 어떻게 활용되는지 설명

### [개념 2]
개념에 대한 상세한 설명 (최소 200자 이상)

## 🖥️ AWS 콘솔에서 사용하기

### Step 1: [단계명]
1. AWS Management Console에 로그인합니다
2. 상단 검색창에서 "[서비스명]"을 검색합니다
3. (상세한 단계별 설명 계속...)

> **📸 화면 설명:** 각 단계에서 보이는 화면 요소들을 설명합니다

### Step 2: [단계명]
...계속 상세하게

## ⌨️ AWS CLI로 사용하기

### 사전 준비
```bash
# AWS CLI가 설치되어 있는지 확인
aws --version

# AWS 자격 증명 설정 확인
aws sts get-caller-identity
```

### 예제 1: [기본 사용법]
```bash
# 명령어 설명
aws [서비스] [명령] --옵션 값
```

**명령어 설명:**
- `--옵션1`: 이 옵션의 의미와 사용법
- `--옵션2`: 이 옵션의 의미와 사용법

**예상 출력:**
```json
{{
  "결과": "예시"
}}
```

### 예제 2: [고급 사용법]
```bash
# 더 복잡한 예제
```

## 💰 비용 및 프리티어

### 요금 구조
| 항목 | 요금 | 프리티어 |
|-----|------|---------|
| 항목1 | $X.XX | 무료 Y개월 |
| 항목2 | $X.XX | 월 Z시간 무료 |

### 프리티어 활용 팁
- 팁 1: 구체적인 설명
- 팁 2: 구체적인 설명

> **⚠️ 주의:** 예상치 못한 비용을 피하기 위한 주의사항

## ⚠️ 주의사항 및 베스트 프랙티스

### 보안 관련
- 보안 주의사항 1 (상세 설명)
- 보안 주의사항 2 (상세 설명)

### 성능 관련
- 성능 팁 1
- 성능 팁 2

### 일반적인 실수와 해결법
| 실수 | 원인 | 해결 방법 |
|-----|------|----------|
| 실수1 | 원인 | 해결법 |
| 실수2 | 원인 | 해결법 |

## 📝 요약

### 오늘 배운 핵심 내용
1. **핵심 1**: 요약
2. **핵심 2**: 요약
3. **핵심 3**: 요약

### 핵심 명령어 정리
```bash
# 가장 많이 사용하는 명령어들
```

## ➡️ 다음 학습
다음 시간에는 [주제]에 대해 학습합니다. 오늘 배운 내용을 기반으로...

---

강의 마크다운:""")

        return await self.invoke_with_template(
            template,
            week=week,
            day=day,
            day_data=str(day_data) if day_data else "정보 없음",
            rag_context=rag_context[:1000] if rag_context else "없음",
            web_context=web_context[:1000] if web_context else "없음"
        )

    async def _generate_practice(
        self,
        week: int,
        day: int,
        day_data: Optional[Dict]
    ) -> str:
        """Generate practice guide markdown"""
        # Extract structured data from day_data
        topics = day_data.get("topics", []) if day_data else []
        key_concepts = day_data.get("key_concepts", []) if day_data else []
        practice_goal = day_data.get("practice_goal", "") if day_data else ""
        core_services = day_data.get("core_services", []) if day_data else []

        topics_str = "\n".join([f"- {t}" for t in topics]) if topics else "없음"
        concepts_str = "\n".join([f"- {c}" for c in key_concepts]) if key_concepts else "없음"
        services_str = ", ".join(core_services) if core_services else "AWS 서비스"

        template = self.get_prompt_template("""
Week {week}, Day {day} 실습 가이드를 작성해주세요.

핵심 서비스: {services}
학습 주제(topics):
{topics}
핵심 개념(key_concepts):
{concepts}
실습 목표: {practice_goal}

⚠️ 중요: 이 실습 가이드는 AWS를 처음 사용하는 초보자도 바로 따라할 수 있어야 합니다.
각 단계는 상세하게, 스크린샷을 대체할 수 있을 만큼 구체적으로 작성하세요.

다음 구조로 마크다운을 작성하세요:

# Week {week} Day {day} 실습 가이드

## ⚠️ 필수 사전 준비

> **🚨 중요:** 실습을 시작하기 전에 반드시 아래 가이드를 먼저 완료하세요!

### 📚 필수 선행 문서
실습을 시작하기 전에 다음 문서들을 **반드시** 먼저 읽고 완료하세요:

| 문서 | 설명 | 필수 여부 |
|-----|------|----------|
| [AWS 계정 생성 가이드](../prerequisites/aws-account-setup.md) | AWS 계정이 없다면 이 가이드를 따라 계정을 생성하세요 | ✅ 필수 |
| [AWS CLI 설치 가이드](../prerequisites/aws-cli-setup.md) | AWS CLI 설치 및 설정 방법 | ✅ 필수 |
| [IAM 사용자 생성 가이드](../prerequisites/iam-user-setup.md) | 실습용 IAM 사용자 생성 방법 | ✅ 필수 |
| [VS Code 설정 가이드](../prerequisites/vscode-setup.md) | 개발 환경 설정 (선택) | 선택 |

### ✅ 사전 체크리스트
실습을 시작하기 전 아래 항목들을 모두 확인하세요:

- [ ] AWS 계정이 있고 로그인할 수 있다
- [ ] AWS CLI가 설치되어 있다 (`aws --version` 으로 확인)
- [ ] AWS CLI 자격 증명이 설정되어 있다 (`aws sts get-caller-identity` 로 확인)
- [ ] 실습에 필요한 IAM 권한이 있다
- [ ] 결제 알림이 설정되어 있다 (예상치 못한 비용 방지)

```bash
# 사전 준비 확인 명령어
aws --version
aws sts get-caller-identity
```

> **⚠️ 주의:** 위 체크리스트가 모두 완료되지 않았다면 실습을 진행하지 마세요!
> 문제 발생 시 해결이 어려울 수 있습니다.

---

## 🎯 실습 목표
이 실습을 완료하면 다음을 할 수 있습니다:
- [ ] 목표 1 (구체적)
- [ ] 목표 2 (구체적)
- [ ] 목표 3 (구체적)

## ⏱️ 예상 소요 시간
- 전체 실습: 약 30-45분
- Step 1: 약 10분
- Step 2: 약 15분
- Step 3: 약 10분
- 리소스 정리: 약 5분

---

## 📝 실습 단계

### Step 1: [단계명] (약 10분)

#### 1.1 [세부 단계]
```bash
# 명령어와 설명
```

**예상 출력:**
```
출력 예시
```

> **💡 설명:** 이 명령어가 무엇을 하는지 상세히 설명합니다.

#### 1.2 [세부 단계]
**AWS 콘솔에서:**
1. 화면 상단의 서비스 검색창에서 "[서비스명]" 입력
2. 검색 결과에서 "[서비스명]" 클릭
3. (상세 단계 계속...)

> **📸 화면 확인:** [설명할 화면 요소]가 보이면 정상입니다.

#### ✅ Step 1 완료 확인
다음이 보이면 Step 1이 완료된 것입니다:
- 확인 사항 1
- 확인 사항 2

---

### Step 2: [단계명] (약 15분)

#### 2.1 [세부 단계]
...상세하게 작성...

#### 2.2 [세부 단계]
...상세하게 작성...

#### ✅ Step 2 완료 확인
다음이 보이면 Step 2가 완료된 것입니다:
- 확인 사항 1
- 확인 사항 2

---

### Step 3: [단계명] (약 10분)

...계속 상세하게...

---

## ✅ 실습 완료 확인

### 최종 확인 체크리스트
- [ ] 확인 항목 1
- [ ] 확인 항목 2
- [ ] 확인 항목 3

### 예상 최종 결과
```bash
# 결과 확인 명령어
```

**예상 출력:**
```
정상적인 출력 예시
```

---

## 🔧 트러블슈팅

### 문제 1: [일반적인 오류 메시지]
**증상:** 오류 메시지나 증상 설명

**원인:** 왜 이 문제가 발생하는지

**해결 방법:**
```bash
# 해결 명령어
```

### 문제 2: [또 다른 일반적인 문제]
**증상:** ...
**원인:** ...
**해결 방법:** ...

### 문제 3: 권한 오류 (AccessDenied)
**증상:** `AccessDenied` 또는 `UnauthorizedAccess` 오류

**해결 방법:**
1. IAM 사용자 권한 확인
2. 필요한 정책 연결
```bash
# 현재 사용자 권한 확인
aws sts get-caller-identity
```

---

## 🧹 리소스 정리 (필수!)

> **⚠️ 중요:** 실습 완료 후 반드시 리소스를 정리하세요!
> 정리하지 않으면 **예상치 못한 비용**이 발생할 수 있습니다.

### 정리할 리소스 목록
- [ ] 리소스 1
- [ ] 리소스 2
- [ ] 리소스 3

### 리소스 정리 명령어
```bash
# 1. [리소스 1] 삭제
aws [명령어]

# 2. [리소스 2] 삭제
aws [명령어]

# 3. 삭제 확인
aws [확인 명령어]
```

### 정리 완료 확인
```bash
# 리소스가 모두 삭제되었는지 확인
aws [확인 명령어]
```

---

## 📚 추가 학습 자료
- [AWS 공식 문서 링크]
- [관련 튜토리얼]
- [심화 학습 자료]

---

실습 가이드 마크다운:""")

        return await self.invoke_with_template(
            template,
            week=week,
            day=day,
            services=services_str,
            topics=topics_str,
            concepts=concepts_str,
            practice_goal=practice_goal if practice_goal else "실습 목표 없음"
        )

    async def _generate_quiz(
        self,
        week: int,
        day: int,
        day_data: Optional[Dict]
    ) -> str:
        """Generate quiz markdown - simplified and focused"""
        # Extract structured data from day_data
        topics = day_data.get("topics", []) if day_data else []
        key_concepts = day_data.get("key_concepts", []) if day_data else []
        core_services = day_data.get("core_services", []) if day_data else []

        topics_str = "\n".join([f"- {t}" for t in topics]) if topics else "없음"
        concepts_str = "\n".join([f"- {c}" for c in key_concepts]) if key_concepts else "없음"
        services_str = ", ".join(core_services) if core_services else "AWS 서비스"

        template = self.get_prompt_template("""
Week {week}, Day {day} 복습 퀴즈를 5문제만 작성하세요.

핵심 서비스: {services}
학습 주제(topics):
{topics}
핵심 개념(key_concepts):
{concepts}

형식:

# Week {week} Day {day} 복습 퀴즈

## 객관식 (3문제)

### Q1. [문제]
- A) 선택지1
- B) 선택지2
- C) 선택지3
- D) 선택지4

### Q2. [문제]
- A) 선택지1
- B) 선택지2
- C) 선택지3
- D) 선택지4

### Q3. [문제]
- A) 선택지1
- B) 선택지2
- C) 선택지3
- D) 선택지4

## OX 문제 (2문제)

### Q4. [문장] (O/X)

### Q5. [문장] (O/X)

---

## 정답

| 문제 | 정답 | 해설 |
|-----|------|-----|
| Q1 | ? | 간단한 해설 |
| Q2 | ? | 간단한 해설 |
| Q3 | ? | 간단한 해설 |
| Q4 | O/X | 간단한 해설 |
| Q5 | O/X | 간단한 해설 |

---

퀴즈:""")

        return await self.invoke_with_template(
            template,
            week=week,
            day=day,
            services=services_str,
            topics=topics_str,
            concepts=concepts_str
        )

    async def save_content(self, content: Dict[str, Any], base_path: Optional[Path] = None) -> Dict[str, str]:
        """Save generated content to files - supports new per-service structure"""

        if base_path is None:
            base_path = settings.paths.output_dir

        saved_files = {}

        for key, value in content.items():
            if key == "overview":
                file_path = base_path / "overview.md"
                file_path.write_text(value.get("content", ""), encoding="utf-8")
                saved_files[key] = str(file_path)

            elif key.startswith("week"):
                # Parse week and day from key
                parts = key.split("_")
                week = parts[0]  # e.g., "week1"
                day = parts[1] if len(parts) > 1 else None  # e.g., "day1"

                if day:
                    day_dir = base_path / week / day
                else:
                    day_dir = base_path / week

                day_dir.mkdir(parents=True, exist_ok=True)

                if isinstance(value, dict):
                    # New structure with service_files
                    if "service_files" in value:
                        # Save per-service files
                        for service_name, service_content in value.get("service_files", {}).items():
                            file_path = day_dir / f"{service_name}.md"
                            file_path.write_text(service_content, encoding="utf-8")
                            saved_files[f"{key}_{service_name}"] = str(file_path)

                        # Save README
                        if "readme" in value:
                            file_path = day_dir / "README.md"
                            file_path.write_text(value["readme"], encoding="utf-8")
                            saved_files[f"{key}_readme"] = str(file_path)

                        # Save practice
                        if "practice" in value:
                            file_path = day_dir / "practice.md"
                            file_path.write_text(value["practice"], encoding="utf-8")
                            saved_files[f"{key}_practice"] = str(file_path)

                        # Save quiz
                        if "quiz" in value:
                            file_path = day_dir / "quiz.md"
                            file_path.write_text(value["quiz"], encoding="utf-8")
                            saved_files[f"{key}_quiz"] = str(file_path)
                    else:
                        # Legacy structure - save each content type
                        for content_type, content_text in value.items():
                            if isinstance(content_text, str):
                                file_path = day_dir / f"{content_type}.md"
                                file_path.write_text(content_text, encoding="utf-8")
                                saved_files[f"{key}_{content_type}"] = str(file_path)
                else:
                    file_path = day_dir / "content.md"
                    file_path.write_text(str(value), encoding="utf-8")
                    saved_files[key] = str(file_path)

        return saved_files

    def _generate_week_readme(self, week: int, week_data: Dict, days_per_week: int = 5) -> str:
        """Generate README for a week with index of all days"""
        title = week_data.get("title", f"Week {week}")
        description = week_data.get("description", "")
        services = week_data.get("core_services", week_data.get("services", []))
        objectives = week_data.get("learning_objectives", [])

        readme = f"""# Week {week}: {title}

---

| [📚 전체 목차](../README.md) | [⬅️ 이전 주차](../week{week-1}/README.md) | [다음 주차 ➡️](../week{week+1}/README.md) |
|---------------------------|----------------------------------------|----------------------------------------|

---

## 📋 주차 개요

{description}

## 🎯 학습 목표

"""
        for obj in objectives:
            readme += f"- [ ] {obj}\n"

        readme += f"""
## 🔧 다루는 서비스

"""
        for svc in services:
            readme += f"- {svc}\n"

        readme += f"""
## 📅 일별 학습 내용

| Day | 제목 | 핵심 서비스 | 바로가기 |
|-----|------|-----------|---------|
"""
        days = week_data.get("days", [])
        for day_data in days:
            if isinstance(day_data, dict):
                day_num = day_data.get("day", 1)
                day_title = day_data.get("title", f"Day {day_num}")
                day_services = day_data.get("core_services", [])
                services_str = ", ".join(day_services[:3])
                if len(day_services) > 3:
                    services_str += " ..."
                readme += f"| Day {day_num} | {day_title} | {services_str} | [📖 학습하기](./day{day_num}/README.md) |\n"

        readme += f"""

---

| [📚 전체 목차](../README.md) | [⬅️ 이전 주차](../week{week-1}/README.md) | [다음 주차 ➡️](../week{week+1}/README.md) |
|---------------------------|----------------------------------------|----------------------------------------|
"""
        return readme

    def _generate_course_readme(self, curriculum: Dict) -> str:
        """Generate main README for the entire course"""
        title = curriculum.get("title", "AWS Solutions Architect Associate (SAA-C03) 학습 과정")
        total_weeks = curriculum.get("total_weeks", 4)
        total_services = curriculum.get("total_services", 50)

        readme = f"""# {title}

---

## 📋 과정 소개

이 학습 과정은 AWS Solutions Architect Associate (SAA-C03) 자격증 준비를 위한 체계적인 커리큘럼입니다.

- **총 학습 기간:** {total_weeks}주
- **다루는 AWS 서비스:** {total_services}개+
- **학습 형태:** 이론 + 콘솔 실습 + CLI 실습

## 🎯 학습 목표

이 과정을 완료하면:
- [ ] AWS 핵심 서비스들을 이해하고 활용할 수 있습니다
- [ ] SAA-C03 시험에 출제되는 주요 개념을 마스터합니다
- [ ] 실무에서 AWS 아키텍처를 설계할 수 있습니다

---

## 📅 주차별 학습 내용

| 주차 | 제목 | 핵심 서비스 | 바로가기 |
|-----|------|-----------|---------|
"""
        weeks = curriculum.get("weeks", [])
        for week_data in weeks:
            week_num = week_data.get("week", 1)
            week_title = week_data.get("title", f"Week {week_num}")
            week_services = week_data.get("core_services", week_data.get("services", []))
            services_str = ", ".join(week_services[:4])
            if len(week_services) > 4:
                services_str += " ..."
            readme += f"| Week {week_num} | {week_title} | {services_str} | [📖 학습하기](./week{week_num}/README.md) |\n"

        readme += """

---

## 📚 필수 사전 준비

실습을 시작하기 전에 다음 문서를 먼저 확인하세요:

| 문서 | 설명 |
|-----|------|
| [AWS 계정 생성 가이드](./prerequisites/aws-account-setup.md) | AWS 계정 생성 방법 |
| [AWS CLI 설치 가이드](./prerequisites/aws-cli-setup.md) | AWS CLI 설치 및 설정 |
| [IAM 사용자 생성 가이드](./prerequisites/iam-user-setup.md) | 실습용 IAM 사용자 생성 |

---

## 🎓 학습 방법

1. **순서대로 학습**: Week 1부터 순차적으로 진행하세요
2. **실습 필수**: 각 서비스별 콘솔/CLI 실습을 반드시 완료하세요
3. **퀴즈 풀이**: 각 Day의 퀴즈로 학습 내용을 점검하세요
4. **복습**: 시험 포인트 섹션을 중심으로 복습하세요

---

> 🤖 이 자료는 AWS Lecture Generator로 자동 생성되었습니다.
"""
        return readme
