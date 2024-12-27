import pandas as pd
import os
import json
import time
from services.S2_ClassifierLogic import Classifier



def normalize_agent_name(agent_name):
    """Normalize agent names by removing spaces and underscores, and converting to lowercase."""
    if pd.isna(agent_name):  # Check for NaN or None
        return None
    return agent_name.replace(" ", "").replace("_", "").lower()

def get_json_from_response(response) :
    first_opening_brace = response.find('{')
    last_closing_brace = response.rfind('}')
    json_str = response[first_opening_brace:last_closing_brace + 1]

    try : 
        parsed_json = json.loads(json_str)
    except Exception as e:
        parsed_json = None
    return parsed_json

model_name = "cohere"
# Folder containing the JSON files
output_folder = f'tests/{model_name}'

results_folder = 'tests/results'

# Create the folder if it doesn't exist
os.makedirs(results_folder, exist_ok=True)
    
def classify_dataset(start_index=0):  # Add start_index parameter
    # Replace 'input_file.xlsx' with the path to your Excel file
    excel_file = 'Classifier_Agent_test.xlsx'

    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Create the folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Initialize the classifier and classify the query
    classifier_model = Classifier()

    # Loop through the rows starting from the specified index
    for index, row in df.iterrows():
        if index < start_index:  # Skip rows before the start_index
            continue

        query_value = row['query']
        print(f"Row {index}: {query_value}")
        
        try:
            response = classifier_model.classify_query(query_value)
            print("\nRaw Classifier Response:\n")
            print(response)

            json_response = get_json_from_response(response)
            print("\nJson Classifier Response:\n")
            print(json_response)

            if json_response is not None:
                # Save the parsed JSON response to a file
                output_file = os.path.join(output_folder, f'query_{index}.json')
                with open(output_file, 'w') as json_file:
                    json.dump(json_response, json_file, indent=4)

                print(f"Response saved to {output_file}")
            else:
                print(f"Failed to parse JSON for Row {index}")

        except Exception as e:
            print(f"Error processing Row {index}: {e}")
        
        # Pause for 5 seconds before the next iteration
        print("--------------------------------")
        time.sleep(3)


def merge_json_files():
    # Path to the Excel file
    excel_file = 'Classifier_Agent_test.xlsx'

    # Read the Excel file
    df = pd.read_excel(excel_file)

    # List to store rows for the dataset
    dataset = []

    # Loop through each row in the Excel file
    for index, row in df.iterrows():
        query_value = row['query']

        # Construct the corresponding JSON file path based on the row index
        json_file_name = f'query_{index}.json'
        json_file_path = os.path.join(output_folder, json_file_name)

        # Initialize a row dictionary with columns from the Excel file
        row_data = {'query': query_value}

        # Include the agent columns from the Excel file
        for i in range(1, 7):  # Assuming agent_1 to agent_6
            ground_truth_agent_name  = row.get(f'agent_{i}', None)
            print(ground_truth_agent_name)
            row_data[f'agent_{i}'] = normalize_agent_name(ground_truth_agent_name)
            

        if os.path.exists(json_file_path):
            # Load the JSON file
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            # Extract agent names and normalize them
            selected_agents = data['agent_allocation']['selected_agents']
            agent_names = [normalize_agent_name(agent['agent_name']) for agent in selected_agents]

            # Add each agent name from the JSON to the row
            for i, agent_name in enumerate(agent_names):
                row_data[f'predicted_agent_{i+1}'] = agent_name
        else:
            print(f"JSON file not found for Row {index}: {json_file_name}")

        # Append the row to the dataset
        dataset.append(row_data)

    # Convert the dataset to a DataFrame
    result_df = pd.DataFrame(dataset)

    # Save the dataset to a CSV file
    output_csv = f'{results_folder}/{model_name}_query_agent_dataset.csv'
    result_df.to_csv(output_csv, index=False)

    print(f"Dataset saved to {output_csv}")



# Function to calculate the number of correctly predicted agents
def calculate_accuracy(row):
    # Get ground truth agents (non-empty columns)
    ground_truth_agents = {row[f'agent_{i+1}'] for i in range(6) if pd.notna(row[f'agent_{i+1}'])}
    
    # Get predicted agents (non-empty columns)
    predicted_agents = {row[f'predicted_agent_{i+1}'] for i in range(3) if pd.notna(row[f'predicted_agent_{i+1}'])}
    
    # Count how many predicted agents are in the ground truth agents
    correct_predictions = len(predicted_agents.intersection(ground_truth_agents))
    
    # Return the ratio of correct predictions to total predictions
    return correct_predictions / len(predicted_agents) if predicted_agents else 0

def evaluate_llm():
    
    
    # Read the merged dataset
    merged_df = pd.read_csv(f'{results_folder}/{model_name}_query_agent_dataset.csv')

    # Apply the accuracy calculation to each row and store the results
    merged_df['accuracy'] = merged_df.apply(calculate_accuracy, axis=1)

    # Calculate the overall accuracy (percentage of correct predictions)
    accuracy_percentage = merged_df['accuracy'].mean() * 100

    print(f"Overall accuracy: {accuracy_percentage:.2f}%")

    # Save the accuracy results to a new CSV file if needed
    output_with_accuracy_csv = f'{results_folder}/{model_name}_final_query_agent_with_accuracy.csv'
    merged_df.to_csv(output_with_accuracy_csv, index=False)

    print(f"Dataset with accuracy saved to {output_with_accuracy_csv}")
    
# Example usage:
# Start from the row where the script stopped, e.g., index 42
# classify_dataset(start_index=26)

# Example usage:
# merge_json_files()

evaluate_llm()