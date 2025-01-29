from agent.core_agent import CoreAgent
from utils import data_utils, report_utils

class SRSAgent(CoreAgent):
    def __init__(self):
        super().__init__()

    def generate_srs(self, diagram_data, identified_hazards, risk_assessment, srs_data):
        srs_prompt = f"""
            As a highly experienced Safety Instrumented Systems (SIS) engineer, generate a Safety Requirements Specification (SRS) document based on the following information:

            1. Process Diagram Description:
            {data_utils.format_data(diagram_data)}

             2. SIS System Description:
            {data_utils.format_data(srs_data)}

            3. Identified Hazards:
            {identified_hazards}

            4. Risk Assessment:
            {risk_assessment}

            Your Task:
             1. Analyze the provided information to identify Safety Instrumented Functions (SIFs). For each SIF:
                *   Define the safety function (what the system is supposed to do to prevent a hazardous event)
                *   Identify the initiating event that triggers the safety function
                *   Specify the required Safety Integrity Level (SIL) for the safety function. Based on risk level from the risk assessment and LOPA.
                *   Specify the performance requirements for the safety function, including the required response time.
                *   Identify the sensors involved (tag numbers, types, and location)
                *   Identify the logic solver used (PLC type)
                *   Identify the final elements (actuators) involved (tag numbers, types, and location)
                 *   Specify the testing requirements, including frequency and procedures.
                *   Identify any specific conditions for operation or restrictions.
                *    Include any requirements for redundancy and diagnostic capabilities.
             2. Base all findings on the information provided.
             3. Include all information in a structured and well formatted SRS report.
            4. If you are unable to determine any aspect from the provided information, then you must include a note saying "further information is required regarding (item)".
             5. Ensure that the SRS document is in a formal format that would be expected in the chemical process industry.

            Output:
             - The output should be a formal SRS document that includes all of the points listed above, in a well formatted way, using technical language.
            """
        try:
            response = self.model.generate_content(srs_prompt)
            srs_report = response.text
            report_utils.generate_pdf("srs_report.pdf", "Safety Requirements Specification (SRS)", srs_report)
            return srs_report
        except Exception as e:
            print(f"Error during SRS generation: {e}")
            return {"error": str(e)}
