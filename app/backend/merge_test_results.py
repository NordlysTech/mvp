import os
import json
import pandas as pd


model_name = "cohere"
# Folder containing the JSON files
input_folder = f'tests/{model_name}'


def normalize_agent_name(agent_name):
    """Normalize agent names by removing spaces and underscores, and converting to lowercase."""
    return agent_name.replace(" ", "").replace("_", "").lower()

def merge_json_files() :
    # List to store rows for the dataset
    dataset = []

    # Loop through all JSON files in the folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.json'):
            file_path = os.path.join(input_folder, file_name)
            
            # Load the JSON file
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
            
            # Extract the original_query
            original_query = data['query_analysis']['original_query']
            
            # Extract agent names
            selected_agents = data['agent_allocation']['selected_agents']
            agent_names = [normalize_agent_name(agent['agent_name']) for agent in selected_agents]

            
            # Add the original_query and agent names to the dataset
            row = {'original_query': original_query}
            
            # Add each agent name as a separate column in the row
            for i, agent_name in enumerate(agent_names):
                row[f'predicted_agent_{i+1}'] = agent_name
            
            # Append the row to the dataset
            dataset.append(row)

    # Convert the dataset to a DataFrame
    df = pd.DataFrame(dataset)

    # Save the dataset to a CSV file
    output_csv = 'query_agent_dataset.csv'
    df.to_csv(output_csv, index=False)

    print(f"Dataset saved to {output_csv}")


def merge_original_predicted() :
    # Paths to the original Excel file and the query_agent_dataset.csv
    original_excel_file = 'Classifier_Agent_test.xlsx'  # Replace with your original file path
    predicted_csv_file = 'query_agent_dataset.csv'      # The CSV file generated from the model predictions

    # Read the original Excel file into a DataFrame
    original_df = pd.read_excel(original_excel_file)

    # Read the predicted agents CSV file into a DataFrame
    predicted_df = pd.read_csv(predicted_csv_file)

    # Merge the original dataset with the predicted dataset on the 'query' column
    merged_df = pd.merge(original_df, predicted_df, how='left', left_on='query', right_on='original_query')

    # Drop the 'original_query' column from the merged dataframe
    merged_df.drop(columns=['original_query'], inplace=True)

    # Reorganize the columns to ensure proper ordering (query first, then ground truth agents, then predicted agents)
    # Get columns for the ground truth agents ('agent_1', 'agent_2', ...) from the original DataFrame
    ground_truth_columns = [f'agent_{i+1}' for i in range(6)]  # Adjust according to the maximum number of agents

    # Get columns for the predicted agents ('predicted_agent_1', 'predicted_agent_2', ...) from the predicted DataFrame
    predicted_columns = [f'predicted_agent_{i+1}' for i in range(len(predicted_df.columns) - 1)]

    # Reorder the columns: query, ground truth agents, and predicted agents
    final_columns = ['query'] + ground_truth_columns + predicted_columns

    # Reorder the DataFrame to match the final column order
    final_df = merged_df[final_columns]

    # Save the final merged dataset to a CSV file
    output_csv = 'final_query_agent_dataset.csv'
    final_df.to_csv(output_csv, index=False)

    print(f"Final dataset saved to {output_csv}")
    
    




'''
# Function to calculate accuracy for each query
def calculate_accuracy(row):
    # Get ground truth agents (non-empty columns)
    ground_truth_agents = {row[f'agent_{i+1}'] for i in range(6) if pd.notna(row[f'agent_{i+1}'])}
    
    # Get predicted agents (non-empty columns)
    predicted_agents = {row[f'predicted_agent_{i+1}'] for i in range(4) if pd.notna(row[f'predicted_agent_{i+1}'])}
    
    # Check if predicted agents are a subset of ground truth agents
    return predicted_agents.issubset(ground_truth_agents)
'''

# Function to calculate the number of correctly predicted agents
def calculate_accuracy(row):
    # Get ground truth agents (non-empty columns)
    ground_truth_agents = {row[f'agent_{i+1}'] for i in range(6) if pd.notna(row[f'agent_{i+1}'])}
    
    # Get predicted agents (non-empty columns)
    predicted_agents = {row[f'predicted_agent_{i+1}'] for i in range(4) if pd.notna(row[f'predicted_agent_{i+1}'])}
    
    # Count how many predicted agents are in the ground truth agents
    correct_predictions = len(predicted_agents.intersection(ground_truth_agents))
    
    # Return the ratio of correct predictions to total predictions
    return correct_predictions / len(predicted_agents) if predicted_agents else 0


#merge_original_predicted()

# Read the merged dataset
merged_df = pd.read_csv('final_query_agent_dataset.csv')

# Apply the accuracy calculation to each row and store the results
merged_df['accuracy'] = merged_df.apply(calculate_accuracy, axis=1)

# Calculate the overall accuracy (percentage of correct predictions)
accuracy_percentage = merged_df['accuracy'].mean() * 100

print(f"Overall accuracy: {accuracy_percentage:.2f}%")

# Save the accuracy results to a new CSV file if needed
output_with_accuracy_csv = 'final_query_agent_with_accuracy.csv'
merged_df.to_csv(output_with_accuracy_csv, index=False)

print(f"Dataset with accuracy saved to {output_with_accuracy_csv}")



