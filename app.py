import streamlit as st
from github import Github, Auth

def check_github_connection():
    try:
        auth = Auth.Token(st.secrets["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"])
        g = Github(auth=auth)
        repo = g.get_repo("pwngithub/pwnhomes")
        return f"Connected to: {repo.full_name}"
    except Exception as e:
        return f"Connection Failed: {e}"

if st.sidebar.button("Test GitHub Connection"):
    status = check_github_connection()
    st.sidebar.write(status)
