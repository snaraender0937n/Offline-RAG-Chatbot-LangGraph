from typing import Any, Dict

from graph.chains.retrieval_grader import retrieval_grader, GradeDocuments
from graph.state import GraphState


def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determine whether retrieved docs are relevant to the question.
    If all docs are irrelevant (or none exist), set a flag to run web search.
    """
    print("--- grade_documents: check document relevance to question ---")

    trace = list(state.get("trace", []))
    question = state["question"]
    documents = state.get("documents", []) or []

    # If no documents at all, immediately fall back to web search
    if not documents:
        trace.append("No documents retrieved -> enable web search")
        return {
            "documents": [],
            "question": question,
            "web_search": True,
            "trace": trace,
        }

    filtered_docs = []
    web_search = False

    for doc in documents:
        try:
            score: GradeDocuments = retrieval_grader.invoke(
                {"question": question, "document": doc.page_content}
            )
            grade = score.binary_score
        except Exception as e:
            # In case of any grading failure, mark as irrelevant and enable web search
            print(f"--- grade_documents error: {e} ---")
            trace.append(f"Grader error -> treat doc as irrelevant, enable web search")
            web_search = True
            continue

        if isinstance(grade, str):
            is_yes = grade.lower() == "yes"
        else:
            is_yes = bool(grade)

        if is_yes:
            print("--- grade: document relevant ---")
            trace.append("Grader: relevant doc kept")
            filtered_docs.append(doc)
        else:
            print("--- grade: document not relevant ---")
            trace.append("Grader: irrelevant doc -> enable web search")
            web_search = True

    return {
        "documents": filtered_docs,
        "question": question,
        "web_search": web_search,
        "trace": trace,
    }