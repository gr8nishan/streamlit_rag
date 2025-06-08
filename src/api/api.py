from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from src.core.document_processor import DocumentProcessor
import logging
import traceback

# Initialize logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("api")


app = FastAPI(title="Document Q&A API")

# Store processor instances in memory (in production, use a proper session management)
processors: Dict[str, DocumentProcessor] = {}

@app.post("/process")
async def process_documents(
    files: List[UploadFile] = File(...),
    api_key: str = Form(...)
):
    """Process uploaded documents and create vector store."""
    try:
        # Initialize processor
        processor = DocumentProcessor(api_key)
        
        # Prepare files
        file_contents = []
        for file in files:
            content = await file.read()
            file_contents.append({
                "name": file.filename,
                "content": content
            })
        
        # Process files
        result = processor.process_files(file_contents)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Store processor instance (in production, use proper session management)
        session_id = "test_session"  # In production, generate a unique session ID
        processors[session_id] = processor
        
        return JSONResponse(content={"session_id": session_id, "message": result["message"]})
    
    except Exception as e:
        logger.error("Error processing documents: %s", str(traceback.format_exc()))
        raise HTTPException(status_code=500, detail=str(traceback.format_exc()))

@app.post("/query")
async def query_documents(
    question: str = Form(...),
    session_id: str = Form(...)
):
    """Query processed documents."""
    try:
        processor = processors.get(session_id)
        if not processor:
            raise HTTPException(status_code=404, detail="Session not found")
        
        result = processor.query_documents(question)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Note: In a production environment, you would also need:
# 1. Proper session management
# 2. Authentication and authorization
# 3. Rate limiting
# 4. Error handling middleware
# 5. Logging
# 6. Configuration management
# 7. Health check endpoints 