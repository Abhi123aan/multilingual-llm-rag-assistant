import faiss
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.IndexFlatL2(384)
        self.documents = []

    def add_documents(self, texts):
        embeddings = self.model.encode(texts, show_progress_bar=True)
        self.index.add(embeddings)
        self.documents.extend(texts)

    def search(self, query, k):
        q_emb = self.model.encode([query])
        distances, indices = self.index.search(q_emb, k)
        return [self.documents[i] for i in indices[0]]
