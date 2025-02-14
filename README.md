# Bitbucket CLI
Tool developed for a coding challenge.

### About it 
Bitbucket CLI is a Python script that handles basic functions in the Bitbucket Cloud. 
These base functions are:
* Create Project - Creates a project in a defined Workspace
* Create Repository - Creates a repository in a defined Workspace and assigns it to a Project
* Add  User - Add users and their permissions to a Repository
* Delete User - Remove users from a Repository 
* Branch Restriction - Add restriction to a branch. You can limit push to master, block deletion, etc.

### First step
Create a consumer using the Atlassian Bitbucket Cloud documentation:
https://support.atlassian.com/bitbucket-cloud/docs/use-oauth-on-bitbucket-cloud/
Add the Key and Secret to a .env file or export them in the terminal:
.env:

 KEY=Key
 SECRET=Secret

Terminal:

 export KEY=Key
 export SECRET=Secret
There's no need to get the access_token, it'll be handled when you call the script.

### How to use
There are two options, cli and interaction_cli.
The cli is used to pass the function and arguments directly from the shell.
The interaction_cli is a script with menus that makes the script more user-friendly
*Tip: Put parameters with space or dash between double quotes.*
#### cli
The cli is used in the following way:
python3 cli.py functionName arguments
Functions usage:
**Create Project**:
* python3 cli.py createProject workspace project-name description project-key is-private(true or false). Eg:
* python3 cli.py createProject nelsonhaerchen project "Some description" PJ False

**Create Repository**:
* python3 cli.py createRepo workspace project-key "repository-name" is-private(true or false). Eg:
* python3 cli.py createRepo nelsonhaerchen PJ "application-name" False

**Add User to the Repository**:
* python3 cli.py addUser workspace "repository-name" "User UID" permission
* This API is only accessible with the following authentication types: apppassword, session, api_token

**Delete User to the Repository**:
* python3 cli.py addUser workspace "repository-name" "User UID"
* This API is only accessible with the following authentication types: apppassword, session, api_token

**Branch Restriction**:
There are two ways to match a branch. It is configured in **branch_match_kind**:

1.  `glob`: Matches a branch against the `pattern`. A `'*'` in `pattern` will expand to match zero or more characters, and every other character matches itself. For example, `'foo*'` will match `'foo'` and `'foobar'`, but not `'barfoo'`. `'*'` will match all branches.
2.  `branching_model`: This matches a branch against the repository's branching model. The `branch_type` controls the type of branch to match. Allowed values include `production`, `development`, `bugfix`, `release`, `feature`, and `hotfix`.

**Kind** describes what will be restricted. Allowed values include: 
`push`, `force`, `delete`, `restrict_merges`, `require_tasks_to_be_completed`, `require_approvals_to_merge`, `require_default_reviewer_approvals_to_merge`, `require_no_changes_requested`, `require_passing_builds_to_merge`, `require_commits_behind`, `reset_pullrequest_approvals_on_change`, `smart_reset_pullrequest_approvals`, `reset_pullrequest_changes_requested_on_change`, `require_all_dependencies_merged`, `enforce_merge_checks`, and `allow_auto_merge_when_builds_pass`.

Glob:
* python3 cli.py branchRestriction workspace "repository-name" branch_match_kind kind master. Eg:
* python3 cli.py branchRestriction nelsonhaerchen "application-name" glob push master

Branching model:
* python3 cli.py branchRestriction workspace "repository-name" branch_match_kind kind branch_type. Eg:
* python3 cli.py branchRestriction nelsonhaerchen "application-name" branching_model push production
