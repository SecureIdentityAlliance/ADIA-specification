# DID-specification
Main specification repository

The clone the repository locally:
1. Click on "Code" and copy the HTTPS-URL -or- choose "Open with GitHub Desktop" (see note below)
2. run "git" in a terminal window in a folder for git repositories (download git: https://git-scm.com/downloads)
3. change to the newly created folder "DID-specification"


To compile the .bs files to .html, please:
1. Install bikeshed (install from https://tabatkins.github.io/bikeshed/)
2. Run "python.exe ../bikeshed/bikeshed.py spec  did-sample.bs"

NOTES:
- Bikeshed requires Python 3.7 (download here: https://www.python.org/downloads/release/python-379/) DO NOT USE 3.8 or higher.
- Bikeshed also requires git (download here: https://git-scm.com/downloads)


Please create "Issues" in github to report any errors or room for improvements in the existing draft.
Then create a new branch fixing the "Issue" and create a "Pull Request" that will tie that proposed change
to the Issue.

Important:
- For any pull request, please assign two (2) reviewers.
- Do not merge any pull request without review or discussion within TWG.
- Never commit any changes directly to the 'master' branch. Always create an issue, a different branch and a pull request first!


GitHub Desktop:
Github Desktop is a GUI interface for git operations.  It can be used instead of command line git commands for people who prefer that.
Link to download: https://desktop.github.com/
There is an installation wizard that will guide you to connect GitHub Desktop to GitHub online and you will be able to create a copy of the spec repository on your local machine.
