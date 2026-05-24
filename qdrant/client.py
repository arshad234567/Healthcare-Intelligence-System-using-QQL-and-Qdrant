from dotenv import load_dotenv
import os

from qdrant_client import QdrantClient

#load env variables

load_dotenv()

#qdrant credentials

QDRANT_URL = os.getenv(
    "QDRANT_URL"
)

QDRANT_API_KEY = os.getenv(
    "QDRANT_API_KEY"
)

#qdrant client

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

COLLECTION_NAME = (
    "healthcare_conversations"
)