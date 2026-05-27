def build_prompt(context, query, language):
    return f"""
You are an AI assistant. Answer in {language}.

Context:
{context}

Question:
{query}

Answer:
"""
