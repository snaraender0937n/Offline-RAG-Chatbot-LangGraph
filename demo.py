#!/usr/bin/env python3
"""
Demo script for the RAG Chatbot
Usage: python demo.py "your question here"
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Detect whether we have a real OpenAI API key
OPENAI_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))
app = None

if not OPENAI_AVAILABLE:
    print("⚠️  OFFLINE MODE: OPENAI_API_KEY not set.")
    print("    The demo will print dummy answers instead of real AI responses.\n")
else:
    try:
        from graph.graph import app  # real LangGraph app
    except ImportError as e:
        print(f"❌ Error importing graph module: {e}")
        print("Please ensure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)


def ask_question(question: str):
    """Ask a question to the RAG chatbot"""
    print(f"\n🤖 Processing question: {question}\n")
    
    try:
        if app is None:
            # Offline dummy result
            result = {
                "question": question,
                "generation": (
                    "[OFFLINE MODE] I cannot call OpenAI without an API key. "
                    "Set OPENAI_API_KEY in a .env file to get real answers."
                ),
                "from_vector": False,
                "documents": [],
                "trace": ["offline_mode_no_openai_key"],
            }
        else:
            # Normal online mode
            result = app.invoke(input={"question": question})
        
        print("=" * 60)
        print("📝 FINAL RESULT:")
        print("=" * 60)
        print(f"Question: {result.get('question', 'N/A')}")
        print(f"\nAnswer: {result.get('generation', 'N/A')}")
        
        from_vector = bool(result.get("from_vector", False))
        docs_count = len(result.get("documents", []) or [])
        
        # In offline mode, this will still print "Web Search" but that's fine; we add a hint
        source_label = "📚 Vector DB" if from_vector else "🌐 Web Search / Offline"
        print(f"\nSource: {source_label}")
        print(f"Documents Found: {docs_count}")
        
        trace = result.get("trace", [])
        if trace:
            print("\n📋 Process Trace:")
            for step in trace:
                print(f"  • {step}")
        
        print("=" * 60)
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Default questions if none provided
    questions = [
        "what is agent memory?",
        "what are hallucinations in AI?",
        "explain diffusion models",
    ]
    
    # Use command line argument if provided
    if len(sys.argv) > 1:
        questions = [" ".join(sys.argv[1:])]
    
    print("🚀 Starting RAG Chatbot Demo")
    print("=" * 60)
    
    try:
        for question in questions:
            ask_question(question)
            if len(questions) > 1:
                print("\n" + "-" * 60 + "\n")
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)