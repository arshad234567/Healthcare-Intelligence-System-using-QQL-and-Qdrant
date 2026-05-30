import os
import logging
from typing import List
from groq import Groq

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class PulmonologyAgent:

    def __init__(self):
        api_key=os.getenv(
            "GROQ_API_KEY"
        )
        if not api_key:
            raise EnvironmentError(
                "GROQ_API_KEY not found"
            )
        self.client=Groq(
            api_key=api_key
        )
        self.model=os.getenv(
            "PULMONOLOGY_MODEL",
            "llama-3.3-70b-versatile"
        )
        self.logger=logging.getLogger(
            self.__class__.__name__
        )

    def validate_inputs(
        self,
        query:str,
        graph_context:List,
        semantic_context:List
    )->None:

        if not query.strip():
            raise ValueError(
                "query cannot be empty"
            )
        if not isinstance(
            graph_context,
            list
        ):
            raise TypeError(
                "graph_context must be list"
            )
        if not isinstance(
            semantic_context,
            list
        ):
            raise TypeError(
                "semantic_context must be list"
            )

    def build_prompt(
        self,
        query:str,
        graph_context:List,
        semantic_context:List
    )->str:

        return f"""
You are an expert pulmonology specialist.

User Query:

{query}

Validated Graph Context:

{graph_context}

Semantic Medical Context:

{semantic_context}

Tasks:

1.Focus only on respiratory reasoning.
2.Analyze cough,asthma,copd and breathing symptoms.
3.Use provided evidence only.
4.Avoid hallucinations.
5.Do not provide final diagnosis.
6.Mention possible respiratory concerns.
"""

    def generate_response(
        self,
        query:str,
        graph_context:List,
        semantic_context:List
    )->str:

        self.validate_inputs(
            query,
            graph_context,
            semantic_context
        )

        prompt=self.build_prompt(
            query,
            graph_context,
            semantic_context
        )

        try:
            response=self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {

                        "role":"system",

                        "content":
                        "You are a senior pulmonologist."

                    },

                    {

                        "role":"user",

                        "content":prompt

                    }

                ],

                temperature=0.2

            )
            return response.choices[
                0
            ].message.content

        except Exception as error:

            self.logger.error(
                error
            )

            return (
                "Unable to generate "
                "pulmonology response."
            )

if __name__=="__main__":
    agent=PulmonologyAgent()

    query="""
    I have breathing difficulty and cough
    """

    graph_context=[

        "breathing difficulty RELATED_TO asthma",

        "cough RELATED_TO bronchitis"

    ]

    semantic_context=[

        "Patient reports persistent cough and shortness of breath."

    ]

    result=agent.generate_response(

        query,
        graph_context,
        semantic_context

    )
    print(result)