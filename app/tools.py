import json
from pathlib import Path
from langchain.tools import tool


@tool
def search_solutions(category: str) -> str:
    """
    Search the complaint knowledge base for troubleshooting
    solutions based on the complaint category.
    """

    # Locate knowledge base
    file_path = Path(__file__).parent.parent / "data" / "knowledge_base.json"

    # Read JSON data
    with open(file_path, "r", encoding="utf-8") as file:
        knowledge_base = json.load(file)

    # Find matching solutions
    results = []

    for solution in knowledge_base["solutions"]:

        if solution["category"] == category:
            results.append(solution)

    # Return matching solutions
    if results:
        return results

    return {"message": "No relevant solutions found."}