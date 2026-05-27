import streamlit as st
import sys
import os
from datetime import datetime
from typing import List, Optional
import time

# Import the RAG system from src.api.main
from src.api.main import RAGSystem, QueryRequest, QueryResponse, Source

# Page Config
st.set_page_config(
    page_title="Multilingual RAG Assistant",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main {
            padding: 0rem 1rem;
        }
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 1.1em;
            padding: 0.5em 1em;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize RAG System (cached to avoid reinitializing)
@st.cache_resource
def get_rag_system():
    return RAGSystem()

rag_system = get_rag_system()

# Header
st.markdown("""
# 🌐 Multilingual LLM RAG Assistant

**Bilingual RAG assistant with Streamlit and source-backed responses**

Deploy your queries in multiple languages and get intelligent responses with source citations!
""")

st.divider()

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    language = st.selectbox(
        "Select Language",
        ["English", "Hindi"],
        help="Language for your query"
    )
    
    model_select = st.selectbox(
        "LLM Model",
        ["groq-mixtral", "groq-llama2"],
        help="Select the LLM model to use"
    )
    
    temperature = st.slider(
        "Temperature (Creativity)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher = more creative, Lower = more focused"
    )
    
    max_tokens = st.slider(
        "Max Tokens (Response Length)",
        min_value=100,
        max_value=2000,
        value=1000,
        step=100
    )
    
    st.divider()
    st.markdown("""
    ### 📚 About This Project
    
    - **RAG Framework**: FAISS vector search
    - **Multilingual**: English & Hindi support
    - **Tool Calling**: Function invocation support
    - **Streamlit**: Integrated backend & frontend
    - **Deployed on**: Hugging Face Spaces ✨
    
    ### 🎯 Status
    - Backend: ✅ Running (integrated)
    - Status: ✅ Ready
    """)

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Query Interface")
    user_query = st.text_area(
        "Enter your question:",
        placeholder="Ask me anything in English or Hindi...",
        height=150
    )

with col2:
    st.subheader("📊 Settings Summary")
    st.info(f"""
    **Language**: {language}
    **Model**: {model_select}
    **Temperature**: {temperature}
    **Max Tokens**: {max_tokens}
    """)

st.divider()

# Query Execution
if st.button("🚀 Send Query", use_container_width=True, type="primary"):
    if not user_query.strip():
        st.error("❌ Please enter a query!")
    else:
        try:
            with st.spinner("⏳ Processing your query..."):
                start_time = time.time()
                
                # Validate query
                if not user_query or len(user_query.strip()) == 0:
                    st.error("❌ Query cannot be empty")
                elif len(user_query) > 5000:
                    st.error("❌ Query too long (max 5000 characters)")
                else:
                    # Process query using RAG system
                    sources = rag_system.retrieve(user_query, top_k=3)
                    response_text = rag_system.generate_response(
                        user_query,
                        sources,
                        model=model_select,
                        temperature=temperature,
                    )
                    
                    processing_time = time.time() - start_time
                    tokens_used = len(user_query.split()) + len(response_text.split())
                    detected_language = "Hindi" if any(ord(c) > 127 for c in user_query) else "English"
                    
                    # Display Results
                    st.success("✅ Query processed successfully!")
                    
                    # Response
                    st.subheader("💬 Response")
                    st.markdown(response_text)
                    
                    # Sources
                    if sources:
                        st.subheader("📖 Retrieved Sources")
                        for idx, source in enumerate(sources, 1):
                            with st.expander(f"Source {idx}: {source.title}"):
                                st.text(source.content)
                                st.caption(f"Relevance Score: {source.score:.2f}")
                    
                    # Metadata
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Processing Time", f"{processing_time:.2f}s")
                    with col2:
                        st.metric("Tokens Used", tokens_used)
                    with col3:
                        st.metric("Detected Language", detected_language)
                    
                    # Save to history
                    if 'query_history' not in st.session_state:
                        st.session_state.query_history = []
                    
                    st.session_state.query_history.append({
                        'timestamp': datetime.now().isoformat(),
                        'query': user_query,
                        'response': response_text,
                        'language': language
                    })
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Please try again or contact support")

st.divider()

# Query History
if 'query_history' in st.session_state and st.session_state.query_history:
    with st.expander("📜 Query History"):
        for idx, item in enumerate(reversed(st.session_state.query_history[-10:]), 1):
            st.markdown(f"""
            **Query {idx}** ({item['timestamp'][:19]})
            
            *Language: {item['language']}*
            
            **Q:** {item['query']}
            
            **A:** {item['response'][:200]}...
            """)
            st.divider()

# Footer
st.markdown("""
---
**Built with ❤️ using Streamlit, FastAPI, FAISS, and LLMs**

[GitHub Repository](https://github.com/Abhi123aan/multilingual-llm-rag-assistant) | 
[Documentation](https://github.com/Abhi123aan/multilingual-llm-rag-assistant#readme) |
[Report Issues](https://github.com/Abhi123aan/multilingual-llm-rag-assistant/issues)
""")
