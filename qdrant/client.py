"""
qdrant/client.py

Qdrant client configuration
"""

from qdrant_client import QdrantClient

#initialize qdrant client

client = QdrantClient(
    host="localhost",
    port=6333
)

COLLECTION_NAME = "healthcare_conversations"