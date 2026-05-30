import os
import json
import logging
from typing import Dict
from groq import Groq

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class SafetyAgent:

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
            "SAFETY_MODEL",
            "llama-3.3-70b-versatile"
        )

        self.logger=logging.getLogger(
            self.__class__.__name__
        )

    def validate_response(
        self,
        response:str
    )->None:

        if not isinstance(
            response,
            str
        ):

            raise TypeError(
                "response must be string"
            )

        if not response.strip():

            raise ValueError(
                "response cannot be empty"
            )

    def build_prompt(
        self,
        response:str
    )->str:

        return f"""
You are a healthcare safety review agent.

Healthcare Response:

{response}

Tasks:

1.Check for hallucinations.
2.Check for dangerous medical advice.
3.Check for unsupported diagnoses.
4.Check for false certainty.
5.Check for unsafe recommendations.
6.Check for misinformation.

Safety Decision:

SAFE
UNSAFE

Return only JSON.

{{
    "decision":"SAFE|UNSAFE",
    "reason":"short explanation",
    "corrected_response":"safe version if needed"
}}
"""

    def parse_response(
        self,
        response_text:str
    )->Dict:

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

                "decision":"UNSAFE",

                "reason":"unable to parse safety response",

                "corrected_response":"Please consult a qualified healthcare professional."

            }

    def review_response(
        self,
        response:str
    )->Dict:

        self.validate_response(
            response
        )

        prompt=self.build_prompt(
            response
        )

        try:

            result=self.client.chat.completions.create(

                model=self.model,

                messages=[

                    {

                        "role":"system",

                        "content":
                        "You are a healthcare safety reviewer."

                    },

                    {

                        "role":"user",

                        "content":prompt

                    }

                ],

                temperature=0

            )

            output=result.choices[
                0
            ].message.content

            return self.parse_response(
                output
            )

        except Exception as error:

            self.logger.error(
                error
            )

            return {

                "decision":"UNSAFE",

                "reason":str(error),

                "corrected_response":"Please consult a qualified healthcare professional."

            }

if __name__=="__main__":

    agent=SafetyAgent()

    response="""
    You definitely have a heart attack and should take medication immediately.
    """

    result=agent.review_response(
        response
    )

    print(
        result
    )