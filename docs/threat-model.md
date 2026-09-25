# Threat Model & Security Considerations — Policy-to-Code Mapper

## 1. Overview & System Scope
Policy-to-Code Mapper is a local-first developer guidance assistant operating inside Visual Studio Code and a local FastAPI backend. This document outlines the threat model, privacy guarantees, trust boundaries, and safety safeguards.

---

## 2. Assets & Trust Boundaries

### Key Assets
- **Developer Source Code:** Application source files edited inside the IDE.
- **Policy Knowledge Base:** Curated JSON policy rules (`SEC-LOG-001`, `SEC-LOG-002`).
- **Developer Feedback & Telemetry:** Local action logs (`helpful`, `not_helpful`, `dismiss`).

### Trust Boundaries
- **IDE ↔ Local Backend:** HTTP communication over loopback adapter (`127.0.0.1:8000`).
- **Local Environment ↔ Cloud Services:** External LLM integration (disabled by default).

---

## 3. Threat Matrix & Mitigation Strategies

| Threat Scenario | Risk Level | Mitigation Strategy |
| :--- | :--- | :--- |
| **Code Exfiltration via LLM** | High | LLM is disabled by default (`LLM_ENABLED=false`). Local AST analysis processes source code entirely on loopback. |
| **False Sense of Legal Compliance** | Medium | System messaging explicitly uses advisory language and displays non-legal disclaimers on every finding. |
| **Malicious Code Parsing Exploits** | Medium | Built-in Python `ast` module parses code safely without evaluating or executing `eval()` / `exec()`. |
| **Developer Fatigue / Intrusiveness** | Medium | Guidance is non-blocking (warning diagnostics and hovers). No build or git commit gates are enforced. |
| **Telemetry & Code Leaks** | Low | Feedback and analysis results are kept 100% local; zero external telemetry endpoints exist. |

---

## 4. Privacy-First Guarantees
- **No Cloud Uploads:** Code never leaves the developer's machine during default operation.
- **Fail-Safe Fallback:** If LLM features are enabled and fail or timeout, the system reverts immediately to local deterministic templates.
