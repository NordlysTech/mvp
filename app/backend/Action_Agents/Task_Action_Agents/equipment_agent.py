import google.generativeai as genai
import os
from dotenv import load_dotenv
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import httpx
import json
import logging

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CoreAgent:
    def __init__(self):
      self.model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

    def analyze_diagram(self, image_path):
        system_prompt = """
        As an expert Process Safety Engineer AI assistant, analyze the provided PFD or P&ID image. Focus on identifying key elements, their relationships, and process safety implications. Provide a structured output in JSON format with the following:

        1. Equipment: List major items (e.g., reactors, columns, heat exchangers)
           - Include visible specifications (e.g., MAWP, design temperature)
           - Identify critical equipment and safety implications
        2. Instruments: List key instruments (e.g., flow meters, temperature sensors)
           - Specify types and roles in process control and safety
        3. Pipelines: Describe main process streams
           - Identify compositions, phases, and potential hazards
           - Note critical pipe specifications
        4. Control Systems: Identify control loops and purposes
           - Analyze adequacy for safe operations
           - Identify advanced control strategies
        5. Safety Systems: List visible safety-related equipment
           - Assess placement and potential effectiveness
        6. Process Conditions: Infer process conditions
           - Highlight extreme or unusual conditions
        7. Hazardous Areas: Identify potential hazardous area classifications
        8. Material Handling: Analyze material input, output, and storage systems
        9. Utility Systems: Identify utility systems
        10. Overall Process Description: Summarize process flow, purpose, and critical safety aspects

        Base your analysis solely on the image. Indicate if aspects are unclear. Provide insights into potential process hazards based on the observed configuration and conditions.
        """

        try:
            if image_path.startswith("http://") or image_path.startswith("https://"):
                image = httpx.get(image_path)
                image_data = image.content
            else:
                with open(image_path, "rb") as image_file:
                   image_data = image_file.read()
            image_base64 = base64.b64encode(image_data).decode("utf-8")

        except Exception as e:
            print(f"Error loading image: {e}")
            return {"error": "Could not load image"}

        prompt = f"{system_prompt} Analyze this P&ID diagram."

        try:
            response = self.model.generate_content([
                {'mime_type':'image/jpeg', 'data': image_base64},
                 prompt
            ])
            output_text = response.text
            try:
                return json.loads(output_text)
            except json.JSONDecodeError:
                return {"raw_output": output_text}
        except Exception as e:
            print(f"Error during vision analysis: {e}")
            return {"error": str(e)}
    def analyze_diagram_equipment(self, image_path):
        system_prompt = f"""
           As an expert process engineer specializing in analyzing Piping and Instrumentation Diagrams (P&IDs), your task is to analyze the provided P&ID image and focus solely on extracting information about equipment. Provide the output in a structured JSON format with the following:

            Your Task:
            1. Identify all equipment items on the diagram.
            2. For each item, identify the Tag ID, the type of equipment (reactor, pump, valve, separator, heat exchanger etc) and any specifications for the equipment (e.g. MAWP, Design Temperature, Size)
           3. Also, for each item, provide any notes on safety implications.

           All data must be returned in a structured JSON format. If you are unable to identify any of the data then use "missing" as the value.
        """

        try:
            if image_path.startswith("http://") or image_path.startswith("https://"):
                image = httpx.get(image_path)
                image_data = image.content
            else:
                with open(image_path, "rb") as image_file:
                   image_data = image_file.read()
            image_base64 = base64.b64encode(image_data).decode("utf-8")

        except Exception as e:
            print(f"Error loading image: {e}")
            return {"error": "Could not load image"}

        prompt = f"{system_prompt} Analyze this P&ID diagram."

        try:
            response = self.model.generate_content([
                {'mime_type':'image/jpeg', 'data': image_base64},
                 prompt
            ])
            output_text = response.text
            try:
                return json.loads(output_text)
            except json.JSONDecodeError:
                return {"raw_output": output_text}
        except Exception as e:
            print(f"Error during valve analysis: {e}")
            return {"error": str(e)}
    def execute_step(self, prompt):
         try:
            response = self.model.generate_content(prompt)
            if response.text:
               return response.text
            else:
                return "The AI Model Returned an Empty Response"
         except Exception as e:
            print(f"Error in execution step: {e}")
            return  {"error": str(e)}


    def prepare_base_data(self, diagram_data, identified_hazards):
        """Prepare base data for risk assessment and report generation."""
        return {
            "diagram_data": json.dumps(diagram_data, indent=2),
            "identified_hazards": identified_hazards
        }

    def process_documents(self, file_paths):
        all_data = {}
        for file_path in file_paths:
           if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                 diagram_data = self.analyze_diagram(file_path)
                 if diagram_data and "error" not in diagram_data:
                     all_data['diagram_data'] = diagram_data
                     equipment_data = self.analyze_diagram_equipment(file_path)
                     if equipment_data and "error" not in equipment_data:
                        all_data['equipment_data'] = equipment_data
                     else:
                        print("Equipment Data Not Available")
           else:
                with open(file_path, 'r') as file:
                    all_data['text_data']= file.read()
        return all_data

class EquipmentAgent(CoreAgent):
    def __init__(self):
        super().__init__()
        self.predefined_equipment = self.initialize_predefined_equipment()

    def initialize_predefined_equipment(self):
         return [
             "Reactor", "Distillation Column", "Absorption Column", "Stripping Column", "Heat Exchanger", "Shell and Tube Heat Exchanger", "Plate Heat Exchanger",
            "Air Cooled Heat Exchanger", "Reboiler", "Condenser", "Evaporator", "Cooling Tower", "Storage Tank", "Mixer", "Agitator",
            "Pump", "Centrifugal Pump", "Positive Displacement Pump", "Reciprocating Pump", "Gear Pump", "Vacuum Pump", "Compressor",
            "Centrifugal Compressor", "Reciprocating Compressor", "Screw Compressor", "Blower", "Separator", "Gravity Separator",
            "Cyclone Separator", "Filter", "Bag Filter", "Cartridge Filter", "Screen", "Distillation Tray", "Packing Material",
            "Demister", "Coalescer", "Dryer", "Fluid Bed Dryer", "Rotary Dryer", "Spray Dryer", "Crystallizer", "Evaporator",
             "Extruder", "Granulator", "Pelletizer", "Centrifuge", "Decanter", "Mixer Settler", "Adsorber", "Desorber", "Stripper",
             "Scrubber", "Absorber", "Distributor", "Nozzle", "Injector", "Ejector", "Vessel", "Drum", "Silo", "Hopper",
            "Conveyor", "Belt Conveyor", "Screw Conveyor", "Pneumatic Conveyor", "Bucket Elevator", "Feeder", "Rotary Valve",
            "Gate Valve", "Butterfly Valve", "Globe Valve", "Ball Valve", "Check Valve", "Control Valve", "Pressure Relief Valve",
             "Rupture Disc", "Flame Arrestor", "Flame Detector", "Gas Detector", "Level Gauge", "Pressure Gauge", "Temperature Gauge",
            "Flow Meter", "Orifice Plate", "Venturi Meter", "Magnetic Flow Meter", "Ultrasonic Flow Meter", "Actuator", "Transmitter",
             "Controller", "PLC", "DCS", "Analyzer", "Sample Point", "Solenoid Valve", "Manual Valve", "Safety Valve", "Emergency Shutdown Valve", "Sight Glass", "Vibration Sensor", "Thermocouple", "RTD"
         ]

    def _identify_equipment(self, diagram_data, equipment_data):
        prompt = f"""
           As an expert process engineer, your role is to extract a detailed list of all equipment items from the given process diagram description.

            Process Diagram Description:
            {json.dumps(diagram_data, indent=2)}

            Equipment Data:
            {json.dumps(equipment_data, indent=2)}

            Your Task:
            1. Identify each item of equipment on the diagram, and make note of the tag ID for each item (e.g. R-101, P-102, V-103 etc). Use the data from both the diagram analysis, and the equipment analysis.
            2. Identify the type of equipment and provide a brief description, use this list of common equipment types to ensure a complete list: {self.predefined_equipment}.

            Output:
             - The output should be a structured report that contains a list of all the equipment, including tag and type.
          """
        return self.execute_step(prompt)

    def _extract_specifications(self, diagram_data, identified_equipment, equipment_data):
        prompt = f"""
           As an expert process engineer, your role is to extract the specifications for the identified equipment, from the diagram data.

            Process Diagram Data:
            {json.dumps(diagram_data, indent=2)}

             Equipment Data:
            {json.dumps(equipment_data, indent=2)}

            Identified Equipment:
            {identified_equipment}

            Your Task:
            1. For each item of equipment that has been identified, extract the following data, where available:
                -   Specifications (e.g. MAWP, Design Temperature, Size). Use the data from both sources if possible.
           2. If any data is missing, then use a "-" in the corresponding field.
            Output:
              - The output should be a structured table with the following columns, for each item of equipment:
             | Specifications |
              If any data is missing then use a "-" in the relevant field.
           """
        return self.execute_step(prompt)

    def _extract_safety_implications(self, diagram_data, identified_equipment, equipment_data):
       prompt = f"""
          As an expert process safety engineer, your role is to identify any safety implications for each item of equipment.

            Process Diagram Data:
            {json.dumps(diagram_data, indent=2)}

             Equipment Data:
            {json.dumps(equipment_data, indent=2)}

            Identified Equipment:
            {identified_equipment}

            Your Task:
            1. For each item of equipment that has been identified, extract the following data, where available:
                -   Any safety implications for the equipment, or a description of what it is designed to do to keep the system safe. Use the data from both the diagram data and the equipment data.
           2. If any data is missing, then use a "-" in the corresponding field.

           Output:
              - The output should be a structured table with the following columns, for each item of equipment:
              |  Safety Implications |
               If any data is missing then use a "-" in the relevant field.
           """
       return self.execute_step(prompt)

    def _generate_report(self, identified_equipment, specifications, safety_implications):
        prompt = f"""
             As an expert in report generation, your task is to combine the data from the different analyses into a single structured report:

            Identified Equipment:
            {identified_equipment}

            Equipment Specifications:
            {specifications}

            Equipment Safety Implications:
             {safety_implications}

           Your Task:
            1. Combine all of the data into a single, well-formatted, and structured report.

           Output:
              - The output should be a well structured report with the following columns:
                | Tag | Type | Specifications | Safety Implications |
               If any data is missing then use a "-" in the corresponding field.
           """
        return self.execute_step(prompt)


    def generate_equipment_list(self, diagram_data, equipment_data):
        identified_equipment = self._identify_equipment(diagram_data, equipment_data)
        specifications = self._extract_specifications(diagram_data, identified_equipment, equipment_data)
        safety_implications = self._extract_safety_implications(diagram_data, identified_equipment, equipment_data)
        equipment_list = self._generate_report(identified_equipment, specifications, safety_implications)
        return equipment_list
def generate_pdf(filename, title, content):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Add title
        story.append(Paragraph(title, styles['Title']))
        
        # Add content
        if isinstance(content, dict):
            story.append(Paragraph(json.dumps(content, indent=2), styles['BodyText']))
        elif isinstance(content,str):
            for paragraph in content.split('\n\n'):
                story.append(Paragraph(paragraph, styles['BodyText']))

        doc.build(story)

# Usage
if __name__ == "__main__":
    core_agent = CoreAgent()
    equipment_agent = EquipmentAgent()
    image_path = r"C:\Users\yuris\Downloads\vision models\Task_Action_EcoSystem\images\PID qwen 2.png"

    diagram_data = core_agent.analyze_diagram(image_path)
    equipment_data = core_agent.analyze_diagram_equipment(image_path)

    all_data = {}
    all_data['diagram_data']=diagram_data
    all_data['equipment_data']=equipment_data


    if diagram_data and "error" not in diagram_data and equipment_data and "error" not in equipment_data:
         equipment_list = equipment_agent.generate_equipment_list(all_data['diagram_data'], all_data['equipment_data'])
         print("Equipment List:")
         print(equipment_list)
         generate_pdf("equipment_list_005.pdf","Equipment List_005", equipment_list)
    else:
        print("Could not load the diagram")

    with open("equipment_list_005.txt", "w") as f:
      f.write(equipment_list)