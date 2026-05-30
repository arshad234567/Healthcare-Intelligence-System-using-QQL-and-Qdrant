import os
import logging
from typing import Dict
from groq import Groq

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class EmergencyDetectionAgent:

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
            "EMERGENCY_MODEL",
            "llama-3.3-70b-versatile"
        )

        self.logger=logging.getLogger(
            self.__class__.__name__
        )

    def validate_query(
        self,
        query:str
    )->None:

        if not isinstance(
            query,
            str
        ):

            raise TypeError(
                "query must be string"
            )

        if not query.strip():

            raise ValueError(
                "query cannot be empty"
            )

    def build_prompt(
        self,
        query:str
    )->str:

        return f"""
You are an emergency medical triage specialist.

User Query:

{query}

Tasks:

1.Analyze symptoms carefully.
2.Identify emergency warning signs.
3.Classify urgency level.

Emergency Levels:

EMERGENCY
URGENT
NON_URGENT

Examples:

Chest pain with left arm pain = EMERGENCY

Loss of consciousness = EMERGENCY

Difficulty breathing with severe distress = EMERGENCY

High fever for several days = URGENT

Mild headache = NON_URGENT

Return only JSON.

{{
    "emergency_level":"EMERGENCY|URGENT|NON_URGENT",
    "reason":"short explanation"
}}
"""

    #parse response
    def parse_response(
        self,
        response_text:str
    )->Dict:

        import json
        import re

        cleaned=re.sub(
            r"```(?:json)?",
            "",
            response_text
        ).strip()

        try:

            return json.loads(
                cleaned
            )

        except Exception:

            return {

                "emergency_level":
                "URGENT",

                "reason":
                "unable to parse response"

            }

    #detect emergency
    def detect_emergency(
        self,
        query:str
    )->Dict:

        self.validate_query(
            query
        )

        prompt=self.build_prompt(
            query
        )

        try:

            response=self.client.chat.completions.create(

                model=self.model,

                messages=[

                    {

                        "role":"system",

                        "content":
                        "You are an emergency medical triage expert."

                    },

                    {

                        "role":"user",

                        "content":prompt

                    }

                ],

                temperature=0

            )

            result=response.choices[
                0
            ].message.content

            return self.parse_response(
                result
            )

        except Exception as error:

            self.logger.error(
                error
            )

            return {

                "emergency_level":
                "URGENT",

                "reason":
                str(error)

            }

if __name__=="__main__":

    agent=EmergencyDetectionAgent()

    query="""
    I have severe chest pain spreading to my left arm and difficulty breathing
    """

    result=agent.detect_emergency(query)

    print(result)