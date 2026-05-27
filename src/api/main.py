from datetime import datetime
from typing import List, Optional
import time

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict


app = FastAPI(
    title="Multilingual LLM RAG Assistant API",
    description="Bilingual retrieval-augmented assistant API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    model_config = ConfigDict(protected_namespaces=())

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


query_history = []
metrics = {
    "queries_total": 0,
    "query_errors_total": 0,
    "query_latency_seconds_total": 0.0,
}


class RAGSystem:
    def __init__(self):
        self.documents = [
            {
                "title": "Python Basics",
                "content": "Python is a high-level programming language known for its simplicity and readability.",
            },
            {
                "title": "Machine Learning",
                "content": "Machine Learning is a subset of AI that enables systems to learn and improve from experience.",
            },
            {
                "title": "FastAPI",
                "content": "FastAPI is a modern, fast web framework for building APIs with Python.",
            },
            {
                "title": "FAISS Vector Search",
                "content": "FAISS is a library for efficient similarity search and clustering of dense vectors.",
            },
        ]

    def retrieve(self, query: str, top_k: int = 3) -> List[Source]:
        return [
            Source(
                title=doc["title"],
                content=doc["content"],
                score=0.95 - (i * 0.05),
            )
            for i, doc in enumerate(self.documents[:top_k])
        ]

    def generate_response(self, query: str, sources: List[Source], **kwargs) -> str:
        sources_text = "\n".join([f"- {s.title}: {s.content}" for s in sources])
        response = f"""Based on the retrieved sources, here's my response to your query: "{query}"

**Context from sources:**
{sources_text}

**Response:**
I've found relevant information about your query. The key points are:
1. The topic is covered in the current knowledge base
2. Multiple source snippets are available
3. This is a demonstration response for the {kwargs.get('model', 'groq-mixtral')} model

For a production setup, this would be powered by actual LLM inference.
"""
        return response.strip()


rag_system = RAGSystem()


@app.get("/", tags=["Health"])
async def root():
    return {
        "name": "Multilingual LLM RAG Assistant API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "query": "/v1/query (POST)",
            "legacy_query": "/query (POST)",
            "history": "/history (GET)",
            "metrics": "/metrics",
            "docs": "/docs",
        },
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
    )


async def _process_query(request: QueryRequest):
    try:
        start_time = time.time()

        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        if len(request.query) > 5000:
            raise HTTPException(status_code=400, detail="Query too long (max 5000 chars)")

        sources = rag_system.retrieve(request.query, top_k=3)
        response_text = rag_system.generate_response(
            request.query,
            sources,
            model=request.model,
            temperature=request.temperature,
        )
        processing_time = time.time() - start_time
        tokens_used = len(request.query.split()) + len(response_text.split())
        detected_language = "Hindi" if any(ord(c) > 127 for c in request.query) else "English"

        query_history.append({
            "timestamp": datetime.now().isoformat(),
            "query": request.query,
            "language": request.language,
            "model": request.model,
        })
        metrics["queries_total"] += 1
        metrics["query_latency_seconds_total"] += processing_time

        return QueryResponse(
            response=response_text,
            sources=sources,
            processing_time=round(processing_time, 2),
            tokens_used=tokens_used,
            detected_language=detected_language,
            model_used=request.model,
        )

    except HTTPException:
        metrics["query_errors_total"] += 1
        raise
    except Exception as exc:
        metrics["query_errors_total"] += 1
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(exc)}")


@app.post("/query", response_model=QueryResponse, tags=["Query"])
async def process_query(request: QueryRequest):
    """Legacy query endpoint. Prefer /v1/query for new clients."""
    return await _process_query(request)


@app.post("/v1/query", response_model=QueryResponse, tags=["Query"])
async def process_query_v1(request: QueryRequest):
    return await _process_query(request)


@app.get("/history", tags=["History"])
async def get_history(limit: int = 10):
    return {
        "total_queries": len(query_history),
        "recent_queries": query_history[-limit:],
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/models", tags=["Config"])
async def list_models():
    return {
        "available_models": [
            {
                "name": "groq-mixtral",
                "description": "Groq Mixtral model - Fast and accurate",
                "params": {"temperature": [0.0, 1.0], "max_tokens": [100, 4000]},
            },
            {
                "name": "groq-llama2",
                "description": "Groq Llama2 model - Good for context understanding",
                "params": {"temperature": [0.0, 1.0], "max_tokens": [100, 2000]},
            },
        ]
    }


@app.get("/languages", tags=["Config"])
async def list_languages():
    return {
        "supported_languages": [
            {"code": "en", "name": "English"},
            {"code": "hi", "name": "Hindi"},
        ]
    }


@app.get("/metrics", tags=["Observability"])
async def prometheus_metrics():
    average_latency = (
        metrics["query_latency_seconds_total"] / metrics["queries_total"]
        if metrics["queries_total"]
        else 0.0
    )
    body = "\n".join([
        "# HELP rag_queries_total Total successful RAG queries.",
        "# TYPE rag_queries_total counter",
        f"rag_queries_total {metrics['queries_total']}",
        "# HELP rag_query_errors_total Total failed RAG queries.",
        "# TYPE rag_query_errors_total counter",
        f"rag_query_errors_total {metrics['query_errors_total']}",
        "# HELP rag_query_latency_seconds_avg Average query latency in seconds.",
        "# TYPE rag_query_latency_seconds_avg gauge",
        f"rag_query_latency_seconds_avg {average_latency:.6f}",
        "",
    ])
    return Response(content=body, media_type="text/plain; version=0.0.4")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat(),
        },
    )
