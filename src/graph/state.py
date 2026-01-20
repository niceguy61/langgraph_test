"""State definitions for LangGraph workflow"""
from typing import Any, Dict, List, Optional, TypedDict, Annotated
from operator import add


class GraphState(TypedDict, total=False):
    """State that flows through the graph"""

    # User request
    request: str
    target_week: Optional[int]
    target_day: Optional[int]
    search_query: Optional[str]

    # Workflow control
    current_step: str
    next_agent: str
    completed_tasks: Annotated[List[str], add]
    iteration_count: int
    max_iterations: int

    # Agent outputs
    curriculum: Dict[str, Any]
    generated_content: Dict[str, Any]
    rag_context: str
    web_context: str
    reviews: Dict[str, Any]

    # Quality metrics
    average_score: float
    needs_revision: bool

    # Supervisor reasoning
    supervisor_reasoning: str

    # Final output
    final_output: Dict[str, Any]
    saved_files: Dict[str, str]

    # Error handling
    error: Optional[str]


def create_initial_state(
    request: str,
    target_week: Optional[int] = None,
    target_day: Optional[int] = None
) -> GraphState:
    """Create initial state for the workflow"""
    return GraphState(
        request=request,
        target_week=target_week,
        target_day=target_day,
        current_step="start",
        next_agent="",
        completed_tasks=[],
        iteration_count=0,
        max_iterations=10,
        curriculum={},
        generated_content={},
        rag_context="",
        web_context="",
        reviews={},
        average_score=0.0,
        needs_revision=False,
        supervisor_reasoning="",
        final_output={},
        saved_files={},
        error=None
    )
