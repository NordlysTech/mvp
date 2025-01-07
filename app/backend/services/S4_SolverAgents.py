import openai
import os
from dotenv import load_dotenv
from services.llm_utils import instantiate_llm_model

import json
from abc import ABC, abstractmethod
import re


from services.config_utils import load_config, get_config

config_path = "config.yaml"
config = load_config(config_path)



load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

model_to_use = get_config(config, "llms", "llm_name")

class BaseSolverAgent(ABC):
    """Base class for all solver agents."""

    def __init__(self, agent_name, agent_expertise):
        self.model = instantiate_llm_model(model_to_use, temperature=0.2, max_tokens=2500)
        self.agent_name = agent_name
        self.agent_expertise = agent_expertise

    @abstractmethod
    def _process_plan(self, full_plan_evidence, user_query):
       """Process the full plan and evidence."""
       pass

    def execute_plan(self, plan, retrieved_evidence, user_query, agent_allocation):
      """Executes the plan by processing each step and integrating the evidence."""
      
      # Initialize the full_plan_evidence as a dictionary
      full_plan_evidence = retrieved_evidence
      
      # Optional: Add logic to process or combine evidence here

      print("full_plan_evidence", full_plan_evidence)

      # Process the full plan and evidence
      analysis_results = self._process_plan(self,full_plan_evidence, user_query)

      return analysis_results

        
        # Extract other agents' info
        # other_agents_data = [
        #     {"agent_name": agent["agent_name"], "role": agent["role"]}
        #         for agent in agent_allocation["selected_agents"]
        #         if agent["agent_name"] != self.agent_name
        # ]
        
        # for step in steps:
        #     if step.strip().startswith("#Step"):
        #         step_number = step.split(":")[0].replace("#Step","")
                
        #     elif step.strip().startswith("#E"):
        #          try:
        #             step_number_e = step.split(":")[0].replace("#E","")
        #             retrieved_info = retrieved_evidence.get(f"Step {step_number_e}")
        #             if retrieved_info and isinstance(retrieved_info, dict) and "data" in retrieved_info:
        #                 data = retrieved_info["data"]
        #             else:
        #                 data = None
                    
        #             full_plan_evidence[f"Step {step_number_e}"] = data
        #          except Exception as e:
        #             full_plan_evidence[f"Step {step_number_e}"] = None
        
        #
    
class SuperSolverAgent(BaseSolverAgent):
    """A single solver agent capable of synthesizing all information."""

    def __init__(self, agent_name, agent_expertise):
        """Initialize the SuperSolverAgent."""
        super().__init__(agent_name, agent_expertise)

    def _process_plan(self, full_plan_evidence, user_query, other_agents):
        """Processes all plans and evidence to create a comprehensive report."""
        prompt = f"""
            SUPER SOLVER AGENT PROMPT

            - You are a highly specialized Super Solver Agent, an expert in generating comprehensive, in-depth, and accurate technical engineering reports. Your task is to create a detailed, technical engineering report based on the provided evidence in an optimal way to adress the original user query. Your report should be structured and be a few paragraphs in length, no less than 2000 tokens, and in a technical industry grade manner.

            PRIORITIZATION DIRECTIVE:
            - Absolute Priority: Generate a final complete technical engineering report, addressing the original query, using only the provided evidence.
            - Include relevant equations, formulas, correlations, and balances when relevant.

            CORE IDENTITY AND SELF-CONCEPTUALIZATION:
            - You are a Super Solver, a pinnacle of expertise in generating in-depth technical reports. You embody a profound and nuanced understanding of chemical separation processes, combining theoretical depth with practical engineering disciplines and capabilities.
            - Your role is to transform the provided evidence into a single, cohesive, high-quality final report that could be used in a technical industry grade context.

            FUNDAMENTAL PROFESSIONAL SELF-AWARENESS:
            - You are not just an algorithm but a representation of comprehensive engineering knowledge, capable of applying deep analysis across different disciplines and then summarizing all the findings into one report, and outputing it as a final product.
            - Your primary goal is to generate the most accurate and detailed technical report to address the original user query.
             - Your purpose is to transform complex problems into clear, innovative, and practical solutions using the provided information.
            - You synthesize all available information into a single, final, comprehensive, technical, and in-depth report, and generate strategic insights that make the report as comprehensive as possible.

            OPERATIONAL FRAMEWORK:
            1. ORIGINAL USER QUERY:
             \"\"\"
            {user_query}
             \"\"\"

            2. INPUTS:
             - EXTRACTED EVIDENCE/CONTEXTUAL INFORMATION:
            \"\"\"
            {full_plan_evidence}
            \"\"\"

        """
        try:
            response = self.model.predict(prompt)
            return {"report":response}
        except Exception as e:
            print(f"Error in SuperSolverAgent: {e}")
            return {}


