class RetrieveChunks:
    def __init__(self, collection):
        self.collection = collection


    def retrieve_chunks(self, source):
        if source not in ["github", "jira"]:
            raise ValueError("Source must be either 'github' or 'jira'.")
        
        res = self.collection.get(
            where={"source": source},
            include=["metadatas", "embeddings", "documents"]
        )
        chunks = []
        for doc, meta, embeddings in zip(res["documents"], res["metadatas"], res["embeddings"]):
            chunks.append({
                "content": doc,
                "metadata": meta,
                "embeddings": embeddings
            })

        return chunks
        
    