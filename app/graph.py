
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from app.state import ComplaintState
from app.schemas import ComplaintAnalysis
from app.tools import search_solutions


# ==========================================
# 1. Load environment variables
# ==========================================

load_dotenv()


# ==========================================
# 2. Initialize LLM
# ==========================================

llm = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)

structured_llm = llm.with_structured_output(
    ComplaintAnalysis
)


# ==========================================
# NODE 1: Complaint Classification
# ==========================================

def classify_node(state: ComplaintState):

    result = structured_llm.invoke(
        f"""
        Analyze the customer complaint.

        Identify the category, priority and reason.

        Categories:
        technical_support,
        payment,
        account_access,
        service_request,
        general_inquiry

        Priority:
        low, medium, high

        Treat suspected unauthorized account access,
        security incidents, duplicate charges and urgent
        time-sensitive failures as high priority.

        Complaint:
        {state['complaint']}
        """
    )

    return {
        "category": result.category,
        "priority": result.priority,
        "reason": result.reason
    }


# ==========================================
# NODE 2: Solution Search
# ==========================================

def solution_node(state: ComplaintState):

    result = search_solutions.invoke({
        "category": state["category"]
    })

    return {
        "solutions": result
    }


# ==========================================
# NODE 3: Escalation
# ==========================================

def escalation_node(state: ComplaintState):

    return {
        "escalation_required": True,
        "escalation_reason": (
            "High-priority complaint requires human review."
        )
    }


# ==========================================
# ROUTER: Priority-based routing
# ==========================================

def priority_router(state: ComplaintState):

    if state["priority"] == "high":
        return "escalate"

    return "search"


# ==========================================
# NODE 4: Response Generation
# ==========================================

def response_node(state: ComplaintState):

    response = llm.invoke(
        f"""
        You are a customer support assistant.

        Customer complaint:
        {state['complaint']}

        Category:
        {state['category']}

        Priority:
        {state['priority']}

        Reason:
        {state['reason']}

        Retrieved solutions:
        {state['solutions']}

        Escalation required:
        {state['escalation_required']}

        Escalation reason:
        {state['escalation_reason']}

        Generate a helpful customer response.

        If escalation is required:
        - Inform the customer that the complaint
          has been flagged for human review.
        - Do not claim that a real support team
          has been contacted.

        If solutions are available:
        - Explain the relevant troubleshooting steps.

        Do not claim that the issue is resolved.
        """
    )

    return {
        "final_response": response.content
    }


# ==========================================
# BUILD LANGGRAPH
# ==========================================

def build_graph():

    graph_builder = StateGraph(ComplaintState)

    # Register nodes
    graph_builder.add_node("classify", classify_node)
    graph_builder.add_node("search", solution_node)
    graph_builder.add_node("escalate", escalation_node)
    graph_builder.add_node("respond", response_node)

    # Starting edge
    graph_builder.add_edge(START, "classify")

    # Conditional routing
    graph_builder.add_conditional_edges(
        "classify",
        priority_router,
        {
            "search": "search",
            "escalate": "escalate"
        }
    )

    # Connect both paths to response generation
    graph_builder.add_edge("search", "respond")
    graph_builder.add_edge("escalate", "respond")

    # End edge
    graph_builder.add_edge("respond", END)

    return graph_builder.compile()


# Initialize graph
complaint_graph = build_graph()
