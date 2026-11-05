from pydantic import BaseModel, Field
from typing import Literal


class ComplaintAnalysis(BaseModel):

    category: Literal[
        "technical_support",
        "payment",
        "account_access",
        "service_request",
        "general_inquiry"
    ]

    priority: Literal["low", "medium", "high"]

    reason: str = Field(
        description="Reason for assigning this category and priority"
    )