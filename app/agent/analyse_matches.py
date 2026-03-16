from utils.output_parser import Parser
import time

op = Parser()

class AnalyseMatches:

    def __init__(self, matches, agent):
        self.matches = matches
        self.agent = agent

    def analyse_matches(self):
        print(f"\nAnalysing {len(self.matches)} matches with agent...")
        results= []
        
        for i, match in enumerate(self.matches ,1):
            jira_key = match.get("source_metadata", {}).get("key", "Unknown") #get jira ticket key
            github_file = match.get("matched_metadata", {}).get("path", "Unknown") #get github file path
            print(f"[{i}/{len(self.matches)}] Analysing {jira_key} <--> {github_file}")

            input_text = (
                f"jira Issue Key: {jira_key}\n"
                f"Jira Content:\n{match['source_content']}\n\n"
                f"GitHub File: {github_file}\n"
                f"GitHub Code:\n{match['matched_content']}\n\n"
                f"Similarity Score: {match['similarity_score']}\n\n"
                "Analyse the relationship between this Jira issue and the GitHub code."
            )
            try:
                response = self.agent.run(input_text)
                analysis = op.parse_output(
                    response.get("output", ""), jira_key, github_file, match['similarity_score']
                )
                results.append(analysis)
                if i < len(self.matches):
                    time.sleep(3)
            #if error
            except Exception as e:
                results.append({
                    "jira_key": jira_key,
                    "github_file": github_file,
                    "relationship_type": "error",
                    "summary": f"Analysis failed: {str(e)}",
                    "suggested_action": "Retry analysis manually",
                    "similarity_score": match['similarity_score']
                })

        return results