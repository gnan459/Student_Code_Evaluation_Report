import os
import io
import re
import json
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# ✅ Authenticate using credentials from .streamlit/secrets.toml
def get_drive_service():
    credentials_info = {
        "type": st.secrets["google"]["type"],
        "project_id": st.secrets["google"]["project_id"],
        "private_key_id": st.secrets["google"]["private_key_id"],
        "private_key": st.secrets["google"]["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["google"]["client_email"],
        "client_id": st.secrets["google"]["client_id"],
        "auth_uri": st.secrets["google"]["auth_uri"],
        "token_uri": st.secrets["google"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["google"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["google"]["client_x509_cert_url"],
        "universe_domain": st.secrets["google"]["universe_domain"],
    }
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    return build("drive", "v3", credentials=credentials)

# ✅ Replace unsafe characters in filenames
def sanitize_filename(name):
    return re.sub(r'[\\\\/*?:"<>|]', '_', name)

# ✅ List student subfolders
def list_subfolders(service, parent_folder_id):
    query = f"'{parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get("files", [])

# ✅ List .ipynb files in a folder
def list_ipynb_files(service, folder_id):
    query = f"'{folder_id}' in parents and name contains '.ipynb'"
    results = service.files().list(q=query, fields="files(id, name, modifiedTime)").execute()
    return results.get("files", [])

# ✅ Count subfolders inside a given folder
def count_subfolders(service, folder_id):
    query = f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id)").execute()
    return len(results.get("files", []))

# ✅ Download file from Google Drive
def download_file(service, file_id, destination):
    try:
        request = service.files().get_media(fileId=file_id)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with open(destination, "wb") as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
    except Exception as e:
        print(f"❌ Failed to download file ID {file_id} → {destination}: {e}")

# ✅ Main function to fetch student notebook data
def fetch_notebooks_from_drive(root_folder_id, temp_dir):
    service = get_drive_service()
    student_data = {}

    subfolders = list_subfolders(service, root_folder_id)
    for sub in subfolders:
        sub_id = sub['id']
        student_name = sanitize_filename(sub['name'])

        files = list_ipynb_files(service, sub_id)
        subfolder_count = count_subfolders(service, sub_id)

        if not files:
            print(f"ℹ️ No .ipynb files found for {student_name}, skipping.")
            continue

        notebook_entries = []
        for file in files:
            filename = sanitize_filename(file['name'])
            local_path = os.path.join(temp_dir, f"{student_name}_{filename}")

            download_file(service, file["id"], local_path)
            notebook_entries.append({
                "path": local_path,
                "modifiedTime": file.get("modifiedTime", "N/A")
            })

        student_data[student_name] = {
            "notebooks": notebook_entries,
            "subfolder_count": subfolder_count
        }

    return student_data
