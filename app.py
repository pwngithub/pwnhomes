import streamlit as st
import pandas as pd
import io
from github import Github
import datetime

# App configuration
st.set_page_config(page_title="Homes Service Dashboard", layout="wide")

# --- GITHUB CONFIGURATION ---
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
REPO_NAME = "pwngithub/pwnhomes"
BRANCH = "main"
UPLOAD_FOLDER = "upload/" # Folder name in GitHub

def upload_to_github(file_content, file_name):
    """Uploads the file content to the specified GitHub repository."""
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        
        # Create unique filename with timestamp to avoid collisions
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        full_path = f"{UPLOAD_FOLDER}{timestamp}_{file_name}"
        
        repo.create_file(
            path=full_path,
            message=f"Upload new homes data: {file_name}",
            content=file_content,
            branch=BRANCH
        )
        return True, full_path
    except Exception as e:
        return False, str(e)

# --- UI LAYOUT ---
st.title("🏠 Broadband Connectivity Dashboard")

uploaded_file = st.sidebar.file_uploader("Upload 'Homes Summary' TXT file", type="txt")

if uploaded_file is not None:
    # Read the file
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    raw_text = stringio.read()
    
    # Action Button for GitHub
    if st.sidebar.button("Push to GitHub & Run Report"):
        success, info = upload_to_github(raw_text, uploaded_file.name)
        if success:
            st.sidebar.success(f"Uploaded to GitHub: {info}")
        else:
            st.sidebar.error(f"GitHub Error: {info}")

    # Process Data for Report
    try:
        # Handling the extra leading commas in your format
        df = pd.read_csv(io.StringIO(raw_text), header=None)
        
        # Clean up: remove empty columns and select useful ones
        # Based on your sample: Col 2=ID, Col 5=Name, Col 6=Total, Col 7=Active
        df = df.iloc[:, [2, 5, 6, 7]] 
        df.columns = ["ID", "Name", "Total Homes", "Active Homes"]
        
        # Calculate KPIs
        df["Total Homes"] = pd.to_numeric(df["Total Homes"], errors='coerce')
        df["Active Homes"] = pd.to_numeric(df["Active Homes"], errors='coerce')
        df = df.dropna(subset=["Total Homes", "Active Homes"])
        df["Active %"] = (df["Active Homes"] / df["Total Homes"] * 100).round(2)

        # Global Totals
        total_h = df["Total Homes"].sum()
        total_a = df["Active Homes"].sum()
        overall_p = (total_a / total_h * 100) if total_h > 0 else 0

        # UI Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Homes Passed", f"{total_h:,.0f}")
        col2.metric("Total Active Homes", f"{total_a:,.0f}")
        col3.metric("Overall Penetration", f"{overall_p:.2f}%")

        st.divider()

        # Display Data Table
        st.subheader("Line-by-Line Service Detail")
        st.dataframe(
            df[["Name", "Total Homes", "Active Homes", "Active %"]],
            column_config={
                "Active %": st.column_config.ProgressColumn(
                    "Activation Rate", format="%.2f%%", min_value=0, max_value=100
                ),
            },
            use_container_width=True,
            hide_index=True
        )
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a .txt file in the sidebar to generate the report.")
