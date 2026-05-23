# 🚀 Complete Deployment Guide

## Quick Navigation
- ⭐ **[Hugging Face Spaces](#hugging-face-spaces-recommended)** (Recommended - No setup required)
- 🐳 **[Docker Compose](#docker-compose-local--cloud)** (Local & Cloud)
- 💻 **[Python Local](#python-local-development)** (Development)
- ☁️ **[Other Cloud Platforms](#other-cloud-platforms)** (AWS, GCP, Azure)

---

## 🌟 Hugging Face Spaces (Recommended)

### What is Hugging Face Spaces?
Free hosting for ML applications with built-in Docker support. Perfect for demos and portfolio projects!

### Live Demo URL
👉 **[https://huggingface.co/spaces/Abhi123aan/multilingual-llm-rag-assistant](https://huggingface.co/spaces/Abhi123aan/multilingual-llm-rag-assistant)**

### Steps to Deploy

#### Step 1: Create Hugging Face Account
1. Go to https://huggingface.co
2. Sign up (free account)
3. Verify your email

#### Step 2: Create a New Space
1. Navigate to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in details:
   - **Space name**: `multilingual-llm-rag-assistant`
   - **License**: MIT
   - **SDK**: Docker
   - **Visibility**: Public (for portfolio) or Private
4. Click **"Create space"**

#### Step 3: Add Secrets
1. Go to Space **Settings**
2. Find **"Repository secrets"**
3. Add your `GROQ_API_KEY`:
   - **Name**: `GROQ_API_KEY`
   - **Value**: Your actual Groq API key
4. Save

#### Step 4: Push Your Code
```bash
# Clone the HF Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/multilingual-llm-rag-assistant
cd multilingual-llm-rag-assistant

# Add GitHub repository as remote
git remote add github https://github.com/Abhi123aan/multilingual-llm-rag-assistant.git

# Pull the latest code
git pull github main

# Push to HF Spaces
git push
```

#### Step 5: Monitor Deployment
1. Space will automatically build and deploy
2. Check the **"Building"** tab for logs
3. Once complete, space is live at:
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/multilingual-llm-rag-assistant
   ```

### Sharing Your Deployment
- Share the direct URL with anyone
- Embed in portfolio/resume
- Add to GitHub profile
- Share on LinkedIn/Twitter

---

## 🐳 Docker Compose (Local & Cloud)

### Prerequisites
- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop/))
- `.env` file with `GROQ_API_KEY`

### Local Deployment

#### Step 1: Clone Repository
```bash
git clone https://github.com/Abhi123aan/multilingual-llm-rag-assistant.git
cd multilingual-llm-rag-assistant
```

#### Step 2: Setup Environment
```bash
# Copy example file
cp .env.example .env

# Edit .env with your API key
# Add your GROQ_API_KEY=xxxx
```

#### Step 3: Start Containers
```bash
# Build and run
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

#### Step 4: Access Application
- **Web UI**: http://localhost:7860
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

#### Step 5: Stop Containers
```bash
docker-compose down

# Remove volumes too
docker-compose down -v
```

### Cloud Deployment (AWS, GCP, Azure)

#### AWS EC2
```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# Clone and deploy
git clone https://github.com/Abhi123aan/multilingual-llm-rag-assistant.git
cd multilingual-llm-rag-assistant

# Create .env file
echo "GROQ_API_KEY=your_key" > .env

# Start
sudo docker-compose up -d

# Access at: http://your-instance-ip:7860
```

#### Google Cloud Run
```bash
# Build and push to Cloud Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/rag-assistant

# Deploy
gcloud run deploy rag-assistant \
  --image gcr.io/PROJECT_ID/rag-assistant \
  --platform managed \
  --port 7860 \
  --set-env-vars GROQ_API_KEY=your_key
```

---

## 💻 Python Local Development

### Prerequisites
- Python 3.10+
- pip package manager

### Installation

#### Step 1: Clone Repository
```bash
git clone https://github.com/Abhi123aan/multilingual-llm-rag-assistant.git
cd multilingual-llm-rag-assistant
```

#### Step 2: Create Virtual Environment
```bash
# Create venv
python -m venv venv

# Activate
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Setup Environment
```bash
cp .env.example .env
# Edit .env with your GROQ_API_KEY
```

#### Step 5: Run Backend (Terminal 1)
```bash
python main.py

# Output should show:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

#### Step 6: Run Frontend (Terminal 2)
```bash
streamlit run app.py --server.port 7860

# Output should show:
# You can now view your Streamlit app in your browser.
# URL: http://localhost:7860
```

#### Step 7: Access Application
- Open http://localhost:7860 in browser
- API docs at http://localhost:8000/docs

### Development Commands

```bash
# Format code
python -m black .

# Run tests (if available)
pytest tests/

# Check for issues
flake8 .

# Type checking
mypy .
```

---

## ☁️ Other Cloud Platforms

### Heroku
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port \$PORT --server.address 0.0.0.0" > Procfile

# Deploy
heroku login
heroku create your-app-name
git push heroku main
```

### Railway
1. Connect GitHub repository
2. Add `GROQ_API_KEY` environment variable
3. Auto-deploys on push

### Render
1. Connect GitHub repository
2. Create new Web Service
3. Set start command: `streamlit run app.py`
4. Add environment variables
5. Deploy

### DigitalOcean App Platform
1. Connect GitHub repository
2. Use Dockerfile (auto-detected)
3. Add env vars
4. Deploy

---

## 🔑 Getting Your GROQ API Key

1. Go to https://groq.com
2. Sign up for free
3. Navigate to API Keys
4. Create new API key
5. Copy the key (keep it secret!)
6. Add to `.env` file: `GROQ_API_KEY=your_key_here`

---

## 📊 Monitoring & Logs

### Local Docker
```bash
# View logs
docker-compose logs -f

# View specific service
docker-compose logs -f frontend
docker-compose logs -f backend

# Check container status
docker-compose ps
```

### Hugging Face Spaces
1. Go to Space URL
2. Click **"Building"** tab
3. View real-time logs

### Troubleshooting

#### Port Already in Use
```bash
# Linux/Mac
lsof -ti:7860 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :7860
taskkill /PID <PID> /F
```

#### Memory Issues
```bash
# Increase Docker memory limit
# In Docker Desktop: Settings > Resources > Memory
```

#### API Connection Error
- Ensure backend is running
- Check `http://localhost:8000/health` returns 200
- Verify `GROQ_API_KEY` is set

---

## 🎯 Deployment Checklist

- [ ] Cloned repository
- [ ] Created `.env` file
- [ ] Added `GROQ_API_KEY`
- [ ] Installed dependencies
- [ ] Started backend
- [ ] Started frontend
- [ ] Can access http://localhost:7860
- [ ] Can see API docs at http://localhost:8000/docs
- [ ] Query processing works
- [ ] Ready to deploy to production

---

## 📱 Sharing Your Deployment

### For HF Spaces
```markdown
# Hugging Face Spaces Link
🎯 Visit: https://huggingface.co/spaces/YOUR_USERNAME/multilingual-llm-rag-assistant

# Add to README
[![Hugging Face Space](https://img.shields.io/badge/🤗-Open%20in%20Spaces-blue.svg)](https://huggingface.co/spaces/YOUR_USERNAME/multilingual-llm-rag-assistant)
```

### For Resume/Portfolio
```
Multilingual LLM RAG Assistant
- Production-ready FastAPI with FAISS vector search
- Deployed on Hugging Face Spaces
- Supports English & Hindi
- Live Demo: [https://huggingface.co/spaces/YOUR_USERNAME/...]
- GitHub: [https://github.com/Abhi123aan/...]
```

### Social Media
```
🚀 Just deployed my Multilingual LLM RAG Assistant!
📌 Features: FAISS vector search, FastAPI, Streamlit
🎯 Live: https://huggingface.co/spaces/YOUR_USERNAME/...
⭐ GitHub: https://github.com/Abhi123aan/...
```

---

## 🆘 Getting Help

- **GitHub Issues**: Report bugs
- **Discussions**: Ask questions
- **Stack Overflow**: Tag with `fastapi`, `streamlit`, `rag`
- **Hugging Face Community**: Forum discussions

---

**Happy Deploying! 🚀**
