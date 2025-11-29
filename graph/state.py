from typing import List, TypedDict, Any


class GraphState(TypedDict, total=False):
    """
    Include all the states needed for graph execution.

    Attributes:
        question: user question
        generation: generated answer
        web_search: whether to trigger web search
        documents: list of retrieved documents
        trace: internal log messages for UI / debugging
        from_vector: whether answer came only from vector store
    """
    question: str
    generation: str
    web_search: bool
    documents: List[Any]
    trace: List[str]
    from_vector: bool