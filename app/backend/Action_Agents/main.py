from agent.core_agent import CoreAgent
from agent.psi_agent import PSIAgent
from agent.hazid_agent import HAZIDAgent
from agent.risk_agent import RiskAgent
from agent.hazop_agent import HAZOPAgent
from agent.srs_agent import SRSAgent
from agent.lopa_agent import LOPAAgent
from agent.erp_agent import ERPAgent
from utils import file_utils
from agent.control_agent import ControlPhilosophyAgent
import os

if __name__ == "__main__":
    core_agent = CoreAgent()
    psi_agent = PSIAgent()
    hazid_agent = HAZIDAgent()
    risk_agent = RiskAgent()
    hazop_agent = HAZOPAgent()
    srs_agent = SRSAgent()
    lopa_agent = LOPAAgent()
    erp_agent = ERPAgent()
    control_agent = ControlPhilosophyAgent()


    image_path = r"C:\Users\yuris\Downloads\vision models\Safety_Risk_Agent_EcoSystem - V2\images\Capsol EoP 1.png"
    text_path = ""

    file_paths = [image_path,text_path]
    all_data = core_agent.process_documents([f for f in file_paths if f]) # Process only valid paths

    if all_data:
          diagram_data = all_data.get('diagram_data', {})
          text_data = all_data.get('text_data','')
          identified_hazards = psi_agent.identify_hazards(diagram_data) if diagram_data else "No Diagram Data Available"
          risk_assessment = risk_agent.generate_risk_assessment(diagram_data, identified_hazards) if diagram_data else "No Diagram Data Available"
          srs_data = all_data.get('srs_data',{})
          lopa_data = all_data.get('lopa_data',{})
          erp_data = all_data.get('erp_data',{})
          control_data = all_data.get('control_data',{})
          # Task Selection and Execution
          while True:
               task = input("Select Task (Generate HAZID, Generate Risk Assessment, Generate HAZOP Table, Generate SRS, Generate LOPA, Generate ERP, Generate Control Philosophy, or exit): ").strip().lower()

               if task == "generate hazid":
                    if diagram_data:
                         report = hazid_agent.generate_hazid_report(diagram_data, identified_hazards, risk_assessment)
                         print("Final Report:")
                         print(report)
                         file_utils.save_to_file("final_report.txt",report)
                    else:
                         print("No Diagram Data is available for this task")
               elif task == "generate risk assessment":
                    if diagram_data:
                        assessment = risk_agent.generate_risk_assessment(diagram_data, identified_hazards)
                        print("Risk Assessment:")
                        print(assessment)
                        file_utils.save_to_file("risk_assessment.txt", assessment)
                    else:
                        print("No Diagram Data is available for this task")
               elif task == "generate hazop table":
                   if diagram_data:
                       hazop_table = hazop_agent.generate_hazop_table(diagram_data, risk_assessment,identified_hazards)
                       print("Hazop Table")
                       print(hazop_table)
                       file_utils.save_to_file("hazop_table.txt", hazop_table)
                   else:
                        print("No Diagram Data is available for this task")
               elif task == "generate srs":
                   if diagram_data:
                       srs_report = srs_agent.generate_srs(diagram_data, identified_hazards, risk_assessment, srs_data)
                       print("SRS Report")
                       print(srs_report)
                       file_utils.save_to_file("srs_report.txt", srs_report)
                   else:
                         print("No Diagram Data is available for this task")
               elif task == "generate lopa":
                   if diagram_data:
                       lopa_report = lopa_agent.generate_lopa_report(diagram_data, identified_hazards, risk_assessment, lopa_data)
                       print("LOPA Report")
                       print(lopa_report)
                       file_utils.save_to_file("lopa_report.txt", lopa_report)
                   else:
                        print("No Diagram Data is available for this task")
               elif task == "generate erp":
                   if diagram_data:
                        erp_report = erp_agent.generate_erp_report(diagram_data, identified_hazards, erp_data)
                        print("ERP Report")
                        print(erp_report)
                        file_utils.save_to_file("erp_report.txt", erp_report)
                   else:
                        print("No Diagram Data is available for this task")
               elif task == "generate control philosophy":
                   if diagram_data:
                       control_report = control_agent.generate_control_philosophy(diagram_data, control_data)
                       print("Control Philosophy Report:")
                       print(control_report)
                       file_utils.save_to_file("control_philosophy.txt",control_report)
                   else:
                       print("No Diagram Data is available for this task")
               elif task == "exit":
                   break
               else:
                   print("Invalid task, Please select one of the available tasks")
    else:
        print("Could not load data")
