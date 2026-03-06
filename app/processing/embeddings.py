from langchain_chroma import Chroma
from langchain_core.documents import Document

class EmbeddingsProcessor:
    def __init__(self, collection_name, embeddings_model, persist_directory):
        self.collection_name = collection_name
        self.embeddings_model = embeddings_model
        self.persist_directory = persist_directory
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings_model,
            persist_directory=self.persist_directory
        )

    def create_embeddings(self, documents):
        docs = [Document(page_content=doc["content"], metadata=doc.get("metadata", {})) for doc in documents]
        self.vector_store.add_documents(docs)
    