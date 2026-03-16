import json
from github import Github
from atlassian import Jira
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from core.config import GITHUB_TOKEN, JIRA_SERVER, JIRA_USERNAME, JIRA_API_TOKEN
from llm.gemini_llm import GeminiLLM

from agent.build_tools import BuildTools



class AnalysisAgent:
    def __init__(self, collection):
        self.github_client = Github(GITHUB_TOKEN)
        self.jira_client = Jira(
            url=JIRA_SERVER,
            username=JIRA_USERNAME,
            password=JIRA_API_TOKEN,
            cloud=True
        )
        
        self.collection = collection

        bt = BuildTools(self.github_client, self.jira_client, self.collection)
        self.tools = bt._build_tools()
        self.llm = GeminiLLM().get_llm()

        

    def _build_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a code-Jira relationship analyst. You will be given a Jira issue chunk and a semantically similar GitHub code chunk.

Your task is to:
1. Analyse the relationship between the Jira issue and the GitHub code
2. Use tools to fetch more context if the chunks alone are insufficient
3. Classify the relationship as exactly one of:
   - implements: the code directly implements the Jira story or task
   - bug_fix: the code addresses a Jira bug report
   - related: generally related but not a direct implementation
   - stale_ticket: the Jira ticket appears already done based on the existing code
   - unrelated: high similarity score but actually unrelated content

Always end your response with a JSON block in this exact format:
```json
{{
    "jira_key": "<jira issue key>",
    "github_file": "<github file path>",
    "relationship_type": "<implements|bug_fix|related|stale_ticket|unrelated>",
    "summary": "<one sentence describing the relationship>",
    "suggested_action": "<recommended next step for the engineering team>"
}}
```"""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=False, handle_parsing_errors=True)

