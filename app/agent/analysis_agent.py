import json
import re
import time
from github import Github
from atlassian import Jira

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

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

        self.agent = self._build_agent()

    def _build_agent(self):

        system_prompt = """
You are a code-Jira relationship analyst. You will be given a Jira issue chunk
and a semantically similar GitHub code chunk.

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

{
    "jira_key": "<jira issue key>",
    "github_file": "<github file path>",
    "relationship_type": "<implements|bug_fix|related|stale_ticket|unrelated>",
    "summary": "<one sentence describing the relationship>",
    "suggested_action": "<recommended next step for the engineering team>"
}
"""

        agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=system_prompt
        )

        return agent

    def run(self, user_input: str):
        attempt = 0
        max_attempts = 3
        while attempt < max_attempts:
            try:
                result = self.agent.invoke(
                    {
                        "messages": [
                            HumanMessage(content=user_input)
                        ]
                    }
                )
                return {"output": self._extract_output_text(result)}
            except Exception as e:
                error_message = str(e)
                if "RESOURCE_EXHAUSTED" in error_message or "quota" in error_message.lower():
                    attempt += 1
                    if attempt >= max_attempts:
                        raise

                    wait_time = self._get_retry_wait_seconds(error_message)
                    print(f"Rate limit reached. Retrying in {wait_time}s... ({attempt}/{max_attempts})")
                    time.sleep(wait_time)
                else:
                    raise

    def _extract_output_text(self, result):
        if isinstance(result, dict) and "output" in result and isinstance(result["output"], str):
            return result["output"]

        messages = result.get("messages", []) if isinstance(result, dict) else []
        if not messages:
            return ""

        last_message = messages[-1]
        content = getattr(last_message, "content", "")

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            text_blocks = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_blocks.append(block.get("text", ""))
            return "\n".join(text_blocks)

        return str(content)

    def _get_retry_wait_seconds(self, error_message):
        retry_match = re.search(r"retry in\s+([0-9]+(?:\.[0-9]+)?)s", error_message, re.IGNORECASE)
        if retry_match:
            return max(1, int(float(retry_match.group(1))) + 1)
        return 45