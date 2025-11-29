"""
Graph module for RAG chatbot workflow
"""

from dotenv import load_dotenv

from langgraph.graph import END, StateGraph

from graph.consts import *
from graph.nodes import *
from graph.state import GraphState
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.router import question_router, RouteQuery

load_dotenv()


def decide_to_generate(state: GraphState) -> str:
    """
    After retrieval + grading, decide whether to generate directly
    or fall back to web search.
    """
    print("--- assess graded documents ---")
    trace = list(state.get("trace", []))

    if state.get("web_search"):
        # At least one doc was irrelevant or no docs → prefer web search
        print("--- decision: docs not sufficient, go to web search ---")
        trace.append("Decision: not all docs relevant → web search")
        return WEBSEARCH
    else:
        print("--- decision: docs sufficient, generate answer ---")
        trace.append("Decision: docs sufficient → generate")
        return GENERATE


def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    """
    Check if the generated answer is grounded in the retrieved documents.

    If grounded → 'useful' (end the workflow).
    If not grounded → 'not supported' (regenerate).
    """
    print("--- check hallucination ---")
    trace = list(state.get("trace", []))

    question = state["question"]
    documents = state.get("documents", [])
    generation = state.get("generation", "")

    # Call hallucination grader (offline-safe wrapper in current setup)
    score = hallucination_grader.invoke(
        {"documents": documents, "question": question, "generation": generation}
    )

    binary = getattr(score, "binary_score", True)

    if isinstance(binary, str):
        grounded = binary.lower() in ("yes", "true")
    else:
        grounded = bool(binary)

    if grounded:
        print("--- decision: generation is grounded in documents ---")
        trace.append("Check: grounded in documents ✔")
        trace.append("Check: answer accepted ✔")
        return "useful"
    else:
        print("--- decision: generation is not grounded, regenerate ---")
        trace.append("Check: not grounded → regenerate")
        return "not supported"


def route_question(state: GraphState) -> str:
    """
    Route incoming question either to:
    - WEBSEARCH (directly), or
    - RETRIEVE (RAG flow).
    """
    print("--- route question ---")
    question = state["question"]
    source: RouteQuery = question_router.invoke({"question": question})

    if source.datasource == WEBSEARCH:
        print("--- route: websearch ---")
        return WEBSEARCH
    elif source.datasource == "vectorstore":
        print("--- route: vectorstore (RAG) ---")
        return RETRIEVE
    else:
        # Fallback: default to RAG
        print("--- route: default to RAG ---")
        return RETRIEVE


# Build the LangGraph workflow
workflow = StateGraph(GraphState)

# Nodes
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)

# Entry routing: decide between websearch and RAG
workflow.set_conditional_entry_point(
    route_question,
    {
        WEBSEARCH: WEBSEARCH,
        RETRIEVE: RETRIEVE,
    },
)

# RAG branch: retrieve → grade documents → generate
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
        WEBSEARCH: WEBSEARCH,
        GENERATE: GENERATE,
    },
)

# After websearch, always go to generate
workflow.add_edge(WEBSEARCH, GENERATE)

# After generate, decide whether to accept or regenerate
workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    {
        "not supported": GENERATE,  # regenerate answer
        "useful": END,              # return answer to user
    },
)

# Compile app
app = workflow.compile()

# Optionally render the graph (best-effort; safe failure)
try:
    app.get_graph().draw_mermaid_png(output_file_path="graph.png")
except Exception:
    try:
        print(app.get_graph().draw_mermaid())
    except Exception:
        pass