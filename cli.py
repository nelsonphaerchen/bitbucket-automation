import sys, os
from cloud.bitbucket import bitbucketCli

# Try to load the .env file. If doesn't exists, use the environment variable
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("KEY")
secret = os.getenv("SECRET")
cli = bitbucketCli(key=key, secret=secret)

def main():
    # Need at least the script name and the function name
    if len(sys.argv) < 2:
        print_usage()
        # Indicate an error
        return 1  

    function_name = sys.argv[1]
     # Arguments after the function name
    arguments = sys.argv[2:] 

    if function_name == "createProject":
        if len(arguments) != 5:
            print_usage("createProject")
            return 1
        create = cli.createProject(arguments[0],arguments[1],arguments[2],arguments[3],arguments[4])
        print (create)

    elif function_name == "createRepo":
        if len(arguments) != 4:
            print_usage("createRepo")
            return 1
        create = cli.createRepo(arguments[0], arguments[1], arguments[2], arguments[3])
        print (create)
    elif function_name == "addUser":
        if len(arguments) != 4:
            print_usage("addUser")
            return 1
        addUser = cli.addUser(arguments[0], arguments[1], arguments[2], arguments[3])
        print (addUser)
    elif function_name == "deleteUser":
        if len(arguments) != 4:
            print_usage("deleteUser")
            return 1
        delete = cli.deleteUser(arguments[0], arguments[1], arguments[2], arguments[3])
        print (delete)
    elif function_name == "branchRestriction":
        if len(arguments) != 5:
            print_usage("branchRestriction")
            return 1
        create = cli.branchRestriction(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4])
        print (create)        
    else:
        print_usage()  # Invalid function name
        return 1

def print_usage(func_name=None):
    print("Usage:")
    print(f"  python {sys.argv[0]} createProject workspace project-name description project-key is-private(true or false)")
    print(f"  python {sys.argv[0]} createRepo workspace project-key repository-name is-private(true or false)")
    print(f"  python {sys.argv[0]} addUser workspace repository-name User UID permission")
    print(f"  python {sys.argv[0]} deleteUser workspace repository-name User UID")
    print(f"  python {sys.argv[0]} cli.py branchRestriction workspace repository-name branch_match_kind kind type")
    
    if func_name:
        if func_name == "createProject":
          print("  createProject: Takes five arguments.")
        elif func_name == "createRepo":
          print("  createRepo: Takes four arguments.")
        elif func_name == "addUser":
          print("  addUser: Takes four arguments.")
        elif func_name == "deleteUser":
          print("  deleteUser: Takes four arguments.")
        elif func_name == "branchRestriction":
          print("  branchRestriction: Takes five arguments.")
    else:
        print("Function not avaliable")


if __name__ == "__main__":
    sys.exit(main()) # Use sys.exit to return the error code