import json

def extract_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw_output": text}

def format_data(data):
    try:
      return json.dumps(data, indent=2)
    except Exception as e:
          print(f"Error Formatting data {e}")
          return None

def store_data(data,filename):
    with open(filename, "w") as f:
        json.dump(data,f,indent=2)
        return True
