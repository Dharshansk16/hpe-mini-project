from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from core.config import GOOGLE_API_KEY

from retrieving.retrieve_chunks import RetrieveChunks
from similarity.similar_chunks import SimilaritySearch
from utils.pretty_print import PrettyPrint

class SimilarityPipeline:
    def __init__(self):
        pass
        
    def runSimilarityPipeline(self):
        gemini_chroma_client = Chroma(
            collection_name="unified_docs_gemini",
            persist_directory="./app/vector_store/chroma_gemini",
            embedding_function=GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                google_api_key=GOOGLE_API_KEY
            ),
            collection_metadata={"hnsw:space": "cosine"}
        )
        ollama_chroma_client = Chroma(
            collection_name="unified_docs_ollama",
            persist_directory="./app/vector_store/chroma_ollama",
            embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
            collection_metadata={"hnsw:space": "cosine"}
        )

        gemini_retriever = RetrieveChunks(gemini_chroma_client)
        jira_chunks_gemini = gemini_retriever.retrieve_chunks("jira")

        ollama_retriever = RetrieveChunks(ollama_chroma_client)
        jira_chunks_ollama= ollama_retriever.retrieve_chunks("jira")

        similarity_search_gemini = SimilaritySearch(docs=jira_chunks_gemini, target_source="github", collection=gemini_chroma_client)
        similar_chunks_gemini = similarity_search_gemini.find_similar_chunks()

        similarity_search_ollama = SimilaritySearch(docs=jira_chunks_ollama, target_source="github", collection=ollama_chroma_client)
        similar_chunks_ollama = similarity_search_ollama.find_similar_chunks()

        PrettyPrint.pretty_print(similar_chunks_ollama[:5])
        PrettyPrint.pretty_print(similar_chunks_gemini[:5])






        

        
        
