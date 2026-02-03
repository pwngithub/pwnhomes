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
