from agent.core_agent import CoreAgent
from utils import data_utils, report_utils
import logging

class RiskAgent(CoreAgent):
    def __init__(self):
         super().__init__()

    def generate_risk_assessment(self, diagram_data, identified_hazards):
        base_data = self.prepare_base_data(diagram_data, identified_hazards)
        results = {}

        # Step 1: Likelihood and Severity Estimation
        step1_prompt = f"""
        Based on the following information:
        {data_utils.format_data(base_data)}
        Previous step results:
        For each identified hazard:
        a. Estimate the likelihood of occurrence (Rare, Unlikely, Possible, Likely, Almost Certain)
        b. Estimate the potential severity of consequences (Insignificant, Minor, Moderate, Major, Catastrophic)
        c. Determine the overall risk level (Low, Medium, High, Extreme)
        
        Provide your assessment in a structured format.
        """
        results['step1'] = self.execute_step(step1_prompt)

        # Step 2: Risk Rationale and Mitigation
        step2_prompt = f"""
        Based on the following information:
        {data_utils.format_data(base_data)}
        Previous step results: {results['step1']}
        For each identified hazard:
        d. Provide a detailed rationale for your risk estimations
        e. Suggest specific risk mitigation measures, including both preventive and mitigative controls, make sure these are in-depth measures not just a list of recommendations.
        f. Evaluate the potential effectiveness of proposed risk mitigation measures
        
        Provide your assessment in a structured format.
        """
        results['step2'] = self.execute_step(step2_prompt)


        # Step 3: Layer of Protection Analysis (LOPA)
        step3_prompt = f"""
        Based on the following information:
        {data_utils.format_data(base_data)}
        Previous step results: {data_utils.format_data(results)}

        Conduct a Layer of Protection Analysis (LOPA) for high-risk scenarios:
        a. Identify initiating events and their frequencies
        b. List Independent Protection Layers (IPLs) and their Probability of Failure on Demand (PFD)
        c. Calculate the mitigated event likelihood
        d. Determine if additional risk reduction is required
        
        Provide your analysis in a structured format.
        """
        results['step3'] = self.execute_step(step3_prompt)

        # Step 4: Gap Analysis and Risk Trade-offs
        step4_prompt = f"""
        Based on the following information:
        {data_utils.format_data(base_data)}
        Previous step results: {data_utils.format_data(results)}

        1. Perform a gap analysis:
           a. Identify areas where current safeguards may be insufficient
           b. Suggest process safety improvements based on industry best practices and standards

        2. Discuss potential risk trade-offs and optimization strategies
        
        Provide your analysis in a structured format.
        """
        results['step4'] = self.execute_step(step4_prompt)


        # Step 5: Risk Matrix and Recommendations
        step5_prompt = f"""
        Based on the following information:
        {data_utils.format_data(base_data)}
        Previous step results: {data_utils.format_data(results)}

        1. Create a risk matrix to visualize the overall risk profile of the process, including:
           a. A description of a color-coded 5x5 matrix showing likelihood vs. consequence
           b. Plotting of identified hazards on the matrix
           c. Indication of risk tolerance criteria

        2. Provide recommendations for:
           a. Short-term risk reduction measures
           b. Long-term process safety improvements
           c. Areas requiring further study or quantitative risk assessment

        Present your assessment in a structured, professional format suitable for a chemical industry risk management team. 
        Use technical language and reference relevant industry standards (e.g., API, ASME, NFPA) where applicable.
        """
        results['step5'] = self.execute_step(step5_prompt)

        # Combine all results
        final_assessment_list = [results.get(f"step{i}", "") for i in range(1, 6)]
        final_assessment = "\n\n".join([item if isinstance(item, str) else str(item) for item in final_assessment_list]) # Ensures that the items are string
        report_utils.generate_pdf("risk_assessment.pdf", "Risk Assessment", final_assessment)
        return final_assessment
