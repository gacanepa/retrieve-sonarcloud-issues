import json
from os import getenv

from dotenv import load_dotenv
import openpyxl
from http_constants.status import OK
import requests
import logging

from constants import EXCLUSION_PATTERNS, ISSUE_FIELDS, SONARCLOUD_API_URL, OUTPUT_FILE

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def filter_issues_by_component(issues):
    return [
        issue for issue in issues
        if all(pattern not in issue.get("component", "") for pattern in EXCLUSION_PATTERNS)
    ]

def get_open_issues(project_key, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    issues = []
    page = 1
    # Maximum items per page as per SonarCloud API
    page_size = 100

    while True:
        params = {
            "componentKeys": project_key,
            "statuses": "OPEN",
            "pageSize": page_size,
            "p": page
        }

        try:
            response = requests.get(SONARCLOUD_API_URL, headers=headers, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data for project {project_key}: {e}")
            break

        data = response.json()
        
        # Refer to the README file for a list of all available fields
        for issue in data.get("issues", []):
            issue_info = {
                "message": issue.get("message"),
                "type": issue.get("type"),
                "severity": issue.get("impacts")[0].get("severity"),
                "effort": issue.get("effort"),
                "component": issue.get("component"),
                "line": issue.get("line"),
            }
            issues.append(issue_info)

        # Check if there are more pages
        if data.get("paging", {}).get("total", 0) <= len(issues):
            break
        # Move to the next page
        page += 1 

    return filter_issues_by_component(issues)

def write_issues_to_excel(project_keys, token, output_file):
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
