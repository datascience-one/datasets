import os
import pandas as pd
import json
import argparse
##############################################
##########      Data Science Academy  ########
##########     https:/datascience.one ########
##############################################


def remove_non_printable(text):
    # Remove non-printable characters and Unicode escape sequences
    cleaned_text = ''.join(char for char in text if char.isprintable() or char == '\n' or char == '\t')
    return cleaned_text

def generate_jsonl_file_from_db(file_path, system_prompt, output_file="output.jsonl"):
    """
    Generate a JSON Lines (JSONL) file containing messages from the given DataFrame.

    Parameters:
    - file_path (str): The path to the CSV or Excel file containing questions and answers.
    - system_prompt (str): Content for the system role.
    - output_file (str): The name of the output JSONL file. Default is "output.jsonl".
    """
    # Load the DataFrame from the CSV or Excel file
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")
    df.Question = df.Question.astype(str)
    df.Answer = df.Answer.astype(str)
    # Define a function to convert a row to the desired JSON format
    def row_to_json(row):
        system_msg = {"role": "system", "content": remove_non_printable(system_prompt)}
        user_msg = {"role": "user", "content": remove_non_printable(row['Question'])}
        assistant_msg = {"role": "assistant", "content": remove_non_printable(row['Answer'])}
        return {"messages": [system_msg, user_msg, assistant_msg]}

    # Write each row's JSON to the output file in JSON Lines format
    with open(output_file, 'w') as f:
        for _, row in df.iterrows():
            json_data = row_to_json(row)
            f.write(json.dumps(json_data) + '\n')

def convert_to_jsonl(json_data, output_file):
    # Split the content based on the pattern
    split_content = json_data.strip().split("\n")

    # Initialize a string to store the current conversation
    current_conversation = ""

    # Open the output file in write mode
    with open(output_file, 'w') as f:
        # Iterate through each line in the content
        for line in split_content:
            # Append the line to the current conversation
            current_conversation += line.strip()

            # Check if the line ends with '}' indicating the end of a JSON object
            if line.strip().endswith("}"):
                try:
                    # Attempt to parse the current conversation as JSON
                    conversation = json.loads(current_conversation)
                    # Write the parsed JSON object to the file in JSONL format
                    f.write(json.dumps(conversation) + '\n')
                    # Reset the current conversation string
                    current_conversation = ""
                except json.JSONDecodeError:
                    # If parsing fails, ignore the current conversation
                    pass

def generate_jsonl_file(file_path, system_prompt, output_file="output.jsonl"):
    # Load the DataFrame from the CSV or Excel file
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")

    # Define a function to convert a row to the desired JSON format
    def row_to_json(row):
        system_msg = {"role": "system", "content": remove_non_printable(system_prompt)}
        user_msg = {"role": "user", "content": remove_non_printable(row['Question'])}
        assistant_msg = {"role": "assistant", "content": remove_non_printable(row['Answer'])}
        return {"messages": [system_msg, user_msg, assistant_msg]}

    # Write each row's JSON to the output file in JSON Lines format
    with open(output_file, 'w') as f:
        for _, row in df.iterrows():
            json_data = row_to_json(row)
            f.write(json.dumps(json_data) + '\n')

    # Convert the written JSON to JSONL format
    with open(output_file, 'r') as f:
        json_data = f.read()
        convert_to_jsonl(json_data, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CSV/Excel data to JSONL format.")
    parser.add_argument("file_path", help="Path to the CSV or Excel file")
    parser.add_argument("system_prompt", help="Content for the system role")
    parser.add_argument("--output_file", help="Output file name (default is output.jsonl)", default="output.jsonl")
    args = parser.parse_args()

    # Create folder if not exists
    folder_name = "jsonl_files"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    output_path = os.path.join(folder_name, args.output_file)
    generate_jsonl_file(args.file_path, args.system_prompt, output_path)

