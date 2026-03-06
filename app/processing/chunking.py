from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from abc import ABC, abstractmethod


class BaseChunker(ABC):
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    @abstractmethod
    def get_splitter(self, doc):
        pass

    def getChunks(self, documents):
        chunked_docs= []
        for doc in documents:
            splitter = self.get_splitter(doc)
            splits = splitter.split_text(doc["content"])
            for i , split in enumerate(splits):
                chunked_docs.append({
                    "content": split,
                    "metadata": doc.get("metadata", {}),
                    "chunk_index": i
                })

        return chunked_docs

class GithubChunker(BaseChunker):
    EXTENSION_MAP = {
        "py": Language.PYTHON,
        "js": Language.JAVASCRIPT,
        "java": Language.JAVA,
        "md": Language.MARKDOWN,
        "txt": Language.PLAIN_TEXT,
    }

    def get_splitter(self, doc):
        metadata = doc.get("metadata", {})
        extension = metadata.get("extension", "txt").lower()
        language = self.EXTENSION_MAP.get(extension, Language.PLAIN_TEXT)
        return RecursiveCharacterTextSplitter(
            language=language,
            chunk_size= self.chunk_size,
            chunk_overlap= self.chunk_overlap,
        )
class JiraChunker(BaseChunker):
    def get_splitter(self, doc):
        return RecursiveCharacterTextSplitter(language=Language.PLAIN_TEXT,
                                              chunk_size=self.chunk_size,
                                              chunk_overlap=self.chunk_overlap)
    
            
            