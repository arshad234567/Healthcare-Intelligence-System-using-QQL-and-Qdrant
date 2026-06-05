from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from agent.healthcare_agent import HealthcareAgent
from gliner_entities.entity_pipeline import EntityPipeline
from neo4j_graph.medical_knowledge_graph import MedicalKnowledgeGraph

app=FastAPI(
    title="Agentic Healthcare GraphRAG API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#request schema
class HealthcareRequest(BaseModel):
    query:str

#initialize services
entity_pipeline=EntityPipeline()

medical_graph=MedicalKnowledgeGraph()

healthcare_agent=HealthcareAgent()

#health check
@app.get("/")
def home():

    return {

        "message":
        "Agentic Healthcare GraphRAG API Running",

        "status":
        "healthy"

    }

#entity extraction endpoint
@app.post("/extract_entities")
def extract_entities(
    request:HealthcareRequest
):

    result=entity_pipeline.process(
        request.query
    )

    return result

#graph retrieval endpoint
@app.post("/graph_context")
def graph_context(
    request:HealthcareRequest
):

    entities=entity_pipeline.process(
        request.query
    )

    symptoms=[]

    for symptom in entities[
        "symptoms"
    ]:

        symptoms.append(

            symptom[
                "entity_text"
            ]

        )

    graph_context=medical_graph.retrieve_context(
        symptoms
    )

    return {

        "query":
        request.query,

        "symptoms":
        symptoms,

        "graph_context":
        graph_context

    }

@app.post("/ask")
def ask_healthcare_agent(
    request:HealthcareRequest
):

    try:

        entities=entity_pipeline.process(
            request.query
        )

        symptoms=[]

        for symptom in entities["symptoms"]:

            symptoms.append(
                symptom["entity_text"]
            )

        graph_context=medical_graph.retrieve_context(
            symptoms
        )

        semantic_context=[]

        result=healthcare_agent.process_query(

            request.query,

            graph_context,

            semantic_context

        )

        return result

    except Exception as error:

        return {

            "error":
            str(error)

        }