import openai
import os
from dotenv import load_dotenv

import json
import re
from S3_SupportAgents import KnowledgeRetriever, EquationsFormulasRetriever, PhysChemPropertiesRetriever, IndustryStandardsRetriever
from S4_SolverAgents import SuperSolverAgent
from llm_utils import instantiate_llm_model, get_json_from_response
from config_utils import load_config, get_config

config_path = "config.yaml"
config = load_config(config_path)

print("config : ",config)

    
load_dotenv()

model_to_use = get_config(config, "llms", "llm_name")

class Classifier:
    def __init__(self):
            """
            Initialize the Classifier model.
            """
            self.model = instantiate_llm_model(model_to_use, temperature=0.2, max_tokens=2000)
            
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

        example_3 = {
            "input_query": "We've got these massive geothermal brine pools in Nevada, and our management is pushing hard to monetize the lithium. Current extraction methods are a money pit. Any ideas on a novel approach that doesn't require crazy expensive infrastructure?",
            "analysis": {
                "query_analysis": {
                    "original_query": "We've got these massive geothermal brine pools in Nevada, and our management is pushing hard to monetize the lithium. Current extraction methods are a money pit. Any ideas on a novel approach that doesn't require crazy expensive infrastructure?",
                    "expanded_query": "Investigate and generate a technical benchmark report for a cost-effective lithium isolation process from high-salinity geothermal fluid with minimal capital investment",
                    "complexity_level": "advanced",
                    "primary_domain": "Critical Metal Recovery",
                    "secondary_domains": ["Resource Extraction", "Economic Process Design"]
                },
                "agent_allocation": {
                    "selected_agents": [
                        {
                            "agent_name": "Separation Technologist",
                            "role": "Extraction process design",
                            "interaction_type": "lead"
                        },
                        {
                            "agent_name": "Thermodynamics Expert",
                            "role": "Ionic interaction mechanism analysis",
                            "interaction_type": "collaborative"
                        },
                        {
                            "agent_name": "Mathematical Solver",
                            "role": "Economic feasibility modeling",
                            "interaction_type": "advisory"
                        }
                    ],
                    "communication_strategy": {
                        "primary_communication_agent": "Separation Technologist",
                        "information_flow": "Lithium isolation mechanism development",
                        "collaboration_protocol": "Integrated extraction strategy refinement"
                    }
                },
                "clarification_questions": [
                    "What's the current lithium concentration in your brine?",
                    "What extraction methods have you already tried?"
                    "Are there any constraints on the process design or technology?"
                ]
            }
        }

        example_4 = {
            "input_query": "Hey team, we're struggling with CO2 capture in our power plant's flue gas system. I've heard about new membrane technologies - can you recommend a material that might bump up our selectivity without killing our flux rate?",
            "analysis": {
                "query_analysis": {
                    "original_query": "Hey team, we're struggling with CO2 capture in our power plant's flue gas system. I've heard about new membrane technologies - can anyone recommend a material that might bump up our selectivity without killing our flux rate?",
                    "expanded_query": "Identify high-performance membrane material for carbon dioxide selective separation with balanced permeation characteristics",
                    "complexity_level": "intermediate",
                    "primary_domain": "Membrane Separation Technology",
                    "secondary_domains": ["Gas Purification", "Energy Engineering"]
                },
                "agent_allocation": {
                    "selected_agents": [
                        {
                            "agent_name": "Separation Technologist",
                            "role": "Membrane material screening",
                            "interaction_type": "lead"
                        },
                        {
                            "agent_name": "Thermodynamics Expert",
                            "role": "Molecular transport mechanism validation",
                            "interaction_type": "collaborative"
                        }
                    ],
                    "communication_strategy": {
                        "primary_communication_agent": "Separation Technologist",
                        "information_flow": "Membrane performance characterization",
                        "collaboration_protocol": "Direct material recommendation"
                    }
                },
                "clarification_questions": [
                    "What's the typical temperature range of your flue gas and what's its composition?",
                    "Can you share your current membrane technology's properties and its performance metrics?"
                    "Do you have any sort of limitations on the material selection?"
                ]
            }
        }

        example_5 = {
            "input_query": "I am working on designing a separation process for a ternary mixture, I would like the equilibrium data of water-MEA-CO2.",
            "analysis": {
                "query_analysis": {
                    "original_query": "I am working on designing a separation process for a ternary mixture, I would like the equilibrium data of water-MEA-CO2.",
                    "expanded_query": "Obtain the equilibrium data for the system a ternary mixture of water, MEA, and CO2.",
                    "complexity_level": "low",
                    "primary_domain": "Thermodynamic Equilibrium Data Retrieval",
                    "secondary_domains": ["Ternary Mixture Thermodynamics", "Phase Equilibrium"]
                },
                "agent_allocation": {
                    "selected_agents": [
                        {
                            "agent_name": "Thermodynamics Expert",
                            "role": "Equilibrium data retrieval",
                            "interaction_type": "lead"
                        }
                    ],
                },
                "clarification_questions": [
                    "What are the concentrations of water, MEA, and CO2 in the ternary mixture?",
                    "What are the operating conditions (temperature, pressure) for the separation process?"
                ]
            }
        }

        example_6 = {
            "input_query": "Provide the key design steps for a flash separator for crude oil prior to being introduced to the refining process. Also please provide the control of this unit.",
            "analysis": {
                "query_analysis": {
                    "original_query": "Provide the key design steps for a flash separator for crude oil prior to being introduced to the refining process. Also please provide the control of this unit.",
                    "expanded_query": "Provide a detailed explanation of the key design steps involved in designing a flash separator for crude oil prior to its introduction to the refining process. Additionally, please provide information on the control system used for this unit.",
                    "complexity_level": "medium",
                    "primary_domain": "Separation Technology",
                    "secondary_domains": [
                        "Process Design",
                        "Process Control"
                    ]
                },
                "agent_allocation": {
                    "selected_agents": [
                        {
                            "agent_name": "Separation Technologist",
                            "role": "Flash separator design",
                            "interaction_type": "lead"
                        },
                        {
                            "agent_name": "Dynamics & Control Expert",
                            "role": "Process control system design",
                            "interaction_type": "collaborative"
                        }
                    ],
                    "communication_strategy": {
                        "primary_communication_agent": "Separation Technologist",
                        "information_flow": "Design specifications and requirements",
                        "collaboration_protocol": "Continuous feedback and integration"
                    }
                },
                "clarification_questions": [
                    "What are the specific properties and characteristics of the crude oil being processed?",
                    "What are the desired separation performance targets for the flash separator?",
                    "Are there any specific control requirements or constraints for the unit?"
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

        EXAMPLE 3:
        Input Query: {example_3['input_query']}
        Expected Analysis:
        {example_3['analysis']}

        EXAMPLE 4:
        Input Query: {example_4['input_query']}
        Expected Analysis:
        {example_4['analysis']}

        EXAMPLE 5:
        Input Query: {example_5['input_query']} 
        Expected Analysis:
        {example_5['analysis']}

        EXAMPLE 6:
        Input Query: {example_6['input_query']} 
        Expected Analysis:
        {example_6['analysis']}
        

        
        CORE PURPOSE:
        Transform raw user queries from chemical and process engineers into structured, actionable intelligence that can be efficiently processed by a specialized multi-agent system.

        AVAILABLE AGENT POOL:
        1. {"Separation Technologist"}: An expert with multi-level knowledge of separation processes, including different types of separation processes and their design, optimization, and implementation.
        2. {"Thermodynamics Expert"}: A specialist in thermodynamics, with expertise in vast fields of thermodynamics, such as heat transfer, mass transfer, phase changes, phase equilibria, temperature profiles, etc.
        3. {"Troubleshooter"}: An expert in process troubleshooting, with a deep understanding of the root causes of process failures and the ability to identify and diagnose both simple and complex issues.
        4. {"Dynamics & Control Expert"}: An expert in process control and dynamics, with a strong understanding of the dynamic behavior of processes and the ability to design and implement effective control strategies.
        5. {"Safety Expert"}: An expert in safety and regulatory compliance, with expertise in the design and implementation of safety systems, regulatory requirements, and compliance verification processes.
        6. {"Mathematical Solver (Analytical/Numerical)"}: An expert in mathematical analysis and numerical methods, with the ability to solve simple and complex mathematical problems both analytically and numerically, and can perform numerical algorithms when needed.
        7. {"General Process Engineer"}: A generalist with knowledge of all aspects of chemical process design, including economic analysis, process flow diagrams, and equipment selection, mass and energy balances.

        CORE RESPONSIBILITIES:
        1. Query Processing and Understanding
        - Perform deep semantic analysis of input queries
        - Identify explicit and implicit requirements
        - Extract technical nuances and contextual subtleties
        - Be careful, even if the query contains many elements, the classifier should only consider what was directly asked to be assisted with and not the entire query if it does not directly ask for it.

        2. Query Expansion and Clarification
        - If the initial query is ambiguous, generate clarifying questions
        - Infer potential hidden requirements or constraints

        3. Systematic Classification
        - the classification must capture:
        * Primary domain
        * Secondary domains
        * Potential interdisciplinary intersections

        4. Agent Selection and Dynamic Allocation
        - Maintain a comprehensive understanding of available agent capabilities
        - Internalize a dynamic, intelligent agent selection algorithm
        - Determine optimal agent combinations and interaction protocols
        - Predict potential communication pathways and collaborative dynamics

        INPUT QUERY:
        {user_query}

        OUTPUT REQUIREMENTS:
        You MUST respond with a valid JSON output string, adhering strictly to the following format using only double quotes for keys and string values. Do not include new lines inside the JSON string and ensure that no trailing commas exist:
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
        print("response : ",response)
        return response

class PlannerAgent:
    def __init__(self, agent_name, agent_expertise):

        self.model = instantiate_llm_model(model_to_use, temperature=0.2, max_tokens=2500)
        self.agent_name = agent_name
        self.agent_expertise = agent_expertise
        self.knowledge_retriever = KnowledgeRetriever()
        self.equations_retriever = EquationsFormulasRetriever()
        self.properties_retriever = PhysChemPropertiesRetriever()
        self.standards_retriever = IndustryStandardsRetriever()
        self.support_agents = {
            "Knowledge Retriever": self.knowledge_retriever,
            "Equations & Formulas Retriever": self.equations_retriever,
            "Phys/Chem Properties Retriever": self.properties_retriever,
            "Industry Standards Retriever": self.standards_retriever,
        }
    
    def execute_plan(self, plan):
        """Executes the plan using the support agents to retrieve information."""
        steps = plan.split("\n")
        retrieved_info = {}

        for step in steps:
            if step.strip().startswith("#Step"):
                step_number = step.split(":")[0].replace("#Step","")
                
            elif step.strip().startswith("#E"):
                try:
                    step_number_e = step.split(":")[0].replace("#E","")
                    
                    agent_name_search_terms_str = step.split(":", 1)[1].strip()
                    agent_name_search_terms_str = agent_name_search_terms_str.replace("#","")
                    
                    # Find the full support agent name that matches the input
                    matching_agent = None
                    for agent_full_name in self.support_agents.keys():
                        if agent_name_search_terms_str.startswith(agent_full_name):
                            matching_agent = agent_full_name
                            search_terms = agent_name_search_terms_str[len(matching_agent):].strip()
                            break
                    
                    if matching_agent:
                        support_agent = self.support_agents.get(matching_agent)
                        if support_agent:
                            # Use existing methods for each retriever
                            if isinstance(support_agent, KnowledgeRetriever):
                                search_results = support_agent._search_db(search_terms, top_k=3)
                                retrieved_data = support_agent._process_results(search_results)
                            elif isinstance(support_agent, EquationsFormulasRetriever):
                                if hasattr(support_agent, '_search_db'):
                                    search_results = support_agent._search_db(search_terms, top_k=3)
                                    retrieved_data = support_agent._process_results(search_results) if hasattr(support_agent, '_process_results') else search_results
                                else:
                                    retrieved_data = f"No search method for Equations Retriever with terms: {search_terms}"
                            elif isinstance(support_agent, PhysChemPropertiesRetriever):
                                if hasattr(support_agent, '_search_db'):
                                    search_results = support_agent._search_db(search_terms, top_k=3)
                                    retrieved_data = support_agent._process_results(search_results) if hasattr(support_agent, '_process_results') else search_results
                                else:
                                    retrieved_data = f"No search method for Properties Retriever with terms: {search_terms}"
                            elif isinstance(support_agent, IndustryStandardsRetriever):
                                if hasattr(support_agent, '_search_db'):
                                    search_results = support_agent._search_db(search_terms, top_k=3)
                                    retrieved_data = support_agent._process_results(search_results) if hasattr(support_agent, '_process_results') else search_results
                                else:
                                    retrieved_data = f"No search method for Standards Retriever with terms: {search_terms}"
                            else:
                                retrieved_data = f"Error: Unsupported support agent type: {type(support_agent)}"

                            retrieved_info[f"Step {step_number_e}"] = {
                                "agent": matching_agent,
                                "search_terms": search_terms,
                                "data": retrieved_data
                            }
                        else:
                            retrieved_info[f"Step {step_number_e}"] = f"Error: Support Agent '{matching_agent}' not found."
                    else:
                        retrieved_info[f"Step {step_number_e}"] = f"Error: No matching support agent found."
                except Exception as e:
                    retrieved_info[f"Step {step_number_e}"] = f"Error processing step: {str(e)}"

        return retrieved_info

    def create_plan(self, query_analysis, agent_allocation):
        """Creates a plan using the specified prompt."""
        if self.agent_name == "Separation Technologist":
            prompt = self._separation_technologist_prompt(query_analysis, agent_allocation)
        elif self.agent_name == "Thermodynamics Expert":
            prompt = self._thermodynamics_expert_prompt(query_analysis, agent_allocation)
        elif self.agent_name == "Troubleshooter":
            prompt = self._troubleshooter_prompt(query_analysis, agent_allocation)
        elif self.agent_name == "Dynamics & Control Expert":
            prompt = self._dynamics_control_expert_prompt(query_analysis, agent_allocation)
        elif self.agent_name == "Safety Expert":
            prompt = self._safety_expert_prompt(query_analysis, agent_allocation)
        elif self.agent_name == "Mathematical Solver":
            prompt = self._mathematical_solver_prompt(query_analysis, agent_allocation)
        elif self.agent_name == "General Process Engineer":
            prompt = self._general_process_engineer_prompt(query_analysis, agent_allocation)
        else:
            raise ValueError(f"Unknown agent name: {self.agent_name}")

        response = self.model.predict(prompt)
        return response
    


    def _separation_technologist_prompt(self, query_analysis, agent_allocation):
        return f"""
            You are a Separation Technologist Planner agent, specialized in creating detailed action plans for the Separation Technologist agent, a specialist in chemical separation processes. Your task is to develop a single comprehensive plan based on the query analysis and agent allocation provided. Each step within this plan should have a descriptive name and one evidence gatherer support agent assigned. This plan will guide the Separation Technologist agent in effectively addressing the problem.

            **Input:**
            *   **Query Analysis:** {query_analysis}
            *   **Agent Allocation:** {agent_allocation}
            *   **Supporting Agents:** Knowledge Retriever, Equations & Formulas Retriever, Phys/Chem Properties Retriever, and Industry Standards Retriever.

            **Instructions:**
            1.  **Analyze the input:** Carefully review the query analysis and the allocated role of the Separation Technologist agent. Identify the specific goals and tasks required for this agent.
            2.  **Develop a single detailed plan:** Generate a step-by-step plan that the Separation Technologist agent will follow.
                *   Do not exceed 4 or 5 steps at maximum.
                *   Each step should be structured as a distinct sub-task with a descriptive name.
                *   Each step must include a single support agent to retrieve data/info.
                *   Each step should be clear and concise, specifying the information/data the agent needs, the support agent that will provide that information, and any specific search terms or parameters.
                *   Use the following format: `#Step{{number}}: <Step Description>\\n#E{{number}}: #{{Support Agent Name}}# <Action Description and search terms/parameters>`
            3.  **Prioritize actions:** The plan should prioritize essential steps and those that need to be performed first before other ones.
            4.  **Ensure relevance:** Make sure that each step directly relates to the agent’s expertise and the overarching goal of the query.
            5.  **Use Support Agents:** Prioritize using the support agents for *every* data/info retrieval in *each* step.
            6.  **Domain-Specific Logic:** Apply your expert knowledge in separation technology to craft the plan. For separation processes, start by looking for existing technology overviews, performance data and key parameters influencing efficiency. Then, look for detailed process flow diagrams and operating conditions. Consider looking for alternatives if current technology is not efficient. Think about the common workflows a separation technologist would follow to optimize a process.
            7.  **Output Format:** Present your plan in the following format: `Plan: <Plan Description>\\n#Step1: <Step Description>\\n#E1: #{{Support Agent}}# <action>\\n#Step2: <Step Description>\\n#E2: #{{Support Agent}}# <action>\\n ...\\n`

            **Example:**
            #Step1: Define Natural Gas Stream Composition and Target Water Content
            #E1: #Knowledge Retriever# [Retrieve typical composition ranges for natural gas streams, focusing on water content and common impurities. Specify the need for target water content after separation (e.g., ppmv).]
            #Step2: Identify Cryogenic Condenser Technologies for Water Removal
            #E2: #Knowledge Retriever# [Retrieve overview of existing cryogenic condenser technologies used for water removal from natural gas, including their typical operating conditions and limitations.]
            #Step3: Gather Water-Methane VLE Data at Cryogenic Temperatures
            #E3: #Phys/Chem Properties Retriever# [Retrieve Vapor-Liquid Equilibrium (VLE) data for the water-methane system at cryogenic temperatures relevant to natural gas processing.]
            #Step4: Retrieve Equations for Condenser Heat Transfer and Mass Transfer
            #E4: #Equations & Formulas Retriever# [Retrieve equations for calculating heat transfer and mass transfer coefficients in cryogenic condensers, specifically for water condensation.]
            #Step5: Analyze Industry Standards for Water Content in Natural Gas
            #E5: #Industry Standards Retriever# [Retrieve industry standards and guidelines for acceptable water content in processed natural gas.]

            **Output:**
            Provide the full detailed plan as described above. I repeat, do not exceed 4 or 5 steps at maximum. Only use the given support agents: Knowledge Retriever, Equations & Formulas Retriever, Phys/Chem Properties Retriever, and Industry Standards Retriever.
            """

    def _thermodynamics_expert_prompt(self, query_analysis, agent_allocation):
        return f"""
            You are a Thermodynamics Expert Planner agent, specialized in creating detailed action plans for the Thermodynamics Expert agent, a specialist in thermodynamics, heat transfer, mass transfer, phase changes, and phase equilibria. Your task is to develop a single comprehensive plan based on the query analysis and agent allocation provided. Each step within this plan should have a descriptive name and one evidence gatherer support agent assigned. This plan will guide the Thermodynamics Expert agent in effectively addressing the problem.

            **Input:**
            *   **Query Analysis:** {query_analysis}
            *   **Agent Allocation:** {agent_allocation}
            *   **Supporting Agents:** Knowledge Retriever, Equations & Formulas Retriever, Phys/Chem Properties Retriever, and Industry Standards Retriever.

            **Instructions:**
            1.  **Analyze the input:** Carefully review the query analysis and the allocated role of the Thermodynamics Expert agent. Identify the specific goals and tasks required for this agent.
            2.  **Develop a single detailed plan:** Generate a step-by-step plan that the Thermodynamics Expert agent will follow.
                *   Do not exceed 4 or 5 steps at maximum.
                *   Each step should be structured as a distinct sub-task with a descriptive name.
                *   Each step must include a single support agent to retrieve data/info.
                *   Each step should be clear and concise, specifying the information/data the agent needs, the support agent that will provide that information, and any specific search terms or parameters.
                *   Use the following format: `#Step{{number}}: <Step Description>\\n#E{{number}}: #{{Support Agent Name}}# <Action Description and search terms/parameters>`
            3.  **Prioritize actions:** The plan should prioritize essential steps and those that need to be performed first before other ones.
            4.  **Ensure relevance:** Make sure that each step directly relates to the agent’s expertise and the overarching goal of the query.
            5.  **Use Support Agents:** Prioritize using the support agents for *every* data/info retrieval in *each* step.
            6.  **Domain-Specific Logic:** Apply your expert knowledge in thermodynamics to craft the plan. Start by identifying relevant thermodynamic properties such as phase equilibrium data, heat capacities, enthalpies, and entropies. Then look for relevant equations of state, phase diagrams and property correlations that apply for the specific components and conditions. Also look for heat and mass transfer equations that could be relevant for the process.
            7.  **Output Format:** Present your plan in the following format: `Plan: <Plan Description>\\n#Step1: <Step Description>\\n#E1: #{{Support Agent}}# <action>\\n#Step2: <Step Description>\\n#E2: #{{Support Agent}}# <action>\\n ...\\n`

            **Example:**
            Plan: Gather necessary thermodynamic data for cryogenic separation.
            #Step1: Define Relevant Properties and Overview
            #E1: #Knowledge Retriever# [Retrieve an overview of relevant thermodynamic properties and their importance for cryogenic separation of natural gas components.]
            #Step2: Gather Phase Equilibrium Data for Key Components
            #E2: #Phys/Chem Properties Retriever# [Retrieve Vapor-Liquid Equilibrium (VLE) data for methane, water, and heavy hydrocarbons at cryogenic temperatures relevant to natural gas processing.]
            #Step3: Identify Suitable Equations of State for Cryogenic Conditions
            #E3: #Equations & Formulas Retriever# [Retrieve equations of state (EOS) suitable for modeling the behavior of natural gas components at cryogenic temperatures.]
            #Step4: Retrieve Heat and Mass Transfer Equations for Cryogenic Units
            #E4: #Equations & Formulas Retriever# [Retrieve equations governing heat and mass transfer in cryogenic separation units, focusing on condensers and separators.]

            **Output:**
            Provide the full detailed plan as described above. I repeat, do not exceed 4 or 5 steps at maximum. Only use the given support agents: Knowledge Retriever, Equations & Formulas Retriever, Phys/Chem Properties Retriever, and Industry Standards Retriever.
            """

    def _troubleshooter_prompt(self, query_analysis, agent_allocation):
            return f"""
                You are a Troubleshooter Planner agent, specialized in creating detailed action plans for the Troubleshooter agent, a specialist in chemical process troubleshooting and root cause analysis. Your task is to develop a single comprehensive plan based on the query analysis and agent allocation provided. Each step within this plan should have a descriptive name and one evidence gatherer support agent assigned. This plan will guide the Troubleshooter agent in effectively addressing the problem.

                **Input:**
                *   **Query Analysis:** {query_analysis}
                *   **Agent Allocation:** {agent_allocation}
                *   **Supporting Agents:** Knowledge Retriever, Equations & Formulas Retriever, Phys/Chem Properties Retriever, and Industry Standards Retriever.

                **Instructions:**
                1.  **Analyze the input:** Carefully review the query analysis and the allocated role of the Troubleshooter agent. Identify the specific goals and tasks required for this agent.
                2.  **Develop a single detailed plan:** Generate a step-by-step plan that the Troubleshooter agent will follow.
                    *   Do not exceed 4 or 5 steps at maximum.
                    *   Each step should be structured as a distinct sub-task with a descriptive name.
                    *   Each step must include a single support agent to retrieve data/info.
                    *   Each step should be clear and concise, specifying the information/data the agent needs, the support agent that will provide that information, and any specific search terms or parameters.
                    *   Use the following format: `#Step{{number}}: <Step Description>\\n#E{{number}}: #{{Support Agent Name}}# <Action Description and search terms/parameters>`
                3.  **Prioritize actions:** The plan should prioritize essential steps and those that need to be performed first before other ones.
                4.  **Ensure relevance:** Make sure that each step directly relates to the agent’s expertise and the overarching goal of the query.
                5.  **Use Support Agents:** Prioritize using the support agents for *every* data/info retrieval in *each* step.
                6.  **Domain-Specific Logic:** Apply your expert knowledge in troubleshooting to craft the plan. Begin by identifying symptoms and the timeline of the problems. Then, focus on searching for similar failure cases and typical problems associated with the type of equipment and process involved. Identify common root causes and potential mitigation strategies.
                7.  **Output Format:** Present your plan in the following format: `Plan: <Plan Description>\\n#Step1: <Step Description>\\n#E1: #{{Support Agent}}# <action>\\n#Step2: <Step Description>\\n#E2: #{{Support Agent}}# <action>\\n ...\\n`

            **Example:**
            Plan: Investigate causes of performance issues in a distillation column.
            #Step1: Identify Common Distillation Column Issues
            #E1: #Knowledge Retriever# [Retrieve an overview of common performance issues in continuous distillation columns, including causes of efficiency loss and temperature profile deviations.]
            #Step2: Review Operational Standards and Monitoring
            #E2: #Industry Standards Retriever# [Retrieve industry standards and best practices for operating and monitoring continuous distillation columns, focusing on key performance indicators.]
            #Step3: Analyze Failure Modes and Similar Cases
            #E3: #Knowledge Retriever# [Research known failure modes, causes of efficiency loss, and troubleshooting strategies for similar distillation columns.]
            #Step4: Check Material Compatibility and Operational Limits
            #E4: #Phys/Chem Properties Retriever# [Retrieve information on material compatibility with the chemicals, temperatures, and pressures involved in the distillation process, focusing on potential degradation or corrosion.]

                **Output:**
                Provide the full detailed plan as described above. I repeat, do not exceed 4 or 5 steps at maximum. Only use the given support agents: Knowledge Retriever, Equations & Formulas Retriever, Phys/Chem Properties Retriever, and Industry Standards Retriever.
                """

    def _dynamics_control_expert_prompt(self, query_analysis, agent_allocation):
        return f"""
            You are a Dynamics & Control Expert Planner agent, specialized in creating detailed action plans for the Dynamics & Control Expert agent, a specialist in process control and dynamics. Your task is to develop a single comprehensive plan based on the query analysis and agent allocation provided. Each step within this plan should have a descriptive name and one evidence gatherer support agent assigned. This plan will guide the Dynamics & Control Expert agent in effectively addressing the problem.

            **Input:**
            *   **Query Analysis:** {query_analysis}
            *   **Agent Allocation:** {agent_allocation}
            *   **Supporting Agents:** Knowledge Retriever, Equations & Formulas Retriever, Phys/Chem Properties Retriever, and Industry Standards Retriever.

            **Instructions:**
            1.  **Analyze the input:** Carefully review the query analysis and the allocated role of the Dynamics & Control Expert agent. Identify the specific goals and tasks required for this agent.
            2.  **Develop a single detailed plan:** Generate a step-by-step plan that the Dynamics & Control Expert agent will follow.
                *   Do not exceed 4 or 5 steps at maximum.
                *   Each step should be structured as a distinct sub-task with a descriptive name.
                *   Each step must include a single support agent to retrieve data/info.
                *   Each step should be clear and concise, specifying the information/data the agent needs, the support agent that will provide that information, and any specific search terms or parameters.
                *   Use the following format: `#Step{{number}}: <Step Description>\\n#E{{number}}: #{{Support Agent Name}}# <Action Description and search terms/parameters>`
            3.  **Prioritize actions:** The plan should prioritize essential steps and those that need to be performed first before other ones.
            4.  **Ensure relevance:** Make sure that each step directly relates to the agent’s expertise and the overarching goal of the query.
            5.  **Use Support Agents:** Prioritize using the support agents for *every* data/info retrieval in *each* step.
            6.  **Domain-Specific Logic:** Apply your expert knowledge in dynamics and control to craft the plan. Begin by analyzing process variables that should be monitored (flowrates, temperature, pressure, etc). Then, look for dynamic models of the process, and relevant control strategies, as well as necessary sensor data.
            7.  **Output Format:** Present your plan in the following format: `Plan: <Plan Description>\\n#Step1: <Step Description>\\n#E1: #{{Support Agent}}# <action>\\n#Step2: <Step Description>\\n#E2: #{{Support Agent}}# <action>\\n ...\\n`

            **Example:**
            Plan: Evaluate and design control strategies for a distillation column.
            # Step 1: Identify Key Variables and Process Dynamics for Distillation Columns  
            # E1: #Knowledge Retriever# [Search for critical process variables in distillation columns. Identify key manipulated, controlled, and disturbance variables required for dynamic stability and optimal performance] 
            # Step 2: Retrieve Dynamic Models and Control Equations for Distillation Columns 
            # E2: #Equations & Models Retriever# [Obtain validated dynamic models (e.g., mass/energy balances, transfer functions) and relevant control-oriented equations for Distillation Columns . Emphasize linearized models for control design and nonlinear models for comprehensive system behavior.]  
            # Step 3: Explore Control Strategies and Techniques for Distillation Columns 
            # E3: #Knowledge Retriever# [Review conventional and advanced control strategies for Distillation Columns, including PID, MPC, and inferential control. Highlight their applications, benefits, and trade-offs in addressing dynamic changes and disturbances.]  
            # Step 4: Assess Sensors and Standards for Control Systems of Distillation Columns  
            # E4: #Industry Standards Retriever# [Retrieve information on sensor technologies and industry standards for key variables for Distillation Columns . Evaluate sensor accuracy, response time, and compatibility with advanced control systems.]  

            **Output:**
            Provide the full detailed plan as described above. I repeat, do not exceed 4 or 5 steps at maximum. Only use the given support agents: Knowledge Retriever, Equations & Formulas Retriever, Phys/Chem Properties Retriever, and Industry Standards Retriever.
            """

    def _safety_expert_prompt(self, query_analysis, agent_allocation):
        return f"""
            You are a Process Safety Engineer Planner agent, specialized in creating detailed action plans for the Process Safety Engineer agent, a specialist in identifying, evaluating, and mitigating safety hazards in chemical processes. Your task is to develop a single comprehensive plan based on the query analysis and agent allocation provided. Each step within this plan should have a descriptive name and one evidence gatherer support agent assigned. This plan will guide the Process Safety Engineer agent in effectively addressing the problem, particularly in the context of chemical processes.

            **Input:**
            *   **Query Analysis:** {query_analysis}
            *   **Agent Allocation:** {agent_allocation}
            *   **Supporting Agents:** Knowledge Retriever, Equations & Formulas Retriever, Phys/Chem Properties Retriever, and Industry Standards Retriever.

            **Instructions:**
            1.  **Analyze the input:** Carefully review the query analysis and the allocated role of the Process Safety Engineer agent. Identify the specific goals and tasks required for this agent, focusing on the safety aspects of the problem.
            2.  **Develop a single detailed plan:** Generate a step-by-step plan that the Process Safety Engineer agent will follow.
                *   Do not exceed 4 or 5 steps at maximum.
                *   Each step should be structured as a distinct sub-task with a descriptive name.
                *   Each step must include a single support agent to retrieve data/info.
                *   Each step should be clear and concise, specifying the information/data the agent needs, the support agent that will provide that information, and any specific search terms or parameters.
                *   Use the following format: `#Step{{number}}: <Step Description>\\n#E{{number}}: #{{Support Agent Name}}# <Action Description and search terms/parameters>`
            3.  **Prioritize actions:** The plan should prioritize essential steps, starting with hazard identification, then moving to risk assessment, regulatory compliance, and finally risk mitigation.
            4.  **Ensure relevance:** Make sure that each step directly relates to the agent’s expertise and the overarching goal of the query, focusing on safety and regulatory aspects.
            5.  **Use Support Agents:** Prioritize using the support agents for *every* data/info retrieval in *each* step.
            6.  **Domain-Specific Logic:** Apply your expert knowledge in process safety to craft the plan. Start by identifying the hazards associated with the chemicals and the process, then research relevant safety standards and regulations, and finally develop risk mitigation strategies.
            7.  **Output Format:** Present your plan in the following format: `Plan: <Plan Description>\\n#Step1: <Step Description>\\n#E1: #{{Support Agent}}# <action>\\n#Step2: <Step Description>\\n#E2: #{{Support Agent}}# <action>\\n ...\\n`

            **Example:**
                **Original Query:** "Evaluate the safety and regulatory requirements for a cryogenic separation process involving methane, nitrogen, and trace amounts of hydrogen sulfide. The process operates at temperatures as low as -150°C and pressures up to 50 bar. Develop a safety plan to address potential hazards."

                Plan: Safety and Regulatory Requirements for Cryogenic Separation Process
                #Step1: Identify Chemical and Process Hazards
                #E1:#Phys/Chem Properties Retriever# Retrieve physical and chemical properties of methane, nitrogen, and hydrogen sulfide under cryogenic (-150°C) and high-pressure (50 bar) conditions, including phase behavior, toxicity, flammability, and reactivity.  
                #Step2: Identify key safety and regulatory standards for cryogenic and hazardous gas processes. 
                #E2:#Industry Standards Retriever# Retrieve OSHA, API, and ISO standards for cryogenic systems, hazardous gas handling, and pressure vessel design.  
                #Step3: Ensure materials and equipment used in the process are safe and compatible with operating conditions.*
                #E3:#Equations & Formulas Retriever# Retrieve material selection criteria and equations to assess material performance under cryogenic temperatures and hydrogen sulfide exposure.  
                #Step4: Propose measures to address identified risks, including safety systems and emergency protocols. 
                #E4:#Knowledge Retriever#** Retrieve best practices for cryogenic system hazard mitigation, including emergency response planning and operational safeguards.  
                #Step5: Compile Comprehensive Safety Plan: Integrate findings into a detailed safety and compliance plan.
                #E5:#Knowledge Retriever#** Retrieve templates and examples for developing a detailed safety plan for chemical processes, ensuring alignment with regulatory requirements.  


            **Output:**
            Provide the full detailed plan as described above. I repeat, do not exceed 4 or 5 steps at maximum. Only use the given support agents: Knowledge Retriever, Equations & Formulas Retriever, Phys/Chem Properties Retriever, and Industry Standards Retriever.
            """

    def _mathematical_solver_prompt(self, query_analysis, agent_allocation):
        return f"""
            You are a Mathematical Solver Planner agent, specialized in creating detailed action plans for the Mathematical Solver agent, a specialist in mathematical analysis and numerical methods applied to chemical separation processes and other related chemical engineering problems. Your task is to develop a single comprehensive plan based on the query analysis and agent allocation provided. This plan should guide the Mathematical Solver agent in effectively addressing the problem by first understanding the problem, classifying it, and then creating a tailored solution plan. Each step within this plan should have a descriptive name and one evidence gatherer support agent assigned.

            **Input:**
            *   **Query Analysis:** {query_analysis}
            *   **Agent Allocation:** {agent_allocation}
            *   **Supporting Agents:** Knowledge Retriever, Equations & Formulas Retriever, Phys/Chem Properties Retriever, and Industry Standards Retriever.

            **Instructions:**
            1.  **Analyze the input:** Carefully review the query analysis and the allocated role of the Mathematical Solver agent. Identify the specific goals and tasks required for this agent, focusing on the mathematical aspects of the problem.
            2.  **Problem Classification and Analysis:** Based on the query, classify the problem according to the following:
                *   **Problem Type:** (e.g., steady-state, dynamic, optimization, parameter estimation, analytical model derivation)
                *   **Key Variables and Parameters:** Identify the dependent and independent variables, and any relevant physical parameters.
                *   **Governing Equations:** Determine the relevant mathematical equations (e.g., differential equations, algebraic equations, mass/energy balances, transport equations).
                *   **Boundary and Initial Conditions:** Identify any necessary boundary or initial conditions for solving the equations.
                *   **Physical Constraints:** Note any physical limitations or constraints on the system.
                *   **Expected Solution Characteristics:** Describe the expected nature of the solution (e.g., analytical expression, numerical solution, steady-state profile, transient behavior).
                *   **Required Mathematical Methods:** Determine the appropriate mathematical methods for solving the problem (e.g., analytical solution, separation of variables, numerical integration, finite difference method).
            3.  **Develop a single detailed plan:** Generate a step-by-step plan that the Mathematical Solver agent will follow.
                *   Do not exceed 4 or 5 steps at maximum.
                *   Each step should be structured as a distinct sub-task with a descriptive name.
                *   Each step must include a single support agent to retrieve data/info.
                *   Each step should be clear and concise, specifying the information/data the agent needs, the support agent that will provide that information, and any specific search terms or parameters.
                *   Use the following format: `#Step{{number}}: <Step Description>\\n#E{{number}}: #{{Support Agent Name}}# <Action Description and search terms/parameters>`
            4.  **Prioritize actions:** The plan should prioritize essential steps, starting with problem understanding and classification, then moving to data retrieval (if needed) and solution methods.
            5.  **Ensure relevance:** Make sure that each step directly relates to the agent’s expertise and the overarching goal of the query.
            6.  **Use Support Agents:** Prioritize using the support agents for *every* data/info retrieval in *each* step.
            7.  **Domain-Specific Logic:** Apply your expert knowledge in mathematical analysis to craft the plan. Start by identifying relevant mathematical models for the process, also identify equations that need to be solved and whether they can be solved analytically, and when not, search for numerical methods to solve the equations. The plan should be modular, allowing for both simple and complex problems, and should be able to handle problems that require analytical solutions without numerical data.
            8.  **Output Format:** Present your plan in the following format: `Plan: <Plan Description>\\n#Step1: <Step Description>\\n#E1: #{{Support Agent}}# <action>\\n#Step2: <Step Description>\\n#E2: #{{Support Agent}}# <action>\\n ...\\n`

            **Example:**
                **Original Query:** "Consider a porous, spherical catalyst particle where a first-order reaction A → B is occurring on the internal surface of the pores. The gas-phase reactant A diffuses into the particle and reacts on the catalyst surface. The reaction rate is first-order with respect to the concentration of A, and diffusion through the pores is described by Fick’s law. The external concentration of A at the surface of the catalyst particle is CA,s. Develop an analytical model to describe the concentration profile of A within the catalyst particle."

                Plan: Develop an analytical model for reactant diffusion and reaction in a porous catalyst particle.
                #Step1: Classify the Catalyst Particle Problem
                #E1: #Knowledge Retriever# [Retrieve information on diffusion and reaction in porous catalysts, focusing on its classification as a steady-state mass transfer problem with reaction.]
                #Step2: Identify Governing Equations and Boundary Conditions
                #E2: #Equations & Formulas Retriever# [Retrieve Fick's law for diffusion and the first-order reaction rate equation, and identify the appropriate boundary conditions for the spherical catalyst particle.]
                #Step3: Derive Analytical Solution for Concentration Profile
                #E3: #Knowledge Retriever# [Research analytical methods for solving the resulting differential equation, such as separation of variables or other relevant techniques, and outline the steps to derive the concentration profile.]
                #Step4: Analyze the Thiele Modulus and Effectiveness Factor
                #E4: #Equations & Formulas Retriever# [Retrieve the definitions and equations for the Thiele modulus and effectiveness factor, and discuss their relevance to the derived concentration profile.]

            **Output:**
            Provide the full detailed plan as described above. I repeat, do not exceed 4 or 5 steps at maximum. Only use the given support agents: Knowledge Retriever, Equations & Formulas Retriever, Phys/Chem Properties Retriever, and Industry Standards Retriever.
            """
        
    def _general_process_engineer_prompt(self, query_analysis, agent_allocation):
        return f"""
            You are a General Process Engineer Planner agent, specialized in creating detailed action plans for the General Process Engineer agent, a specialist in various process engineering unit operations and equipment, *excluding* separation processes. This includes reactors, compressors, heat exchangers, pumps, and other common process equipment. Your task is to develop a single comprehensive plan based on the query analysis and agent allocation provided. Each step within this plan should have a descriptive name and one evidence gatherer support agent assigned. This plan will guide the General Process Engineer agent in effectively addressing the problem, particularly when the query involves equipment or unit operations beyond separation processes, *within a larger context that may include separation*.

            **Input:**
            *   **Query Analysis:** {query_analysis}
            *   **Agent Allocation:** {agent_allocation}
            *   **Supporting Agents:** Knowledge Retriever, Equations & Formulas Retriever, Phys/Chem Properties Retriever, and Industry Standards Retriever.

            **Instructions:**
            1.  **Analyze the input:** Carefully review the query analysis and the allocated role of the General Process Engineer agent. Identify the specific goals and tasks required for this agent, paying attention to whether the query involves equipment or unit operations *other than* separation processes, even if the overall query is related to a separation process.
            2.  **Develop a single detailed plan:** Generate a step-by-step plan that the General Process Engineer agent will follow. The plan should be flexible enough to handle a variety of process engineering tasks related to non-separation equipment, within the context of a larger process.
                *   Do not exceed 4 or 5 steps at maximum.
                *   Each step should be structured as a distinct sub-task with a descriptive name.
                *   Each step must include a single support agent to retrieve data/info.
                *   Each step should be clear and concise, specifying the information/data the agent needs, the support agent that will provide that information, and any specific search terms or parameters.
                *   Use the following format: `#Step{{number}}: <Step Description>\\n#E{{number}}: #{{Support Agent Name}}# <Action Description and search terms/parameters>`
            3.  **Prioritize actions:** The plan should prioritize essential steps and those that need to be performed first before other ones. A typical workflow should start with understanding the equipment or unit operation, then move to design considerations, performance analysis, and finally material/operational aspects, all within the context of the larger process.
            4.  **Ensure relevance:** Make sure that each step directly relates to the agent’s expertise and the overarching goal of the query, focusing on non-separation equipment and unit operations, even when the query is primarily about a separation process.
            5.  **Use Support Agents:** Prioritize using the support agents for *every* data/info retrieval in *each* step.
            6.  **Domain-Specific Logic:** Apply your expert knowledge in process engineering to craft the plan. Start by understanding the function and requirements of the specific equipment or unit operation, then analyze its performance characteristics, then consider design parameters and operational aspects, and finally identify necessary materials and standards, all within the context of the larger process. The plan should be adaptable to different types of non-separation process equipment.
            7.  **Output Format:** Present your plan in the following format: `Plan: <Plan Description>\\n#Step1: <Step Description>\\n#E1: #{{Support Agent}}# <action>\\n#Step2: <Step Description>\\n#E2: #{{Support Agent}}# <action>\\n ...\\n`

            **Example:**
                **Original Query:** "Design a process for separating methane from a natural gas stream using cryogenic distillation. The natural gas feed stream is at 20 bar and 25°C with a flow rate of 1000 kg/hr. Include a compressor to increase the pressure of the feed stream to 60 bar before it enters the distillation column. Also, specify the heat exchanger needed to cool the stream to 10°C before compression."

                Plan: Analyze the compressor and heat exchanger requirements for a cryogenic distillation process.
                #Step1: Define the Compressor Requirements for the Natural Gas Feed
                #E1: #Knowledge Retriever# [Retrieve information on the required pressure increase (from 20 bar to 60 bar), flow rate (1000 kg/hr), and inlet conditions (20 bar, 25°C) for the natural gas stream entering the compressor.]
                #Step2: Gather Relevant Compressor Performance Equations
                #E2: #Equations & Formulas Retriever# [Retrieve relevant equations for calculating compressor power, efficiency, and outlet temperature based on the required pressure increase, flow rate, and inlet conditions.]
                #Step3: Analyze the Heat Exchanger Requirements for Pre-Compression Cooling
                #E3: #Knowledge Retriever# [Research the heat transfer duty required to cool the natural gas stream from 25°C to 10°C before compression, considering the stream's composition (assuming primarily methane) and flow rate (1000 kg/hr).]
                #Step4: Identify Suitable Materials and Design Standards for the Compressor and Heat Exchanger
                #E4: #Industry Standards Retriever# [Research industry standards for selecting materials and design parameters for compressors and heat exchangers used in natural gas processing, considering the operating conditions, fluids involved, and the specified temperature and pressure ranges.]

            **Output:**
            Provide the full detailed plan as described above. I repeat, do not exceed 4 or 5 steps at maximum. Only use the given support agents: Knowledge Retriever, Equations & Formulas Retriever, Phys/Chem Properties Retriever, and Industry Standards Retriever.
            """

class OverviewPlanner:
        def __init__(self):
            self.model = instantiate_llm_model(model_to_use, temperature=0.2, max_tokens=2000)
            
        def coordinate_plans(self, list_of_agent_plans, agent_allocation):
            """Coordinates the plans from all planner agents."""
            prompt = self._overview_planner_prompt(list_of_agent_plans, agent_allocation)
            response = self.model.predict(prompt)
            return response

        def _overview_planner_prompt(self, list_of_agent_plans, agent_allocation):
            return f"""
                You are the Overview Planner agent, responsible for coordinating the plans generated by individual planner agents. Your task is to review the plans, identify potential overlaps, ensure that they are agent-specific, and create a collaboration sequence between agents if required.

                **Input:**
                *   **Individual Agent Plans:** {list_of_agent_plans}
                *   **Agent Allocation:** {agent_allocation}

                **Instructions:**
                1.  **Review all plans:** Carefully examine each plan generated by the individual planner agents, ensuring a clear understanding of the steps, their descriptions, and the selected support agent for each step.
                2.  **Identify overlaps:** Pinpoint any areas where plans might have overlapping steps that request similar information, focusing on steps that use the same support agents or request information of the same kind. Also identify if the descriptions of different steps are aiming to achieve the same objective.
                3.  **Ensure agent specificity:** Verify that each plan is tailored to the specific expertise and allocated role of its designated agent.
                4.  **Create collaboration sequences:** If the agent allocation specifies any collaboration between agents, create a collaboration protocol, detailing the sequence of exchange and interactions.
                5.  **Prioritize and Sequence Actions:** Ensure that steps between all plans do not conflict and are performed in a sequence that is necessary to achieve the goal, considering dependencies between agents. If needed, reorder the steps within or between the plans to maintain consistency.
                6.  **Output:** Return a revised version of the plans making sure that the overall plan is consistent and coherent. Also, provide a clear indication of any collaboration sequences required. Present the plans in a structured way and make a short overall summary of your overview work.

                **Output Format:**
                ```
                Revised Plans:
                <Agent Name> Plan: <Revised Plan>
                <Agent Name> Plan: <Revised Plan>
                ...

                Collaboration Sequences:
                <Agent 1> -> <Agent 2> -> <Agent 3> (if any, and explain what the interaction is about)

                Overview Summary:
                <Short summary of your work, including if you changed anything in particular>
                ```
            """


def normalize_agent_name(agent_name):
    """Normalize agent names by removing spaces and underscores, and converting to lowercase."""
    if pd.isna(agent_name):  # Check for NaN or None
        return None
    return agent_name.replace(" ", "").replace("_", "").lower()

def main():
    """
    Main function to interact with the agents.
    """
    print("Please provide your query:")
    user_input = input().strip()

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

    print("\nFinal Report:\n")
    print(final_report)
    
    
    
if __name__ == "__main__":
    main()
    