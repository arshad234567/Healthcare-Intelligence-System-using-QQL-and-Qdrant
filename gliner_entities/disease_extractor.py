#import libraries
import logging
from typing import Dict
from typing import List

from gliner_entities.entity_extractor import EntityExtractor

#configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class DiseaseExtractor:

    #initialize extractor
    def __init__(self):

        self.entity_extractor=EntityExtractor()

        self.logger=logging.getLogger(
            self.__class__.__name__
        )

    #extract diseases
    def extract_diseases(
        self,
        text:str
    )->List[Dict]:

        entities=self.entity_extractor.extract_entities(
            text
        )

        diseases=[]

        for entity in entities:

            if entity[
                "entity_label"
            ].lower() in [

                "disease",

                "medical_condition"

            ]:

                diseases.append(
                    entity
                )

        return diseases

    #extract disease names only
    def extract_disease_names(
        self,
        text:str
    )->List[str]:

        diseases=self.extract_diseases(
            text
        )

        disease_names=[]

        for disease in diseases:

            disease_names.append(

                disease[
                    "entity_text"
                ]

            )

        return disease_names

if __name__=="__main__":

    extractor=DiseaseExtractor()

    query="""
    Patient has diabetes,hypertension and chest pain
    """

    diseases=extractor.extract_disease_names(
        query
    )

    print(
        diseases
    )