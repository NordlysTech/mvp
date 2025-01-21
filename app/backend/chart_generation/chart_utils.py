import pandas as pd
from .query_utils import execute_query_and_return_results

import pandas as pd
from datetime import datetime, date
from decimal import Decimal

# Function to convert query results to a Pandas DataFrame
def results_to_dataframe(query):
    results, column_names = execute_query_and_return_results(query)
    if results is None or column_names is None:
        print("No results or column names to process.")
        return None

    # Prepare a list of dictionaries, one per row
    rows_as_dicts = []
    for row in results:
        row_dict = {}
        for i, column in enumerate(column_names):
            # Handle specific data types for proper formatting
            if isinstance(row[i], datetime) or isinstance(row[i], date):
                row_dict[column] = row[i].isoformat()  # Convert to ISO format
            elif isinstance(row[i], Decimal) or isinstance(row[i], float):
                row_dict[column] = round(row[i], 2)  # Round decimals/floats
            else:
                row_dict[column] = row[i]
        rows_as_dicts.append(row_dict)

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(rows_as_dicts)
    return df


def results_to_dataframe_1(results, column_names):
    if results is None or column_names is None:
        print("No results or column names to process.")
        return None

    # Prepare a list of dictionaries, one per row
    rows_as_dicts = []
    for row in results:
        row_dict = {}
        for i, column in enumerate(column_names):
            # Handle specific data types for proper formatting
            if isinstance(row[i], datetime) or isinstance(row[i], date):
                row_dict[column] = row[i].isoformat()  # Convert to ISO format
            elif isinstance(row[i], Decimal) or isinstance(row[i], float):
                row_dict[column] = round(row[i], 2)  # Round decimals/floats
            else:
                row_dict[column] = row[i]
        rows_as_dicts.append(row_dict)

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(rows_as_dicts)
    df.to_csv('static/data/data.csv', index=False)
    return df
