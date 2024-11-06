import json
from os import getenv

from dotenv import load_dotenv
import openpyxl
import logging
from utils import get_open_issues
from constants import ISSUE_FIELDS, OUTPUT_FILE

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def write_issues_to_excel(project_keys, token, output_file):
    """
    Write issues for multiple projects to an Excel file.
    
    Args:
        project_keys (list): List of SonarCloud project keys.
        token (str): The authentication token.
        output_file (str): Path to the output Excel file.
    """
    workbook = openpyxl.Workbook()
    for idx, project_key in enumerate(project_keys):
        issues = get_open_issues(project_key, token)
        
        if idx == 0:
            sheet = workbook.active
            sheet.title = project_key
        else:
            sheet = workbook.create_sheet(title=project_key)

        # Define the headers
        headers = [field.capitalize() for field in ISSUE_FIELDS]
        sheet.append(headers)

        # Write each issue's information as a new row in the Excel sheet
        for issue in issues:
            row = [issue.get(field) for field in ISSUE_FIELDS]
            sheet.append(row)

    # Save the workbook to the specified file
    try:
        workbook.save(output_file)
        logging.info(f"Data written to {output_file}")
    except Exception as e:
        logging.error(f"Error saving the workbook to {output_file}: {e}")

def main():
    """
    Main function to load environment variables and write issues to an Excel file.
    """
    load_dotenv()
    project_keys_list = json.loads(getenv('SONARCLOUD_PROJECT_KEYS'))
    token = getenv('SONARCLOUD_TOKEN')

    write_issues_to_excel(
        project_keys_list,
        token,
        OUTPUT_FILE
    )

if __name__ == "__main__":
    main()
