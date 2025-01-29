from agent.core_agent import CoreAgent
from utils import data_utils, report_utils

class HAZIDAgent(CoreAgent):
    def __init__(self):
         super().__init__()

    def generate_hazid_report(self, diagram_data, identified_hazards, risk_assessment):
        report_prompt = f"""
            As a highly experienced process safety consultant, generate a comprehensive HAZID (Hazard Identification) report based on the following information:

            1. Process Description:
            {data_utils.format_data(diagram_data)}

            2. Identified Hazards:
            {identified_hazards}

            3. Risk Assessment:
            {risk_assessment}

            - Do not add any technical content, nor delete content that is not repeated in the report, just format the given information in a structured, professional format suitable for a chemical industry risk management team.
            - Clean the report of any repeated information.
            - Use technical language appropriate for a chemical industry engineering audience.
            - DO not use regular standard terms such as "promptly", "intricately", etc.

            """
        try:
             response = self.model.generate_content(report_prompt)
             final_report = response.text
             report_utils.generate_pdf("final_hazid_report.pdf", "HAZID Report", final_report)
             return final_report
        except Exception as e:
             print(f"Error during report generation: {e}")
             return {"error": str(e)}
