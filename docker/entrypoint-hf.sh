#!/usr/bin/env bash
# Entrypoint script for HuggingFace Spaces deployment
# Starts both FastAPI backend and Streamlit frontend

set -euo pipefail

# Default port (HF Spaces uses 7860)
: ${PORT:=7860}

echo "🚀 Starting Semantic Recipe Finder on HuggingFace Spaces"
echo "📊 Backend API: http://localhost:8000"
echo "🎨 Frontend UI: http://localhost:${PORT}"

# Start FastAPI backend in background
echo "🔧 Starting FastAPI backend..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info &
BACKEND_PID=$!

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Backend failed to start in time"
        exit 1
    fi
    sleep 2
done

# Start Streamlit frontend (foreground)
echo "🎨 Starting Streamlit frontend..."
exec streamlit run frontend/app.py \
    --server.port ${PORT} \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --browser.gatherUsageStats false

# If Streamlit exits, kill backend
trap "kill ${BACKEND_PID}" EXIT
