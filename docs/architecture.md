# Architecture Documentation — Policy-to-Code Mapper

## 1. System Overview
Policy-to-Code Mapper is designed as a local, lightweight, context-aware developer guidance assistant. It follows a multi-tiered decoupled architecture where the developer interface (VS Code Extension) communicates with a local FastAPI analysis backend.

## 2. Target Architecture Diagram

```mermaid
flowchart TD
    subgraph IDE ["Visual Studio Code IDE"]
        UI["VS Code Extension UI\n(Diagnostics API + Hover + Traceability View)"]
        Trigger["Command / File Event Trigger"]
    end

    subgraph Backend ["Local FastAPI Service"]
        API["FastAPI REST Endpoints\n(/health, /analyze)"]

        subgraph Pipeline ["Analysis & Guidance Pipeline"]
            AST["Python AST Analyzer\n(Deterministic Pattern Detection)"]
            Mapper["Policy Mapper\n(JSON Policy Knowledge Base)"]
            RAG["Optional Vector Store / RAG\n(ChromaDB + SentenceTransformers)"]
            LLM["Optional Explanation Layer\n(OpenAI API / Local LLM - Disabled by default)"]
        end
    end

    subgraph Knowledge ["Policy Data"]
        KB["Curated Policies (JSON)\nSEC-LOG-001 / SEC-LOG-002"]
        GDPR["Supporting Regulatory Context\nGDPR Article 32 / Article 5"]
    end

    Trigger --> UI
    UI -->|HTTP POST /analyze| API
    API --> AST
    AST -->|Observed Pattern| Mapper
    KB --> Mapper
    GDPR --> KB
    Mapper -->|Mapped Guidance| API
    RAG -.->|Semantic Retrieval (Optional)| Pipeline
    LLM -.->|Explanation Formatting (Optional)| Pipeline
    API -->|Structured JSON Finding| UI
    UI -->|Display Non-Blocking Hover & Diagnostics| Developer["Developer Decision-Making"]
```

## 3. Data Flow & Conceptual Chain

1. **Source Code Evidence:**
   The developer writes code containing a pattern (e.g. `logger.info("Password: %s", password)`).
2. **AST Analysis:**
   The Python AST analyzer parses the syntax tree deterministically to identify function calls (`logger.info`) and sensitive variable identifiers (`password`).
3. **Policy Mapping:**
   The observed pattern is mapped to internal policy record `SEC-LOG-001` (Sensitive Data Must Not Be Logged).
4. **Context Association:**
   The policy references supporting regulatory framework details (GDPR Article 32 — Security of processing).
5. **Structured Guidance Output:**
   The FastAPI backend generates a structured JSON response containing findings, explanation, recommended action, safer code example, and full traceability.
6. **Point-of-Action UX:**
   VS Code displays an advisory warning diagnostic with hover details and full traceability options without blocking code execution, saving, or commits.

## 4. Security & Privacy Guarantees
- **Local Processing:** By default, code remains strictly on the developer's machine and is evaluated by the local AST engine.
- **Privacy-First Design:** No cloud LLM dependencies are enabled by default.
- **Strict Legal Separation:** Policy guidance is advisory and educational; the system explicitly avoids legal terms such as "non-compliant", "illegal", or "violation".
