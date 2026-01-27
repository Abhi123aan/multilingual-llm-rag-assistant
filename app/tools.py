def search_documents(query, retriever):
    return retriever.search(query, k=5)

def summarize_text(text):
    return text[:500]  # placeholder logic
