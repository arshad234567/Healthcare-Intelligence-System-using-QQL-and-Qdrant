import logging
from typing import List
from typing import Dict

from neo4j_graph.neo4j_client import Neo4jClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class GraphQueries:

    def __init__(self):
        self.neo4j_client=Neo4jClient()
        self.logger=logging.getLogger(
            self.__class__.__name__
        )

    def get_related_diseases(
        self,
        symptom:str
    )->List[Dict]:

        query="""

        MATCH
        (s:Symptom)-[:RELATED_TO]->(d:Disease)

        WHERE
        toLower(s.name)=toLower($symptom)

        RETURN
        s.name AS symptom,
        d.name AS disease

        """

        records=self.neo4j_client.execute_query(
            query,
            {
                "symptom":symptom
            }
        )

        results=[]

        for record in records:
            results.append({
                "symptom":
                record["symptom"],

                "disease":
                record["disease"]

            })

        return results

    def get_related_symptoms(
        self,
        disease:str
    )->List[Dict]:

        query="""

        MATCH
        (s:Symptom)-[:RELATED_TO]->(d:Disease)

        WHERE
        toLower(d.name)=toLower($disease)

        RETURN
        d.name AS disease,
        s.name AS symptom

        """

        records=self.neo4j_client.execute_query(
            query,
            {
                "disease":disease
            }
        )

        results=[]

        for record in records:
            results.append({

                "disease":
                record["disease"],

                "symptom":
                record["symptom"]
            })
        return results

    def retrieve_graph_context(
        self,
        symptoms:List[str]
    )->List[Dict]:

        graph_context=[]

        for symptom in symptoms:
            diseases=self.get_related_diseases(
                symptom
            )

            graph_context.extend(
                diseases
            )
        return graph_context

    def close(self):
        self.neo4j_client.close()

if __name__=="__main__":
    graph_queries=GraphQueries()
    result=graph_queries.get_related_diseases(
        "chest pain"
    )
    print(
        result
    )
    graph_queries.close()