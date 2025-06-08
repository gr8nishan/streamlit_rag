import streamlit as st
from src.utils.file_utils import prepare_files_for_processing
from src.utils.api_client import DocumentQAClient
from src.utils.config import Config

def main():
    st.title("Document Q&A System")
    
    # Initialize API client
    client = DocumentQAClient(base_url="http://api:8888")
    
    # Check if API key is set in environment
    if not Config.GROQ_API_KEY:
        # Groq API Key input
        groq_api_key = st.sidebar.text_input("Groq API Key", type="password")
        if not groq_api_key:
            st.warning("Please enter your Groq API key in the sidebar.")
            return
    else:
        groq_api_key = Config.GROQ_API_KEY
    
    uploaded_files = st.file_uploader(
        "Upload PDF/DOCX files containing these files",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        key="file_uploader"
    )

    if not uploaded_files:
        st.info("Please upload some documents to get started.")
        return

    # Process files only if not already processed
    if "processed_files" not in st.session_state or st.session_state.get("last_uploaded_files") != uploaded_files:
        with st.spinner("Processing documents..."):
            files = prepare_files_for_processing(uploaded_files)
            result = client.process_documents(files, groq_api_key)
            
            if "error" in result:
                st.error(result["error"])
                return
            else:
                st.success(result["message"])
                st.session_state.processed_files = files
                st.session_state.last_uploaded_files = uploaded_files  # store for comparison
                st.session_state.session_id = result.get("session_id", "test_session")  
                files = st.session_state.processed_files
                st.success("Documents already processed. Ready for questions.")

    st.write("Processed files:")    
    # Question input
    question = st.text_input("Ask a question about your documents:")
    
    if question and st.session_state.get("session_id") and st.session_state.processed_files:
        with st.spinner("Generating answer..."):
            result = client.query_documents(question, st.session_state.session_id)
            
            if "error" in result:
                st.error(result["error"])
            else:
                st.write("Answer:", result["answer"])
                
                # Show retrieved context
                if st.checkbox("Show retrieved context"):
                    st.write("Retrieved Context:")
                    for i, context in enumerate(result["context"], 1):
                        st.write(f"Document {i}:")
                        st.write(context["content"])
                        st.write("---")

if __name__ == "__main__":
    main() 