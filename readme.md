# Multilingual LLM Assistant with Tool-Calling

This project implements a production-style multilingual AI assistant using
Retrieval-Augmented Generation (RAG), FAISS vector search, and FastAPI.

## Features
- Multilingual query support (English + Hindi)
- FAISS-based dense retrieval
- Prompt-based tool calling
- FastAPI backend for deployment
- CPU-efficient inference

## Run Locally

```bash
pip install -r requirements.txt
python scripts/ingest.py
uvicorn app.main:app --reload
