from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()

OPENAI_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))


class GradeHallucination(BaseModel):
    """Binary score for hallucination present in generation answer."""
    binary_score: bool = Field(
        description="Whether the answer is grounded in the provided facts."
    )


class _OfflineHallucinationGrader:
    """
    Offline dummy grader.

    Provides an .invoke(...) method so it can be used
    like a normal runnable. Always returns 'grounded'.
    """

    def invoke(self, inputs: dict) -> GradeHallucination:
        return GradeHallucination(binary_score=True)


if OPENAI_AVAILABLE:
    from langchain_core.runnables import RunnableSequence
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4", temperature=0)
    structured_llm_grader = llm.with_structured_output(GradeHallucination)

    system = (
        "You are a grader assessing whether an LLM generation is grounded in / "
        "supported by a set of facts.\n"
        "Give a binary score 'yes' or 'no'. 'yes' means the answer is grounded "
        "in / supported by the set of facts."
    )

    hallucination_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Set of facts:\n\n{documents}\n\nLLM generation:\n{generation}"),
        ]
    )

    hallucination_grader: RunnableSequence = hallucination_prompt | structured_llm_grader
else:
    hallucination_grader = _OfflineHallucinationGrader()