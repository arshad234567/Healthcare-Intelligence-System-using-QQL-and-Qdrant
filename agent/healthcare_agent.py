"""
agent/healthcare_agent.py

Main Agentic Healthcare RAG Agent
using Groq + Agno
"""

import os

from agno.agent import Agent
from agno.models.groq import Groq

from agent.retrieval_tool import healthcare_retrieval_node

from agent.prompts import (
    HEALTHCARE_SYSTEM_PROMPT,
    RAG_INSTRUCTIONS,
    SAFETY_PROMPT,
    FINAL_RESPONSE_PROMPT
)

#build healthcare agent

healthcare_agent = Agent(

    model=Groq(
        id="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY")
    ),

    description="Agentic Healthcare RAG System",

    instructions=[
        HEALTHCARE_SYSTEM_PROMPT,
        RAG_INSTRUCTIONS,
        SAFETY_PROMPT,
        FINAL_RESPONSE_PROMPT
    ],

    markdown=True
)

#main rag pipeline

def run_healthcare_rag(user_query: str):

    #workflow state
    state = {
        "user_query": user_query,
        "retrieved_contexts": [],
        "trace": []
    }

    #retrieve medical contexts
    updated_state = healthcare_retrieval_node(state)

    retrieved_contexts = updated_state["retrieved_contexts"]

    #build retrieval context
    context_text = ""

    for idx, context in enumerate(retrieved_contexts):

        context_text += f"""
Medical Context {idx + 1}

Patient Query:
{context['patient_query']}

Doctor Response:
{context['doctor_response']}
"""

    #final prompt
    final_prompt = f"""
User Healthcare Query:
{user_query}

Retrieved Medical Conversations:
{context_text}

Generate a medically grounded healthcare response
using the retrieved context.
"""

    #generate response
    response = healthcare_agent.run(final_prompt)

    return {
        "query": user_query,
        "retrieved_contexts": retrieved_contexts,
        "response": response.content,
        "trace": updated_state["trace"]
    }

#testing

if __name__ == "__main__":

    query = "I have chest pain and difficulty breathing"

    result = run_healthcare_rag(query)

    print("\n")
    print("=" * 80)
    print("USER QUERY")
    print(result["query"])

    print("\n")
    print("=" * 80)
    print("AI RESPONSE")
    print(result["response"])

    print("\n")
    print("=" * 80)
    print("TRACE")
    print(result["trace"])