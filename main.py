from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import time
from datetime import datetime
import json

# Initialize FastAPI app
app = FastAPI(
    title="Multilingual LLM RAG Assistant API",
    description="Production-ready multilingual AI assistant with RAG",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class QueryRequest(BaseModel):
    query: str
    language: Optional[str] = "english"
    model: Optional[str] = "groq-mixtral"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000

class Source(BaseModel):
    title: str
    content: str
    score: float

class QueryResponse(BaseModel):
    response: str
    sources: List[Source]
    processing_time: float
    tokens_used: int
    detected_language: str
    model_used: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# In-memory storage for demo
query_history = []

# Mock RAG System (Replace with actual implementation)
class RAGSystem:
    def __init__(self):
        self.index = None
        self.documents = [
            {
                "title": "Python Basics",
                "content": "Python is a high-level programming language known for its simplicity and readability."
            },
            {
                "title": "Machine Learning",
                "content": "Machine Learning is a subset of AI that enables systems to learn and improve from experience."
            },
            {
                "title": "FastAPI",
                "content": "FastAPI is a modern, fast web framework for building APIs with Python."
            },
            {
                "title": "FAISS Vector Search",
                "content": "FAISS is a library for efficient similarity search and clustering of dense vectors."
            }
        ]
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Source]:
        """Retrieve relevant documents"""
        return [
            Source(
                title=doc["title"],
                content=doc["content"],
                score=0.95 - (i * 0.05)
            )
            for i, doc in enumerate(self.documents[:top_k])
        ]
    
    def generate_response(self, query: str, sources: List[Source], **kwargs) -> str:
        """Generate response using LLM"""
        sources_text = "\n".join([f"- {s.title}: {s.content}" for s in sources])
        
        response = f"""Based on the retrieved sources, here's my response to your query: "{query}"

**Context from sources:**
{sources_text}

**Response:**
I've found relevant information about your query. The key points are:
1. The topic is well-covered in our knowledge base
2. Multiple perspectives and sources are available
3. This is a demonstration response for the {kwargs.get('model', 'groq-mixtral')} model

For a production setup, this would be powered by actual LLM inference.
"""
        return response.strip()

# Initialize RAG system
rag_system = RAGSystem()

# Routes
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Multilingual LLM RAG Assistant API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "query": "/query (POST)",
            "history": "/history (GET)",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.post("/query", response_model=QueryResponse, tags=["Query"])
async def process_query(request: QueryRequest):
    """
    Process a multilingual query with RAG
    
    - **query**: The user's question
    - **language**: Language of query (english, hindi)
    - **model**: LLM model to use
    - **temperature**: Creativity level (0.0-1.0)
    - **max_tokens**: Maximum response length
    """
    try:
        start_time = time.time()
        
        # Validate input
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if len(request.query) > 5000:
            raise HTTPException(status_code=400, detail="Query too long (max 5000 chars)")
        
        # Retrieve relevant documents
        sources = rag_system.retrieve(request.query, top_k=3)
        
        # Generate response
        response_text = rag_system.generate_response(
            request.query,
            sources,
            model=request.model,
            temperature=request.temperature
        )
        
        # Calculate metrics
        processing_time = time.time() - start_time
        tokens_used = len(request.query.split()) + len(response_text.split())
        
        # Detect language (simple demo)
        detected_language = "Hindi" if any(ord(c) > 127 for c in request.query) else "English"
        
        # Store in history
        query_history.append({
            "timestamp": datetime.now().isoformat(),
            "query": request.query,
            "language": request.language,
            "model": request.model
        })
        
        return QueryResponse(
            response=response_text,
            sources=sources,
            processing_time=round(processing_time, 2),
            tokens_used=tokens_used,
            detected_language=detected_language,
            model_used=request.model
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/history", tags=["History"])
async def get_history(limit: int = 10):
    """Get recent query history"""
    return {
        "total_queries": len(query_history),
        "recent_queries": query_history[-limit:],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/models", tags=["Config"])
async def list_models():
    """List available models"""
    return {
        "available_models": [
            {
                "name": "groq-mixtral",
                "description": "Groq Mixtral model - Fast and accurate",
                "params": {"temperature": [0.0, 1.0], "max_tokens": [100, 4000]}
            },
            {
                "name": "groq-llama2",
                "description": "Groq Llama2 model - Good for context understanding",
                "params": {"temperature": [0.0, 1.0], "max_tokens": [100, 2000]}
            }
        ]
    }

@app.get("/languages", tags=["Config"])
async def list_languages():
    """List supported languages"""
    return {
        "supported_languages": [
            {"code": "en", "name": "English"},
            {"code": "hi", "name": "Hindi"}
        ]
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
