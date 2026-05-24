#!/bin/bash
set -e

echo "🚀 Starting Multilingual RAG Assistant..."

# Check if GROQ_API_KEY is set
if [ -z "$GROQ_API_KEY" ]; then
    echo "⚠️  WARNING: GROQ_API_KEY not set. App will run in demo mode."
else
    echo "✅ GROQ_API_KEY detected"
fi

# Start Streamlit app
echo "🎯 Starting Streamlit app on port 7860..."
exec streamlit run app.py \
    --server.port=7860 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --logger.level=debug \
    --client.showErrorDetails=true
