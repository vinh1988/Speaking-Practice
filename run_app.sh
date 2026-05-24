#!/bin/bash

# Multimodal AI Speaking Coach - Startup Script
echo "🚀 Starting Multimodal AI Speaking Coach Setup..."

# 1. Define and check Python version
PYTHON_VERSION="3.12"
PYTHON_CMD="python$PYTHON_VERSION"

if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "⚠️  Warning: Python $PYTHON_VERSION is not installed. Trying python3..."
    PYTHON_CMD="python3"
    if ! command -v $PYTHON_CMD &> /dev/null; then
        echo "❌ Error: Python not found."
        exit 1
    fi
fi

echo "✅ Using $( $PYTHON_CMD --version )."

# 2. Setup Virtual Environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment using $PYTHON_CMD..."
    $PYTHON_CMD -m venv venv
    echo "📥 Installing dependencies (this may take a few minutes)..."
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt
else
    echo "✅ Virtual environment found."
fi

# 5. Handle Process Cleanup
echo "🧹 Cleaning up old processes..."
pkill -f uvicorn
pkill -f streamlit

# 6. Run Backend
echo "⚙️ Starting FastAPI Backend on port 8080..."
./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080 &

# 7. Run Frontend
echo "🌐 Starting Streamlit Frontend on port 8501..."
echo "---"
echo "The terminal will show Streamlit logs. Press CTRL+C to stop both services."
echo "---"
./venv/bin/streamlit run frontend/streamlit_app.py --server.port 8501 --server.headless true

# Final Cleanup on exit
trap "pkill -f uvicorn; pkill -f streamlit; exit" INT TERM
