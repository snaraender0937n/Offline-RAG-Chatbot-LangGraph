"""
ingestion.py
- Build or update the ChromaDB vector store from local files and/or URLs
- Always exposes a `retriever` for runtime use by the app

Examples
1) Index a local folder and a couple URLs (fresh build):
   python ingestion.py --paths docs handbook/*.pdf --urls https://example.com/a https://example.com/b --rebuild

2) Only add URLs to existing index:
   python ingestion.py --urls https://example.com/faq

3) Only (re)load retriever at runtime (imported by app):
   from ingestion import retriever
"""

from __future__ import annotations
import argparse
import glob
import os
from pathlib import Path
from typing import Iterable, List

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    WebBaseLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# --------------------------------------------------
# API key / environment check
# --------------------------------------------------
OPENAI_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))

if not OPENAI_AVAILABLE:
    import warnings
    warnings.warn(
        "OPENAI_API_KEY not found. Embeddings/indexing are disabled.\n"
        "You can still run the app in OFFLINE MODE (dummy answers), "
        "but ingestion and vector search will not work until you set an API key."
    )

# -----------------------------
# Configuration
# -----------------------------
PERSIST_DIR = os.environ.get("RAGBOT_CHROMA_DIR", "./.chroma")
COLLECTION_NAME = os.environ.get("RAGBOT_COLLECTION", "ragbot-chroma")

# -----------------------------
# Helpers
# -----------------------------

def _load_local_paths(paths: Iterable[str]) -> List:
    documents = []
    for p in paths:
        for path_str in glob.glob(p, recursive=True):
            path = Path(path_str)
            if path.is_dir():
                # load common file types in the directory
                for ext in ("*.pdf", "*.md", "*.txt"):
                    for f in path.rglob(ext):
                        documents.extend(_load_single_file(f))
            elif path.is_file():
                documents.extend(_load_single_file(path))
    return documents


def _load_single_file(path: Path) -> List:
    docs = []
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        docs.extend(PyPDFLoader(str(path)).load())
    elif suffix in {".md", ".txt"}:
        docs.extend(TextLoader(str(path), encoding="utf-8").load())
    # silently skip unsupported extensions
    return docs


def _load_urls(urls: Iterable[str]) -> List:
    documents = []
    for url in urls:
        try:
            print(f"  Loading URL: {url}")
            documents.extend(WebBaseLoader(url).load())
        except Exception as e:
            # skip bad URLs but keep indexing others
            print(f"  ⚠️  Warning: Failed to load URL {url}: {e}")
            continue
    return documents


# -----------------------------
# CLI build entrypoint
# -----------------------------

def build_index(paths: List[str] | None, urls: List[str] | None, rebuild: bool = False):
    # If no API key, do not even try to build embeddings
    if not OPENAI_AVAILABLE:
        print("⚠️  OPENAI_API_KEY is not set.")
        print("    Ingestion (building the vector index) is disabled in offline mode.")
        print("    Set OPENAI_API_KEY in a .env file to enable indexing.\n")
        return

    try:
        print("📚 Loading documents...")
        local_docs = _load_local_paths(paths or []) if paths else []
        web_docs = _load_urls(urls or []) if urls else []
        all_docs = local_docs + web_docs
        
        if not all_docs:
            print("⚠️  No documents found to index. Provide --paths and/or --urls.")
            return

        print(f"✅ Loaded {len(local_docs)} local documents and {len(web_docs)} web documents")

        if rebuild and os.path.isdir(PERSIST_DIR):
            # clean persistence for a fresh build
            import shutil
            print(f"🗑️  Rebuilding index: removing existing directory {PERSIST_DIR}")
            shutil.rmtree(PERSIST_DIR, ignore_errors=True)

        print("🔨 Splitting documents into chunks...")
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=250, chunk_overlap=0
        )
        chunks = splitter.split_documents(all_docs)
        print(f"✅ Created {len(chunks)} chunks from {len(all_docs)} documents")

        print("💾 Creating/updating vector store...")
        # Create or extend the vector store
        _ = Chroma.from_documents(
            documents=chunks,
            collection_name=COLLECTION_NAME,
            embedding=OpenAIEmbeddings(),
            persist_directory=PERSIST_DIR,
        )
        print(f"✅ Indexed {len(all_docs)} source docs into collection '{COLLECTION_NAME}'.")
        
    except Exception as e:
        print(f"❌ Error building index: {e}")
        import traceback
        traceback.print_exc()
        raise


# -----------------------------
# Runtime retriever (imported by the app)
# -----------------------------
if OPENAI_AVAILABLE:
    try:
        retriever = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=PERSIST_DIR,
            embedding_function=OpenAIEmbeddings(),
        ).as_retriever()
    except Exception as e:
        import warnings
        warnings.warn(
            f"Could not initialize retriever: {e}. "
            "You may need to build the index first."
        )
        retriever = None
else:
    import warnings
    warnings.warn(
        "OPENAI_API_KEY not set. Retriever is disabled; "
        "vector search will not be available (offline mode)."
    )
    retriever = None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Index local files and/or URLs into Chroma.")
    parser.add_argument("--paths", nargs="*", help="File or directory globs (e.g., docs, docs/*.pdf)")
    parser.add_argument("--urls", nargs="*", help="One or more web URLs to index")
    parser.add_argument("--rebuild", action="store_true", help="Delete existing index before building")
    args = parser.parse_args()

    build_index(paths=args.paths, urls=args.urls, rebuild=args.rebuild)