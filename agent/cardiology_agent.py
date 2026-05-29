#import libraries
import os
import logging
from typing import Dict,List

from groq import Groq

#configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

#cardiology agent
class CardiologyAgent:

    #initialize agent
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
            "CARDIOLOGY_MODEL",
            "llama-3.3-70b-versatile"
        )

        self.logger=logging.getLogger(
            self.__class__.__name__
        )

    #validate inputs
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

    #build cardiology prompt
    def build_prompt(
        self,
        query:str,
        graph_context:List,
        semantic_context:List
    )->str:

        return f"""
You are an expert cardiology specialist.

User Query:

{query}

Validated Graph Context:

{graph_context}

Semantic Medical Context:

{semantic_context}

Tasks:

1.Focus only on heart related reasoning.
2.Analyze chest pain and cardiac symptoms.
3.Use provided evidence only.
4.Avoid hallucinations.
5.Do not provide final diagnosis.
6.Mention possible cardiac concerns.
"""

    #generate cardiology response
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
                        "You are a senior cardiologist."

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
                "cardiology response."
            )

#run smoke test
if __name__=="__main__":

    agent=CardiologyAgent()

    query="""
    I have chest pain and palpitations
    """

    graph_context=[

        "chest pain RELATED_TO cardiac disease",
        "palpitations RELATED_TO arrhythmia"

    ]

    semantic_context=[

        "Patient reports chest discomfort during exercise."

    ]

    result=agent.generate_response(

        query,

        graph_context,

        semantic_context

    )

    print(
        result
    )