from fastapi import FastAPI
from pydantic import BaseModel

from agent.healthcare_agent import run_healthcare_rag
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Agentic Healthcare RAG API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#request schema
class HealthcareRequest(BaseModel):
    query: str

#health check route
@app.get("/")

def home():
    return {
        "message": "Healthcare RAG API is running"
    }

#main healthcare rag endpoint

@app.post("/ask")

def ask_healthcare_agent(request: HealthcareRequest):
    result = run_healthcare_rag(
        request.query
    )
    return {
        "user_query": result["query"],
        "ai_response": result["response"],
        "retrieved_contexts": result["retrieved_contexts"],
        "trace": result["trace"]
    }