from github import Github
from github import Auth

# Authenticate using the fine-grained token from secrets
auth = Auth.Token(st.secrets["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"])
g = Github(auth=auth)

# The rest of your upload logic remains the same
repo = g.get_repo("pwngithub/pwnhomes")
