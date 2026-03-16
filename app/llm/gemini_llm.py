from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import GOOGLE_API_KEY


class GeminiLLM:
    def __init__(self, model="gemini-2.0-flash"):
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=GOOGLE_API_KEY,
            temperature=0
        )

    def get_llm(self):
        return self.llm
