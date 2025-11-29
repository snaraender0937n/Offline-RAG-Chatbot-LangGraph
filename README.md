## 🔹 Project Highlights

- Designed and implemented a **Retrieval-Augmented Generation (RAG)** workflow using **LangGraph**, modeling the complete question–answering pipeline.
- Built a **stateful, multi-step graph** incorporating question routing, document retrieval, relevance grading, answer generation, and hallucination checking.
- Structured the project with clear separation of concerns using a modular `graph/` architecture (chains, nodes, state, constants).
- Implemented a **self-reflection / hallucination grading step** at the design level to ensure generated answers are grounded in retrieved context.
- Developed a **robust CLI and demo interface** with clear execution traces and error handling for easy inspection and debugging.
- Created an **offline-first implementation** that runs without API keys, returning dummy responses while still exercising the full LangGraph workflow.
- Designed the system to be easily extensible for real LLMs, vector databases, and web search once API keys are configured.

---

## 🎯 Purpose of the Project

This project implements a **Retrieval-Augmented Generation (RAG) chatbot workflow** using LangGraph.  
The primary purpose is to design and demonstrate a structured, stateful question-answering pipeline that can retrieve documentation, evaluate relevance, generate answers, and validate responses to reduce hallucinations.

The project is built as an **offline-first system**, allowing it to run without external API keys. While the current version uses dummy responses, the architecture fully supports future integration with real Large Language Models, vector databases, and web search APIs.

---

## 📄 Abstract

This project presents a LangGraph-based RAG chatbot that models the end-to-end flow of document-based question answering. The workflow consists of multiple stages, including routing, retrieval, relevance grading, answer generation, and hallucination checking. Each stage is implemented as a separate node or chain in a stateful graph, enabling clear traceability and controlled execution.

The system emphasizes clean architecture, robustness, and explainability. By supporting an offline-first mode, the project can be evaluated, demonstrated, and extended without reliance on external services, while remaining ready for full online deployment when required.