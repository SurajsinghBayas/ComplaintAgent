
from typing import TypedDict


class ComplaintState(TypedDict):

    # Customer input
    complaint: str

    # Classification results
    category: str
    priority: str
    reason: str

    # Solution retrieval
    solutions: str

    # Escalation details
    escalation_required: bool
    escalation_reason: str

    # Final response
    final_response: str
