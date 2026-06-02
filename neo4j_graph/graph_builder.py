import logging
from typing import List
from typing import Dict

from neo4j_graph.neo4j_client import Neo4jClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class GraphBuilder:

    def __init__(self):

        self.neo4j_client=Neo4jClient()

        self.logger=logging.getLogger(
            self.__class__.__name__
        )

    #create relationship
    def create_relationship(
        self,
        symptom:str,
        disease:str
    )->None:

        query="""

        MERGE (s:Symptom {
            name:$symptom
        })

        MERGE (d:Disease {
            name:$disease
        })

        MERGE (s)-[:RELATED_TO]->(d)

        """

        parameters={

            "symptom":symptom,

            "disease":disease

        }

        self.neo4j_client.execute_query(

            query,

            parameters

        )

    def build_graph(
        self,
        relationships:List[Dict]
    )->None:
        inserted_count=0

        for relation in relationships:
            try:
                self.create_relationship(
                    relation[
                        "symptom"
                    ],
                    relation[
                        "disease"
                    ]
                )
                inserted_count+=1
            except Exception as error:
                self.logger.error(
                    error
                )
        self.logger.info(
            f"{inserted_count} relationships inserted"

        )
    def close(self):

        self.neo4j_client.close()

#run smoke test
if __name__=="__main__":
    sample_relationships=[
        {

            "symptom":
            "chest pain",
            "disease":
            "myocardial infarction"

        },
        {

            "symptom":
            "dizziness",
            "disease":
            "bppv"

        },
        {

            "symptom":
            "breathing difficulty",
            "disease":
            "asthma"

        }
    ]
    graph_builder=GraphBuilder()
    graph_builder.build_graph(
        sample_relationships
    )
    graph_builder.close()