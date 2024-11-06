SONARCLOUD_API_URL = "https://sonarcloud.io/api/issues/search"
EXCLUSION_PATTERNS = ["/migrations/", "html"]
OUTPUT_FILE = "sonarcloud_issues2.xlsx"
ISSUE_FIELDS= ["message", "type", "severity", "effort", "component", "line"]