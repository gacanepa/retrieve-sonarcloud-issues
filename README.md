# Retrieve Issues From SonarCloud

List of issue keys. Pick from here and update `ISSUE_FIELDS` in the constants file to retrieve the desired fields.

- `key`
- `rule`
- `severity`
- `component`
- `project`
- `line`
- `hash`
- `textRange`
- `flows`
- `status`
- `message`
- `effort`
- `debt`
- `assignee`
- `author`
- `tags`
- `creationDate`
- `updateDate`
- `type`
- `organization`
- `cleanCodeAttribute`
- `cleanCodeAttributeCategory`
- `impacts`
- `issueStatus`

## How to run

0. Set the environment variables via an .env file

```
SONARCLOUD_PROJECT_KEYS = ["project1", "project2"]
SONARCLOUD_TOKEN = "your-sonarcloud-token"
```

1. Create a virtual environment and install the dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```

2. Run the script

```bash
python retrieve_issues.py
```