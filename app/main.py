import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.schemas import ComplaintAnalysis

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)

# Create structured LLM
structured_llm = llm.with_structured_output(
    ComplaintAnalysis
)

# Customer complaint
complaint = ["""My internet connection has stopped working since yesterday.
I have restarted my router twice.
I have an important online examination tomorrow.""","""I paid twice for the same subscription but was charged twice.""","""I am not able to access my account since yesterday."""]


for i,complaint in enumerate(complaint,start=1):
# Generate classification
    result = structured_llm.invoke(
        f"""
        Analyze the following customer complaint.
        Identify its category and priority.
        Complaint:
        {complaint}
        """
    )
    print("\n--- Complaint Analysis ---")
    print(result.model_dump())
    