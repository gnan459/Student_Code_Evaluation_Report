import nbformat
import pandas as pd
import google.generativeai as genai
import json
import streamlit as st
import re
import os

# ✅ Gemini model
MODEL_NAME = "gemini-1.5-flash"

# ✅ Load Gemini API key
if "gemini" not in st.secrets or "api_key" not in st.secrets["gemini"]:
    st.error("❌ 'api_key' under [gemini] not found in .streamlit/secrets.toml.")
    st.stop()

api_key = st.secrets["gemini"]["api_key"]
genai.configure(api_key=api_key)

# ✅ Initialize Gemini model
model = genai.GenerativeModel(model_name=MODEL_NAME)

# ✅ Extract notebook content (code + markdown cells)
def extract_notebook_content(nb_path):
    try:
        if not os.path.exists(nb_path):
            return f"Error: Notebook file not found → {nb_path}"
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        content = "\n\n".join([
            cell['source']
            for cell in nb.cells
            if cell['cell_type'] in ['markdown', 'code']
        ])
        return content
    except Exception as e:
        return f"Error reading notebook: {e}"

# ✅ Evaluation rubric
rubric = """
You are a productivity evaluator. Given a student's Jupyter notebook, score it on the following:
1. Completeness (0-10): Are required tasks/code cells implemented?
2. Code Quality (0-10): Is the code clean, modular, and readable?
3. Documentation (0-10): Are markdown explanations present and clear?
4. Insightfulness (0-10): Are outputs meaningful (e.g., graphs, conclusions)?

Respond only in JSON format like:
{
  "Completeness": 8,
  "Code Quality": 7,
  "Documentation": 9,
  "Insightfulness": 8
}
"""

# ✅ Evaluate a single notebook
def get_productivity_scores(content):
    prompt = f"{rubric}\n\nNotebook Content:\n{content}\n"
    try:
        response = model.generate_content(prompt)
        json_match = re.search(r'\{[\s\S]*?\}', response.text)
        if json_match:
            return json.loads(json_match.group())
        return {"Completeness": 0, "Code Quality": 0, "Documentation": 0, "Insightfulness": 0, "error": "No valid JSON found"}
    except Exception as e:
        return {"Completeness": 0, "Code Quality": 0, "Documentation": 0, "Insightfulness": 0, "error": str(e)}

# ✅ Evaluate all student notebooks
def evaluate_student_notebooks(student_data):
    results = []

    for student, data in student_data.items():
        notebooks = data.get("notebooks", [])
        subfolder_count = data.get("subfolder_count", 0)
        num_notebooks = len(notebooks)

        for notebook in notebooks:
            path = notebook.get("path", "")
            modified = notebook.get("modifiedTime", "N/A")

            content = extract_notebook_content(path)
            scores = get_productivity_scores(content)

            total = sum([
                scores.get("Completeness", 0),
                scores.get("Code Quality", 0),
                scores.get("Documentation", 0),
                scores.get("Insightfulness", 0)
            ])
            percent = round((total / 40) * 100, 2)

            results.append({
                "Student ID": student,
                "Notebook": os.path.basename(path),
                "Last Modified": modified,
                "Completeness": scores.get("Completeness", 0),
                "Code Quality": scores.get("Code Quality", 0),
                "Documentation": scores.get("Documentation", 0),
                "Insightfulness": scores.get("Insightfulness", 0),
                "Total Score (%)": percent,
                "Notes": scores.get("error", ""),
                "Notebook Count": num_notebooks,
                "Total Subfolders": subfolder_count
            })

    return pd.DataFrame(results)
