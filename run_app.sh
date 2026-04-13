#!/bin/bash

# Multimodal AI Speaking Coach - Startup Script
echo "🚀 Starting Multimodal AI Speaking Coach Setup..."

# 1. Define and check Python version
PYTHON_VERSION="3.12"
PYTHON_CMD="python$PYTHON_VERSION"

if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ Error: Python $PYTHON_VERSION is not installed."
    echo "Please install it using: sudo apt install python$PYTHON_VERSION python$PYTHON_VERSION-venv"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected."

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

# 3. Check for Piper voice model
if [ ! -f "models/piper/en_US-lessac-medium.onnx" ]; then
    echo "🎙️ Downloading Piper voice model..."
    mkdir -p models/piper
    curl -L https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx -o models/piper/en_US-lessac-medium.onnx
    curl -L https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json -o models/piper/en_US-lessac-medium.onnx.json
fi

# 4. Check for Ollama and Phi-3 model
if command -v ollama &> /dev/null; then
    if ! ollama list | grep -q "phi3"; then
        echo "🦙 Pulling Phi-3 model for Ollama (this may take a while)..."
        ollama pull phi3
    else
        echo "✅ Phi-3 model found in Ollama."
    fi
else
    echo "⚠️ Warning: Ollama not found. Please install it from https://ollama.com"
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
