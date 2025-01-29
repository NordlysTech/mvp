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
    def analyze_diagram_instrument(self, image_path):
        system_prompt = """
        As an expert Process Control Engineer AI assistant specializing in analyzing Piping and Instrumentation Diagrams (P&IDs), your task is to analyze the provided P&ID image. Focus solely on identifying all instruments, their types, and their locations, and any other relevant control or instrumentation aspects. Provide a structured output in JSON format with the following:

       1. Instruments: List key instruments (e.g., flow meters, temperature sensors, pressure sensors, level switches, control valves, PSV's)
           - For each instrument specify the tag, type, line number, P&ID number, service, description, location, size, rating, design pressure and temperature, min range, max range, unit, accuracy, remarks, status.
        2. Control Systems: Identify control loops and purposes
           - Analyze adequacy for safe operations
           - Identify advanced control strategies
        3. Safety Systems: List visible safety-related equipment
           - Assess placement and potential effectiveness

       Base your analysis solely on the image. Indicate if aspects are unclear.
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
                     instrument_data = self.analyze_diagram_instrument(file_path)
                     if instrument_data and "error" not in instrument_data:
                        all_data['instrument_data'] = instrument_data
                     else:
                        print("Instrument Data Not Available")
           else:
                with open(file_path, 'r') as file:
                    all_data['text_data']= file.read()
        return all_data

class InstrumentAgent(CoreAgent):
    def __init__(self):
        super().__init__()

    def _identify_instruments(self, diagram_data, instrument_data):
        prompt = f"""
           As an expert Process Control Engineer AI assistant specializing in analyzing Piping and Instrumentation Diagrams (P&IDs), your task is to carefully examine the provided P&ID image data and generate a list of all instruments.

             Process Diagram Data:
            {json.dumps(diagram_data, indent=2)}

            Instrument Data:
            {json.dumps(instrument_data, indent=2)}

           Your Task:
           1. Scan the entire P&ID thoroughly, identifying all instruments and valves. Use the data from both the diagram data and the instrument data, when performing your analysis.
            2. Pay close attention to labels, annotations, and symbols used in the diagram.
            3. List all items that are identified as being instruments or valves.

             Output:
              - The output should be a structured report, listing all instruments and valves that can be identified in the P&ID data. This must include the tag of each item and their type.
           """
        return self.execute_step(prompt)

    def _extract_tag_and_pid(self, instrument_data, identified_instruments):
        prompt = f"""
           As an expert process control engineer, your role is to extract the Tag Number and P&ID Number of the identified instruments from the P&ID diagram data.

            Process Diagram Data:
             {json.dumps(instrument_data, indent=2)}

             Identified Instruments:
            {identified_instruments}

           Your Task:
            1. For each instrument and valve that has been identified, extract the following data:
                 - **Tag Number**: The unique identifier for the item (e.g., FIC-101, PV-201).
                - **P&ID Number**: The document number or reference of the P&ID.
            2. If any data is missing, then you must use a "-" in the corresponding field.

            Output:
              - The output should be a well structured table with the following columns:
             | Tag Number | P&ID Number |
              If any data is missing then put "-" in the relevant field.
           """
        return self.execute_step(prompt)
    def _extract_service_description(self, instrument_data, identified_instruments):
        prompt = f"""
           As an expert process control engineer, your role is to extract the Service and Description data of the identified instruments from the P&ID diagram data.

            Process Diagram Data:
             {json.dumps(instrument_data, indent=2)}

             Identified Instruments:
            {identified_instruments}

           Your Task:
            1. For each instrument and valve that has been identified, extract the following data:
                - **Service**: The function or service performed (e.g., Flow Control, Pressure Relief).
                 - **Description**: A clear description of the item, including type and key characteristics.
            2. If any data is missing, then you must use a "-" in the corresponding field.

            Output:
              - The output should be a well structured table with the following columns:
              | Service | Description |
               If any data is missing then put "-" in the relevant field.
           """
        return self.execute_step(prompt)

    def _extract_pipe_details(self, instrument_data, identified_instruments):
           prompt = f"""
            As an expert process control engineer, your role is to extract the Line Number and Pipe Size of the identified instruments from the P&ID diagram data.

            Process Diagram Data:
            {json.dumps(instrument_data, indent=2)}

            Identified Instruments:
           {identified_instruments}

            Your Task:
            1. For each instrument and valve that has been identified, extract the following data:
                 -  **Line Number**: The associated pipeline identifier.
                 - **Pipe Size**: Starting with "DN" or as shown in the diagram.
            2. If any data is missing, then you must use a "-" in the corresponding field.

            Output:
              - The output should be a well structured table with the following columns:
              | Line Number | Pipe Size |
              If any data is missing then put "-" in the relevant field.
           """
           return self.execute_step(prompt)

    def _extract_ranges_units_accuracy(self, instrument_data, identified_instruments):
           prompt = f"""
             As an expert process control engineer, your role is to extract the Min Range, Max Range, Unit and Accuracy of the identified instruments from the P&ID diagram data.

            Process Diagram Data:
            {json.dumps(instrument_data, indent=2)}

            Identified Instruments:
           {identified_instruments}

           Your Task:
             1. For each instrument that has been identified, extract the following data:
                 - **Min. Range**: Minimum operational range.
                 - **Max. Range**: Maximum operational range.
                 - **Unit**: Unit of measurement for the ranges.
                 - **Accuracy**: Instrument accuracy or tolerance levels, if provided.
            2. If any data is missing, then you must use a "-" in the corresponding field.

            Output:
              - The output should be a well structured table with the following columns:
              | Min. Range | Max. Range | Unit | Accuracy |
               If any data is missing then put "-" in the relevant field.
           """
           return self.execute_step(prompt)

    def _extract_design_pt_status_remarks(self, instrument_data, identified_instruments):
        prompt = f"""
            As an expert process control engineer, your role is to extract the Design Pressure, Design Temperature, Status, and any Remarks of the identified instruments from the P&ID diagram data.

            Process Diagram Data:
            {json.dumps(instrument_data, indent=2)}

            Identified Instruments:
            {identified_instruments}

           Your Task:
            1. For each instrument that has been identified, extract the following data:
                - **Design Pressure/Temperature (P/T)**: Design conditions, if specified.
                 - **Remarks**: Any additional notes or comments.
                 - **Status**: Current status of the item (e.g., In Service, Spare).
            2. If any data is missing, then you must use a "-" in the corresponding field.

            Output:
              - The output should be a well structured table with the following columns:
               | Design P/T | Remarks | Status |
               If any data is missing then put "-" in the relevant field.
           """
        return self.execute_step(prompt)

    def generate_instrument_list(self, diagram_data, instrument_data):
      identified_instruments = self._identify_instruments(diagram_data, instrument_data)
      tag_and_pid_data = self._extract_tag_and_pid(instrument_data, identified_instruments)
      service_description_data = self._extract_service_description(instrument_data, identified_instruments)
      pipe_details_data = self._extract_pipe_details(instrument_data, identified_instruments)
      ranges_units_accuracy_data = self._extract_ranges_units_accuracy(instrument_data, identified_instruments)
      design_pt_status_remarks_data = self._extract_design_pt_status_remarks(instrument_data, identified_instruments)
      
      combined_data = f"""
            Tag and PID Data:
            {tag_and_pid_data}

            Service and Description Data:
            {service_description_data}

            Pipe Details Data:
            {pipe_details_data}

            Ranges, Units and Accuracy Data:
            {ranges_units_accuracy_data}

            Design P/T, Status and Remarks:
            {design_pt_status_remarks_data}
      """

      report_prompt = f"""
           Combine the data from the following analyses into a single, well formatted instrument list:

          Combined Data:
          {combined_data}

          Output:
            -  The output should be a well structured table with the following columns:
             | Tag Number | Service | P&ID Number | Description | Line Number | Design P/T | Pipe Size | Min. Range | Max. Range | Unit | Accuracy | Remarks | Status |
             If any data is missing then put "-" in the relevant field.
          """
      return self.execute_step(report_prompt)

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
    instrument_agent = InstrumentAgent()
    image_path = r"C:\Users\yuris\Downloads\vision models\Task_Action_EcoSystem\images\P&ID LNG Kollsnes II System 25 - GASSKONDENSERING-1.png"

    diagram_data = core_agent.analyze_diagram(image_path)
    instrument_data = core_agent.analyze_diagram_instrument(image_path)

    all_data = {}
    all_data['diagram_data']=diagram_data
    all_data['instrument_data']=instrument_data

    if diagram_data and "error" not in diagram_data and instrument_data and "error" not in instrument_data:
         instrument_list = instrument_agent.generate_instrument_list(all_data['diagram_data'], all_data['instrument_data'])
         print("Instrument List:")
         print(instrument_list)
         generate_pdf("instrument_list_002_v3.pdf","Instrument List_002_v3", instrument_list)
    else:
        print("Could not load the diagram")
    with open("instrument_list_002_v3.txt", "w") as f:
      f.write(instrument_list)
