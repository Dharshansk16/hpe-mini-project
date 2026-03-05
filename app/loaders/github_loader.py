class GithubLoader:
    def __init__(self,git_client, repo):
        if not repo or not isinstance(repo ,str):
            raise ValueError("GitHub repository name must be a non-empty string.")
        
        self.git_client = git_client
        self.repo =repo

    def fetch_files(self):
        try:
            repo =self.git_client.get_user().get_repo(self.repo)
        except Exception as e:
            raise ValueError(f" Failed to connect to github: {str(e)}")
        
        contents = repo.get_contents("")
        

        documents = []
        while contents:
            file_content = contents.pop(0)
            if file_content.type=="dir":
                contents.extend(repo.get_contents(file_content.path))
            elif file_content.type=="file":
                try:
                    file_data = file_content.decoded_content.decode("utf-8")
                    doc= {
                        "content": file_data,
                        "metadata": {
                            "path": file_content.path,
                            "filename": file_content.name,
                            "repository":self.repo, 
                            "source":"github",

                        }
                    }
                    documents.append(doc)
                except Exception as e:
                    print(f"Failed to decode file {file_content.path}: {str(e)}")
        return documents
    

    

    