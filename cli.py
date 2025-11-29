#!/usr/bin/env python3
"""
cli.py - Terminal interface for RAG Chatbot

Examples:
  # Rebuild index from local folder and URLs, then ask
  python cli.py --paths docs handbook/*.pdf --urls https://example.com/a https://example.com/b --rebuild --question "what is X?"

  # Add URLs only, then ask
  python cli.py --urls https://example.com/faq --question "summarize faq"

  # Just ask using existing index
  python cli.py --question "what is agent memory?"
"""
from __future__ import annotations
import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Detect whether we have a real OpenAI API key
OPENAI_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))

# Always try to import ingestion (for build_index)
try:
    from ingestion import build_index
except ImportError as e:
    print(f"❌ Error importing ingestion module: {e}")
    print("Please ensure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)

# Only import the LangGraph app if we actually have an API key
if OPENAI_AVAILABLE:
    try:
        from graph.graph import app
    except ImportError as e:
        print(f"❌ Error importing graph module: {e}")
        print("Please ensure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
else:
    app = None
    print("⚠️  OFFLINE MODE: OPENAI_API_KEY not set.")
    print("    CLI will return a dummy answer instead of calling the real model.\n")


def main():
    parser = argparse.ArgumentParser(
        description="RAG Chatbot CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Rebuild index and ask a question
  python cli.py --paths docs --urls https://example.com --rebuild --question "what is X?"

  # Ask using existing index
  python cli.py --question "what is agent memory?"
        """
    )
    parser.add_argument("--paths", nargs="*", help="File/dir globs to ingest (e.g., docs, *.pdf)")
    parser.add_argument("--urls", nargs="*", help="URLs to ingest")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the index from scratch")
    parser.add_argument("--question", required=True, help="Question to ask")
    args = parser.parse_args()

    try:
        # Build index if paths or URLs provided
        if (args.paths or args.urls):
            print("📚 Building index...")
            try:
                build_index(paths=args.paths, urls=args.urls, rebuild=args.rebuild)
                print("✅ Index built successfully!\n")
            except Exception as e:
                print(f"⚠️  Warning: Error building index: {e}")
                print("Continuing with existing index...\n")

        print("=" * 60)
        print("🤖 Advanced RAG Chatbot")
        print("=" * 60)
        
        print(f"\n💬 Question: {args.question}\n")
        print("🔄 Processing...\n")
        
        # OFFLINE / NO-API-KEY MODE
        if app is None:
            result = {
                "question": args.question,
                "generation": (
                    "[OFFLINE MODE] I received your question, but no OpenAI API key "
                    "is configured. Configure OPENAI_API_KEY in a .env file to get "
                    "real AI-generated answers."
                ),
                "from_vector": False,
                "documents": [],
                "trace": ["offline_mode_no_openai_key"],
            }
        else:
            # Normal online mode
            result = app.invoke(input={"question": args.question})

        from_vector = bool(result.get("from_vector", False))
        docs_count = len(result.get("documents", []) or [])

        print("=" * 60)
        print("✅ RESULT")
        print("=" * 60)
        print(f"Question: {result.get('question')}")
        
        if from_vector:
            print("Source: 📚 Provided documents (vector DB)")
        else:
            print("Source: 🌐 Augmented with web search (or offline dummy mode)")
        
        print(f"Documents used: {docs_count}")
        print("\n" + "-" * 60)
        print("Answer:")
        print("-" * 60)
        print(result.get("generation", "No answer generated."))

        logs = result.get("trace", [])
        if logs:
            print("\n" + "-" * 60)
            print("📋 Process Trace:")
            print("-" * 60)
            for line in logs:
                print(f"  • {line}")
        
        print("\n" + "=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()