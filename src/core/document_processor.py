import os
import io
import zipfile
import tempfile
from typing import List, Union, Dict, Any
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from src.utils.config import Config

class DocumentProcessor:
    def __init__(self, groq_api_key: str = None, model_name: str = None):
        self.groq_api_key = groq_api_key or Config.GROQ_API_KEY
        self.model_name = model_name or Config.LLM_MODEL_NAME
        self.vectorstore = None
        self.qa_chain = None
        self.llm = ChatGroq(
            model_name=self.model_name,
            temperature=0.1,
            groq_api_key=self.groq_api_key
        )

    def process_files(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process uploaded files and create vector store."""
        try:
            extracted_files = self._extract_files(files)
            if not extracted_files:
                return {"error": "No valid files found."}

            documents = self._load_documents(extracted_files)
            self.vectorstore = self._create_vectorstore(documents)
            self.qa_chain = self._initialize_qa_chain()
            
            return {"status": "success", "message": "Documents processed successfully"}
        except Exception as e:
            return {"error": f"Error processing documents: {str(e)}"}

    def query_documents(self, question: str) -> Dict[str, Any]:
        """Query the documents with a question."""
        if not self.qa_chain:
            return {"error": "Documents not processed yet."}
        
        try:
            answer = self.qa_chain.run(question)
            context = self._get_context(question)
            return {
                "answer": answer,
                "context": context
            }
        except Exception as e:
            return {"error": f"Error generating answer: {str(e)}"}

    def _extract_files(self, files: List[Dict[str, Any]]) -> List[bytes]:
        """Extract files from uploaded files or ZIP."""
        extracted_files = []
        
        for file in files:
            if file["name"].endswith('.zip'):
                with zipfile.ZipFile(io.BytesIO(file["content"])) as zip_ref:
                    for file_name in zip_ref.namelist():
                        if not (file_name.endswith('.pdf') or file_name.endswith('.docx')):
                            continue
                        extracted_files.append(zip_ref.read(file_name))
            elif file["name"].endswith(('.pdf', '.docx')):
                extracted_files.append(file["content"])
        
        return extracted_files

    def _load_documents(self, files: List[bytes]) -> List:
        """Load documents using LangChain's UnstructuredFileLoader."""
        documents = []
        
        for file_content in files:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file_content)
                temp_file.flush()
                
                loader = UnstructuredFileLoader(temp_file.name)
                documents.extend(loader.load())
                
                os.unlink(temp_file.name)
        
        return documents

    def _create_vectorstore(self, docs: List) -> Qdrant:
        """Create and return a Qdrant vector store with embedded documents."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        texts = text_splitter.split_documents(docs)
        embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL_NAME)
        
        return Qdrant.from_documents(
            documents=texts,
            embedding=embeddings,
            location=":memory:",
            collection_name="documents"
        )

    def _initialize_qa_chain(self) -> RetrievalQA:
        """Initialize and return a RetrievalQA chain."""
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3})
        )

    def _get_context(self, question: str) -> List[Dict[str, str]]:
        """Get relevant context for a question."""
        docs = self.vectorstore.similarity_search(question, k=3)
        return [{"content": doc.page_content} for doc in docs] 