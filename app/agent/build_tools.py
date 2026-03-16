from core.config import GITHUB_REPO, JIRA_PROJECT_KEY
from pydantic import BaseModel, Field   
from langchain_core.tools import StructuredTool
class BuildTools:
    def __init__(self, github_client, jira_client,collection):
        self.github_client = github_client
        self.jira_client = jira_client
        self.collection = collection    
    
    def _build_tools(self):
        github_client = self.github_client
        jira_client = self.jira_client
        collection = self.collection

        class GetFileInput(BaseModel):
            path: str = Field(description="The file path in the GitHub repository")
        
        class GetJiraInput(BaseModel):
            key: str = Field(description="The Jira issue key ,e.g. SCRUM-42")
        
        class SearchInput(BaseModel):
            query: str = Field(description="The text query to search for related chunks in the vector store")
            


        def get_full_github_file(path: str)-> str:
            try:
                repo = github_client.get_user().get_repo(GITHUB_REPO)
                file_content = repo.get_contents(path)
                return file_content.decode_content.decode("utf-8")
            except Exception as e:
                return f"Error fetching file: {str(e)}"

        def get_full_jira_issue(key: str) -> str:
            try:
                issue = jira_client.issue(key)
                fields = issue.get("fields", {})
                description = fields.get("description", "No description")
                summary = fields.get("summary", "No summary")
                status = fields.get("status", {}).get("name", "Unknown")
                comments = fields.get("comment", {}).get("comments", [])
                comment_text = "\n".join([c.get("body", "") for c in comments[:3]])
                return f"Key: {key}\nSummary: {summary}\nStatus: {status}\nDescription: {description}\nComments:\n{comment_text}"
            except Exception as e:
                return f"Error fetching Jira issue: {str(e)}"
                                    

        def search_related_chunks(query: str) -> str:
            try:
                results = collection.similarity_search(query, k=3)
                return "\n\n".join([f"File: {r.metadata.get('file_path', 'Unknown')}\nContent: {r.page_content}" for r in results])
            except Exception as e:
                return f"Error searching for related chunks: {str(e)}"

        
        return [
            StructuredTool.from_function(
                func=get_full_github_file,
                name="get_full_github_file",
                description="Fetch the full content of a GitHub file by its path. Use when you need more context beyond the matched code chunk.",
                args_schema=GetFileInput
            ),
            StructuredTool.from_function(
                func=get_full_jira_issue,
                name="get_full_jira_issue",
                description="Fetch the full details of a Jira issue including description, status and comments. Use when the chunk alone lacks enough context.",
                args_schema=GetJiraInput
            ),
            StructuredTool.from_function(
                func=search_related_chunks,
                name="search_related_chunks",
                description="Search for additional related chunks in the vector store using a text query.",
                args_schema=SearchInput
            ),
        ]