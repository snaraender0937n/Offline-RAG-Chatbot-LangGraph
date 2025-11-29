from __future__ import annotations

import os
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_core.documents import Document

from graph.state import GraphState

load_dotenv()

TAVILY_AVAILABLE = bool(os.getenv("TAVILY_API_KEY"))


class _OfflineWebSearch:
    """
    Offline dummy web search.

    Mimics a web search node without calling external APIs.
    """

    def invoke(self, query: str) -> list[Document]:
        return [
            Document(
                page_content=(
                    "[OFFLINE MODE] Web search is disabled.\n"
                    f"Simulated web result for question: '{query}'."
                )
            )
        ]


# Initialize web search tool
if TAVILY_AVAILABLE:
    from langchain_community.tools.tavily_search import TavilySearchResults

    web_search_tool = TavilySearchResults(k=3)
else:
    web_search_tool = _OfflineWebSearch()


def web_search(state: GraphState) -> Dict[str, Any]:
    print("--- web_search ---")

    question = state.get("question", "")
    documents = list(state.get("documents", []))
    trace = list(state.get("trace", []))

    try:
        if TAVILY_AVAILABLE:
            docs = web_search_tool.invoke({"query": question})
            contents = "\n".join(d.get("content", "") for d in docs)
            result_doc = Document(page_content=contents)
            trace.append("Web search executed (online)")
        else:
            result_doc = web_search_tool.invoke(question)[0]
            trace.append("Web search simulated (offline)")
    except Exception as e:
        trace.append(f"Web search error: {e}")
        return {
            "documents": documents,
            "question": question,
            "trace": trace,
            "from_vector": False,
        }

    documents.append(result_doc)

    return {
        "documents": documents,
        "question": question,
        "trace": trace,
        "from_vector": False,
    }