from pipeline.knowledge_ingestion_pipeline import KnowledgeIngestionPipeline
from core.config import GITHUB_REPO, JIRA_PROJECT_KEY, GITHUB_TOKEN, JIRA_SERVER, JIRA_USERNAME, JIRA_API_TOKEN
from github import Github
from atlassian import Jira

class Main:
    def __init__(self):
        self.github_client =Github(GITHUB_TOKEN)
        self.jira_client=Jira(
            url=JIRA_SERVER,
            username=JIRA_USERNAME,
            password=JIRA_API_TOKEN,
            cloud=True
        )

        self.pipeline = KnowledgeIngestionPipeline(
            github_client=self.github_client,
            jira_client=self.jira_client,
            github_repo=GITHUB_REPO,
            jira_project_key=JIRA_PROJECT_KEY
        )
    def run(self):
        print("Starting knowledge ingestion pipeline...")
        self.pipeline.runPipeline()


if __name__ == "__main__":
    main= Main()
    main.run()
