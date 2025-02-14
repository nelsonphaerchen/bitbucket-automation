import requests
import json
from requests.auth import HTTPBasicAuth

class bitbucketCli():
    # Initialize the script and get the access_token to be used in all functions
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

        auth_url = 'https://bitbucket.org/site/oauth2/access_token'
        auth_data = {
            'grant_type': 'client_credentials'
        }

        response = requests.post(auth_url, data=auth_data, auth=HTTPBasicAuth(self.key, self.secret))

        if response.status_code == 200:
            access_token = response.json().get('access_token')
            self.token = access_token
        else:
            print(f'Error: {response.content}')

    ### Create a Project in the a workspace.
    ### Project name, project Key and if it's private or not are mandatory
    ### The values from the function arguments are used to create the Json payload
    ### AS private is boolean, I added a if to validate if the value is boolean, if not
    ### it'll convert it to boolean  
    def createProject(self, workspace, project, description, key, private):
        url = f"https://api.bitbucket.org/2.0/workspaces/{workspace}/projects"
        token = self.token
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
            }
        if type(private)!=bool:
            private = eval(private)

        payload = json.dumps( {
                "name": project,
                "key": key,
                "description": description,
                "is_private": private
                } )
        
        response = requests.post(url, headers=headers, data=payload)
        print(response.json)
        return response.json()

    ### Create a Repositoru in the a Project.
    ### Workspace, Repository name, Project Key, and private or not are mandatory
    ### AS private is boolean, I added a if to validate if the value is boolean, if not
    ### it'll convert it to boolean  
    def createRepo(self, workspace, project_key, repo_name, private):
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_name}"
        token = self.token
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
            }
        
        if type(private)!=bool:
            private = eval(private)

        payload = json.dumps( {
            "scm": "git",
            "project": {
               "key": project_key
              },
            "is_private": private
            } )
        print (payload)
        response = requests.post(url, headers=headers, data=payload)
        return response.json()

    ### Add user and permission to the repository.
    ### The project request user management, but I couldn't how to create
    ### users in the  Bitbucket cloud. 
    ### Added it instead of function to add user to Bitbucket. 
    ### App token needed.
    def addUser(self, workspace, repo_name, username, permission):
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_name}/permissions-config/users/{username}"
        token = self.token
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
            }
        
        payload = json.dumps( {
        "permission": permission
        } )

        response = requests.put(url, headers=headers, data=payload)

        return response.json()

    ### Delete user permission added to the repository.
    ### Added it instead of function to delete user from Bitbucket.
    ### App token needed.
    def deleteUser(self, workspace, repo_name, username, permission):
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_name}/permissions-config/users/{username}"
        token = self.token
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
            }
        
        payload = json.dumps( {
        "permission": permission
        } )

        response = requests.delete(url, headers=headers, data=payload)

        return response.json()

    ### Create the restriction for the branch.
    ### It has a if statement to create different payloads for Glob and Branching model
    ### One restriction at the time. I'm looking for a better documentation to create multiple rules
    ### at once.   
    def branchRestriction (self, workspace, repo_name, branch_kind, kind, pattern_type):
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_name}/branch-restrictions"
        token = self.token
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
            }
        
        payload = {}

        if kind == "restrict_merges":
            print("Report the number of merger approvals")
            value = input("")
        else:
            value = None

        branch_name = pattern_type
        branch_type = pattern_type

        if branch_kind.lower() == "glob":

            payload.update({
                    "pattern": branch_name,
                    "branch_match_kind": branch_kind,
                    "kind": kind,
                    "value": value,
                    "users": [],
                    "groups": []
                    })

        elif branch_kind.lower() == "branching_model":
            
            payload.update(
                    {                            
                    "branch_match_kind": branch_kind,
                    "branch_type": branch_type,
                    "kind": kind,
                    "value": value,
                    "users": [],
                    "groups": []
                    }
                )

        else:
            print("\n Type of restriction not found")

        payload = json.dumps(payload)
        
        response = requests.post(url, headers=headers, data=payload)
        
        return response.json()

    ### Function to get the restriction rule and colect values to be 
    ### used in the update restriction function

    def getRestricitons(self, workspace, repo_name):
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_name}/branch-restrictions"
        token = self.token
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
            }

        response = requests.get(url, headers=headers)
        return response.json()

    ### Update the restriction already created
    ### It has a if statement to create different payloads for Glob and Branching model
    ### Step is in development   
    def updateRestriction(self, workspace, repo_name, kind, type):
        roles = self.getRestricitons(workspace=workspace,repo_name=repo_name)
        for values in roles["values"]:
            ruleType = (values["branch_match_kind"])
            if ruleType == type:
                id = values["id"]

                url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_name}/branch-restrictions/{id}"
                token = self.token
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                    }

                payload = {}

                if kind == "restrict_merges":
                    print("Report the number of merger approvals")
                    value = input("")
                else:
                    value = None

                if type.lower() == "glob":

                    payload.update({
                            "pattern": values["pattern"],
                            "branch_match_kind": values["branch_match_kind"],
                            "kind": kind,
                            "value": value,
                            "users": [],
                            "groups": []
                            })

                elif type.lower() == "branching_model":
                    
                    payload.update(
                            {                            
                            "branch_match_kind": values["branch_match_kind"],
                            "branch_type": values["branch_type"],
                            "kind": kind,
                            "value": value,
                            "users": [],
                            "groups": []
                            }
                        )

                else:
                    print("\n Type of restriction not found")
                    break

                payload = json.dumps(payload)
                response = requests.put(url, headers=headers, data=payload)

                return response.json()
            
