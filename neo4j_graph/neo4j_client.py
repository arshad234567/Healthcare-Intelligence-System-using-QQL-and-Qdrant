import logging
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

#neo4j_graph client
class Neo4jClient:

    #initialize client
    def __init__(self):

        self.uri=os.getenv(
            "NEO4J_URI"
        )

        self.username=os.getenv(
            "NEO4J_USERNAME"
        )

        self.password=os.getenv(
            "NEO4J_PASSWORD"
        )

        self.driver=GraphDatabase.driver(

            self.uri,

            auth=(
                self.username,
                self.password
            )

        )

        self.logger=logging.getLogger(
            self.__class__.__name__
        )

        self.logger.info(
            "Neo4j client initialized successfully"
        )

    #get session
    def get_session(self):

        return self.driver.session()

    #test connection
    def test_connection(
        self
    )->bool:

        try:

            with self.driver.session() as session:

                result=session.run(
                    """
                    RETURN 'Neo4j Connected'
                    AS message
                    """
                )

                record=result.single()

                self.logger.info(
                    record["message"]
                )

                return True

        except Exception as error:

            self.logger.error(
                error
            )

            return False

    #execute query
    def execute_query(
        self,
        query:str,
        parameters:dict=None
    ):

        try:

            with self.driver.session() as session:

                result=session.run(

                    query,

                    parameters or {}

                )

                return list(
                    result
                )

        except Exception as error:

            self.logger.error(
                error
            )

            return []

    #close connection
    def close(self):

        self.driver.close()

        self.logger.info(
            "Neo4j connection closed"
        )

#run smoke test
if __name__=="__main__":

    client=Neo4jClient()

    connection_status=client.test_connection()

    print(
        "\nConnection Status:",
        connection_status
    )

    client.close()