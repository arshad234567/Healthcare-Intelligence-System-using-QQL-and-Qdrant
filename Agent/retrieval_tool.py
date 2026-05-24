"""
agent/retrieval_tool.py

Semantic healthcare retrieval agent for retrieving
relevant patient-doctor medical conversations
from Qdrant vector database.

Uses:
- Qdrant Vector DB
- FastEmbed embeddings
- Semantic vector similarity search

This module acts as the retrieval layer
for the Agentic Healthcare RAG System.
"""

from qdrant_client import QdrantClient
from fastembed import TextEmbedding

#Qdrant Configuration
COLLECTION_NAME = "healthcare_conversations"
client = QdrantClient(
    host="localhost",
    port=6333
)
# Embedding Model
embedding_model = TextEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)
#Semantic Retrieval Function
def _semantic_search(
    query: str,
    top_k: int = 5
):
    """
    Performs semantic vector search
    on healthcare conversations stored in Qdrant.
    """

    # Generate query embedding
    query_embedding = list(
        embedding_model.embed([query])
    )[0]
    # Query Qdrant
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding.tolist(),
        limit=top_k
    )
    retrieved_documents = []
    # Extract relevant payloads
    for result in results.points:
        retrieved_documents.append({
            "score": round(result.score, 4),
            "patient_query": result.payload.get(
                "patient_query",
                ""
            ),
            "doctor_response": result.payload.get(
                "doctor_response",
                ""
            ),
            "retrieval_text": result.payload.get(
                "retrieval_text",
                ""
            )
        })

    return retrieved_documents

#Retrieval Agent Node
def healthcare_retrieval_node(state: dict):
    """
    Agent retrieval node for semantic healthcare RAG.
    """
    user_query = state["user_query"]
    retrieved_contexts = _semantic_search(
        query=user_query,
        top_k=3
    )
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


#Testing
if __name__ == "__main__":
    sample_state = {
        "user_query": (
            "I have severe chest pain and breathing issues"
        ),
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