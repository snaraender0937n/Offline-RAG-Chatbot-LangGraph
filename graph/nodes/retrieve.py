from typing import Any, Dict

from graph.state import GraphState
from ingestion import retriever


def retrieve(state: GraphState) -> Dict[str, Any]:
    print("--- retrieve ---")

    trace = list(state.get("trace", []))
    question = state["question"]

    # Retriever not available (offline mode or no index)
    if retriever is None:
        trace.append("Retriever not initialized. No documents found (offline / no index).")
        return {
            "documents": [],
            "question": question,
            "trace": trace,
            "from_vector": False,
        }

    try:
        trace.append("Retrieving relevant documents from vector store")
        documents = retriever.invoke(question)
        return {
            "documents": documents,
            "question": question,
            "trace": trace,
            "from_vector": True,
        }
    except Exception as e:
        trace.append(f"Error retrieving documents: {e}")
        return {
            "documents": [],
            "question": question,
            "trace": trace,
            "from_vector": False,
        }