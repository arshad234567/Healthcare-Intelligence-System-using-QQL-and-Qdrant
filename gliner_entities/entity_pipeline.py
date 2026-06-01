import logging
from typing import Dict

from gliner_entities.entity_extractor import EntityExtractor
from gliner_entities.symptom_extractor import SymptomExtractor
from gliner_entities.disease_extractor import DiseaseExtractor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class EntityPipeline:

    def __init__(self):

        self.entity_extractor=EntityExtractor()
        self.symptom_extractor=SymptomExtractor()
        self.disease_extractor=DiseaseExtractor()

        self.logger=logging.getLogger(
            self.__class__.__name__
        )

    def process(
        self,
        text:str
    )->Dict:

        entities=self.entity_extractor.extract_entities(
            text
        )
        symptoms=self.symptom_extractor.extract_symptoms(
            text
        )
        diseases=self.disease_extractor.extract_diseases(
            text
        )

        return {
            "total_entities":
            len(
                entities
            ),
            "entities":
            entities,
            "symptoms":
            symptoms,
            "diseases":
            diseases
        }

#run smoke test
if __name__=="__main__":
    pipeline=EntityPipeline()
    query="""
    I have chest pain,dizziness,breathing difficulty and diabetes
    """
    result=pipeline.process(
        query
    )
    print(result)