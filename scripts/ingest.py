from src.rag.config import EMBEDDING_MODEL
from src.rag.embeddings import VectorStore

docs = [
    "Government schemes provide financial assistance.",
    "PM Kisan Yojana supports farmers.",
]

store = VectorStore(EMBEDDING_MODEL)
store.add_documents(docs)
