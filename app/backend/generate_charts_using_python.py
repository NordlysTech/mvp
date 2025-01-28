import io
import sys
from contextlib import contextmanager
import re
import pandas as pd
import altair as alt
from services.config_utils import load_config, get_config
from dotenv import load_dotenv

from services.llm_utils import make_llm_inference, instantiate_llm_model
from services.config_utils import load_config, get_config

config_path = "config.yaml"
config = load_config(config_path)

load_dotenv()

selected_llm = get_config(config, "llms", "llm_name")

@contextmanager
def capture_print() :
    output_capture = io.StringIO()
    original_stdout = sys.stdout

    sys.stdout = output_capture

    try :
        yield output_capture
    finally :
        sys.stdout = original_stdout

question = input("Please enter your question: ")



invoke_parameters_dict = {"text" : question}
language = "fr"




df = pd.read_csv('static/data/data.csv')




pandas_dataframe = df.head(5).to_string()

question_dict = {"question" : question}
invoke_parameters_dict = {"question" : question, "pandas_dataframe" : pandas_dataframe}

prompt_path = "./prompts/prompt_chart_generation_code.json"
model = instantiate_llm_model(selected_llm, temperature=0.2, max_tokens=2000)

response = make_llm_inference(invoke_parameters_dict, prompt_path, model)
print("response : ",response)
llm_code = response.content


code_file_path = "code.txt"
with open(code_file_path, "w") as file :
    file.write(llm_code)
# Nettoyage pour extraire uniquement le code
#cleaned_code = llm_code.strip("```python").strip("```").strip()

cleaned_code = re.search(r"```python(.*?)```", llm_code, re.DOTALL).group(1).strip()

# Espace de noms pour passer la variable au code exécuté
namespace = {"df": df}


with capture_print() as captured_output :
    exec(cleaned_code, namespace)


code_execution_logs =  captured_output.getvalue()
print("code_execution_logs : ", code_execution_logs)



