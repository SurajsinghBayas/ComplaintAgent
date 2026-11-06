
from app.graph import complaint_graph


def process_complaint(complaint: str):

    # Initial state
    initial_state = {
        "complaint": complaint,
        "category": "",
        "priority": "",
        "reason": "",
        "solutions": "",
        "escalation_required": False,
        "escalation_reason": "",
        "final_response": ""
    }

    print("\n" + "=" * 55)
    print("SMART COMPLAINT MANAGEMENT AGENT")
    print("=" * 55)

    print("\nCustomer Complaint:")
    print(complaint)

    # Execute graph
    print("\nProcessing complaint...")

    result = complaint_graph.invoke(initial_state)

    # Classification
    print("\n--- COMPLAINT ANALYSIS ---")

    print("Category:", result["category"])
    print("Priority:", result["priority"])
    print("Reason:", result["reason"])

    # Routing result
    print("\n--- ROUTING DECISION ---")

    if result["escalation_required"]:
        print("Route: ESCALATION")
        print("Reason:", result["escalation_reason"])

    else:
        print("Route: SOLUTION SEARCH")

    # Retrieved solutions
    print("\n--- RETRIEVED SOLUTIONS ---")

    if result["solutions"]:
        print(result["solutions"])
    else:
        print("No solutions retrieved.")

    # Final response
    print("\n--- FINAL CUSTOMER RESPONSE ---")

    print(result["final_response"])

    print("\n" + "=" * 55)


def main():

    complaints = [
        "My internet is a little slow today.",

        "Someone has accessed my account without permission.",

        "I paid twice for the same subscription."
    ]

    for complaint in complaints:
        process_complaint(complaint)


if __name__ == "__main__":
    main()
