#import libraries
from agent.routing_agent import RoutingAgent

#initialize routing agent
routing_agent=RoutingAgent()

#test cardiology routing
def test_cardiology_routing():

    query="""
    I have chest pain and palpitations
    """

    result=routing_agent.route(
        query
    )

    print("\nTEST CASE 1")
    print("="*80)
    print("CARDIOLOGY ROUTING")
    print("="*80)
    print(result)

#test neurology routing
def test_neurology_routing():

    query="""
    I have dizziness and headache
    """

    result=routing_agent.route(
        query
    )

    print("\nTEST CASE 2")
    print("="*80)
    print("NEUROLOGY ROUTING")
    print("="*80)
    print(result)

#test pulmonology routing
def test_pulmonology_routing():

    query="""
    I have breathing difficulty and cough
    """

    result=routing_agent.route(
        query
    )

    print("\nTEST CASE 3")
    print("="*80)
    print("PULMONOLOGY ROUTING")
    print("="*80)
    print(result)

#test multi specialist routing
def test_multi_specialist_routing():

    query="""
    I have chest pain,dizziness and breathing difficulty
    """

    result=routing_agent.route(
        query
    )

    print("\nTEST CASE 4")
    print("="*80)
    print("MULTI SPECIALIST ROUTING")
    print("="*80)
    print(result)

#test general physician routing
def test_general_routing():

    query="""
    I have fever and body pain
    """

    result=routing_agent.route(
        query
    )

    print("\nTEST CASE 5")
    print("="*80)
    print("GENERAL PHYSICIAN ROUTING")
    print("="*80)
    print(result)

#test empty query validation
def test_empty_query():

    try:

        query=""

        routing_agent.route(
            query
        )

    except Exception as error:

        print("\nTEST CASE 6")
        print("="*80)
        print("EMPTY QUERY VALIDATION")
        print("="*80)
        print(error)

#run all tests
if __name__=="__main__":

    print("\nRUNNING ROUTING AGENT TESTS\n")

    test_cardiology_routing()

    test_neurology_routing()

    test_pulmonology_routing()

    test_multi_specialist_routing()

    test_general_routing()

    test_empty_query()

    print("\nALL ROUTING TESTS COMPLETED")