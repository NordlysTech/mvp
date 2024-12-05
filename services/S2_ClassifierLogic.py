import openai
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class Classifier:
    def __init__(self):
        """
        Initialize the Classifier model.
        """
        self.model = ChatOpenAI(
            temperature=0.2,
            model="gpt-3.5-turbo-16k",
            max_tokens=2000,
            openai_api_key=openai.api_key,
        )

    def classify_query(self, user_query: str):
        """
        Process the user query using the Classifier Agent Prompt with few-shot learning examples.
        """
        # Few-shot learning examples
        example_1 = {
            "input_query": "Develop an improved separation technique for reducing hydrocarbon content in produced water from our offshore platform to meet strict environmental discharge regulations.",
            "analysis": {
                "query_analysis": {
                    "original_query": "Develop an improved separation technique for reducing hydrocarbon content in produced water from our offshore platform to meet strict environmental discharge regulations.",
                    "expanded_query": "Design an advanced water treatment process to minimize hydrocarbon contamination in offshore platform produced water, ensuring compliance with stringent environmental regulations.",
                    "complexity_level": "medium",
                    "primary_domain": "Produced Water Treatment",
                    "secondary_domains": ["Environmental Compliance", "Separation Technology"]
                },
                "agent_allocation": {
                    "selected_agents": [
                        {
                            "agent_name": "Separation Technologist",
                            "role": "Primary separation process design",
                            "interaction_type": "lead"
                        },
                        {
                            "agent_name": "Thermodynamics Expert",
                            "role": "Phase separation mechanism optimization",
                            "interaction_type": "collaborative"
                        },
                        {
                            "agent_name": "Safety Expert",
                            "role": "Regulatory compliance verification",
                            "interaction_type": "advisory"
                        }
                    ],
                    "communication_strategy": {
                        "primary_communication_agent": "Separation Technologist",
                        "information_flow": "Iterative compliance and performance optimization",
                        "collaboration_protocol": "Continuous standards and technical parameter alignment"
                    }
                },
                "clarification_questions": [
                    "What are the current hydrocarbon concentration levels in the produced water?",
                    "What specific environmental discharge regulations need to be met?",
                    "Are there any constraints on separation technology implementation?"
                ]
            }
        }

        example_2 = {
            "input_query": "We're experiencing unexpected performance degradation in our continuous distillation column for petrochemical processing. The column efficiency has dropped by 15%, and we're seeing unusual temperature profiles.",
            "analysis": {
                "query_analysis": {
                    "original_query": "We're experiencing unexpected performance degradation in our continuous distillation column for petrochemical processing. The column efficiency has dropped by 15%, and we're seeing unusual temperature profiles.",
                    "expanded_query": "Investigate and diagnose the root causes of performance decline in a petrochemical continuous distillation column, focusing on efficiency loss and abnormal temperature distributions.",
                    "complexity_level": "medium",
                    "primary_domain": "Industrial Distillation Troubleshooting",
                    "secondary_domains": ["Process Control", "Thermodynamic Analysis"]
                },
                "agent_allocation": {
                    "selected_agents": [
                        {
                            "agent_name": "Troubleshooter",
                            "role": "Root cause investigation",
                            "interaction_type": "lead"
                        },
                        {
                            "agent_name": "Dynamics & Control Expert",
                            "role": "System dynamics analysis",
                            "interaction_type": "collaborative"
                        },
                        {
                            "agent_name": "Thermodynamics Expert",
                            "role": "Temperature profile investigation",
                            "interaction_type": "collaborative"
                        }
                    ],
                    "communication_strategy": {
                        "primary_communication_agent": "Troubleshooter",
                        "information_flow": "Diagnostic cross-referencing and hypothesis testing",
                        "collaboration_protocol": "Sequential problem decomposition and integrated analysis"
                    }
                },
                "clarification_questions": [
                    "When did the performance degradation first become noticeable?",
                    "Have there been any recent changes in feed composition or operating conditions?",
                    "Can you provide detailed temperature profiles from before and after the performance drop?"
                ]
            }
        }

        # Classifier Agent Prompt with few-shot learning examples
        classifier_agent_prompt = f"""
        You are the Classifier and Allocator Agent for a superhuman chemical separation processes AI engineering ecosystem. Your mission is to intelligently process and transform chemical engineering queries into actionable, multi-agent intelligence.

        FEW-SHOT LEARNING EXAMPLES:

        EXAMPLE 1:
        Input Query: {example_1['input_query']}
        Expected Analysis:
        {example_1['analysis']}

        EXAMPLE 2:
        Input Query: {example_2['input_query']}
        Expected Analysis:
        {example_2['analysis']}

        CORE PURPOSE:
        Transform raw user queries from chemical and process engineers into structured, actionable intelligence that can be efficiently processed by a specialized multi-agent system.

        AVAILABLE AGENT POOL:
        1. Separation Technologist
        2. Thermodynamics Expert
        3. Troubleshooter
        4. Dynamics & Control Expert
        5. Safety Expert
        6. Mathematical Solver (Analytical/Numerical)

        CORE RESPONSIBILITIES:
        1. Query Processing and Understanding
        - Perform deep semantic analysis of input queries
        - Identify explicit and implicit requirements
        - Extract technical nuances and contextual subtleties
        - Recognize potential interdisciplinary aspects of the problem

        2. Query Expansion and Clarification
        - If the initial query is ambiguous, generate clarifying questions
        - Infer potential hidden requirements or constraints
        - Develop a comprehensive understanding that goes beyond surface-level interpretation

        3. Systematic Classification
        - Create a multi-dimensional classification framework that captures:
        * Primary domain
        * Complexity level
        * Required computational and theoretical approaches
        * Potential interdisciplinary intersections

        4. Agent Selection and Dynamic Allocation
        - Maintain a comprehensive understanding of available agent capabilities
        - Develop a dynamic, intelligent agent selection algorithm
        - Determine optimal agent combinations and interaction protocols
        - Predict potential communication pathways and collaborative dynamics

        INPUT QUERY:
        {user_query}

        OUTPUT REQUIREMENTS:
        Generate a structured JSON response containing:
        {{
            "query_analysis": {{
                "original_query": "{user_query}",
                "expanded_query": "<detailed, clarified query>",
                "complexity_level": "<low/medium/high/advanced>",
                "primary_domain": "<specific domain classification>",
                "secondary_domains": ["<potential related domains>"]
            }},
            "agent_allocation": {{
                "selected_agents": [
                    {{
                        "agent_name": "<agent identifier>",
                        "role": "<specific contribution>",
                        "interaction_type": "<independent/collaborative>"
                    }}
                ],
                "communication_strategy": {{
                    "primary_communication_agent": "<lead agent>",
                    "information_flow": "<description of knowledge transfer>",
                    "collaboration_protocol": "<specific interaction mechanism>"
                }}
            }},
            "clarification_questions": [
                "<potential questions to refine understanding>"
            ]
        }}
        """
        # Send the prompt to the model
        response = self.model.predict(classifier_agent_prompt)
        return response


def main():
    """
    Main function to interact with the classifier.
    """
    print("Please provide your query:")
    user_input = input().strip()

    # Initialize the classifier and classify the query
    classifier_model = Classifier()
    response = classifier_model.classify_query(user_input)

    # Print the response
    print("\nResponse:\n")
    print(response)


if __name__ == "__main__":
    main()
