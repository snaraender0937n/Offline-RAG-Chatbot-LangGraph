from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

OPENAI_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))


class _OfflineGenerationChain:
    """
    Offline dummy generation chain.

    Provides a .invoke(...) method so it can be used
    like a normal LangChain / LangGraph runnable.
    """

    def invoke(self, inputs: dict) -> str:
        question = inputs.get("question", "")
        # We ignore context in offline mode; this is just a placeholder.
        return (
            "[OFFLINE MODE] Dummy answer.\n"
            f"I received your question: '{question}'.\n"
            "Configure OPENAI_API_KEY to enable real answer generation."
        )


if OPENAI_AVAILABLE:
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4", temperature=0)

    # Custom RAG prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are an assistant for question-answering tasks. "
                    "Use the following pieces of retrieved context to answer the question. "
                    "If you don't know the answer, just say that you don't know. "
                    "Use three sentences maximum and keep the answer concise."
                ),
            ),
            (
                "human",
                "Question: {question}\nContext: {context}\nAnswer:",
            ),
        ]
    )

    # Real online generation chain
    generation_chain = prompt | llm | StrOutputParser()
else:
    # Offline dummy chain
    generation_chain = _OfflineGenerationChain()