import sys, os
from cloud.bitbucket import bitbucketCli

key = os.getenv("KEY")
secret = os.getenv("SECRET")
cli = bitbucketCli(key=key, secret=secret)

def main():
    if len(sys.argv) < 2:  # Need at least the script name and the function name
        print_usage()
        return 1  # Indicate an error

    function_name = sys.argv[1]
    arguments = sys.argv[2:]  # Arguments after the function name

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
        if len(arguments) != 5:
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
    print(f"  python {sys.argv[0]} function1 arg1 arg2")
    print(f"  python {sys.argv[0]} function2 arg3 arg4")
    if func_name:
        if func_name == "branchRestriction":
          print("  branchRestriction: Takes five arguments.")
        elif func_name == "function2":
          print("  function2: Takes two arguments.")
    else:
        print("  Available functions: function1, function2")


if __name__ == "__main__":
    sys.exit(main()) # Use sys.exit to return the error code