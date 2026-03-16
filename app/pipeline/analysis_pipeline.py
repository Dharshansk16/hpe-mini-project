from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from agent.analysis_agent import AnalysisAgent
from core.config import GOOGLE_API_KEY
from retrieving.retrieve_chunks import RetrieveChunks
from similarity.similar_chunks import SimilaritySearch
from utils.pretty_print import PrettyPrint
from agent.analyse_matches import AnalyseMatches

class AnalysisPipeline:
    def __init__(self):
        pass

    def runAnalysisPipeline(self):
        gemini_chroma_client = Chroma(
            collection_name="unified_docs_gemini",
            persist_directory="./app/vector_store/chroma_gemini",
            embedding_function=GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                google_api_key=GOOGLE_API_KEY
            ),
            collection_metadata={"hnsw:space": "cosine"}
        )

        gemini_retriever = RetrieveChunks(gemini_chroma_client)
        jira_chunks = gemini_retriever.retrieve_chunks("jira")

        similarity_search = SimilaritySearch(
            docs=jira_chunks,
            target_source="github",
            collection=gemini_chroma_client
        )
        similar_chunks = similarity_search.find_similar_chunks()
        similar_chunks.sort(key=lambda x: x["similarity_score"], reverse=True)

        top_matches = similar_chunks[:5]
        PrettyPrint.pretty_print(top_matches)

        agent = AnalysisAgent(collection=gemini_chroma_client)
        analyser = AnalyseMatches(top_matches, agent)
        analysis_results = analyser.analyse_matches()
        PrettyPrint.pretty_print_analysis(analysis_results)