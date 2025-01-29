from agent.core_agent import CoreAgent
from utils import data_utils, report_utils
import logging

class ControlPhilosophyAgent(CoreAgent):
    def __init__(self):
        super().__init__()

    def _identify_control_loops(self, diagram_data, control_data):
        prompt = f"""
            As an expert process control engineer, identify and describe all control loops present in the provided process diagram:

            1. Process Diagram Description:
            {data_utils.format_data(diagram_data)}

            2. Control System Data:
            {data_utils.format_data(control_data)}

             Your Task:
             1. Identify all control loops present in the system.
            2. Provide a tag number, the process parameter being controlled (e.g. pressure, temperature, flow, level, etc) and what the control objective is for each loop.
            3. Describe each control loop in detail, including the location of the instruments (sensor, controller, and final element).

           Output:
            - The output should be a structured report, with all of the identified control loops, including their tag numbers, process parameters, control objective and a detailed description.
           """
        return self.execute_step(prompt)

    def _identify_control_strategies(self, diagram_data, control_data):
        prompt = f"""
            As an expert process control engineer, identify and describe all control strategies used in the provided process diagram:

            1. Process Diagram Description:
           {data_utils.format_data(diagram_data)}

            2. Control System Data:
           {data_utils.format_data(control_data)}

            Your Task:
             1. Identify all control strategies used in the process (e.g. cascade, ratio, feedforward, override control, etc).
            2. Provide a detailed description of each control strategy, and explain why it has been selected for that part of the process.
            3. Use clear and concise technical language.

            Output:
             - The output should be a structured report, listing all identified control strategies, with a detailed description, including reasons for selection.
           """
        return self.execute_step(prompt)

    def _describe_loop_interactions(self, diagram_data, control_data):
       prompt = f"""
           As an expert process control engineer, analyze the provided information to describe the interaction between the different control loops:

           1. Process Diagram Description:
           {data_utils.format_data(diagram_data)}

           2. Control System Data:
           {data_utils.format_data(control_data)}

          Your Task:
            1. Describe how different control loops interact with each other.
           2. Explain how different loops affect each other, and if there are any dependencies.
           3. Explain any cascade control loops and their function.

          Output:
           -  The output should be a clear and concise description of the interactions between the different control loops.
           """
       return self.execute_step(prompt)

    def _explain_alarms_and_interlocks(self, diagram_data, control_data):
        prompt = f"""
            As an expert process control engineer, analyze the provided information to explain any alarm and interlock strategies:

            1. Process Diagram Description:
           {data_utils.format_data(diagram_data)}

            2. Control System Data:
           {data_utils.format_data(control_data)}

         Your Task:
           1. Explain any specific strategies for handling alarms or any interlocks.
          2. For each alarm or interlock, describe its purpose and what conditions activate it.
           3. Provide a detailed explanation of how the alarms will be used, and which alarms are most important.

         Output:
          - The output should be a detailed description of any alarms and interlocks and their specific purpose, including set points, actions, and which alarms are most important.
           """
        return self.execute_step(prompt)

    def _explain_control_system_operation(self, diagram_data, control_data):
         prompt = f"""
           As an expert process control engineer, provide an overview of how the control system operates:

           1. Process Diagram Description:
           {data_utils.format_data(diagram_data)}

            2. Control System Data:
           {data_utils.format_data(control_data)}

         Your Task:
           1. Clearly explain what the control system is designed to do, and how it operates in normal conditions.
           2. Explain how the system responds to common upset conditions and what actions will occur.
            3. Provide a high level overview of the control system to allow the reader to easily understand the basic operating principles.

         Output:
            -  The output should be an overview of how the control system operates, both in normal and upset conditions.
            """
         return self.execute_step(prompt)

    def generate_control_philosophy(self, diagram_data, control_data):
        control_loops = self._identify_control_loops(diagram_data, control_data)
        control_strategies = self._identify_control_strategies(diagram_data, control_data)
        loop_interactions = self._describe_loop_interactions(diagram_data, control_data)
        alarms_and_interlocks = self._explain_alarms_and_interlocks(diagram_data, control_data)
        control_system_operation = self._explain_control_system_operation(diagram_data, control_data)

        report_prompt = f"""
            As an expert process control engineer, generate a Control Philosophy document using the following information:

            1. Control Loops:
            {control_loops}

            2. Control Strategies:
            {control_strategies}

            3. Loop Interactions:
            {loop_interactions}

            4. Alarms and Interlocks:
            {alarms_and_interlocks}

            5. Control System Operation:
           {control_system_operation}

            Your Task:
               1. Combine the information provided into a single detailed control philosophy document.
              2. Include all key details of how the system is controlled.
              3. Present all of this information in a well formatted document that would be used by operators and engineers.

            Output:
             - The output should be a well formatted control philosophy document, using technical language, and including all of the items listed above.
            """
        try:
            response = self.model.generate_content(report_prompt)
            control_report = response.text
            report_utils.generate_pdf("control_philosophy.pdf", "Control Philosophy Report", control_report)
            return control_report
        except Exception as e:
            logging.error(f"Error during control philosophy report generation: {e}")
            return {"error": str(e)}
