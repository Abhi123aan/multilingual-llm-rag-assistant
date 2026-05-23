# 🌐 Multilingual LLM RAG Assistant

[![Hugging Face Space](https://img.shields.io/badge/🤗-Open%20in%20Spaces-blue.svg)](https://huggingface.co/spaces/Abhi123aan/multilingual-llm-rag-assistant)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black.svg)](https://github.com/Abhi123aan/multilingual-llm-rag-assistant)

**Production-ready multilingual AI assistant using RAG, FAISS, and FastAPI with tool-calling support.**

## ✨ Features

- 🌍 **Multilingual Support**: English & Hindi query handling
- 🔍 **Retrieval-Augmented Generation**: FAISS-based dense vector search
- 🔧 **Tool Calling**: Prompt-based function invocation
- ⚡ **FastAPI Backend**: Production-grade REST API
- 💻 **Streamlit Frontend**: Interactive web interface
- 🚀 **Docker Ready**: Complete containerization for easy deployment
- 📊 **Query History**: Track and review previous interactions
- 🎯 **Hugging Face Spaces**: One-click deployment

## 🚀 Quick Start

### **Option 1: Hugging Face Spaces (Easiest)**

Visit the deployed version: 
**👉 [https://huggingface.co/spaces/Abhi123aan/multilingual-llm-rag-assistant](https://huggingface.co/spaces/Abhi123aan/multilingual-llm-rag-assistant)**

No setup required! Just ask your questions in English or Hindi.

### **Option 2: Run Locally with Docker**

```bash
# Clone the repository
git clone https://github.com/Abhi123aan/multilingual-llm-rag-assistant.git
cd multilingual-llm-rag-assistant

# Create .env file
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Run with Docker Compose
docker-compose -f docker-compose.yml up --build
```

Access the application:
- **Frontend (Streamlit)**: http://localhost:7860
- **API Docs (FastAPI)**: http://localhost:8000/docs

### **Option 3: Run Locally with Python**

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Terminal 1: Start FastAPI backend
python main.py

# Terminal 2: Start Streamlit frontend
streamlit run app.py --server.port=7860
```

## 📋 Project Structure

```
multilingual-llm-rag-assistant/
├── app.py                      # Streamlit web interface
├── main.py                     # FastAPI backend
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # Multi-container setup
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                   # This file
```

## 🔌 API Endpoints

### Health Check
```bash
GET /health
```

### Process Query
```bash
POST /query
Content-Type: application/json

{
  "query": "What is machine learning?",
  "language": "english",
  "model": "groq-mixtral",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

**Response:**
```json
{
  "response": "Machine learning is a subset of AI...",
  "sources": [
    {
      "title": "ML Basics",
      "content": "ML enables systems to learn...",
      "score": 0.95
    }
  ],
  "processing_time": 2.34,
  "tokens_used": 156,
  "detected_language": "English",
  "model_used": "groq-mixtral"
}
```

### Get Query History
```bash
GET /history?limit=10
```

### List Available Models
```bash
GET /models
```

### List Supported Languages
```bash
GET /languages
```

## 🌐 Supported Languages

- 🇬🇧 **English** (en)
- 🇮🇳 **Hindi** (hi)

*More languages can be added easily!*

## 🧠 Models Available

- **groq-mixtral** - Fast and accurate, great for diverse queries
- **groq-llama2** - Excellent for context understanding

## 📦 Dependencies

- **fastapi** (0.104.1) - REST API framework
- **streamlit** (1.28.1) - Web UI framework
- **sentence-transformers** (2.2.2) - Embedding models
- **faiss-cpu** (1.7.4) - Vector similarity search
- **transformers** (4.35.2) - Model loading
- **torch** (2.0.0) - Deep learning framework
- **pydantic** (2.5.0) - Data validation
- **groq** (0.4.2) - Groq API client

See `requirements.txt` for complete list.

## 🔑 Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key_here
DEFAULT_MODEL=groq-mixtral
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=1000
LOG_LEVEL=INFO
```

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t multilingual-rag-assistant .
```

### Run Container
```bash
docker run -p 7860:7860 \
  -e GROQ_API_KEY=your_key \
  multilingual-rag-assistant
```

### Docker Compose
```bash
docker-compose up --build
```

## 📝 Usage Examples

### Example 1: English Query
```
Query: "What are the benefits of machine learning?"
Language: English
Model: groq-mixtral
```

### Example 2: Hindi Query
```
Query: "मशीन लर्निंग के क्या लाभ हैं?"
Language: Hindi
Model: groq-mixtral
```

## 🚀 Deployment to Hugging Face Spaces

1. **Create a new Space**:
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Select **Docker** as SDK
   - Name it `multilingual-llm-rag-assistant`

2. **Add Secrets** (in Space Settings):
   - `GROQ_API_KEY`: Your Groq API key

3. **Push Code**:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/multilingual-llm-rag-assistant
   cd multilingual-llm-rag-assistant
   git remote add github https://github.com/Abhi123aan/multilingual-llm-rag-assistant.git
   git pull github main
   git push
   ```

4. **Space URL**:
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/multilingual-llm-rag-assistant
   ```

## 📊 Performance

- **Response Time**: ~2-5 seconds
- **Vector Search**: <100ms with FAISS
- **Memory**: ~2GB RAM for CPU inference
- **Concurrent Users**: Supports multiple simultaneous queries

## 🔒 Security

- CORS enabled for web requests
- Input validation on all endpoints
- Environment variables for sensitive data
- Rate limiting ready for production

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 7860
lsof -ti:7860 | xargs kill -9
```

### Connection Error
- Ensure backend is running on `http://localhost:8000`
- Check `.env` file has `GROQ_API_KEY`
- Verify firewall isn't blocking ports

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

## 📚 Documentation

- **FastAPI Docs**: http://localhost:8000/docs
- **GitHub**: https://github.com/Abhi123aan/multilingual-llm-rag-assistant
- **Hugging Face**: https://huggingface.co/spaces/Abhi123aan/multilingual-llm-rag-assistant

## 📄 License

MIT License - Feel free to use this project!

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 💬 Support

For issues, questions, or suggestions:
- Open a GitHub Issue
- Check existing discussions
- Contact: [Your Email]

---

**Built with ❤️ using FastAPI, Streamlit, FAISS, and LLMs**

**Live Demo**: 🎯 [https://huggingface.co/spaces/Abhi123aan/multilingual-llm-rag-assistant](https://huggingface.co/spaces/Abhi123aan/multilingual-llm-rag-assistant)
