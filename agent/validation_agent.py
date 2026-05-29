import os
import re
import json
import logging
from typing import Dict, Any
from groq import Groq

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger=logging.getLogger(__name__)


class ValidationAgent:
    VALID_LEVELS={

        "VERY_HIGH",
        "HIGH",
        "MEDIUM",
        "LOW",
        "VERY_LOW"

    }
    REQUIRED_KEYS={

        "source",
        "relationship",
        "target"

    }

    def __init__(self):

        api_key=os.getenv(
            "GROQ_API_KEY"
        )
        if not api_key:
            raise EnvironmentError(
                "GROQ_API_KEY environment variable not found."
            )
        self.client=Groq(
            api_key=api_key
        )
        self.model=os.getenv(
            "VALIDATION_MODEL",
            "llama-3.3-70b-versatile"
        )
        logger.info(
            "ValidationAgent initialized successfully."
        )

    def validate_input(
        self,
        relation:Dict[str,Any]
    )->None:
        missing_keys=self.REQUIRED_KEYS-relation.keys()
        if missing_keys:
            raise ValueError(
                f"Missing required keys: {missing_keys}"
            )
        for key in self.REQUIRED_KEYS:
            value=str(
                relation[key]
            ).strip()
            if not value:
                raise ValueError(
                    f"{key} cannot be empty."
                )
    def build_prompt(
        self,
        relation:Dict[str,Any]
    )->str:
        return f"""
You are an expert clinical relationship validation agent.

Evaluate the following medical relationship.

Relationship:

Symptom:
{relation['source']}

Relationship:
{relation['relationship']}

Target:
{relation['target']}

Validation Guidelines:

1. Focus on clinically meaningful relationships.
2. Prioritize common medical reasoning.
3. Ignore weak theoretical associations.
4. Reduce hallucination risk.
5. Consider real-world diagnostic usefulness.
6. Use only accepted clinical knowledge.

Clinical Relevance Levels:

VERY_HIGH
HIGH
MEDIUM
LOW
VERY_LOW

Return ONLY JSON.

{{
    "clinical_relevance":"LEVEL",
    "reason":"Short clinical explanation"
}}
"""
    def parse_response(
        self,
        response_text:str
    )->Dict[str,Any]:
        cleaned=re.sub(
            r"```(?:json)?",
            "",
            response_text
        ).strip()

        try:
            data=json.loads(
                cleaned
            )

        except json.JSONDecodeError:
            level_match=re.search(
                r"(VERY_HIGH|VERY_LOW|HIGH|MEDIUM|LOW)",
                cleaned,
                re.IGNORECASE
            )
            if not level_match:
                raise ValueError(
                    f"Unable to parse response:\n{response_text}"
                )
            data={
                "clinical_relevance":
                level_match.group(1).upper(),
                "reason":
                cleaned
            }
        level=str(
            data.get(
                "clinical_relevance",
                "VERY_LOW"
            )
        ).upper()
        if level not in self.VALID_LEVELS:
            logger.warning(
                "Invalid level received: %s",
                level
            )
            level="VERY_LOW"
        return {
            "clinical_relevance":level,
            "reason":data.get(
                "reason",
                "N/A"
            )
        }

    def validate_relationship(
        self,
        relation:Dict[str,Any]
    )->Dict[str,Any]:
        self.validate_input(
            relation
        )
        prompt=self.build_prompt(
            relation
        )
        logger.info(
            "Validating relation: %s -> %s",
            relation["source"],
            relation["target"]
        )
        try:
            response=self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role":"system",
                        "content":
                        """
                        You are a healthcare validation agent.
                        Always return valid JSON.
                        """
                    },
                    {
                        "role":"user",
                        "content":prompt
                    }
                ],
                temperature=0
            )
        except Exception as error:
            logger.error(
                "Groq API error: %s",
                error
            )
            raise RuntimeError(
                str(error)
            )
        raw_response=response.choices[
            0
        ].message.content
        return self.parse_response(
            raw_response
        )

    def classify_relationship(
        self,
        relation:Dict[str,Any]
    )->str:
        try:
            result=self.validate_relationship(
                relation
            )
            return result[
                "clinical_relevance"
            ]
        except Exception as error:
            logger.error(
                "Classification failed: %s",
                error
            )
            return "VERY_LOW"
    def classify_with_reason(
        self,
        relation:Dict[str,Any]
    )->Dict[str,Any]:
        try:
            return self.validate_relationship(
                relation
            )
        except Exception as error:
            logger.error(
                "Validation failed: %s",
                error
            )
            return {
                "clinical_relevance":
                "VERY_LOW",

                "reason":
                str(error)

            }


if __name__=="__main__":
    validation_agent=ValidationAgent()
    sample_relation={
        "source":"chest pain",
        "relationship":"RELATED_TO",
        "target":"myocardial infarction"
    }
    result=validation_agent.classify_with_reason(
        sample_relation
    )
    print(
        json.dumps(
            result,
            indent=4
        )
    )