import json
from urllib import request
import requests


class ResponseError(Exception):
    pass


class TransferRepos:
    '''Class for GitHub Repository Transfer to new owner[user or organization]'''

    def __init__(self, token, username, transfer_to):
        '''Initialize the class variables'''
        _BASE_URL = "https://api.github.com/{ext}"
        self.phrase = "react-hooks-components-basics " #specify the repository keyword you wanna transfer
        self._username = username
        self._transfer_to = transfer_to

        self._TRANSFER_URL = _BASE_URL.format(ext="repos/{username}/{repository}/transfer")
        self._REPOSITORY_URL = _BASE_URL.format(ext="users/{username}/repos")

        self._TRANSFER_HEADERS = {
            "Accept": "application/vnd.github.nightshade-preview+json",
            "Content-Type": "application/json",
            "Authorization": "token {}".format(token)
        }

    @staticmethod
    def _validate_response(response):

        if response.status_code >= 200 and response.status_code <= 300:
            return response.text

        raise ResponseError(f"Status code out of range: {response.status_code}\n{response.text}")

    def get_repos2(self,username, phrase):
        '''
        This method returns a list of repositories you want to move
        It calls the GitHub Get repos API given the phrase and your username
        '''
        phrase="phase-3-methods"
        base_url = f"https://api.github.com/users/{username}/repos?per_page=1000"
        url = request.Request(base_url, method='GET')

        phrase_s = phrase.split("-")[0]

        with request.urlopen(url) as url:
            get_repos = url.read()
            get_repo_resp = json.loads(get_repos)
            
            repo_names = []

            for repo in get_repo_resp:
                

                rpnm = repo['name'].split('-')
                # print (phrase_s) 
                if phrase_s in rpnm:
                    # print("here")
                    repo_names.append(repo["name"])
            
            if len(repo_names) == 0:
                return "empty"
            # print(repo_names)
            return repo_names


    def transfer_repo(self, repo):
        '''This method does the actual repository transfer with the help 
        of the GitHub API (POST) 
        The API Takes in your username and the new owner details alongside your token details
        '''
        print(f"Making request for {repo}")

        response = requests.post(
            self._TRANSFER_URL.format(
                username=self._username,
                repository=repo
            ),
            headers=self._TRANSFER_HEADERS,
            data=json.dumps({
                "new_owner": self._transfer_to
            })
        )

        if self._validate_response(response):
            print("Success")

    def main(self, keep=None, transfer=None):
        print("Starting transfer process")

        for repo in self.get_repos2(self._username,self.phrase):
            print(repo)
            if keep is not None and repo in keep:
                continue

            elif transfer is not None:
                if repo in transfer:
                    self.transfer_repo(repo)

            else:
                self.transfer_repo(repo)

        print("Done")
    

''' Creating an Instance of your class and giving the object actual values'''

tkn = "ghp_v6k5m2K7FOdYyqdZ17VY9H" #insert your GitHub Token
from_user = "kilonzif" #insert your GitHub Username
new_owner = "FlatironMoringa" #insert your new organization to transfer to 


trans= TransferRepos(tkn,from_user,new_owner)

trans.main()
