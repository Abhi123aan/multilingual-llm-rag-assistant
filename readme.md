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


## 🚀 How to Run with Docker

The easiest way to run the Multilingual RAG Assistant is using **Docker Compose**. This will automatically set up the FastAPI backend and the Streamlit frontend in an isolated environment.

### 1. Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.
* A `.env` file in the root directory with your `GROQ_API_KEY`.

### 2. Launch the Application
Run the following command in your terminal:
```bash
docker-compose up --build
