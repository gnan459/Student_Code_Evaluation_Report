
# 📊 Student Productivity Report Generator

This is a Streamlit-based tool that uses **LLMs (via Gemini API)** to automatically evaluate the productivity of students based on their Jupyter Notebook submissions stored in Google Drive. It assesses each student's work on **code completeness, quality, documentation, and insightfulness**.

---

## 🚀 Features

- ✅ Accepts a **Google Drive folder link or ID**
- 📂 Automatically fetches subfolders (each representing a student)
- 📘 Displays all notebooks inside each student folder with **last modified date**
- 📈 Uses **Gemini Pro (via Google Generative AI)** to score each notebook
- 🧠 Evaluation Criteria:
  - Completeness
  - Code Quality
  - Documentation
  - Insightfulness
- 📥 Exports results to a downloadable **CSV report**

---

## 🧰 Tech Stack

- [Streamlit](https://streamlit.io/)
- [Google Drive API](https://developers.google.com/drive)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
- Python (with `nbformat`, `pandas`, etc.)

---

## 🔧 Setup Instructions

### 1. 🔐 Create `.streamlit/secrets.toml`

Create a file at `.streamlit/secrets.toml` and add your credentials:

```toml
[gemini]
api_key = "your_gemini_api_key"

[google]
type = "service_account"
project_id = "your_project_id"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n....\n-----END PRIVATE KEY-----\n"
client_email = "your_service_account@your_project.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
universe_domain = "googleapis.com"
```

Make sure this file is **NOT committed** to Git (already handled in `.gitignore`).

---

### 2. 📦 Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📁 Folder Structure

```
your-project/
├── app.py
├── compare.py
├── drive_utils.py
├── requirements.txt
├── .gitignore
├── .gitattributes
└── .streamlit/
    └── secrets.toml
```

---

## 📷 Screenshots

> _(Optional)_ Add screenshots here to show app input, dropdown, notebook list, and final report.

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE) — feel free to fork and build on top of it!

---

## 🙋‍♂️ Contact

For any queries or suggestions, feel free to reach out via [GitHub Issues](https://github.com/your-username/your-repo/issues).
