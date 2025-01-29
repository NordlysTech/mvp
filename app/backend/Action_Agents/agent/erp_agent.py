from agent.core_agent import CoreAgent
from utils import data_utils, report_utils

class ERPAgent(CoreAgent):
    def __init__(self):
        super().__init__()

    def _identify_emergency_scenarios(self, diagram_data, identified_hazards, erp_data):
        prompt = f"""
            As an expert in emergency response planning, identify and describe potential emergency scenarios based on the available information.

            1. Process Diagram Description:
            {data_utils.format_data(diagram_data)}

             2. ERP System Data:
            {data_utils.format_data(erp_data)}

            3. Identified Hazards:
            {identified_hazards}

             Your Task:
             1. Identify potential emergency scenarios based on the available data. This includes but is not limited to, fires, explosions, releases of hazardous substances, or any other process upsets.
            2. Provide a detailed description of each scenario and its potential impact on the plant, personnel, and the environment.

             Output:
              - The output should be a structured report listing potential emergency scenarios with detailed descriptions.
        """
        return self.execute_step(prompt)

    def _define_evacuation_procedures(self, diagram_data, erp_data):
        prompt = f"""
          As an expert in emergency response planning, create a set of evacuation procedures:

            1. Process Diagram Description:
            {data_utils.format_data(diagram_data)}

             2. ERP System Data:
            {data_utils.format_data(erp_data)}

           Your Task:
            1. Identify suitable evacuation routes based on the location of the emergency scenarios.
            2. Provide detailed instructions on how personnel will safely evacuate in case of an incident, including a primary route and any secondary routes.
            3. Identify the locations of assembly points.
            4. Consider all available information (including location of emergency exits, any equipment and the type of hazards).

           Output:
             - The output should be a detailed description of the evacuation procedures, including routes and assembly points.
        """
        return self.execute_step(prompt)

    def _allocate_resources(self, diagram_data, erp_data):
         prompt = f"""
            As an expert in emergency response, determine the resources that will be needed in an emergency, based on the available information:

            1. Process Diagram Description:
            {data_utils.format_data(diagram_data)}

             2. ERP System Data:
            {data_utils.format_data(erp_data)}

          Your Task:
           1. Based on the different scenarios and the available information, identify all resources required for an emergency event.
           2. Identify personnel, fire fighting equipment, spill control material, first aid equipment, communication equipment, rescue equipment.
           3. If location data is available, provide location information as well.

          Output:
            - The output should be a detailed list of resources and locations.
           """
         return self.execute_step(prompt)

    def _define_communication_protocols(self, diagram_data, erp_data):
       prompt = f"""
           As an expert in emergency response planning, define the required communication protocols, based on the available information:

            1. Process Diagram Description:
           {data_utils.format_data(diagram_data)}

            2. ERP System Data:
           {data_utils.format_data(erp_data)}

         Your Task:
            1. Describe how communication will be managed during an emergency.
            2. Define the process for internal communication (to all personnel) and external communications (to emergency responders and regulators)
            3. Specify what communication equipment will be used, including radios, telephone, alarms, public address systems.
            4. Clearly define who should be contacted in an emergency, and what information will be relayed.

            Output:
             - The output should be a set of communication protocols that can be used in an emergency event.
           """
       return self.execute_step(prompt)

    def _identify_key_personnel(self, diagram_data, erp_data):
        prompt = f"""
           As an expert in emergency response planning, identify the key personnel involved in an emergency, based on the available information.

            1. Process Diagram Description:
           {data_utils.format_data(diagram_data)}

             2. ERP System Data:
            {data_utils.format_data(erp_data)}

         Your Task:
           1. Based on the available data and process flow, identify personnel that will have a key role in an emergency situation (Incident Commander, Fire Marshall, First Aiders, etc.)
          2. Describe each of the roles and their responsibilities.
          3. If information is available, specify their location, and contact details.

           Output:
             - The output should be a description of key personnel, their roles, responsibilities, and contact details (if available).
            """
        return self.execute_step(prompt)


    def generate_erp_report(self, diagram_data, identified_hazards, erp_data):
        emergency_scenarios = self._identify_emergency_scenarios(diagram_data, identified_hazards, erp_data)
        evacuation_procedures = self._define_evacuation_procedures(diagram_data, erp_data)
        resource_allocation = self._allocate_resources(diagram_data, erp_data)
        communication_protocols = self._define_communication_protocols(diagram_data, erp_data)
        key_personnel = self._identify_key_personnel(diagram_data, erp_data)


        report_prompt = f"""
            As an expert in emergency response planning, compile a detailed emergency response plan using the following information:

             1. Emergency Scenarios:
             {emergency_scenarios}

            2. Evacuation Procedures:
             {evacuation_procedures}

            3. Resource Allocation:
             {resource_allocation}

           4. Communication Protocols:
            {communication_protocols}

           5. Key Personnel:
             {key_personnel}

          Your Task:
               1. Combine the information provided into a single detailed emergency response plan that would be suitable for use in a process plant.
              2. Include all key details, and all aspects of an emergency response that are required to mitigate the impact of a hazardous event.
              3. Present all of this information in a well formatted document that would be used by operators.

              Output:
              -  The output should be a well formatted emergency response plan, using technical language, and including all of the items listed above.
          """

        try:
           response = self.model.generate_content(report_prompt)
           erp_report = response.text
           report_utils.generate_pdf("erp_report.pdf", "Emergency Response Plan (ERP)", erp_report)
           return erp_report
        except Exception as e:
           print(f"Error during LOPA report generation: {e}")
           return {"error": str(e)}
