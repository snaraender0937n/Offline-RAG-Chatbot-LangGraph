#!/bin/bash

# Offline RAG Chatbot - Startup Script

echo "=============================================="
echo " Starting Offline RAG Chatbot"
echo "=============================================="
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo " Activating virtual environment..."
    source venv/bin/activate
    echo " Virtual environment activated"
else
    echo " Virtual environment not found (continuing without it)"
fi

echo ""
echo " MODE: OFFLINE (NO API KEYS, DUMMY ANSWERS)"
echo ""

# Check if a question is provided
if [ $# -eq 0 ]; then
    echo " Running default demo questions..."
    python demo.py
else
    echo " Processing your question:"
    echo "  $*"
    python demo.py "$*"
fi

echo ""
echo "=============================================="
echo " Session complete"
echo "=============================================="
echo " Usage:"
echo "   ./start.sh \"your question here\""
echo ""