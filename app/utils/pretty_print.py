
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

    @staticmethod #pretty print for analysis results
    def pretty_print_analysis(analysis_results):
        print("\n" + "="*80)
        print(f"{'AGENT ANALYSIS RESULTS':^80}")
        print("="*80)

        if not analysis_results:
            print("No analysis results available.")
        else:
            for i, result in enumerate(analysis_results, 1):
                relationship = result.get('relationship_type', 'unknown').upper()
                score = result.get('similarity_score', 0)
                print(f"\n[ANALYSIS #{i}] | Score: {score:.4f} | Type: {relationship}")
                print("-" * 40)
                print(f"Jira:             {result.get('jira_key', 'Unknown')}")
                print(f"GitHub File:      {result.get('github_file', 'Unknown')}")
                print(f"Summary:          {result.get('summary', '')}")
                print(f"Suggested Action: {result.get('suggested_action', '')}")
                print("-" * 80)