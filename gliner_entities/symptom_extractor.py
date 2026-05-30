import logging
from typing import Dict
from typing import List

from gliner_entities.entity_extractor import EntityExtractor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

#symptom extractor
class SymptomExtractor:

    def __init__(self):

        self.entity_extractor=EntityExtractor()

        self.logger=logging.getLogger(
            self.__class__.__name__
        )

    def extract_symptoms(
        self,
        text:str
    )->List[Dict]:

        entities=self.entity_extractor.extract_entities(
            text
        )

        symptoms=[]

        for entity in entities:

            if entity[
                "entity_label"
            ].lower()=="symptom":

                symptoms.append(
                    entity
                )

        return symptoms

    def extract_symptom_names(
        self,
        text:str
    )->List[str]:

        symptoms=self.extract_symptoms(
            text
        )

        symptom_names=[]

        for symptom in symptoms:
            symptom_names.append(
                symptom[
                    "entity_text"
                ]
            )
        return symptom_names

if __name__=="__main__":

    extractor=SymptomExtractor()

    query="""
    I have chest pain,dizziness and breathing difficulty
    """

    symptoms=extractor.extract_symptom_names(query)

    print(symptoms)