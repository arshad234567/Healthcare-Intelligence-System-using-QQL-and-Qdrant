#import libraries
import logging
from typing import Dict
from typing import List
from gliner import GLiNER


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


class EntityExtractor:

    def __init__(self):
        self.labels=[

            "symptom",

            "disease",

            "medication",

            "body_part",

            "medical_condition",

            "treatment"

        ]

        self.model=GLiNER.from_pretrained(
            "urchade/gliner_medium-v2.1"
        )

        self.logger=logging.getLogger(
            self.__class__.__name__
        )

        self.logger.info(
            "GLiNER model loaded successfully"
        )

    def validate_text(
        self,
        text:str
    )->None:

        if not isinstance(
            text,
            str
        ):

            raise TypeError(
                "text must be string"
            )

        if not text.strip():

            raise ValueError(
                "text cannot be empty"
            )



    def extract_entities(
        self,
        text:str
    )->List[Dict]:

        self.validate_text(
            text
        )

        try:
            entities=self.model.predict_entities(text,self.labels)

            extracted=[]

            for entity in entities:
                extracted.append({

                    "entity_text":
                    entity["text"],

                    "entity_label":
                    entity["label"],

                    "confidence":
                    round(
                        entity["score"],
                        4
                    )
                })
                return extracted

        except Exception as error:
            self.logger.error(
                error
            )

            return []

if __name__=="__main__":
    extractor=EntityExtractor()

    query="""
    I have chest pain,dizziness and breathing difficulty
    """

    result=extractor.extract_entities(query)
    print(result)