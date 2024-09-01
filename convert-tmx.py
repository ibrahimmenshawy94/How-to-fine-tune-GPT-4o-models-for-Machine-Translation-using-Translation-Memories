import pandas as pd
from lxml import etree as ET
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_and_correct_path(file_path):
    # Replace single backslashes with double backslashes
    corrected_path = file_path.replace("\\", "\\\\")
    return corrected_path

def parse_tmx_filtered(tmx_file_path, source_lang, target_lang):
    try:
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(tmx_file_path, parser)
        root = tree.getroot()
        data_pairs = []

        for tu in root.findall('.//tu'):
            tu_data = {}
            tu_id = tu.attrib.get('tuid', 'Unknown ID')  # Capture the tuid for logging

            for tuv in tu.findall('tuv'):
                lang = tuv.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
                seg_element = tuv.find('seg')
                if seg_element is not None:
                    # Extract text content, ignoring inline tags like <ph>
                    seg_text = ''.join(seg_element.itertext())
                    tu_data[lang] = seg_text.strip()

            # Ensure both source and target languages are in the tu_data
            if source_lang in tu_data and target_lang in tu_data:
                source_text = tu_data[source_lang]
                target_text = tu_data[target_lang]
                if source_text and target_text:
                    data_pairs.append({'Source': source_text, 'Target': target_text})
            else:
                logging.warning(f"Missing language pair for {source_lang} and {target_lang} in translation unit with tuid {tu_id}.")

        if not data_pairs:
            logging.warning("No valid translation pairs found in the TMX file.")

        extracted_tm = pd.DataFrame(data_pairs)
        # Remove duplicated segments
        filtered_tm = extracted_tm.drop_duplicates(subset=['Source', 'Target'], keep='first')
        filtered_tm.reset_index(drop=True, inplace=True)
        return filtered_tm

    except Exception as e:
        logging.error(f"Error parsing TMX file: {e}")
        return pd.DataFrame()

def create_finetuning_json(tmx_file_path, source_lang, source_lang_code, target_lang, target_lang_code, jsonl_output_path):
    df = parse_tmx_filtered(tmx_file_path, source_lang_code, target_lang_code)
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
    tmx_file_path = input("Enter the TMX file path: ") # The location of the TMX file on your machine.
    tmx_file_path = validate_and_correct_path(tmx_file_path)
    if not tmx_file_path:
        exit()

    source_lang = input("Enter the source language  (e.g., English): ") # e.g., 'English'
    source_lang_code = input("Enter the source language code in the tmx file (e.g., en, en-us, en-uk, ...): ") # e.g., 'en'
    target_lang = input("Enter the Target language  (e.g., Arabic): ") # e.g., 'English'
    target_lang_code = input("Enter the target language code in the tmx file(e.g., ar, ar-eg, fr-fr, ...): ") # e.g., 'ar'

    jsonl_output_path = input("Enter the output JSONL file path: ") # e.g., 'output.jsonl'
    jsonl_output_path = validate_and_correct_path(jsonl_output_path)

    # Run the script:
    create_finetuning_json(tmx_file_path, source_lang, source_lang_code, target_lang, target_lang_code, jsonl_output_path)
