from __future__ import annotations

import os
from pydantic import BaseModel, Field

# Detect offline mode
OPENAI_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))


class GradeAnswer(BaseModel):
    binary_score: bool = Field(
        description="Whether the answer sufficiently addresses the question"
    )


def _offline_answer_grader(_: dict) -> GradeAnswer:
    """
    Offline dummy grader.
    Always returns True so pipeline continues smoothly.
    """
    return GradeAnswer(binary_score=True)


if OPENAI_AVAILABLE:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnableSequence
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4", temperature=0)
    structured_llm = llm.with_structured_output(GradeAnswer)

    system = (
        "You are a grader assessing whether an answer addresses a question. "
        "Answer strictly with yes or no."
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Question:\n{question}\n\nAnswer:\n{generation}"),
        ]
    )

    answer_grader: RunnableSequence = prompt | structured_llm
else:
    # Offline fallback
    answer_grader = _offline_answer_grader