from typing import List, Dict, Any
import streamlit as st

def validate_file_type(filename: str) -> bool:
    """Validate if the file type is supported."""
    return filename.endswith(('.pdf', '.docx', '.zip'))

def prepare_files_for_processing(uploaded_files: Any) -> List[Dict[str, Any]]:
    """Convert Streamlit uploaded files to a format suitable for processing."""
    files = []
    
    for uploaded_file in uploaded_files:
        if not validate_file_type(uploaded_file.name):
            continue
            
        files.append({
            "name": uploaded_file.name,
            "content": uploaded_file.getvalue()
        })
    
    return files 