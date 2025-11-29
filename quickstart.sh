#!/bin/bash

# Offline RAG Chatbot Quickstart (Linux / macOS)

clear
echo "╔════════════════════════════════════════════════════════════╗"
echo "║            Offline RAG Chatbot - Quickstart 🤖            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Activate virtual environment (optional)
if [ -d "venv" ]; then
    echo "🔄 Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found (continuing anyway)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " MODE: OFFLINE (NO API KEYS, DUMMY ANSWERS)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "• No external APIs are called"
echo "• No document ingestion or vector indexing"
echo "• Responses are offline dummy outputs"
echo ""

# Interactive Q&A loop
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " ASK QUESTIONS (type 'exit' or 'quit' to stop)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

while true; do
    read -p " Your question: " question

    if [ "$question" = "exit" ] || [ "$question" = "quit" ]; then
        echo ""
        echo "✅ Exiting. Goodbye!"
        break
    fi

    if [ -z "$question" ]; then
        echo "⚠️  Please enter a question."
        continue
    fi

    echo ""
    echo "🔄 Processing (offline dummy mode)..."
    echo ""

    # Call offline-safe demo
    python demo.py "$question" 2>/dev/null

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
done