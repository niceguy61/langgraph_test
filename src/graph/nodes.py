"""Node definitions for LangGraph workflow"""
from typing import Dict, Any
import asyncio

from .state import GraphState
from src.agents import (
    SupervisorAgent,
    CurriculumDesignerAgent,
    ContentGeneratorAgent,
    WebSearcherAgent,
    RAGSearcherAgent,
    ReviewerAgent
)


# Initialize agents
supervisor = SupervisorAgent()
curriculum_designer = CurriculumDesignerAgent()
content_generator = ContentGeneratorAgent()
web_searcher = WebSearcherAgent()
rag_searcher = RAGSearcherAgent()
reviewer = ReviewerAgent()


async def supervisor_node(state: GraphState) -> Dict[str, Any]:
    """Supervisor node - decides next agent"""
    try:
        result = await supervisor.execute(dict(state))
        return {
            "next_agent": result.get("next_agent", "FINISH"),
            "supervisor_reasoning": result.get("supervisor_reasoning", ""),
            "iteration_count": state.get("iteration_count", 0) + 1
        }
    except Exception as e:
        return {
            "next_agent": "FINISH",
            "error": str(e)
        }


async def curriculum_designer_node(state: GraphState) -> Dict[str, Any]:
    """Curriculum designer node - generates and indexes curriculum"""
    try:
        result = await curriculum_designer.execute(dict(state))
        curriculum = result.get("curriculum", {})

        # Index curriculum to ChromaDB
        if curriculum:
            try:
                index_result = await rag_searcher.index_curriculum(curriculum)
                print(f"커리큘럼 인덱싱 완료: {index_result}")
            except Exception as index_error:
                print(f"커리큘럼 인덱싱 실패 (계속 진행): {index_error}")

        return {
            "curriculum": curriculum,
            "completed_tasks": ["curriculum_design"],
            "current_step": "curriculum_designed"
        }
    except Exception as e:
        return {"error": f"Curriculum design failed: {e}"}


async def content_generator_node(state: GraphState) -> Dict[str, Any]:
    """Content generator node"""
    try:
        result = await content_generator.execute(dict(state))

        # Save generated content
        content = result.get("generated_content", {})
        saved_files = await content_generator.save_content(content)

        return {
            "generated_content": content,
            "saved_files": saved_files,
            "completed_tasks": ["content_generation"],
            "current_step": "content_generated"
        }
    except Exception as e:
        return {"error": f"Content generation failed: {e}"}


async def web_searcher_node(state: GraphState) -> Dict[str, Any]:
    """Web searcher node"""
    try:
        result = await web_searcher.execute(dict(state))
        return {
            "web_context": result.get("web_context", ""),
            "completed_tasks": ["web_search"],
            "current_step": "web_searched"
        }
    except Exception as e:
        return {"error": f"Web search failed: {e}"}


async def rag_searcher_node(state: GraphState) -> Dict[str, Any]:
    """RAG searcher node - searches curriculum and existing documents"""
    try:
        result = await rag_searcher.execute(dict(state))

        # Also get curriculum context if week/day specified
        target_week = state.get("target_week")
        target_day = state.get("target_day")
        curriculum_context = ""

        if target_week and target_day:
            try:
                curriculum_context = await rag_searcher.get_curriculum_context_for_generation(
                    target_week, target_day
                )
            except Exception as ctx_error:
                print(f"커리큘럼 컨텍스트 조회 실패: {ctx_error}")

        combined_context = result.get("rag_context", "")
        if curriculum_context:
            combined_context = f"{curriculum_context}\n\n---\n\n{combined_context}"

        return {
            "rag_context": combined_context,
            "curriculum_context": curriculum_context,
            "completed_tasks": ["rag_search"],
            "current_step": "rag_searched"
        }
    except Exception as e:
        return {"error": f"RAG search failed: {e}"}


async def reviewer_node(state: GraphState) -> Dict[str, Any]:
    """Reviewer node - reviews content and validates against curriculum"""
    try:
        result = await reviewer.execute(dict(state))

        # Also validate against curriculum
        target_week = state.get("target_week")
        target_day = state.get("target_day")
        curriculum_validation = None

        if target_week and target_day:
            try:
                curriculum_validation = await reviewer.validate_against_curriculum(
                    target_week, target_day
                )
                print(f"커리큘럼 검증 결과: {curriculum_validation.get('status')}")
            except Exception as val_error:
                print(f"커리큘럼 검증 실패: {val_error}")

        return {
            "reviews": result.get("reviews", {}),
            "average_score": result.get("average_score", 0),
            "needs_revision": result.get("needs_revision", False),
            "curriculum_validation": curriculum_validation,
            "completed_tasks": ["review"],
            "current_step": "reviewed"
        }
    except Exception as e:
        return {"error": f"Review failed: {e}"}


async def finalize_node(state: GraphState) -> Dict[str, Any]:
    """Finalize node - prepare final output with curriculum validation"""
    final_output = {
        "curriculum": state.get("curriculum", {}),
        "generated_content": state.get("generated_content", {}),
        "saved_files": state.get("saved_files", {}),
        "reviews": state.get("reviews", {}),
        "average_score": state.get("average_score", 0),
        "curriculum_validation": state.get("curriculum_validation"),
        "completed_tasks": list(state.get("completed_tasks", [])),
        "status": "completed"
    }

    return {
        "final_output": final_output,
        "current_step": "finalized"
    }


# Synchronous wrappers for LangGraph
def sync_supervisor_node(state: GraphState) -> Dict[str, Any]:
    """Sync wrapper for supervisor node"""
    return asyncio.run(supervisor_node(state))


def sync_curriculum_designer_node(state: GraphState) -> Dict[str, Any]:
    """Sync wrapper for curriculum designer node"""
    return asyncio.run(curriculum_designer_node(state))


def sync_content_generator_node(state: GraphState) -> Dict[str, Any]:
    """Sync wrapper for content generator node"""
    return asyncio.run(content_generator_node(state))


def sync_web_searcher_node(state: GraphState) -> Dict[str, Any]:
    """Sync wrapper for web searcher node"""
    return asyncio.run(web_searcher_node(state))


def sync_rag_searcher_node(state: GraphState) -> Dict[str, Any]:
    """Sync wrapper for RAG searcher node"""
    return asyncio.run(rag_searcher_node(state))


def sync_reviewer_node(state: GraphState) -> Dict[str, Any]:
    """Sync wrapper for reviewer node"""
    return asyncio.run(reviewer_node(state))


def sync_finalize_node(state: GraphState) -> Dict[str, Any]:
    """Sync wrapper for finalize node"""
    return asyncio.run(finalize_node(state))
