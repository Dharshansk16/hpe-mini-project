
class PrettyPrint:
    @staticmethod
    def pretty_print(similar_chunks):
        
        #Pretty print the similar chunks with their metadata and similarity scores
        print("\n" + "="*80)
        print(f"{'SIMILARITY SEARCH RESULTS':^80}")
        print("="*80)

        if not similar_chunks:
            print("No matches found above the similarity threshold.")
        else:
            for i, match in enumerate(similar_chunks, 1):
                print(f"\n[MATCH #{i}] | Score: {match['similarity_score']:.4f}")
                print("-" * 40)
                
                #jira
                print(f"JIRA (Source):")
                print(f"   Content: {match['source_content']}")
                
                #github
                print(f"GITHUB (Matched Code):")
                print(f"   File: {match['matched_metadata'].get('file_path', 'Unknown')}")
                print(f"   Code: {match['matched_content']}")
                
                print("-" * 80)