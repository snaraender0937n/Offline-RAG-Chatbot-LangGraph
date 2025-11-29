from __future__ import annotations

import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()

OPENAI_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""
    datasource: Literal["vectorstore", "websearch"] = Field(
        description="Route decision for the user query"
    )


class _OfflineQuestionRouter:
    """
    Offline dummy router.

    Mimics LangChain runnable behavior and always routes
    to vectorstore (safe default for offline mode).
    """

    def invoke(self, inputs: dict) -> RouteQuery:
        return RouteQuery(datasource="vectorstore")


if OPENAI_AVAILABLE:
    from langchain_openai import ChatOpenAI
    from langchain_core.runnables import RunnableSequence

    llm = ChatOpenAI(model="gpt-4", temperature=0)
    structured_llm_router = llm.with_structured_output(RouteQuery)

    system = (
        "You are an expert at routing a user question to a vectorstore or web search.\n"
        "The vectorstore contains documents related to agents, prompt engineering, "
        "and adversarial attacks.\n"
        "Use the vectorstore for questions on those topics. "
        "For all other questions, use websearch."
    )

    route_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{question}"),
        ]
    )

    question_router: RunnableSequence = route_prompt | structured_llm_router
else:
    # Offline fallback
    question_router = _OfflineQuestionRouter()