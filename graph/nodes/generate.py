from typing import Any, Dict

from graph.chains.generation import generation_chain
from graph.state import GraphState


def generate(state: GraphState) -> Dict[str, Any]:
    print("--- generate ---")

    trace = list(state.get("trace", []))
    question = state["question"]
    documents = state.get("documents", [])

    try:
        generation = generation_chain.invoke(
            {"context": documents, "question": question}
        )
        trace.append("Generated answer")
    except Exception as e:
        generation = (
            "[ERROR] Generation failed in offline mode."
        )
        trace.append(f"Generation error: {e}")

    return {
        "documents": documents,
        "question": question,
        "generation": generation,
        "trace": trace,
    }