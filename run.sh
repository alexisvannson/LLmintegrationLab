#!/bin/bash

# Carbon Footprint Analyzer Launch Script

echo "Carbon Footprint Analyzer"
echo "=============================="
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "[ERROR] Ollama is not installed"
    echo "Please install Ollama from: https://ollama.ai/"
    exit 1
fi

# Check if llama3:8b model is available
if ! ollama list | grep -q "llama3:8b"; then
    echo "[WARNING] llama3:8b model not found"
    echo "Pulling model (this may take a few minutes)..."
    ollama pull llama3:8b
fi

echo "[OK] Ollama is ready"
echo ""

# Check Python dependencies
echo "Checking dependencies..."
pip install -q -r requirements.txt

echo "[OK] Dependencies installed"
echo ""

# Launch the app
echo "Launching application..."
echo "Opening in browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Set PYTHONPATH to project root so 'src' package can be found
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
streamlit run src/app.py
