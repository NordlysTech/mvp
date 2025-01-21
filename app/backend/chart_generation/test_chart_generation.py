from utils.chart_utils import results_to_dataframe
import io
import sys
from contextlib import contextmanager
import utils.llm_utils as llm_utils
import re
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


selected_llm = "gpt4"

invoke_parameters_dict = {"text" : question}
language = "fr"




df = results_to_dataframe(query)


with capture_print() as captured_output :
    if df is not None:
        print(df.head())  # Display the first few rows of the DataFrame
    else:
        print("Failed to retrieve data.")


pandas_dataframe =  captured_output.getvalue()
print("pandas_dataframe : ", pandas_dataframe)


question_dict = {"question" : question}
invoke_parameters_dict = {"question" : question, "pandas_dataframe" : pandas_dataframe}

prompt_path = "./prompts/prompt_chart_generation_1.json"
response = llm_utils.make_llm_inference(invoke_parameters_dict, prompt_path, selected_llm)
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

exec(cleaned_code, namespace)

