class SimilaritySearch:
    def __init__(self, docs, target_source, collection, threshold =0.5):
        self.docs= docs
        self.target_source=target_source
        self.collection = collection
        self.threshold = threshold
    
    def find_similar_chunks(self):
        res=[]
        for doc in self.docs:
            embedding= doc.get("embeddings")
            matches = self.collection.similarity_search_by_vector_with_relevance_scores(
                embedding= embedding,
                k=3,
                filter={"source": self.target_source}
            )
            for matched_doc, dist in matches:
                similarity_score = 1.0 - dist
                if similarity_score >= self.threshold:
                    res.append({
                        "source_content": doc["content"],
                        "source_metadata": doc.get("metadata", {}),
                        "matched_content": matched_doc.page_content,
                        "matched_metadata": matched_doc.metadata,
                        "similarity_score": round(similarity_score, 4)
                    })
        return res