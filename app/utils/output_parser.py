import json


class Parser:
    def parse_output(self, output, jira_key, github_file, similarity_score):
        try:
            start = output.find("```json")
            end = output.find("```", start + 7)# len("```json") = 7
            if start != -1 and end != -1:
                json_str = output[start + 7:end].strip()
                parsed = json.loads(json_str)
                parsed["similarity_score"] = similarity_score
                return parsed
        except Exception:
            pass

        return {
            "jira_key": jira_key,
            "github_file": github_file,
            "relationship_type": "unknown",
            "summary": output[:200] if output else "No output",
            "suggested_action": "Review manually",
            "similarity_score": similarity_score
        }
