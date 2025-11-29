"""
Main entry point for the RAG Chatbot
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Detect whether we have a real OpenAI API key
OPENAI_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))
app = None

if not OPENAI_AVAILABLE:
    print("⚠️  OFFLINE MODE: OPENAI_API_KEY not set.")
    print("    main.py will show a dummy answer instead of real AI output.\n")
else:
    try:
        from graph.graph import app  # real LangGraph app
    except ImportError as e:
        print(f"❌ Error importing graph module: {e}")
        print("Please ensure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Advanced RAG Chatbot")
    print("=" * 60)
    
    try:
        # Show the workflow graph (only if app is available)
        print("\n📊 Workflow Graph:")
        print("-" * 60)
        if app is not None:
            try:
                graph_mermaid = app.get_graph().draw_mermaid()
                print(graph_mermaid)
            except Exception as e:
                print(f"Could not generate graph visualization: {e}")
        else:
            print("Offline mode: cannot load LangGraph app to render graph.")
        
        print("\n" + "=" * 60)
        print("💬 Processing Question...")
        print("=" * 60)
        
        question = "what is agent memory?"

        if app is None:
            # Offline dummy result
            result = {
                "question": question,
                "generation": (
                    "[OFFLINE MODE] I received your question, but no OpenAI API key "
                    "is configured. Set OPENAI_API_KEY in a .env file to get real answers."
                ),
                "trace": ["offline_mode_no_openai_key"],
                "from_vector": False,
                "documents": [],
            }
        else:
            # Online mode with real graph
            result = app.invoke(input={"question": question})
        
        print("\n" + "=" * 60)
        print("✅ RESULT")
        print("=" * 60)
        print(f"Question: {result.get('question', 'N/A')}")
        print(f"\nAnswer: {result.get('generation', 'N/A')}")
        
        # Show trace information
        trace = result.get("trace", [])
        if trace:
            print("\n📋 Process Trace:")
            for step in trace:
                print(f"  • {step}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)