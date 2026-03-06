import dotenv
import os

dotenv.load_dotenv()

REQUIERED_ENV_VARS = [
    "GITHUB_TOKEN",
    "GITHUB_REPO",
    "JIRA_SERVER",
    "JIRA_USERNAME",
    "JIRA_API_TOKEN",
    "JIRA_PROJECT_KEY",
    "GOOGLE_API_KEY",
]

missing_vars = [key for key in REQUIERED_ENV_VARS if not os.getenv(key)]

if missing_vars:
    raise ValueError(f"Missing required environment variables: {missing_vars}")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

