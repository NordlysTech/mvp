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
    def analyze_diagram_valve(self, image_path):
        system_prompt = """
           As an expert Process Safety Engineer AI assistant, your role is to analyse the provided P&ID image, and identify all valves, and extract the required data for each valve.

           Your Task:
           1. Carefully examine the P&ID image, and identify each valve.
           2. For each valve, identify the valve tag, valve type (Ball, Globe, Gate, Butterfly, etc.).
           3. Identify the line number the valve is associated with.
            4. Identify if the valve is manual or automated. If it is automated, note the type of actuator (electric, pneumatic, hydraulic etc.)
            5. Where possible, identify the valve size and the valve rating from the P&ID.
           6. Output all data in a structured JSON format. If you are unable to identify any of the data then use "missing" as the value.
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
            "diagram_data": json.dumps(diagram_data),
            "identified_hazards": identified_hazards
        }

    def process_documents(self, file_paths):
        all_data = {}
        for file_path in file_paths:
           if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                 diagram_data = self.analyze_diagram(file_path)
                 if diagram_data and "error" not in diagram_data:
                     all_data['diagram_data'] = diagram_data
                     valve_data = self.analyze_diagram_valve(file_path)
                     if valve_data and "error" not in valve_data:
                        all_data['valve_data'] = valve_data
                     else:
                         print("Valve Data Not Available")
           else:
                with open(file_path, 'r') as file:
                    all_data['text_data']= file.read()
        return all_data

class ValveListExtractionAgent(CoreAgent):
    def __init__(self):
        super().__init__()

    def _identify_valves(self, diagram_data, valve_data):
        prompt = f"""
            As an expert process engineer, your role is to examine the provided P&ID image data, and identify all valve symbols and tags on the diagram.

             Process Diagram Data:
            {json.dumps(diagram_data, indent=2)}

            Valve Data:
            {json.dumps(valve_data, indent=2)}


           Your Task:
           1. Carefully examine the P&ID, identifying all valve symbols. Use the data from the diagram analysis, and the valve analysis to ensure the correct valves are identified.
           2. Record the Tag ID for each valve identified, and what type of valve it is (Ball valve, Butterfly valve etc.).

            Output:
             - The output should be a list of all of the valves identified, including their tag and their type.
           """
        return self.execute_step(prompt)

    def _extract_valve_details(self, valve_data, identified_valves):
         prompt = f"""
            As an expert process engineer, your role is to extract the relevant details of the identified valves from the provided P&ID data.

            Valve Data:
             {json.dumps(valve_data, indent=2)}

            Identified Valves:
             {identified_valves}

            Your Task:
            1. For each valve that has been identified, extract the following data:
                -  **Tag Number**: The unique identifier for the item (e.g. FV-101, PV-201, XV-301 etc)
                 -  **Type**: The type of valve (e.g. Ball Valve, Butterfly Valve, Globe Valve etc).
                 - **Size**: The size of the valve (e.g DN25, DN50, 1", 2" etc)
                 -  **Rating**: The pressure rating of the valve (e.g. PN16, PN25, 150#, 300# etc)
            2.  If any data is missing, then use a "-" in the field.

            Output:
             -  The output should be a structured table with the following columns:
              | Tag Number | Type | Size | Rating |
               If any data is missing, use a "-" in the corresponding field.
           """
         return self.execute_step(prompt)

    def _extract_valve_location_and_service(self, valve_data, identified_valves):
        prompt = f"""
            As an expert process engineer, your role is to extract the relevant location, line number and service from the provided P&ID diagram for each valve.

            Valve Data:
            {json.dumps(valve_data, indent=2)}

            Identified Valves:
             {identified_valves}

           Your Task:
            1. For each valve that has been identified, extract the following data:
                  - **Line Number**: The associated pipeline identifier.
                  - **Service**: A description of the service that the valve is performing (e.g. Isolation, Control, Relief).
                 -   **Location:** A description of the location of the valve (e.g. Main line, bypass, etc)
            2. If any data is missing, then use a "-" in the corresponding field.

           Output:
             - The output should be a structured table with the following columns:
              | Line Number | Service | Location |
               If any data is missing, use a "-" in the corresponding field.
           """
        return self.execute_step(prompt)

    def _extract_valve_automation(self, valve_data, identified_valves):
         prompt = f"""
            As an expert process control engineer, your role is to determine if a valve is manual or automated, and extract all relevant automation details.

            Valve Data:
            {json.dumps(valve_data, indent=2)}

            Identified Valves:
             {identified_valves}

            Your Task:
           1. Identify if the valve is manual or automated (including electrical, pneumatic or hydraulic).
            2. If the valve is automated, identify all details about its control system (if available). This includes the type of actuator (Pneumatic, electric), the type of control system, and any other available data.

            Output:
             - The output should be a structured table with the following columns:
              | Automation | Actuator Type | Control System |
                If any data is missing, use a "-" in the corresponding field.
           """
         return self.execute_step(prompt)

    def _generate_report(self, identified_valves, valve_details, valve_location_and_service, valve_automation):
        prompt = f"""
             As an expert in report generation, your task is to combine the data from the different analyses into a single structured report:

            Identified Valves:
            {identified_valves}

            Valve Details:
            {valve_details}

            Valve Location and Service:
            {valve_location_and_service}

            Valve Automation Data:
            {valve_automation}

          Your Task:
           1. Combine the data from the analyses above into a single well formatted report.
           2. Ensure all required data is included in the output.

           Output:
              - The output should be a structured table with the following columns:
                | Tag Number | Type | Size | Rating | Line Number | Service | Location | Automation | Actuator Type | Control System |
               If any data is missing, use a "-" in the corresponding field.
          """
        return self.execute_step(prompt)

    def generate_valve_list(self, diagram_data, valve_data):
       identified_valves = self._identify_valves(diagram_data, valve_data)
       valve_details = self._extract_valve_details(valve_data, identified_valves)
       valve_location_and_service = self._extract_valve_location_and_service(valve_data, identified_valves)
       valve_automation = self._extract_valve_automation(valve_data, identified_valves)
       valve_list = self._generate_report(identified_valves, valve_details, valve_location_and_service, valve_automation)
       return valve_list

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
    valve_agent = ValveListExtractionAgent()
    image_path = r"C:\Users\yuris\Downloads\vision models\Safety_Risk_Agent_EcoSystem - Copy\images\P&ID LNG Kollsnes II System 25 - GASSKONDENSERING-1.png"

    diagram_data = core_agent.analyze_diagram(image_path)
    valve_data = core_agent.analyze_diagram_valve(image_path)
    all_data = {}
    all_data['diagram_data']=diagram_data
    all_data['valve_data'] = valve_data
    if diagram_data and "error" not in diagram_data and valve_data and "error" not in valve_data :
         valve_list = valve_agent.generate_valve_list(all_data['diagram_data'], all_data['valve_data'])
         print("Valve List:")
         print(valve_list)
         generate_pdf("valve_list_024.pdf","Valve List_024", valve_list)
    else:
        print("Could not load the diagram")
    with open("valve_list_024.txt", "w") as f:
      f.write(valve_list)