import streamlit as st
import re
import os
import tempfile
import pandas as pd
from drive_utils import fetch_notebooks_from_drive
from compare import evaluate_student_notebooks

# Extract folder ID from Google Drive URL or raw ID
def extract_folder_id(input_str):
    match = re.search(r'/folders/([a-zA-Z0-9_-]+)', input_str)
    return match.group(1) if match else input_str.strip()

# Streamlit page setup
st.set_page_config(page_title="Student Code Evaluation Report", layout="wide")
st.title("📂 Student Code Evaluation Report")
folder_input = st.text_input("📁 Enter Google Drive Folder Link or ID")

if folder_input:
    folder_id = extract_folder_id(folder_input)

    with st.spinner("🔍 Fetching student folders and notebooks..."):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Fetch all notebooks and metadata
                student_data = fetch_notebooks_from_drive(folder_id, temp_dir)

                student_names = list(student_data.keys())
                selected_student = st.selectbox("Select a student folder", student_names)

                if selected_student:
                    student_info = student_data[selected_student]
                    notebooks = student_info["notebooks"]
                    notebook_count = len(notebooks)
                    subfolder_count = student_info["subfolder_count"]
                    st.success(f"📘 {notebook_count} notebook(s) found for **{selected_student}**")
                    st.info(f"📁 {subfolder_count} subfolder(s) found inside **{selected_student}**")
                    st.subheader(f"📄 Notebooks in `{selected_student}`")
                    for nb in notebooks:
                        st.markdown(f"- **{os.path.basename(nb['path'])}** (Last Modified: `{nb['modifiedTime']}`)")

                    if st.button("🧠 Evaluate Selected Student"):
                        sub_dict = {selected_student: notebooks}
                        report = evaluate_student_notebooks(sub_dict)
                        st.dataframe(report, use_container_width=True)

                        # Optional download
                        csv = report.to_csv(index=False).encode('utf-8')
                        st.download_button("⬇️ Download Report as CSV", csv, f"{selected_student}_report.csv", "text/csv")

        except Exception as e:
            st.error(f"❌ Error occurred: {e}")
else:
    st.info("Paste a Google Drive folder link or ID to begin.")
