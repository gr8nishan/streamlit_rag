import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "mixtral-8x7b-32768")
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
    
    # API Server Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8888"))
    API_BASE_URL: str = f"http://{API_HOST}:{API_PORT}"
    print("ragapi", API_BASE_URL)
    @classmethod
    def validate(cls) -> Optional[str]:
        """Validate required configuration."""
        if not cls.GROQ_API_KEY:
            return "GROQ_API_KEY is not set in environment variables"
        return None 