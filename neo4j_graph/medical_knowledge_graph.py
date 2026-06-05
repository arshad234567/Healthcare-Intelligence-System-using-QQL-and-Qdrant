import logging
from typing import List
from typing import Dict

from neo4j_graph.graph_queries import GraphQueries

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

#medical knowledge graph
class MedicalKnowledgeGraph:

    def __init__(self):

        self.graph_queries=GraphQueries()

        self.logger=logging.getLogger(
            self.__class__.__name__
        )

    #retrieve graph context
    def retrieve_context(
        self,
        symptoms:List[str]
    )->List[Dict]:

        graph_context=[]

        for symptom in symptoms:

            relationships=self.graph_queries.get_related_diseases(
                symptom
            )

            graph_context.extend(
                relationships
            )

        return graph_context

    #convert graph context to text
    def build_context_text(
        self,
        symptoms:List[str]
    )->str:

        graph_context=self.retrieve_context(
            symptoms
        )

        if not graph_context:

            return ""

        context_text=""

        for relation in graph_context:

            context_text+=(

                f"{relation['symptom']} "
                f"RELATED_TO "
                f"{relation['disease']}\n"

            )

        return context_text

    def close(self):

        self.graph_queries.close()

#run smoke test
if __name__=="__main__":

    medical_graph=MedicalKnowledgeGraph()

    symptoms=[

        "chest pain",

        "dizziness"

    ]

    graph_context=medical_graph.build_context_text(
        symptoms
    )

    print(
        graph_context
    )

    medical_graph.close()