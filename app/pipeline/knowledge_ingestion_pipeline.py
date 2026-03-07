from core.config import GOOGLE_API_KEY
from loaders.github_loader import GithubLoader
from loaders.jira_loader import JiraLoader
from processing.chunking import GithubChunker, JiraChunker 
from processing.embeddings import EmbeddingsProcessor
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings


class KnowledgeIngestionPipeline:
    def __init__(self, github_client, jira_client, github_repo, jira_project_key):
        self.github_loader = GithubLoader(github_client, github_repo)
        self.jira_loader = JiraLoader(jira_client, jira_project_key)
    
    def runPipeline(self):
        #fetch documents from github and jira
        github_docs = self.github_loader.fetch_files()
        jira_docs = self.jira_loader.fetch_issues()

        #chunk the documents seperately
        github_chunker = GithubChunker(chunk_size=1000, chunk_overlap=200)
        jira_chunker = JiraChunker(chunk_size=600, chunk_overlap=160)
        chunked_github_docs = github_chunker.get_chunks(github_docs)
        chunked_jira_docs= jira_chunker.get_chunks(jira_docs)
        
        print(f"Fetched {len(github_docs)} documents from GitHub and chunked into {len(chunked_github_docs)} chunks.")
        print(f"Fetched {len(jira_docs)} documents from Jira and chunked into {len(chunked_jira_docs)} chunks.")

        # #create embeddings for github chunks and jira chunks for gemini embedding model
        gemini_embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            goole_api_key = GOOGLE_API_KEY
            )
        
        github_embedder_gemini = EmbeddingsProcessor(
            collection_name="unified_docs_gemini",
            embeddings_model=gemini_embedding_model,
            persist_directory="./app/vector_store/chroma_gemini"
            )
        jira_embedder_gemini = EmbeddingsProcessor(
            collection_name="unified_docs_gemini",
            embeddings_model=gemini_embedding_model,
            persist_directory="./app/vector_store/chroma_gemini"
            )
        
        github_embedder_gemini.create_embeddings(chunked_github_docs)
        jira_embedder_gemini.create_embeddings(chunked_jira_docs)

        print("Created embeddings for both GitHub and Jira documents using Gemini embedding model.")

        #create embeddings for github chunks and jira chunks for ollama embedding model
        ollama_embedding_model = OllamaEmbeddings(model="qwen3-embedding:4b")
        github_embedder_ollama = EmbeddingsProcessor(
            collection_name="unified_docs_ollama", 
            embeddings_model=ollama_embedding_model, 
            persist_directory="./app/vector_store/chroma_ollama"
            )
        jira_embedder_ollama = EmbeddingsProcessor(
            collection_name="unified_docs_ollama", 
            embeddings_model=ollama_embedding_model, 
            persist_directory="./app/vector_store/chroma_ollama"
            )
        github_embedder_ollama.create_embeddings(chunked_github_docs)
        jira_embedder_ollama.create_embeddings(chunked_jira_docs)
        print("Created embeddings for both GitHub and Jira documents using Ollama embedding model.")



        
