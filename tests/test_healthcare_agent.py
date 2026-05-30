#import libraries
import os
from dotenv import load_dotenv

from agent.healthcare_agent import HealthcareAgent

#load environment variables
load_dotenv()

#initialize healthcare agent
healthcare_agent=HealthcareAgent()

#test case 1
def test_cardiology_case():

    query="""
    I have chest pain and palpitations
    """

    graph_context=[

        "chest pain RELATED_TO myocardial infarction",

        "palpitations RELATED_TO arrhythmia"

    ]

    semantic_context=[

        "Patient reports chest discomfort during physical activity."

    ]

    result=healthcare_agent.process_query(

        query,

        graph_context,

        semantic_context

    )

    print("\nTEST CASE 1")
    print("="*80)
    print(result["final_response"])
    print("="*80)

#test case 2
def test_neurology_case():

    query="""
    I have dizziness and headache
    """

    graph_context=[

        "dizziness RELATED_TO bppv",

        "headache RELATED_TO migraine"

    ]

    semantic_context=[

        "Patient reports dizziness while walking."

    ]

    result=healthcare_agent.process_query(

        query,

        graph_context,

        semantic_context

    )

    print("\nTEST CASE 2")
    print("="*80)
    print(result["final_response"])
    print("="*80)

#test case 3
def test_pulmonology_case():

    query="""
    I have breathing difficulty and cough
    """

    graph_context=[

        "breathing difficulty RELATED_TO asthma",

        "cough RELATED_TO bronchitis"

    ]

    semantic_context=[

        "Patient reports persistent cough and wheezing."

    ]

    result=healthcare_agent.process_query(

        query,

        graph_context,

        semantic_context

    )

    print("\nTEST CASE 3")
    print("="*80)
    print(result["final_response"])
    print("="*80)

#test case 4
def test_multi_specialist_case():

    query="""
    I have chest pain,dizziness and breathing difficulty
    """

    graph_context=[

        "chest pain RELATED_TO cardiac disease",

        "dizziness RELATED_TO bppv",

        "breathing difficulty RELATED_TO asthma"

    ]

    semantic_context=[

        "Patient reports chest pain,dizziness and breathing issues."

    ]

    result=healthcare_agent.process_query(

        query,

        graph_context,

        semantic_context

    )

    print("\nTEST CASE 4")
    print("="*80)
    print(result["final_response"])
    print("="*80)

#test case 5
def test_emergency_case():

    query="""
    I have severe chest pain radiating to left arm with breathing difficulty
    """

    graph_context=[

        "chest pain RELATED_TO myocardial infarction"

    ]

    semantic_context=[

        "Patient reports severe chest pain lasting 2 hours."

    ]

    result=healthcare_agent.process_query(

        query,

        graph_context,

        semantic_context

    )

    print("\nTEST CASE 5")
    print("="*80)
    print(result["emergency_assessment"])
    print("="*80)
    print(result["final_response"])
    print("="*80)

#run all tests
if __name__=="__main__":

    print("\nRUNNING HEALTHCARE AGENT TESTS\n")

    test_cardiology_case()

    test_neurology_case()

    test_pulmonology_case()

    test_multi_specialist_case()

    test_emergency_case()

    print("\nALL TESTS COMPLETED SUCCESSFULLY")