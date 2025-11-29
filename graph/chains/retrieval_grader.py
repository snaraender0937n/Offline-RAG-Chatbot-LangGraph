from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()

OPENAI_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))


class GradeDocuments(BaseModel):
    """
    Binary score for relevance check on retrieved documents:
    determine whether the retrieved document is relevant to the question.
    """
    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )


class _OfflineRetrievalGrader:
    """
    Offline dummy retrieval grader.

    Provides an .invoke(...) method so it can be used like a runnable.
    Always returns 'yes' so the pipeline can proceed in offline mode.
    """

    def invoke(self, inputs: dict) -> GradeDocuments:
        # In offline mode we cannot really grade; just say 'yes'.
        return GradeDocuments(binary_score="yes")


if OPENAI_AVAILABLE:
    from langchain_core.runnables import RunnableSequence
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4", temperature=0)
    structured_llm_grader = llm.with_structured_output(GradeDocuments)

    system = """
You are a grader assessing relevance of a retrieved document to a user question.
If the document contains keywords or semantic meaning related to the question,
grade it as relevant. Give a binary score 'yes' or 'no' to indicate whether
the document is relevant to the question.
"""

    grade_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                "Retrieved document:\n\n{document}\n\nUser question:\n{question}",
            ),
        ]
    )

    retrieval_grader: RunnableSequence = grade_prompt | structured_llm_grader
else:
    retrieval_grader = _OfflineRetrievalGrader()