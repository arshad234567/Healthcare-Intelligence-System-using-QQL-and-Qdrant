
import uuid
import pandas as pd

from fastembed import TextEmbedding

from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance
)

from qdrant.client import (
    client,
    COLLECTION_NAME
)

#embedding model

embedding_model = TextEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

#load dataset

df = pd.read_csv(
    "data/preprocessed_healthcare_dataset.csv"
)

#parsed documents

parsed_documents = []

for _, row in df.iterrows():

    retrieval_text = f"""
Patient Query:
{row['patient_query']}

Doctor Response:
{row['doctor_response']}
"""

    parsed_documents.append({

        "retrieval_text": retrieval_text,

        "metadata": {

            "patient_query": row["patient_query"],

            "doctor_response": row["doctor_response"]
        }
    })

print(f"Loaded {len(parsed_documents)} documents")

#small subset for development

parsed_documents = parsed_documents[:50]

#extract texts

texts = [
    doc["retrieval_text"]
    for doc in parsed_documents
]

#generate embeddings

embeddings = []

batch_size = 4

for i in range(0, len(texts), batch_size):

    batch = texts[i:i + batch_size]

    batch_embeddings = list(
        embedding_model.embed(batch)
    )

    embeddings.extend(batch_embeddings)

    print(f"Processed batch {(i // batch_size) + 1}")

print(f"Generated {len(embeddings)} embeddings")

#create collection

client.recreate_collection(

    collection_name=COLLECTION_NAME,

    vectors_config=VectorParams(
        size=len(embeddings[0]),
        distance=Distance.COSINE
    )
)

print("Collection created successfully")

#prepare vector points

points = []

for idx, doc in enumerate(parsed_documents):

    point = PointStruct(

        id=str(uuid.uuid4()),

        vector=embeddings[idx].tolist(),

        payload={

            "retrieval_text":
            doc["retrieval_text"],

            "patient_query":
            doc["metadata"]["patient_query"],

            "doctor_response":
            doc["metadata"]["doctor_response"]
        }
    )

    points.append(point)

print(f"Prepared {len(points)} vector points")

#upload vectors

client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print("Vectors uploaded successfully")