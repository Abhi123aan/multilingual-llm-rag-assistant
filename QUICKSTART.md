# ⚡ Quick Start Guide

## 🎯 TL;DR - Get Running in 5 Minutes

### Option 1: Hugging Face Spaces (Easiest - 0 Setup)
```
👉 Go to: https://huggingface.co/spaces/Abhi123aan/multilingual-llm-rag-assistant
✨ No installation needed, just use it!
```

### Option 2: Docker (2 minutes setup)
```bash
# 1. Get the repo
git clone https://github.com/Abhi123aan/multilingual-llm-rag-assistant.git
cd multilingual-llm-rag-assistant

# 2. Create .env file
echo "GROQ_API_KEY=your_api_key_here" > .env

# 3. Start it
docker-compose up --build

# 4. Open browser
# Frontend: http://localhost:7860
# API: http://localhost:8000/docs
```

### Option 3: Python (3 minutes setup)
```bash
# 1. Clone
git clone https://github.com/Abhi123aan/multilingual-llm-rag-assistant.git
cd multilingual-llm-rag-assistant

# 2. Setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure
echo "GROQ_API_KEY=your_api_key_here" > .env

# 4. Run (2 terminals)
# Terminal 1:
python main.py

# Terminal 2:
streamlit run app.py --server.port 7860

# 5. Open http://localhost:7860
```

---

## 🔑 Get Your GROQ API Key (1 minute)

1. Visit https://groq.com
2. Sign up (free)
3. Go to API Keys section
4. Create new key
5. Copy it to `.env` file

---

## 📝 Simple Usage

### Web Interface (Easiest)
1. Open http://localhost:7860
2. Type your question
3. Click "Send Query"
4. Get instant response!

### API Usage (Developers)
```bash
# Query the API
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is AI?",
    "language": "english",
    "model": "groq-mixtral"
  }'
```

### View API Docs
Open http://localhost:8000/docs in browser

---

## ✅ Test It Works

### Backend Health Check
```bash
curl http://localhost:8000/health
```

Expected: `{"status":"healthy","version":"1.0.0"}`

### Frontend Access
Open http://localhost:7860 and you should see the Streamlit interface

### Try a Query
1. Click in the query box
2. Type: "What is machine learning?"
3. Click "Send Query"
4. Wait for response

---

## 🚀 Next Steps

After verification:

1. **For Local Development**
   - Modify code in `app.py` and `main.py`
   - Changes reload automatically
   - Check logs in terminal

2. **For Production Deployment**
   - Read [DEPLOYMENT.md](DEPLOYMENT.md)
   - Deploy to Hugging Face Spaces
   - Set up on cloud platform

3. **For Portfolio/Resume**
   - Share HF Spaces link
   - Add to GitHub profile
   - Include in portfolio

---

## 🆘 Troubleshooting

### Port 7860 Already in Use
```bash
# Find and kill process
lsof -ti:7860 | xargs kill -9
```

### GROQ API Key Error
- Check `.env` file exists
- Verify key format (no extra quotes)
- Check key is valid at groq.com

### Can't Connect to Backend
- Ensure `python main.py` is running
- Check port 8000 is available
- Try: `curl http://localhost:8000/health`

### Docker Issues
```bash
# Clean everything
docker-compose down -v
docker system prune -a

# Rebuild
docker-compose up --build
```

---

## 📚 Full Documentation
See [DEPLOYMENT.md](DEPLOYMENT.md) for complete guide

## 📱 Share Your Project
```markdown
🎉 I just deployed my Multilingual LLM RAG Assistant!
🔗 Live: https://huggingface.co/spaces/YOUR_USERNAME/multilingual-llm-rag-assistant
📖 GitHub: https://github.com/Abhi123aan/multilingual-llm-rag-assistant
```

---

**You're all set! 🎉**
