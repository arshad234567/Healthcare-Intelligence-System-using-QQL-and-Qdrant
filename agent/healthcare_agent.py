#import libraries
import logging
from typing import Dict
from typing import List

from agent.routing_agent import RoutingAgent
from agent.cardiology_agent import CardiologyAgent
from agent.neurology_agent import NeurologyAgent
from agent.pulmonology_agent import PulmonologyAgent
from agent.emergency_detection_agent import EmergencyDetectionAgent
from agent.safety_agent import SafetyAgent

#configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

#healthcare orchestrator agent
class HealthcareAgent:

    #initialize agents
    def __init__(self):

        self.router=RoutingAgent()

        self.cardiology_agent=CardiologyAgent()

        self.neurology_agent=NeurologyAgent()

        self.pulmonology_agent=PulmonologyAgent()

        self.emergency_agent=EmergencyDetectionAgent()

        self.safety_agent=SafetyAgent()

        self.logger=logging.getLogger(
            self.__class__.__name__
        )

    #validate inputs
    def validate_inputs(
        self,
        query:str,
        graph_context:List,
        semantic_context:List
    )->None:

        if not query.strip():

            raise ValueError(
                "query cannot be empty"
            )

        if not isinstance(
            graph_context,
            list
        ):

            raise TypeError(
                "graph_context must be list"
            )

        if not isinstance(
            semantic_context,
            list
        ):

            raise TypeError(
                "semantic_context must be list"
            )

    #run specialist agents
    def run_specialists(
        self,
        selected_agents:List,
        query:str,
        graph_context:List,
        semantic_context:List
    )->Dict:

        specialist_outputs={}

        if "cardiology_agent" in selected_agents:

            specialist_outputs[
                "cardiology"
            ]=self.cardiology_agent.generate_response(

                query,

                graph_context,

                semantic_context

            )

        if "neurology_agent" in selected_agents:

            specialist_outputs[
                "neurology"
            ]=self.neurology_agent.generate_response(

                query,

                graph_context,

                semantic_context

            )

        if "pulmonology_agent" in selected_agents:

            specialist_outputs[
                "pulmonology"
            ]=self.pulmonology_agent.generate_response(

                query,

                graph_context,

                semantic_context

            )

        return specialist_outputs

    #build final response
    def build_final_response(
        self,
        emergency_result:Dict,
        specialist_outputs:Dict
    )->str:

        final_response=""

        final_response+=(
            f"Emergency Level: "
            f"{emergency_result.get('emergency_level')}\n\n"
        )

        final_response+=(
            f"Reason: "
            f"{emergency_result.get('reason')}\n\n"
        )

        for agent_name,response in specialist_outputs.items():

            final_response+=(
                f"\n{agent_name.upper()} "
                f"SPECIALIST OPINION\n"
            )

            final_response+=(
                "-"*50
            )

            final_response+="\n"

            final_response+=response

            final_response+="\n\n"

        return final_response

    #run healthcare pipeline
    def process_query(
        self,
        query:str,
        graph_context:List,
        semantic_context:List
    )->Dict:

        self.validate_inputs(

            query,

            graph_context,

            semantic_context

        )

        emergency_result=self.emergency_agent.detect_emergency(
            query
        )

        routing_result=self.router.route(
            query
        )

        selected_agents=routing_result[
            "selected_agents"
        ]

        specialist_outputs=self.run_specialists(

            selected_agents,

            query,

            graph_context,

            semantic_context

        )

        final_response=self.build_final_response(

            emergency_result,

            specialist_outputs

        )

        safety_result=self.safety_agent.review_response(
            final_response
        )

        if safety_result[
            "decision"
        ]=="UNSAFE":

            final_response=safety_result[
                "corrected_response"
            ]

        return {

            "query":query,

            "emergency_assessment":
            emergency_result,

            "selected_agents":
            selected_agents,

            "specialist_outputs":
            specialist_outputs,

            "safety_review":
            safety_result,

            "final_response":
            final_response

        }

#run smoke test
if __name__=="__main__":

    healthcare_agent=HealthcareAgent()

    query="""
    I have chest pain and dizziness from past 3 hours
    """

    graph_context=[

        "chest pain RELATED_TO cardiac disease",

        "dizziness RELATED_TO bppv",

        "chest pain RELATED_TO myocardial infarction"

    ]

    semantic_context=[

        "Patient reports chest pain and dizziness lasting several hours."

    ]

    result=healthcare_agent.process_query(

        query,

        graph_context,

        semantic_context

    )

    print(
        result["final_response"]
    )