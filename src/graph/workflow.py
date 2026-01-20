"""LangGraph workflow definition"""
from typing import Dict, Any, Literal, Optional
from langgraph.graph import StateGraph, END

from .state import GraphState, create_initial_state
from .nodes import (
    sync_supervisor_node,
    sync_curriculum_designer_node,
    sync_content_generator_node,
    sync_web_searcher_node,
    sync_rag_searcher_node,
    sync_reviewer_node,
    sync_finalize_node
)


def route_supervisor(state: GraphState) -> Literal[
    "curriculum_designer",
    "content_generator",
    "web_searcher",
    "rag_searcher",
    "reviewer",
    "finalize"
]:
    """Route based on supervisor decision"""
    next_agent = state.get("next_agent", "FINISH")
    iteration = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 10)

    # Check for max iterations
    if iteration >= max_iterations:
        return "finalize"

    # Check for errors
    if state.get("error"):
        return "finalize"

    # Route to appropriate agent
    if next_agent == "curriculum_designer":
        return "curriculum_designer"
    elif next_agent == "content_generator":
        return "content_generator"
    elif next_agent == "web_searcher":
        return "web_searcher"
    elif next_agent == "rag_searcher":
        return "rag_searcher"
    elif next_agent == "reviewer":
        return "reviewer"
    else:
        return "finalize"


def should_continue(state: GraphState) -> Literal["supervisor", "finalize"]:
    """Determine if workflow should continue"""

    # Check for completion signals
    current_step = state.get("current_step", "")
    completed_tasks = state.get("completed_tasks", [])

    # If reviewed and no revision needed, we're done
    if "review" in completed_tasks and not state.get("needs_revision", False):
        return "finalize"

    # If content generated but not reviewed yet, continue
    if current_step in ["content_generated", "reviewed"] and not state.get("needs_revision"):
        if "review" not in completed_tasks:
            return "supervisor"

    # Continue to supervisor for next decision
    return "supervisor"


def create_workflow() -> StateGraph:
    """Create the LangGraph workflow"""

    # Create graph with state schema
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("supervisor", sync_supervisor_node)
    workflow.add_node("curriculum_designer", sync_curriculum_designer_node)
    workflow.add_node("content_generator", sync_content_generator_node)
    workflow.add_node("web_searcher", sync_web_searcher_node)
    workflow.add_node("rag_searcher", sync_rag_searcher_node)
    workflow.add_node("reviewer", sync_reviewer_node)
    workflow.add_node("finalize", sync_finalize_node)

    # Set entry point
    workflow.set_entry_point("supervisor")

    # Add conditional edges from supervisor
    workflow.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            "curriculum_designer": "curriculum_designer",
            "content_generator": "content_generator",
            "web_searcher": "web_searcher",
            "rag_searcher": "rag_searcher",
            "reviewer": "reviewer",
            "finalize": "finalize"
        }
    )

    # Add edges from agent nodes back to supervisor or finalize
    workflow.add_conditional_edges(
        "curriculum_designer",
        should_continue,
        {
            "supervisor": "supervisor",
            "finalize": "finalize"
        }
    )

    workflow.add_conditional_edges(
        "content_generator",
        should_continue,
        {
            "supervisor": "supervisor",
            "finalize": "finalize"
        }
    )

    workflow.add_conditional_edges(
        "web_searcher",
        should_continue,
        {
            "supervisor": "supervisor",
            "finalize": "finalize"
        }
    )

    workflow.add_conditional_edges(
        "rag_searcher",
        should_continue,
        {
            "supervisor": "supervisor",
            "finalize": "finalize"
        }
    )

    workflow.add_conditional_edges(
        "reviewer",
        should_continue,
        {
            "supervisor": "supervisor",
            "finalize": "finalize"
        }
    )

    # Finalize ends the workflow
    workflow.add_edge("finalize", END)

    return workflow


def compile_workflow():
    """Compile the workflow for execution"""
    workflow = create_workflow()
    return workflow.compile()


def run_workflow(
    request: str,
    target_week: Optional[int] = None,
    target_day: Optional[int] = None
) -> Dict[str, Any]:
    """Run the complete workflow"""

    # Create initial state
    initial_state = create_initial_state(
        request=request,
        target_week=target_week,
        target_day=target_day
    )

    # Compile and run
    app = compile_workflow()
    final_state = app.invoke(initial_state)

    return final_state.get("final_output", {})


async def arun_workflow(
    request: str,
    target_week: Optional[int] = None,
    target_day: Optional[int] = None
) -> Dict[str, Any]:
    """Async version of run_workflow"""

    initial_state = create_initial_state(
        request=request,
        target_week=target_week,
        target_day=target_day
    )

    app = compile_workflow()
    final_state = await app.ainvoke(initial_state)

    return final_state.get("final_output", {})


def stream_workflow(
    request: str,
    target_week: Optional[int] = None,
    target_day: Optional[int] = None
):
    """Stream workflow execution for real-time updates"""

    initial_state = create_initial_state(
        request=request,
        target_week=target_week,
        target_day=target_day
    )

    app = compile_workflow()

    for event in app.stream(initial_state):
        yield event
