from fastapi import FastAPI
from pydantic import BaseModel
from app.embeddings import VectorStore
from app.rag import RAGPipeline
from app.config import EMBEDDING_MODEL, GENERATION_MODEL

app = FastAPI()

vector_store = VectorStore(EMBEDDING_MODEL)
rag = RAGPipeline(vector_store, GENERATION_MODEL)

class Query(BaseModel):
    question: str

@app.post("/query")
def query_llm(q: Query):
    answer = rag.run(q.question)
    return {"answer": answer}
