import pandas as pd
from services.llm_utils import instantiate_llm_model, get_json_from_response, make_llm_inference
from services.config_utils import load_config, get_config
from dotenv import load_dotenv
import json
import re
import altair as alt

config_path = "config.yaml"
config = load_config(config_path)

print("config : ",config)

    
load_dotenv()

model_to_use = get_config(config, "llms", "llm_name")

question = str(input())

pandas_dataframe = pd.read_csv('static/data/data.csv')
first_five_lines = pandas_dataframe.head(5)
first_five_lines_str = first_five_lines.to_string()
question_dict = {"question" : question}
invoke_parameters_dict = {"question" : question, "pandas_dataframe" : first_five_lines_str}


prompt_path = "./prompts/prompt_chart_generation_vega.json"

model = instantiate_llm_model(model_to_use, temperature=0.2, max_tokens=2000)
response = make_llm_inference(invoke_parameters_dict, prompt_path, model)


answer = ""
if response is not None :
    print("response : ",response)
    vega_json = response.content
    
    if "```json" in vega_json:
        match = re.search(r"```json(.*?)```", vega_json, re.DOTALL)
        if match:
            answer = match.group(1).strip()
        else:
            raise ValueError("Les balises ```json``` sont présentes, mais aucun contenu n'a été trouvé.")
    else:
        answer = vega_json.strip()
print("answer : ",answer)


spec = json.loads(answer)
print(spec)
# Créer le graphique à partir de la spécification
chart = alt.Chart.from_dict(spec)

# Enregistrer le graphique au format HTML
chart.save('chart.png')