from cloud.bitbucket import bitbucketCli
import os
import json

key = os.getenv("KEY")
secret = os.getenv("SECRET")

cli = bitbucketCli(key=key, secret=secret)

def main_menu():
    while True:
        print("Welcome to Bitbucket cli")
        print("1. Create a Project")
        print("2. Create a Repository")
        print("3. Add or remove user from Repository")
        print("4. Change Branch restrictions")
        print("5. Update Branch restrictions")
        print("0. Exit")

        select = input("Option: ")

        if select == "1":
            print("In which workspace do you want to create the project?")
            workspace = input("")
            print("Project Name")
            project = input("")
            print("Project's key. Eg.: Project Name, key = PN")
            key = input("")
            print("Project Description. (Optional)")
            description = input("")
            print("Is a private project? (Y/n)")
            private_i = input("")
            if private_i.lower() == None:
                private = True
            elif private_i.lower() == "y":
                private = True
            elif private_i.lower() == "n":
                private = False
            else:
                print("Not a valid option. Setting to Private by default")
                private = True

            create = cli.createProject(workspace=workspace,project=project,description=description,key=key,private=private)
            print (create)

        if select == "2":
            print("In which workspace do you want to create the repository?")
            workspace = input("")
            print("Project KEY")
            project_key = input("")
            print("Is a private project? (y/n)")
            private = input("")
            if private.lower() == "y":
                private = True
            elif private.lower() == "n":
                private = False
            print("Reposirtoy name")
            repo_name = input("")
            repo_name = repo_name.lower().replace(" ", "-")
            create = cli.createRepo(workspace=workspace,project_key=project_key,repo_name=repo_name, private=private)
            print (create)

        if select == "3":
            print("Inform the Workspace")
            workspace = input("")

            print("Reposirtoy name")
            repo_name = input("")
            repo_name = repo_name.lower().replace(" ", "-")

            print("Username")
            username =  input("")

            print("Permission read, write or admin?")
            permission =  input("")

            addUser = cli.addUser(workspace=workspace, repo_name=repo_name, username=username, permission=permission)
            print(addUser)

        if select == "4":
            print("Inform the Workspace")
            workspace = input("")

            print("Reposirtoy name")
            repo_name = input("")
            repo_name = repo_name.lower().replace(" ", "-")

            print("Is the restriction by branch Name or Model(release,feature,hotfix)? (name/model)")
            type =  input("")

            print("Restriction type. (Check the full list in the README.mb)")
            kind = input("")

            if type.lower() == "name":
                branch_kind = "glob"
                print("Inform the Branch you want to add restriction")
                branch = input("")

                addRestriciton = cli.branchRestriction(workspace=workspace, repo_name=repo_name, kind=kind, branch_kind=branch_kind, pattern_type=branch)
                print(addRestriciton)


            elif type.lower() == "type":
                branch_kind = "branching_model"
                print("Enter the type of branches you want to add restrictions to.")
                print("production, development, bugfix, release, feature or hotfix")
                branch_type = input("")

                print("\n Use option 5 in the main menu to add more restrictions")

                addRestriciton = cli.branchRestriction(workspace=workspace, repo_name=repo_name, kind=kind, branch_kind=branch_kind, pattern_type=branch_type)
                print(addRestriciton)

                
            else:
                print("\nInvalid\n")
                break
            

        if select == "5":
            print("Inform the Workspace")
            workspace = input("")

            print("Inform the repository name")
            repo_name = input("")
            repo_name = repo_name.lower().replace(" ", "-")

            print("Inform the restriction By branch name or model (name or model)")
            type = input("")

            print("Inform the restriction type. (Check the full list in the README.mb)")
            kind = input("")

            if type.lower() == "name":
                type = "glob"
            elif type.lower() == "type":
                type = "branching_model"
            else:
                print("\nInvalid\n")
                break

            updateRestriction = cli.updateRestriction(workspace=workspace, repo_name=repo_name, kind=kind, type=type)
            print(updateRestriction)

        if select == "6":
            uid = cli.getUserID(username="nelsonhaerchen")
            print(uid)

        if select == "0":
            break

# Start menu selection
main_menu()