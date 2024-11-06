import logging
import requests
from constants import EXCLUSION_PATTERNS, SONARCLOUD_API_URL

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def filter_issues_by_component(issues):
    """
    Filter issues based on exclusion patterns defined in EXCLUSION_PATTERNS.
    
    Args:
        issues (list): List of issues to be filtered.
    
    Returns:
        list: List of filtered issues.
    """
    return [
        issue for issue in issues
        if all(pattern not in issue.get("component", "") for pattern in EXCLUSION_PATTERNS)
    ]

def get_open_issues(project_key, token):
    """
    Retrieve open issues from SonarCloud for a given project key.
    
    Args:
        project_key (str): The SonarCloud project key.
        token (str): The authentication token.
    
    Returns:
        list: List of open issues for the project.
    """
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
