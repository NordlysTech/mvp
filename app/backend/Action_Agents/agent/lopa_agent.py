from agent.core_agent import CoreAgent
from utils import data_utils, report_utils

class LOPAAgent(CoreAgent):
    def __init__(self):
        super().__init__()

    def _identify_initiating_events(self, diagram_data, identified_hazards, lopa_data):
        prompt = f"""
            As an expert process safety engineer, analyze the following information to identify and describe initiating events for a LOPA study:

            1. Process Diagram Description:
            {data_utils.format_data(diagram_data)}

            2. LOPA System Data:
            {data_utils.format_data(lopa_data)}

            3. Identified Hazards:
            {identified_hazards}

            Your Task:
            1. Identify specific initiating events that could lead to the hazardous consequences described.
            2. Provide a detailed technical description of each initiating event, focusing on what could happen in the process.
            3. If known, identify the frequency of the initiating event (per year). If a frequency is not available, provide a qualitative description of the likelihood of the initiating event occurring (e.g., rare, unlikely, possible, likely, almost certain).
           4. Provide your analysis in a structured format.

            Output:
              - The output should be a structured report that includes the initiating event, a description and the frequency (if known or a qualitative description)
        """
        return self.execute_step(prompt)

    def _analyze_ipls(self, diagram_data, lopa_data):
        prompt = f"""
            As an expert process safety engineer specializing in Layer of Protection Analysis (LOPA), analyze the following information to identify and categorize Independent Protection Layers (IPLs):

            1. Process Diagram Description:
            {data_utils.format_data(diagram_data)}

             2. LOPA System Data:
            {data_utils.format_data(lopa_data)}

            Your Task:
            1. Identify all independent protection layers (IPLs) that could mitigate the identified initiating events. An IPL is a device, system, or human action that is independent of the initiating event and is capable of preventing or mitigating the event consequences.
           2. Classify each IPL as either Prevention (reduces the likelihood of the initiating event) or Mitigation (reduces the severity of consequences of the event).
            3. For each IPL, clearly specify the type (e.g. basic process control system, safety instrumented system, pressure relief device, operator intervention, etc.).
           4. For each IPL, clearly specify the Probability of Failure on Demand (PFD), If a specific PFD is not available in the provided documentation, then provide a generic value with a clear note of where this generic value was obtained from (e.g. API 521, or IEC 61508).
           5. Provide your analysis in a structured format.

            Output:
              - The output should be a structured report, listing all identified IPLs, their classification, type, and PFD value, or the source of the generic PFD.
        """
        return self.execute_step(prompt)

    def _calculate_mitigated_likelihood(self, lopa_data, initiating_event_analysis, ipl_analysis):
       prompt = f"""
        As an expert in Layer of Protection Analysis (LOPA) perform a calculation for the mitigated event likelihood:

          1. Initiating Event Analysis
            {initiating_event_analysis}

          2. Independent Protection Layer Analysis:
            {ipl_analysis}

            Your Task:
            1. Calculate the mitigated event likelihood by multiplying the initiating event frequency by the PFD of all identified IPL's.
            2. If the information is not available to perform a quantitative calculation, provide a qualitative assessment based on the number and type of IPL's, and provide a clear disclaimer explaining why the calculation cannot be carried out.
          
          Output:
             - If calculated then provide the result.
             - If not calculated then provide the reasons, and a qualitative assessment.
            """
       return self.execute_step(prompt)


    def _determine_risk_reduction_requirements(self, risk_assessment, mitigated_likelihood_analysis):
        prompt = f"""
            As an expert in risk assessment and Layer of Protection Analysis (LOPA), determine the risk reduction requirements:

            1. Risk Assessment:
            {risk_assessment}

            2. Mitigated Event Likelihood Analysis:
            {mitigated_likelihood_analysis}

            Your Task:
              - Assess if the mitigated event likelihood meets the company's defined risk tolerance criteria, based on the risk level from the risk assessment.
             - Determine if additional risk reduction is required.
             - If it is determined that additional risk reduction is required, then provide recommendations for this.
           Output:
            -  The output should be a report stating if risk reduction is required and providing recommendations as required.
        """
        return self.execute_step(prompt)

    def _assess_consequences(self, diagram_data, identified_hazards):
        prompt = f"""
            As an expert process safety engineer, assess the consequences of an event based on the available information:

            1. Process Diagram Description:
            {data_utils.format_data(diagram_data)}

            2. Identified Hazards:
            {identified_hazards}

           Your Task:
              - Clearly and concisely describe the consequences of the hazardous event if all the IPL's were to fail, making reference to the available data.

            Output:
             - The output should be a description of the hazardous event, if all IPL's were to fail.
         """
        return self.execute_step(prompt)

    def _assess_human_factors(self, ipl_analysis):
       prompt = f"""
            As an expert process safety engineer specializing in human factors in process safety, assess the human factors of the identified IPL's based on the available information:

            1. Independent Protection Layer Analysis:
           {ipl_analysis}

           Your Task:
               - Identify any IPL's that rely on human actions (e.g. operator intervention, manual activation of a trip, testing/maintenance).
               - Assess the potential for human error for these IPL's.
              - Make recommendations for mitigation of human error (training, better procedures, changes to interfaces etc.)

           Output:
             - The output should be a human factors assessment, noting any IPL's that depend on a human action, the potential for human error, and any recommendations.
         """
       return self.execute_step(prompt)

    def _data_validation(self,diagram_data, lopa_data, initiating_event_analysis, ipl_analysis, mitigated_likelihood_analysis, risk_reduction_analysis, consequence_analysis, human_factors_analysis ):
        prompt = f"""
            As a data validation expert, review all data generated in the LOPA report and state any assumptions that have been made, and also state all sources of generic data used.

            1. Process Diagram Description:
             {data_utils.format_data(diagram_data)}

            2. LOPA system Data:
             {data_utils.format_data(lopa_data)}

            3. Initiating Event Analysis:
            {initiating_event_analysis}

           4. Independent Protection Layer Analysis:
            {ipl_analysis}

           5. Mitigated Likelihood Analysis:
            {mitigated_likelihood_analysis}

           6. Risk Reduction Analysis:
            {risk_reduction_analysis}

            7. Consequence Analysis:
            {consequence_analysis}

           8. Human Factors Analysis:
            {human_factors_analysis}

           Your Task:
              - Identify all assumptions that have been made during the generation of this report. This includes any assumptions on data that was missing, or any data that is based on a generic data source.
             - Provide details of any generic data sources that have been used (e.g. API 521 or IEC 61508, and specify the table or method used.)

           Output:
            -  The output should be a data validation report listing all assumptions and generic data sources used in the generation of the LOPA report.
            """
        return self.execute_step(prompt)

    def _generate_report(self, initiating_event_analysis, ipl_analysis, mitigated_likelihood_analysis, risk_reduction_analysis, consequence_analysis, human_factors_analysis, data_validation_analysis):
      prompt = f"""
           As an expert in report generation, generate a LOPA report based on the following analyses:

            1. Initiating Event Analysis:
            {initiating_event_analysis}

           2. Independent Protection Layer Analysis:
            {ipl_analysis}

            3. Mitigated Likelihood Analysis:
            {mitigated_likelihood_analysis}

            4. Risk Reduction Analysis:
            {risk_reduction_analysis}

            5. Consequence Analysis:
            {consequence_analysis}

            6. Human Factors Analysis:
            {human_factors_analysis}

            7. Data Validation:
           {data_validation_analysis}

           Your Task:
               Present the information in a structured table format with the following columns:
                  *   Initiating Event
                  *   Description of the event
                  *   Initiating Event Frequency (if available, or qualitative description)
                  *   Independent Protection Layers (include type, description and PFD)
                  *   Mitigated Event Likelihood (with supporting calculations or qualitative description)
                  *   Risk Reduction Assessment (State if risk reduction is required).
                  *   Consequence of Failure
                  *   Human Factor Assessment
                  *   Data Sources

            Output:
             -  The output should be a LOPA report, with all information in a structured table format, using technical language, and including all the items listed above.
         """
      return self.execute_step(prompt)

    def generate_lopa_report(self, diagram_data, identified_hazards, risk_assessment, lopa_data):
        initiating_event_analysis = self._identify_initiating_events(diagram_data, identified_hazards, lopa_data)
        ipl_analysis = self._analyze_ipls(diagram_data, lopa_data)
        mitigated_likelihood_analysis = self._calculate_mitigated_likelihood(lopa_data, initiating_event_analysis, ipl_analysis)
        risk_reduction_analysis = self._determine_risk_reduction_requirements(risk_assessment, mitigated_likelihood_analysis)
        consequence_analysis = self._assess_consequences(diagram_data, identified_hazards)
        human_factors_analysis = self._assess_human_factors(ipl_analysis)
        data_validation_analysis = self._data_validation(diagram_data, lopa_data, initiating_event_analysis, ipl_analysis, mitigated_likelihood_analysis, risk_reduction_analysis, consequence_analysis, human_factors_analysis )
        lopa_report = self._generate_report(initiating_event_analysis, ipl_analysis, mitigated_likelihood_analysis, risk_reduction_analysis, consequence_analysis, human_factors_analysis, data_validation_analysis )
        report_utils.generate_pdf("lopa_report.pdf", "Layer of Protection Analysis (LOPA)", lopa_report)
        return lopa_report
