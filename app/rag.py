from transformers import pipeline
from langdetect import detect
from app.prompts import build_prompt
from app.tools import search_documents

class RAGPipeline:
    def __init__(self, vector_store, model_name):
        self.vector_store = vector_store
        self.generator = pipeline("text2text-generation", model=model_name)

    def run(self, query):
        language = detect(query)
        docs = search_documents(query, self.vector_store)
        context = "\n".join(docs)
        prompt = build_prompt(context, query, language)
        response = self.generator(prompt, max_length=256)
        return response[0]["generated_text"]
