from agent.core_agent import CoreAgent
from utils import data_utils, report_utils

class PSIAgent(CoreAgent):
    def __init__(self):
        super().__init__()

    def identify_hazards(self, diagram_data):
        predefined_hazards = self.initialize_predefined_hazards()
        hazard_prompt = f"""
            As an expert in process safety and chemical engineering, analyze the following process diagram description to identify potential hazards and safety considerations:

            Process Diagram Description:
            {data_utils.format_data(diagram_data)}

            Predefined Hazard Types:
            {predefined_hazards}

            Conduct a comprehensive hazard identification analysis. For each identified hazard:
            1. Select the most appropriate hazard type from the predefined list above. Do not create new hazard types or use process elements as hazards.
            2. Provide a detailed, technical description of the hazard as it relates to the specific process described.
            3. Analyze potential consequences, including domino effects and worst-case scenarios.
            4. Identify the specific associated equipment, process area, or operational phase where this hazard could occur.
            5. Discuss the underlying causes and contributing factors, referencing relevant chemical or physical principles.
            6. Evaluate the potential for escalation and impact on adjacent processes or facilities.
            7. Consider the implications for process safety management systems, citing relevant industry standards or best practices.

            Organize your analysis by process units or operational areas. Pay special attention to:
            - Specific chemical reactivity and incompatibility issues, citing relevant reaction mechanisms or kinetics.
            - Detailed process deviations and their potential consequences, referencing process control theory.
            - Potential for loss of containment scenarios, including failure modes and effects analysis.
            - Human factors and procedural risks, considering cognitive ergonomics and human reliability analysis.
            - Interconnected risks between different process units, applying systems thinking.

            Provide your assessment in a structured format, using technical language appropriate for a professional chemical engineering audience. Include quantitative estimates where possible (e.g., potential release rates, explosion overpressures, toxic exposure levels).

            Remember to only use hazard types from the predefined list. If you encounter a potential issue that doesn't fit neatly into one of these categories, select the most closely related hazard type and explain the specific nature of the hazard in your description.
            """

        try:
            response = self.model.generate_content(hazard_prompt)
            hazards = response.text
            report_utils.generate_pdf("identified_hazards.pdf", "Identified Hazards", hazards)
            return hazards
        except Exception as e:
            print(f"Error during hazard identification {e}")
            return {"error": str(e)}
        
    def initialize_predefined_hazards(self):
        return [
            "Loss of Containment",
            "Fire",
            "Explosion",
            "Toxic Release",
            "Runaway Reaction",
            "Overpressurization",
            "Underpressurization",
            "High Temperature Excursion",
            "Low Temperature Excursion",
            "Chemical Incompatibility",
            "Corrosion",
            "Erosion",
            "Mechanical Failure",
            "Instrumentation Failure",
            "Control System Failure",
            "Utility Failure",
            "Human Error",
            "Inadequate Isolation",
            "Inadequate Purging",
            "Inadequate Venting",
            "Static Electricity Accumulation",
            "Dust Explosion",
            "Confined Space Hazards",
            "Falling Objects",
            "Slips, Trips, and Falls",
            "Ergonomic Hazards",
            "Noise Hazards",
            "Vibration Hazards",
            "Radiation Hazards",
            "Electrical Hazards",
            "Thermal Hazards (Burns)",
            "Asphyxiation",
            "Flammable Atmosphere",
            "Toxic Atmosphere",
            "Oxygen Deficiency",
            "Oxygen Enrichment",
            "Pressure Vessel Failure",
            "Pipeline Failure",
            "Pump Cavitation",
            "Compressor Surge",
            "Valve Malfunction",
            "Relief Device Failure",
            "Heat Exchanger Fouling",
            "Reactor Fouling",
            "Column Flooding",
            "Column Weeping",
            "Distillation Instability",
            "Crystallization",
            "Polymerization",
            "Decomposition",
            "Side Reactions",
            "Catalyst Deactivation",
            "Inadequate Mixing",
            "Phase Separation",
            "Foaming",
            "Scaling",
            "Plugging",
            "Leaching",
            "Material Degradation",
            "Brittle Fracture",
            "Fatigue Failure",
            "Stress Corrosion Cracking",
            "Thermal Shock",
            "Vibration-Induced Failure",
            "Improper Material Selection",
            "Improper Equipment Design",
            "Inadequate Maintenance",
            "Inadequate Inspection",
            "Inadequate Testing",
            "Inadequate Training",
            "Inadequate Procedures",
            "Inadequate Communication",
            "External Impact (e.g., Vehicle Collision)",
            "Natural Disasters (e.g., Earthquake, Flood)",
            "Sabotage or Terrorism",
            "Domino Effects from Adjacent Facilities"
        ]
