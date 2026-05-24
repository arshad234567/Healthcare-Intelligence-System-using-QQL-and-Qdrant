from qdrant.retrieval import semantic_search

#retrieval agent node
def healthcare_retrieval_node(state: dict):
    """
    Agent retrieval node for healthcare RAG.
    """
    user_query = state["user_query"]
    #semantic retrieval
    retrieved_contexts = semantic_search(
        query=user_query,
        top_k=3
    )
    #update workflow state
    state["retrieved_contexts"] = retrieved_contexts
    state["trace"].append({
        "agent": "healthcare_retrieval_agent",
        "documents_retrieved": len(retrieved_contexts)
    })
    print(
        f"[Healthcare Retrieval] Retrieved "
        f"{len(retrieved_contexts)} medical contexts"
    )
    return state
#testing
if __name__ == "__main__":
    sample_state = {
        "user_query":
        "I have severe chest pain and breathing issues",
        "retrieved_contexts": [],
        "trace": []
    }
    updated_state = healthcare_retrieval_node(
        sample_state
    )
    print("\n")
    for idx, context in enumerate(
        updated_state["retrieved_contexts"]
    ):
        print("=" * 80)
        print(f"Result {idx + 1}")
        print("\nSimilarity Score:")
        print(context["score"])
        print("\nPatient Query:")
        print(context["patient_query"])
        print("\nDoctor Response:")
        print(context["doctor_response"])