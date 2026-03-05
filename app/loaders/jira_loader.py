class JiraLoader:
    def __init__(self, jira_client, project_key):
        self.jira_client = jira_client
        if not project_key or not isinstance(project_key, str):
            raise ValueError("Jira project key must be a non-empty string.")
        self.project_key = project_key

    def fetch_issues(self):
        try:
            res = self.jira_client.jql(f'project = {self.project_key}')
            issues = res.get('issues', [])
            documents = []
            for issue in issues:
                fields = issue.get('fields', {})

                description = fields.get('description', '')
                summary = fields.get("summary", "No Summary")
                full_content = f"Summary: {summary}\n\n Description: {description}"
                doc = {
                    "content": full_content,
                    "metadata": {
                        "key": issue.get("key"),
                        "summary": summary,
                        "status": fields.get("status", {}).get("name"),
                        "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
                        "source": "jira",
                        "project_key": self.project_key
                    }
                }
                documents.append(doc)
            return documents
        except Exception as e:
            raise ValueError(f"Failed to fetch issues from Jira: {str(e)}")

