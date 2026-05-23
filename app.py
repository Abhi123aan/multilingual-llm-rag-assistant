import streamlit as st
import requests
import json
from datetime import datetime

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

# Header
st.markdown("""
# 🌐 Multilingual LLM RAG Assistant

**Production-ready multilingual AI assistant with RAG, FAISS, and FastAPI**

Deploy your queries in multiple languages and get intelligent responses with source citations!
""")

st.divider()

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_base = st.text_input(
        "API Base URL",
        value="http://localhost:8000",
        help="Change if deployed on different server"
    )
    
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
    - **FastAPI**: Production-grade API
    - **Deployed on**: Hugging Face Spaces ✨
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
                # Prepare request
                payload = {
                    "query": user_query,
                    "language": language.lower(),
                    "model": model_select,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                
                # Call API
                response = requests.post(
                    f"{api_base}/query",
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display Results
                    st.success("✅ Query processed successfully!")
                    
                    # Response
                    st.subheader("💬 Response")
                    st.markdown(f"""
                    {result.get('response', 'No response generated')}
                    """)
                    
                    # Sources
                    if result.get('sources'):
                        st.subheader("📖 Retrieved Sources")
                        for idx, source in enumerate(result['sources'], 1):
                            with st.expander(f"Source {idx}: {source.get('title', 'Document')}"):
                                st.text(source.get('content', 'No content'))
                                st.caption(f"Relevance Score: {source.get('score', 'N/A')}")
                    
                    # Metadata
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Processing Time", f"{result.get('processing_time', 'N/A')}s")
                    with col2:
                        st.metric("Tokens Used", result.get('tokens_used', 'N/A'))
                    with col3:
                        st.metric("Detected Language", result.get('detected_language', language))
                    
                    # Save to history
                    if 'query_history' not in st.session_state:
                        st.session_state.query_history = []
                    
                    st.session_state.query_history.append({
                        'timestamp': datetime.now().isoformat(),
                        'query': user_query,
                        'response': result.get('response', ''),
                        'language': language
                    })
                else:
                    st.error(f"❌ API Error: {response.status_code}")
                    st.write(response.text)
        
        except requests.exceptions.ConnectionError:
            st.error("""
            ❌ **Connection Error**
            
            Could not connect to the API backend. Make sure:
            1. Backend is running on `{api_base}`
            2. FastAPI server is accessible
            3. Check your API Base URL in the sidebar
            """)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

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
[Documentation](https://github.com/Abhi123aan/multilingual-llm-rag-assistant#readme)
""")
