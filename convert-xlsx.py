import pandas as pd
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_and_correct_path(file_path):
    # Replace single backslashes with double backslashes
    corrected_path = file_path.replace("\\", "\\\\")
    return corrected_path

def parse_xlsx_tm(excel_file_path, source_col, target_col):
    try:
        # Convert column letters to indices (0-indexed)
        source_col_index = ord(source_col.upper()) - ord('A')
        target_col_index = ord(target_col.upper()) - ord('A')

        # Read the Excel file, using the column indices
        df = pd.read_excel(excel_file_path, usecols=[source_col_index, target_col_index], header=0)
        df.columns = ['Source', 'Target']

        # Drop rows with NaN values in either Source or Target columns and remove duplicates based on both Source and Target columns
        df = df.dropna(subset=['Source', 'Target']).drop_duplicates(subset=['Source', 'Target'])
        df.reset_index(drop=True, inplace=True)
        return df
    except Exception as e:
        logging.error(f"Error parsing Excel file: {e}")
        return pd.DataFrame()
    

def create_finetuning_json(excel_file_path, source_lang, source_col, target_lang, target_col, jsonl_output_path):
    df = parse_xlsx_tm(excel_file_path, source_col, target_col)
    if df.empty:
        logging.error("No data to write to JSONL. Exiting.")
        return

    with open(jsonl_output_path, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            entry = {
                "messages": [
                    {"role": "system", "content": f"You are a professional linguist who translates from {source_lang} to {target_lang}."},
                    {"role": "user", "content": f"Translate this segment into {target_lang}:\n{row['Source']}"},
                    {"role": "assistant", "content": row['Target']}
                ]
            }
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    logging.info(f"JSONL file created successfully at {jsonl_output_path}")

# Example Usage:
if __name__ == "__main__":
    file_path = input("Enter the TM .xlsx file path: ") # The location of the Excel file on your machine.
    file_path = validate_and_correct_path(file_path)

    source_lang = input("Enter the source language (e.g., English): ")
    
    # Ensure that column letters are always uppercase
    source_col = input("Enter the source language column in the xlsx file (e.g., A, B, C, ...): ").upper()

    while True:
        target_lang = input("Enter the target language (e.g., Arabic): ")
        target_col = input("Enter the target language column in the xlsx file (e.g., A, B, C, ...): ").upper()

        if target_col == source_col:
            print("Error: The target column cannot be the same as the source column. Please enter a different column for the target language.")
        else:
            break

    jsonl_output_path = input("Enter the output JSONL file path: ") # e.g., 'output.jsonl'
    jsonl_output_path = validate_and_correct_path(jsonl_output_path)

    # Run the script:
    create_finetuning_json(file_path, source_lang, source_col, target_lang, target_col, jsonl_output_path)
