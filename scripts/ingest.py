from app.embeddings import VectorStore
from app.config import EMBEDDING_MODEL

docs = [
    "Government schemes provide financial assistance.",
    "PM Kisan Yojana supports farmers.",
]

store = VectorStore(EMBEDDING_MODEL)
store.add_documents(docs)
