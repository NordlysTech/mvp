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
    def analyze_diagram_line(self, image_path):
        system_prompt = f"""
           As an expert Process Safety Engineer AI assistant, your role is to analyse the provided P&ID image, and identify all pipelines, and extract the required data for each pipe.

           Your Task:
            1. Carefully examine the P&ID image, and identify each pipeline.
            2. For each pipeline, identify the line number, the pipe size, the fluid in the pipe, the material of construction, and design pressure and temperature.
           3. Output all data in a structured JSON format. If you are unable to identify any of the data then use "missing" as the value.
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
                     line_data = self.analyze_diagram_line(file_path)
                     if line_data and "error" not in line_data:
                         all_data['line_data'] = line_data
                     else:
                          print("Line Data Not Available")
           else:
                with open(file_path, 'r') as file:
                    all_data['text_data']= file.read()
        return all_data

class LineListExtractionAgent(CoreAgent):
    def __init__(self):
        super().__init__()

    def _identify_pipelines(self, line_data):
        prompt = f"""
           As an expert process engineer, your role is to carefully examine the provided P&ID diagram data and identify all pipeline elements.

             Piping Diagram Data:
            {json.dumps(line_data, indent=2)}

           Your Task:
           1. Carefully examine the P&ID, identifying all pipelines.
            2. Identify the line numbers and include a description of the type of pipeline (process, utility, drain etc).

            Output:
             - The output should be a list of all identified pipelines, including their line numbers and a description.
           """
        return self.execute_step(prompt)

    def _extract_line_specifications(self, line_data, identified_pipelines):
            prompt = f"""
            As an expert process engineer, your role is to extract the specifications from the identified pipelines, from the provided P&ID diagram.

            Piping Diagram Data:
                {json.dumps(line_data, indent=2)}

            Identified Pipelines:
                {identified_pipelines}

            Your Task:
            1. For each identified pipeline extract the following data:
                - Line Number: The unique identifier of the pipeline. When extracting the line number from the diagram data, make sure to extract any characters that indicate the material (e.g. "SS" for stainless steel, or "CS" for carbon steel, "CRA" for corrosion resistant alloy), include this as part of the line number.
                - Pipe Size: The nominal pipe size (e.g., DN50, 2", 4" etc).
                - Material: The material of construction of the pipe (e.g. Carbon Steel, Stainless Steel, Copper, PVC). If the material is present in the line number (e.g. SS, CS, CU, PVC, CRA), then use that as the material of construction. Use the following list of abbreviations to help you identify the materials: 
                - CS: Carbon Steel,
                - SS: Stainless Steel,
                    - CU: Copper,
                    - PVC: Polyvinyl Chloride,
                    - CRA: Corrosion-Resistant Alloy
                    - If a material can not be identified by one of these methods, then set the value to "-"
                - Fluid: The fluid being transported by the pipeline.
                    - Design Pressure: The design pressure of the pipe.
                    - Design Temperature: The design temperature of the pipe.

                2. If any information is missing use a "-".

            Output:
                - The output should be a structured table with the following columns:
                | Line Number | Pipe Size | Material | Fluid | Design Pressure | Design Temperature |
                    If any data is missing use a "-" in the corresponding field.
            """
            return self.execute_step(prompt)

    def _generate_report(self,identified_pipelines, line_specifications):
        prompt = f"""
            As an expert in report generation, your task is to create a line list report, based on the available analyses:

           Identified Pipelines:
            {identified_pipelines}

            Pipe Specifications:
             {line_specifications}


           Your Task:
            1. Combine all of the data into a single, well-formatted, and structured report.

            Output:
              - The output should be a structured table with the following columns:
              | Line Number |  Description | Pipe Size | Material | Fluid | Design Pressure | Design Temperature |
              If any data is missing use a "-" in the corresponding field.
           """
        return self.execute_step(prompt)

    def generate_line_list(self, diagram_data, line_data):
       identified_pipelines = self._identify_pipelines(line_data)
       line_specifications = self._extract_line_specifications(line_data, identified_pipelines)
       line_list = self._generate_report(identified_pipelines, line_specifications)
       return line_list

def generate_pdf(filename, title, content):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Add title
        story.append(Paragraph(title, styles['Title']))
        
        # Add content
        for paragraph in content.split('\n\n'):
            story.append(Paragraph(paragraph, styles['BodyText']))

        doc.build(story)

# Usage
if __name__ == "__main__":
    core_agent = CoreAgent()
    line_agent = LineListExtractionAgent()
    image_path = r"C:\Users\yuris\Downloads\vision models\Task_Action_EcoSystem\images\P&ID LNG Kollsnes II System 25 - GASSKONDENSERING-1.png"

    diagram_data = core_agent.analyze_diagram(image_path)
    line_data = core_agent.analyze_diagram_line(image_path)

    all_data = {}
    all_data['diagram_data']=diagram_data
    all_data['line_data']=line_data

    if diagram_data and "error" not in diagram_data and line_data and "error" not in line_data:
         line_list = line_agent.generate_line_list(all_data['diagram_data'], all_data['line_data'])
         print("Line List:")
         print(line_list)
         generate_pdf("line_list_006.pdf","Line List_006", line_list)
    else:
        print("Could not load the diagram")
    with open ("line_list_006.txt", "w") as f:
         f.write(line_list)