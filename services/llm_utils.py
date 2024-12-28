from langchain.prompts import ChatPromptTemplate
import os
import json
import openai
from langchain_community.chat_models import ChatAnyscale
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_cohere import ChatCohere
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")




def get_json_from_response(response) :
    first_opening_brace = response.find('{')
    last_closing_brace = response.rfind('}')
    json_str = response[first_opening_brace:last_closing_brace + 1]

    try : 
        parsed_json = json.loads(json_str)
    except Exception as e:
        parsed_json = None
    return parsed_json

def get_answer_from_response(response) :
    content = response.content
    content = content.encode('ISO-8859-1').decode('latin-1')
    first_opening_brace = content.find('{')
    last_closing_brace = content.rfind('}')
    json_str = content[first_opening_brace:last_closing_brace + 1]
    try : 
        parsed_json = json.loads(json_str)
        answer = parsed_json["answer"]
    except Exception as e:
        answer = ""
    return answer

def instantiate_gemini20_flash_exp():
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        temperature=0.2,
        max_tokens=2000
    )
    return model

def instantiate_gpt35_openai():
    model = ChatOpenAI(
        temperature=0.2,
        model="gpt-3.5-turbo-16k",
        max_tokens=2000,
        openai_api_key=openai.api_key,
    )
    return model

def instantiate_cohere():
    model = ChatCohere(
        temperature=0.2,
        max_tokens=2000
    )
    return model

def instantiate_gpt4_o_mini_azure():
    model = AzureChatOpenAI( 
        azure_endpoint = azure_openai_endpoint, 
        openai_api_key = azure_openai_api_key, 
        openai_api_type = 'azure', 
        openai_api_version = "2023-05-15", 
        deployment_name = "o1-preview", 
        model_name = "o1-mini", 
        temperature = 1, 
        request_timeout = 240, 
        top_p = 1, 
        frequency_penalty = 0, 
        presence_penalty = 0, 
        stop = None
    )
    return model

def instantiate_gemini_pro():
    temperature = 0
    MODEL_API_KEY = os.getenv("GEMINIPRO_GOOGLE_API_KEY")
    os.environ["GOOGLE_API_KEY"] = MODEL_API_KEY
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature = temperature)
    return model


def instantiate_claude_3_opus():
    temperature = 0
    MODEL_API_KEY = os.getenv("CLAUDE_MODEL_API_KEY")
    os.environ["ANTHROPIC_API_KEY"] = MODEL_API_KEY
    model = ChatAnthropic(model='claude-3-opus-20240229', temperature = temperature)
    return model

def instantiate_codellama_34b():
    temperature = 0
    MODEL_API_KEY = os.getenv("ANYSCALE_MODEL_API_KEY")
    MODEL_API_BASE = os.getenv("ANYSCALE_MODEL_API_BASE")
    os.environ["ANYSCALE_API_KEY"] = MODEL_API_KEY
    os.environ["ANYSCALE_API_BASE"] = MODEL_API_BASE
    model = ChatAnyscale(model_name="codellama/CodeLlama-34b-Instruct-hf", temperature = temperature)
    return model

def instantiate_codellama_70b():
    temperature = 0
    MODEL_API_KEY = os.getenv("ANYSCALE_MODEL_API_KEY")
    MODEL_API_BASE = os.getenv("ANYSCALE_MODEL_API_BASE")
    os.environ["ANYSCALE_API_KEY"] = MODEL_API_KEY
    os.environ["ANYSCALE_API_BASE"] = MODEL_API_BASE
    model = ChatAnyscale(model_name="codellama/CodeLlama-70b-Instruct-hf", temperature = temperature)
    return model
def instantiate_codellama_34b():
    temperature = 0
    MODEL_API_KEY = os.getenv("ANYSCALE_MODEL_API_KEY")
    MODEL_API_BASE = os.getenv("ANYSCALE_MODEL_API_BASE")
    os.environ["ANYSCALE_API_KEY"] = MODEL_API_KEY
    os.environ["ANYSCALE_API_BASE"] = MODEL_API_BASE
    model = ChatAnyscale(model_name="codellama/CodeLlama-34b-Instruct-hf", temperature = temperature)
    return model
def instantiate_llm_model(model_name):
    switch_dict = {
        "gemini20_flash_exp" : instantiate_gemini20_flash_exp,
        "gpt4_o_mini_azure": instantiate_gpt4_o_mini_azure,
        "gemini_pro" : instantiate_gemini_pro,
        "gpt35_openai" : instantiate_gpt35_openai,
        "codellama_70b" : instantiate_codellama_70b,
        "codellama_34b" : instantiate_codellama_34b,
        "claude_3_opus" : instantiate_claude_3_opus
    }
    # Get the function for the given model_name, or default if not found
    selected_case = switch_dict.get(model_name)
    # Execute the selected function and return the result
    return selected_case()

    

