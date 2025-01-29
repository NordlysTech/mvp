import google.generativeai as genai
from config.config import Config
from utils import file_utils, data_utils
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class CoreAgent:
    def __init__(self):
      genai.configure(api_key=Config.GOOGLE_API_KEY)
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

        image_base64 = file_utils.load_image(image_path)
        if not image_base64:
             return {"error": "Could not load image"}

        prompt = f"{system_prompt} Analyze this P&ID diagram."

        try:
            response = self.model.generate_content([
                {'mime_type':'image/jpeg', 'data': image_base64},
                 prompt
            ])
            output_text = response.text
            return data_utils.extract_json(output_text)

        except Exception as e:
            logging.error(f"Error during vision analysis: {e}")
            return {"error": str(e)}

    def analyze_diagram_srs(self, image_path):
        srs_prompt = f"""
        As an expert process safety engineer specializing in Safety Instrumented Systems (SIS), analyze the provided P&ID image and focus on extracting elements relevant for generating a Safety Requirements Specification (SRS) document. Provide the output in a structured JSON format.

           Your Task:
            1. Identify all Safety Instrumented Functions (SIFs) that are visible on the diagram. For each SIF:
               - Identify all sensors involved (tag, type, location).
               - Identify all logic solvers (type, location if possible).
               - Identify all final elements (actuators, tag, type and location).
               - Identify all manual trip switches involved (tag and location)
               - Identify if there is any redundancy within the system.
                - Identify any diagnostic capabilities.
             2. Identify any safety related control systems and control loops.
             3. Identify any emergency shutdown (ESD) systems.
             4. Identify any alarm systems.
              5. Identify any relief systems, and note the set points.
             6.  Where possible, identify any safety layers present on the diagram and any safety related parameters such as SIL rating, and test intervals.
           7. All results must be provided in a structured JSON format.
             8.  If there is any ambiguity, or missing data, then you should include a note saying "Missing data regarding (item)".

           Base your analysis solely on the image.  If you are unable to identify an element, then you should include "missing" as the value.
        """

        image_base64 = file_utils.load_image(image_path)
        if not image_base64:
            return {"error": "Could not load image"}


        try:
            response = self.model.generate_content([
                 {'mime_type':'image/jpeg', 'data': image_base64},
                 srs_prompt
            ])
            output_text = response.text
            return data_utils.extract_json(output_text)
        except Exception as e:
            logging.error(f"Error during SRS vision analysis: {e}")
            return {"error": str(e)}

    def analyze_diagram_lopa(self, image_path):
        lopa_prompt = f"""
        As an expert process safety engineer specializing in Layer of Protection Analysis (LOPA), analyze the provided P&ID image and focus on extracting elements relevant for a LOPA study. Provide the output in a structured JSON format.

            Your Task:
            1.  Identify potential initiating events from the diagram.
            2.  For each initiating event, identify any independent protection layers (IPLs). An IPL is a device, system, or action that is capable of preventing a consequence of the initiating event. This should include:
                *   Safety instrumented systems (SIS) or safety instrumented functions (SIFs)
                *   Pressure relief valves (PSVs) and other relief devices.
                *   Alarms and operator intervention.
                *   Physical barriers.
                *   Emergency shutdown (ESD) systems.
             3.  Identify any safety related parameters such as SIL rating and test frequency.
              4. Note any missing or unclear information.
            5. Base your analysis solely on the image, and extract all information in a structured JSON format.
            6. If you are unable to identify an element, then you should include "missing" as the value.
        """
        image_base64 = file_utils.load_image(image_path)
        if not image_base64:
            return {"error": "Could not load image"}

        try:
            response = self.model.generate_content([
                  {'mime_type':'image/jpeg', 'data': image_base64},
                 lopa_prompt
            ])
            output_text = response.text
            return data_utils.extract_json(output_text)
        except Exception as e:
           print(f"Error during LOPA vision analysis: {e}")
           return {"error": str(e)}

    def analyze_diagram_erp(self, image_path):
       erp_prompt = f"""
        As an expert process safety engineer specializing in emergency response, analyze the provided P&ID image and focus on extracting elements relevant for generating an Emergency Response Plan (ERP). Provide the output in a structured JSON format.

           Your Task:
            1. Identify potential emergency scenarios based on the diagram. This should include:
               -  Fires, explosions, leaks/releases, and process upsets.
            2. For each identified scenario identify potential evacuation routes
             3. Identify the location of any safety showers, eye wash stations, and fire protection equipment.
            4. Identify the location of the emergency control room or central point.
            5. Identify the locations of key personnel (if available), and any communication routes.
            6. Note any specific hazards or areas of high risk.
             7.  Where possible, identify the type and location of emergency shutdown devices or systems.
           8. All results must be provided in a structured JSON format.
            9. If you are unable to identify an element, then you should include "missing" as the value.

            Base your analysis solely on the image.
        """
       image_base64 = file_utils.load_image(image_path)
       if not image_base64:
           return {"error": "Could not load image"}

       try:
           response = self.model.generate_content([
                {'mime_type':'image/jpeg', 'data': image_base64},
                erp_prompt
           ])
           output_text = response.text
           return data_utils.extract_json(output_text)
       except Exception as e:
            logging.error(f"Error during ERP vision analysis: {e}")
            return {"error": str(e)}

    def analyze_diagram_control(self, image_path):
        control_prompt = f"""
            As an expert process control engineer, analyze the provided P&ID image and focus on extracting elements relevant for generating a Control Philosophy document. Provide the output in a structured JSON format.

            Your Task:
             1. Identify all control loops, including the tags, type and location of all instruments (sensors, controllers, and final elements).
             2. For each control loop, identify what the parameter being controlled (e.g., pressure, flow, level, temperature).
             3. Identify all control strategies used in the system (e.g. cascade, ratio, override control).
             4. Identify any interlock systems.
             5. Where possible, identify the control system used (e.g. DCS, PLC, standalone controller).
             6. Provide all information in a structured JSON format.
             7.  If you are unable to identify an element, then you should include "missing" as the value.

            Base your analysis solely on the image.
            """
        image_base64 = file_utils.load_image(image_path)
        if not image_base64:
            return {"error": "Could not load image"}
        try:
            response = self.model.generate_content([
                {'mime_type':'image/jpeg', 'data': image_base64},
                control_prompt
           ])
            output_text = response.text
            return data_utils.extract_json(output_text)
        except Exception as e:
             logging.error(f"Error during control system vision analysis: {e}")
             return {"error": str(e)}


    def execute_step(self, prompt):
         try:
            response = self.model.generate_content(prompt)
            if response.text:
               return response.text
            else:
                logging.warning(f"The AI model returned an empty response for prompt: {prompt}")
                return "The AI Model Returned an Empty Response"
         except Exception as e:
            logging.error(f"Error in execution step: {e} with prompt: {prompt}")
            return  {"error": str(e)}


    def prepare_base_data(self, diagram_data, identified_hazards):
        """Prepare base data for risk assessment and report generation."""
        return {
            "diagram_data": data_utils.format_data(diagram_data),
            "identified_hazards": identified_hazards
        }

    def process_documents(self, file_paths):
        all_data = {}
        for file_path in file_paths:
           if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                 diagram_data = self.analyze_diagram(file_path)
                 if diagram_data and "error" not in diagram_data:
                     all_data['diagram_data'] = diagram_data
                     srs_data = self.analyze_diagram_srs(file_path)
                     if srs_data and "error" not in srs_data:
                         all_data['srs_data'] = srs_data
                     else:
                         logging.warning(f"SRS data not available")
                     lopa_data = self.analyze_diagram_lopa(file_path)
                     if lopa_data and "error" not in lopa_data:
                          all_data['lopa_data'] = lopa_data
                     else:
                           logging.warning(f"LOPA data not available")
                     erp_data = self.analyze_diagram_erp(file_path)
                     if erp_data and "error" not in erp_data:
                         all_data['erp_data'] = erp_data
                     else:
                         logging.warning(f"ERP data not available")
                     control_data = self.analyze_diagram_control(file_path)
                     if control_data and "error" not in control_data:
                           all_data['control_data'] = control_data
                     else:
                           logging.warning(f"Control Data not available")
                 else:
                    logging.warning(f"Diagram data not available")
           else:
                with open(file_path, 'r') as file:
                    all_data['text_data']= file.read()
        return all_data
