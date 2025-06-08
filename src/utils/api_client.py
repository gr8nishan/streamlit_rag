import requests
from typing import List, Dict, Any, Optional
import streamlit as st
from src.utils.config import Config

class DocumentQAClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or Config.API_BASE_URL
        self.session_id = None

    def process_documents(self, files: List[Dict[str, Any]], api_key: str = None) -> Dict[str, Any]:
        """Process documents using the API."""
        try:
            # Use provided API key or fall back to environment variable
            api_key = api_key or Config.GROQ_API_KEY
            
            # Prepare files for multipart/form-data
            files_to_send = []
            for file in files:
                files_to_send.append(
                    ('files', (file['name'], file['content'], 'application/octet-stream'))
                )

            # Add API key to form data
            data = {'api_key': api_key}
            print("base_url", self.base_url)
            # Make API request
            response = requests.post(
                f"{self.base_url}/process",
                files=files_to_send,
                data=data
            )
            response.raise_for_status()
            
            result = response.json()
            self.session_id = result.get('session_id')
            return result

        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}

    def query_documents(self, question: str) -> Dict[str, Any]:
        """Query documents using the API."""
        if not self.session_id:
            return {"error": "No active session. Please process documents first."}

        try:
            response = requests.post(
                f"{self.base_url}/query",
                data={
                    'question': question,
                    'session_id': self.session_id
                }
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"} 