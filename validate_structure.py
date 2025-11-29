#!/usr/bin/env python3
"""
Validation script to check project structure
"""
import os
import sys

def check_structure():
    """Validate that all required files and directories exist"""
    checks = []
    
    # Check main directories
    checks.append(("graph/", os.path.isdir("graph")))
    checks.append(("graph/chains/", os.path.isdir("graph/chains")))
    checks.append(("graph/nodes/", os.path.isdir("graph/nodes")))
    
    # Check main files
    checks.append(("graph/__init__.py", os.path.isfile("graph/__init__.py")))
    checks.append(("graph/graph.py", os.path.isfile("graph/graph.py")))
    checks.append(("graph/state.py", os.path.isfile("graph/state.py")))
    checks.append(("graph/consts.py", os.path.isfile("graph/consts.py")))
    
    # Check chain files
    chain_files = [
        "answer_grader.py", "hallucination_grader.py", "retrieval_grader.py",
        "router.py", "generation.py", "__init__.py"
    ]
    for f in chain_files:
        checks.append((f"graph/chains/{f}", os.path.isfile(f"graph/chains/{f}")))
    
    # Check node files
    node_files = [
        "retrieve.py", "generate.py", "grade_documents.py",
        "web_search.py", "__init__.py"
    ]
    for f in node_files:
        checks.append((f"graph/nodes/{f}", os.path.isfile(f"graph/nodes/{f}")))
    
    # Check other important files
    checks.append(("main.py", os.path.isfile("main.py")))
    checks.append(("cli.py", os.path.isfile("cli.py")))
    checks.append(("demo.py", os.path.isfile("demo.py")))
    checks.append(("ingestion.py", os.path.isfile("ingestion.py")))
    checks.append(("requirements.txt", os.path.isfile("requirements.txt")))
    
    # Report results
    print("=" * 60)
    print("📋 Project Structure Validation")
    print("=" * 60)
    
    all_pass = True
    for path, exists in checks:
        status = "✅" if exists else "❌"
        print(f"{status} {path}")
        if not exists:
            all_pass = False
    
    print("=" * 60)
    
    if all_pass:
        print("✅ All structure checks passed!")
        return True
    else:
        print("❌ Some files/directories are missing!")
        return False

def check_env():
    """Check environment setup"""
    print("\n" + "=" * 60)
    print("🔧 Environment Check")
    print("=" * 60)
    
    has_openai_key = bool(os.getenv("OPENAI_API_KEY"))
    has_tavily_key = bool(os.getenv("TAVILY_API_KEY"))
    has_env_file = os.path.isfile(".env")
    
    print(f"{'✅' if has_env_file else '⚠️ '} .env file: {'exists' if has_env_file else 'not found'}")
    print(f"{'✅' if has_openai_key else '❌'} OPENAI_API_KEY: {'set' if has_openai_key else 'not set (required)'}")
    print(f"{'✅' if has_tavily_key else '⚠️ '} TAVILY_API_KEY: {'set' if has_tavily_key else 'not set (optional)'}")
    
    print("=" * 60)
    
    if not has_openai_key:
        print("\n⚠️  WARNING: OPENAI_API_KEY is required to run the application.")
        print("Please create a .env file with your API key.")
    
    return has_openai_key

if __name__ == "__main__":
    structure_ok = check_structure()
    env_ok = check_env()
    
    print("\n" + "=" * 60)
    if structure_ok and env_ok:
        print("✅ Project is ready to run!")
        print("\nNext steps:")
        print("  1. Build index: py ingestion.py --paths docs --rebuild")
        print("  2. Run: py cli.py --question 'your question'")
    elif structure_ok:
        print("⚠️  Project structure is correct, but API key is missing.")
        print("Please set OPENAI_API_KEY in your .env file to run the application.")
    else:
        print("❌ Project structure needs to be fixed.")
    print("=" * 60)