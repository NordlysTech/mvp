from agent.core_agent import CoreAgent
from utils import data_utils, report_utils
class HAZOPAgent(CoreAgent):
    def __init__(self):
         super().__init__()
         self.hazop_guidewords = self.initialize_hazop_guidewords()

    def initialize_hazop_guidewords(self):
      return {
           "Pressure": ["HIGH", "LOW", "NO", "REVERSE"],
           "Temperature": ["HIGH", "LOW", "NO", "RATE OF INCREASE", "RATE OF DECREASE"],
           "Flow": ["HIGH", "LOW", "NO", "REVERSE", "INTERMITTENT", "PULSATING", "UNEVEN"],
           "Level": ["HIGH", "LOW", "NO", "OVERFLOW", "UNDERFLOW"],
           "Concentration": ["HIGH", "LOW", "NO", "OTHER"],
           "Composition": ["MORE", "LESS", "OTHER", "CONTAMINANT", "IMPURITY"],
           "Phase": ["MORE", "LESS", "OTHER", "LIQUID", "VAPOR", "SOLID"],
           "Vibration": ["HIGH", "LOW", "NO", "UNUSUAL"],
           "Function": ["NO", "MORE", "LESS", "PARTIAL", "DELAYED", "UNINTENDED"],
           "Refrigerant": ["LEAK", "MORE", "LESS", "CONTAMINATED"],
           "Integrity": ["COMPROMISED", "OK", "CORRODED", "ERODED"],
           "Viscosity": ["HIGH", "LOW", "NO", "UNUSUAL"],
           "Density": ["HIGH", "LOW", "NO", "UNUSUAL"],
           "pH": ["HIGH", "LOW", "NO", "OTHER"],
           "Electrical": ["HIGH", "LOW", "NO", "SHORT CIRCUIT", "OVERLOAD"],
           "Rotation": ["HIGH", "LOW", "NO", "REVERSE", "UNBALANCED"],
           "Speed": ["HIGH", "LOW", "NO", "ERRATIC"],
           "Position": ["WRONG", "MISALIGNED", "NO"],
           "Time": ["DELAYED", "EARLY", "TOO LONG", "TOO SHORT"],
           "Mixing": ["INADEQUATE", "EXCESSIVE", "NONE"],
           "Purge": ["INADEQUATE", "EXCESSIVE", "NONE"],
           "Inerting": ["INADEQUATE", "EXCESSIVE", "NONE"],
           "Cooling": ["INADEQUATE", "EXCESSIVE", "NONE"],
            "Heating": ["INADEQUATE", "EXCESSIVE", "NONE"],
           "Lubrication": ["INADEQUATE", "EXCESSIVE", "NONE"],
           "Isolation": ["INADEQUATE", "NONE", "PARTIAL"],
           "Sampling": ["WRONG", "CONTAMINATED", "NONE"],
           "Power": ["NO", "INTERMITTENT", "FLUCTUATING", "OVERVOLTAGE", "UNDERVOLTAGE"],
           "Signal": ["NO", "ERRATIC", "DELAYED", "INCORRECT"],
           "Control": ["NO", "ERRATIC", "INCORRECT", "FAILED"],
           "Containment": ["LEAK", "RUPTURE", "OVERFLOW"],
           "Alarm": ["NO", "DELAYED", "INCORRECT"],
            "Venting": ["INADEQUATE", "EXCESSIVE", "NONE"],
            "Material": ["WRONG", "CONTAMINATED", "INCOMPATIBLE"],
            "Environment": ["TOO HOT", "TOO COLD", "HUMID", "CORROSIVE"],
            "Human Action": ["WRONG", "OMITTED", "DELAYED"]
        }

    def generate_hazop_table(self, diagram_data, risk_assessment,identified_hazards):
      hazop_prompt = f"""
            As an expert in process safety, generate a detailed HAZOP (Hazard and Operability Study) table based on the following information:

            1. Process Diagram Description:
            {data_utils.format_data(diagram_data)}

            2. Risk Assessment:
            {risk_assessment}

            3. Identified Hazards:
            {identified_hazards}

            HAZOP Guidance:

            1. HAZOP Table Format:
            The HAZOP table will have the following columns:
               - **Node ID:** A unique identifier for the specific process area/node.
               - **Node Description:** A description of the specific location in the process.
               - **Parameter:** The specific process parameter being examined (e.g., Pressure, Temperature, Level, Flow, Composition, Integrity, Function).
               - **Guideword:** Standard HAZOP guidewords (e.g., HIGH, LOW, NO, MORE, LESS, REVERSE, OTHER). Choose from the following available guidewords, based on the parameter being analyzed: {data_utils.format_data(self.hazop_guidewords)}
                - **Deviation:** A specific deviation from the intended operation, based on the parameter and guideword selected. This is created by the guideword on the parameter.
               - **Possible Causes:** Potential reasons for the identified deviation. Based on the identified hazards from the previous step, and the type of equipment.
               - **Consequences:** The potential effects of the deviation on the process, personnel, or environment.
                -   **Existing Safeguards**: Any existing process controls or safety systems (e.g., PSVs, interlocks, alarms, procedures)
               - **Recommendations:** Suggest specific actions for risk mitigation
               - **Risk Ranking:** Rank the risk level using high, medium, and low classifications
               -   **Responsibility:** Identify which team or department (Operations, Engineering, Maintenance) is responsible for the recommendation.

            2. Parameter Selection:
            Select parameters based on the process, considering all potential hazards, for example a pipework integrity should consider "Integrity" as a parameter, and a control system should consider "Function".

            3. Guideword Application:
            Apply guidewords relevant to each parameter (e.g., for "Flow" consider "HIGH," "LOW," "NO" or "REVERSE").

            4. Deviation Generation:
            Generate realistic and specific deviations, for example a blocked pipe is not "High Pressure" it is "High Pressure due to Blockage".

           5. Existing Safeguard Identification:
                Use data from the risk assessment to identify suitable safety systems for each deviation.

            6. Risk Assessment Alignment:
            Use the risk assessment data to help inform the risk ranking. Use the existing likelihood and severity to inform this.

             7. Responsibility Allocation:
                Assign recommendations to the appropriate department, or team.

            8. Node Identification:
                Based on the diagram data, use the equipment descriptions to create a suitable node ID and node description.

            9. Use a table format, similar to an industry standard HAZOP table.

            Create a complete HAZOP table for the entire process, covering all parameters and nodes.
            """

      try:
           response = self.model.generate_content(hazop_prompt)
           hazop_table = response.text
           report_utils.generate_pdf("hazop_table.pdf", "HAZOP Table", hazop_table)
           return hazop_table
      except Exception as e:
         print(f"Error during HAZOP table generation {e}")
         return {"error": str(e)}
