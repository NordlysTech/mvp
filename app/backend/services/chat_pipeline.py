from services.S2_ClassifierLogic import Classifier
from services.S2_ClassifierLogic import PlannerAgent
from services.S4_SolverAgents import SuperSolverAgent

from services.llm_utils import get_json_from_response
import json


def get_answer(user_input) :

    # Initialize the classifier and classify the query
    classifier_model = Classifier()
    response = classifier_model.classify_query(user_input)
    print("\nRaw Classifier Response:\n")
    print(response)


    #response = json.dumps(response)
    classification_result = get_json_from_response(response)
    print("type(classification_result) : ",type(classification_result))
    # Parse the JSON response from the classifier, handle potential errors if JSON is not returned
    try:
        # classification_result = json.loads(response)
        print("\nClassification Result:\n")
        print(json.dumps(classification_result, indent=4))
    except json.JSONDecodeError:
        print("Error: The classifier returned an invalid JSON string. Please check the prompt or LLM output")
        return


    # Initialize planner agents based on the classification result
    planner_agents = []

    # Error handling for agent_allocation
    if (
            "agent_allocation" in classification_result and
            "selected_agents" in classification_result["agent_allocation"] and
            isinstance(classification_result["agent_allocation"]["selected_agents"], list)
        ):
        for agent_data in classification_result["agent_allocation"]["selected_agents"]:
            planner_agents.append(PlannerAgent(agent_data["agent_name"],agent_data["role"]))
    else:
        print("Error: The 'agent_allocation' structure or 'selected_agents' is missing or has incorrect type in the classification result. Check LLM output or your classifier prompt")
        return

    # Generate plans for each selected agent
    agent_plans = {}
    for planner in planner_agents:
        agent_plans[planner.agent_name] = planner.create_plan(
            classification_result["query_analysis"],
            classification_result["agent_allocation"]
        )
    print("\nIndividual Agent Plans:\n")
    for agent, plan in agent_plans.items():
            print(f"Agent: {agent}\nPlan:\n {plan}\n")


    # Execute the plans and retrieve evidence
    retrieved_evidence = {}
    for planner in planner_agents:
        retrieved_evidence[planner.agent_name] = planner.execute_plan(agent_plans[planner.agent_name])

    print("\nRetrieved Evidence:\n")
    for agent, evidence in retrieved_evidence.items():
            print(f"Agent: {agent}\nEvidence:\n {json.dumps(evidence, indent=4)}\n")

    # Initialize and execute the Super Solver agent
    super_solver = SuperSolverAgent("Super Solver", "Comprehensive Engineering Analysis")

    # Collect all the plans and retrieved evidence
    all_plans = agent_plans
    all_evidence = retrieved_evidence

    # Execute the super solver agent to generate the final report
    final_report = super_solver.execute_plan(
        "", # No plan is needed for the SuperSolver
        all_evidence, # Pass all the retrieved evidence
        user_input,  # Pass the original user input query
        classification_result["agent_allocation"], # Pass the classification for the solver to extract the other agents
    )
    
    title = "TEST"
    assistant_answer = final_report['report']
    
    return title, assistant_answer 

