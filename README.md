# How to Create the JSONL File Format for Fine-Tuning GPT-4o Models

This repository contains scripts to help you convert your translation memory (TM) data into the JSONL format required for fine-tuning GPT-4o models.

## Getting Started

If your cleaned TM data is in a TMX format, you can use the `convert-tmx.py` script to generate the JSONL file.

## Running the Script

To run the script, follow these steps:

1. **Ensure Python is Installed**:
   - Make sure Python is installed on your machine. You can check by running `python --version` in your command prompt or terminal.

2. **Navigate to the Script Directory**:
   - Open your command prompt or terminal.
   - Navigate to the directory where the script is located. For example:
     ```bash
     cd path/to/your/script
     ```

3. **Run the Script**:
   - Run the script by entering the following command:
     ```bash
     python convert-tmx.py
     ```

4. **Provide the Required Inputs**:

   **1. Enter the TMX file path**:
   - Enter the full path to the TMX file, including the filename. For example:
     - On Windows:
       ```
       C:\Users\ibrah\Desktop\tmx_test.tmx
       ```
     - On Mac/Linux:
       ```
       /Users/ibrah/Desktop/tmx_test.tmx
       ```

   **2. Enter the Source Language**:
   - Specify the source language that will be used in the fine-tuning prompt. For example:
     ```
     English
     ```

   **3. Enter the Source Language Code in the TMX File**:
   - Enter the language code as it appears in the TMX file. Make sure it matches exactly, including any variants. For example:
     ```
     en
     ```
     or
     ```
     en-us
     ```

   **4. Enter the Target Language**:
   - Specify the target language that will be used in the fine-tuning prompt. For example:
     ```
     Arabic
     ```

   **5. Enter the Target Language Code in the TMX File**:
   - Enter the language code for the target language as it appears in the TMX file. Make sure it matches exactly. For example:
     ```
     ar
     ```

   **6. Enter the Output JSONL File Path**:
   - Specify the path where the generated JSONL file will be saved, including the filename. Ensure the file extension is `.jsonl`. For example:
     - On Windows:
       ```
       C:\Users\ibrah\Desktop\output.jsonl
       ```
     - On Mac/Linux:
       ```
       /Users/ibrah/Desktop/output.jsonl
       ```

5. **Run the Script**:
   - Press Enter, and the script will process the TMX file and generate the JSONL file. If successful, you should see a message like:
     ```
     JSONL file created successfully at C:\Users\ibrah\Desktop\output.jsonl
     ```

## Working with Excel Files

If your TM data is in an Excel format (`.xlsx`), you can use the `convert-xlsx.py` script. The process is similar:

1. **Run the Script**:
   - Use the command:
     ```bash
     python convert-xlsx.py
     ```

2. **Provide the Required Inputs**:

   **1. Enter the Excel file path**:
   - Enter the full path to the Excel file, including the filename.

   **2. Enter the Source Language**:
   - Specify the source language for fine-tuning.

   **3. Enter the Source Language Column in the Excel File**:
   - Enter the column letter where the source language text is located. For example, if the source text is in column A, enter `A`.

   **4. Enter the Target Language**:
   - Specify the target language for fine-tuning.

   **5. Enter the Target Language Column in the Excel File**:
   - Enter the column letter where the target language text is located. Make sure it is different from the source column. For example, if the target text is in column B, enter `B`.

   **6. Enter the Output JSONL File Path**:
   - Specify the path where the generated JSONL file will be saved.

3. **Run the Script**:
   - Press Enter, and the script will create the JSONL file. You should see a confirmation message if successful.

## Additional Notes

- **File Paths**: Ensure that all file paths you enter are correct. Incorrect paths will result in errors.
- **Language Codes**: Make sure the language codes match exactly with what's in your TMX or Excel file, including any regional variations.
- **JSONL File**: The generated JSONL file is formatted for fine-tuning GPT-4o models and should be ready for use immediately after creation.
