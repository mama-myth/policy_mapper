# Policy-to-Code Mapper: A Context-Aware IDE Assistant for Real-Time Security and Policy Guidance

## 1. Project Purpose
**Policy-to-Code Mapper** is an IDE-based developer guidance system that brings relevant organizational security policies and selected regulatory context directly into the software development workflow. By acting as a behavioral intervention at the point of action, the system surfaces contextual, traceable, non-blocking policy guidance when developers encounter code patterns relevant to security or privacy policies.

## 2. Problem Statement
Security, privacy, and compliance policies are often trapped in lengthy PDFs, intranet wikis, or enterprise GRC tools. Developers rarely consult these documents while writing code due to search friction, non-developer-friendly policy phrasing, separation from the IDE, and high delivery pressure. Policy-to-Code Mapper bridges this gap by delivering timely, context-aware guidance right where developers make coding decisions ("shift-left policy awareness").

## 3. Core User Scenario
While editing a Python file in VS Code, a developer writes:
```python
def login(username, password):
    logger.info("Login attempt for %s with password %s", username, password)
```
Policy-to-Code Mapper identifies this sensitive logging pattern and displays advisory, non-blocking guidance in the IDE:
- **Potential Consideration:** Password credential passed to logger.
- **Relevant Policy:** `SEC-LOG-001 — Sensitive Data Must Not Be Logged`.
- **Why It Matters:** Credentials in logs can be exposed through log aggregators, error monitoring tools, or backups.
- **Supporting Regulatory Context:** GDPR Article 32 — Security of processing.
- **Suggested Developer Action:** Remove the password from the log message. Log only a non-sensitive event or masked identifier.

## 4. Research Contribution
The primary contribution of Policy-to-Code Mapper is human-centered security and developer behavioral intervention. It emphasizes:
- **Developer Awareness:** Introducing policy context in real time.
- **Explainability & Traceability:** Linking source code evidence directly to policy rules, regulatory context, and recommendations.
- **Low-Friction Autonomy:** Providing non-blocking hover warnings and quick actionable suggestions without forcing rigid blocking gates.

## 5. Non-Goals & Explicit Boundaries
To ensure strict scope boundaries and clear legal limits, Policy-to-Code Mapper **is NOT**:
- A legal-compliance certification product.
- A GDPR compliance checker or legal audit tool.
- A system that declares code legal/illegal or an organization compliant/non-compliant.
- A legal-advice tool or replacement for legal/compliance/security professionals.

## 6. Scope
- **Initial Language:** Python 3.12+
- **Initial IDE:** Visual Studio Code
- **Initial Policy Domain:** Secure logging (`SEC-LOG-001`: Sensitive Data Must Not Be Logged)
- **Code Contexts:** Built-in `print()` and standard Python `logging` / `logger` methods.

## 7. Technology Stack
- **Backend Framework:** Python 3.12+, FastAPI, Uvicorn, Pydantic v2
- **Code Analysis:** Python built-in `ast` module (deterministic AST analysis)
- **Testing:** `pytest`, `httpx`
- **IDE Extension:** VS Code Extension API (TypeScript, Diagnostics API, Hover Provider)
- **Optional Extensions:** Sentence-Transformers & ChromaDB for semantic RAG; optional local/OpenAI LLM for explanation formatting (disabled by default).

## 8. Safety & Legal Disclaimer
> **Disclaimer:** Policy-to-Code Mapper provides automated technical guidance and developer education only. It does not provide legal advice, legal assessments, or formal compliance certification.

## 9. Phased Roadmap
- **Phase 0:** Research Prototype Plan and Foundation *(Current)*
- **Phase 1:** Mock Policy Guidance Prototype
- **Phase 2:** Deterministic Python Code-Context Detection
- **Phase 3:** Policy-to-Code Mapping and Guidance Generation
- **Phase 4:** FastAPI Backend and Structured API
- **Phase 5:** VS Code Extension Point-of-Action Guidance
- **Phase 6:** Optional RAG and LLM Explanation Layer
- **Phase 7:** Developer Feedback and Behavioral Evaluation
- **Phase 8:** Final Documentation and Presentation Package
