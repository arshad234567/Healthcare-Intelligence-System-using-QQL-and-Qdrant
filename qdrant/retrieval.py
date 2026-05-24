"""
qdrant/retrieval.py

Semantic retrieval functions
"""

from fastembed import TextEmbedding

from qdrant.client import (
    client,
    COLLECTION_NAME
)

#embedding model

embedding_model = TextEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

#semantic search

def semantic_search(
    query: str,
    top_k: int = 3
):

    query_embedding = list(
        embedding_model.embed([query])
    )[0]

    results = client.query_points(

        collection_name=COLLECTION_NAME,

        query=query_embedding.tolist(),

        limit=top_k
    )

    retrieved_documents = []

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