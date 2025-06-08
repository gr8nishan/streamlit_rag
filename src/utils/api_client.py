import requests
from typing import List, Dict, Any, Optional
import streamlit as st
from src.utils.config import Config
from src.core.document_processor import DocumentProcessor

processors: Dict[str, DocumentProcessor] = {}

class DocumentQAClient:
    def __init__(self, base_url: str = None, from_api: bool = False):
        self.base_url = base_url or Config.API_BASE_URL
        self.session_id = None
        self.from_api = from_api
        if not self.from_api:
            # Initialize DocumentProcessor if not using API
            self.processor = DocumentProcessor(Config.GROQ_API_KEY, Config.LLM_MODEL_NAME)
            self.session_id = "test"
            
            # session_id = "test_session"  # In production, generate a unique session ID
            # self.processors[session_id] = processor
    
    def process_documents(self, files: List[Dict[str, Any]], api_key: str = None) -> Dict[str, Any]:
        """Process documents using the API."""
        try:
            
            # Use provided API key or fall back to environment variable
            api_key = api_key or Config.GROQ_API_KEY
            print("grok api_key", api_key)
            # Prepare files for multipart/form-data
            files_to_send = []
            file_contents = []
            for file in files:
                files_to_send.append(
                    ('files', (file['name'], file['content'], 'application/octet-stream'))
                )
                file_contents.append({
                        "name": file['name'],
                        "content": file['content']
                    })

            # Add API key to form data
            data = {'api_key': api_key}

            # Make API request
            if self.from_api:
                response = requests.post(
                    f"{self.base_url}/process",
                    files=files_to_send,
                    data=data
                )
                response.raise_for_status()
                
                result = response.json()
                self.session_id = result.get('session_id')
            else:
                print("Processing files locally using DocumentProcessor")
                result = self.processor.process_files(file_contents)
                processors[self.session_id] = self.processor
                print("result", result)
                return {"session_id": self.session_id, "message": result["message"]}


        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}

    def query_documents(self, question: str, session_id) -> Dict[str, Any]:
        """Query documents using the API."""
        if not self.session_id:
            return {"error": "No active session. Please process documents first."}

        try:
            if self.from_api:
                # Make API request to query documents
                response = requests.post(
                    f"{self.base_url}/query",
                    data={
                        'question': question,
                        'session_id': self.session_id
                    }
                )
                response.raise_for_status()
                return response.json()
            else:
                processor = processors[session_id]
                return processor.query_documents(question)

        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"} 