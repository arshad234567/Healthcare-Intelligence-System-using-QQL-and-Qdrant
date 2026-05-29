#import libraries
import logging
from typing import Dict,List

#configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

#routing agent
class RoutingAgent:

    CARDIOLOGY_KEYWORDS={
        "chest pain",
        "heart",
        "cardiac",
        "palpitations",
        "hypertension"
    }

    NEUROLOGY_KEYWORDS={
        "dizziness",
        "vertigo",
        "headache",
        "migraine",
        "seizure"
    }

    PULMONOLOGY_KEYWORDS={
        "cough",
        "asthma",
        "copd",
        "bronchitis",
        "breathing difficulty"
    }

    #initialize agent
    def __init__(self):

        self.logger=logging.getLogger(
            self.__class__.__name__
        )

    #validate query
    def validate_query(
        self,
        query:str
    )->None:

        if not isinstance(
            query,
            str
        ):
            raise TypeError(
                "query must be string"
            )

        if not query.strip():
            raise ValueError(
                "query cannot be empty"
            )

    #detect specialists
    def detect_specialists(
        self,
        query:str
    )->List[str]:

        self.validate_query(
            query
        )

        query=query.lower()

        selected_agents=[]

        if any(
            keyword in query
            for keyword in self.CARDIOLOGY_KEYWORDS
        ):

            selected_agents.append(
                "cardiology_agent"
            )

        if any(
            keyword in query
            for keyword in self.NEUROLOGY_KEYWORDS
        ):

            selected_agents.append(
                "neurology_agent"
            )

        if any(
            keyword in query
            for keyword in self.PULMONOLOGY_KEYWORDS
        ):

            selected_agents.append(
                "pulmonology_agent"
            )

        if not selected_agents:

            selected_agents.append(
                "general_physician_agent"
            )

        return selected_agents

    #route query
    def route(
        self,
        query:str
    )->Dict:

        agents=self.detect_specialists(
            query
        )

        return {

            "query":query,

            "selected_agents":agents,

            "agent_count":len(
                agents
            )

        }

#run smoke test
if __name__=="__main__":
    agent=RoutingAgent()
    query="""
    I have chest pain,dizziness and breathing difficulty
    """
    result=agent.route(
        query
    )
    print(
        result
    )