# Policy-to-Code Mapper: A Context-Aware VS Code Extension for Real-Time Security and Policy Guidance

> **Research Prototype** | *Governance, Risk and Compliance (GRC) • DevSecOps • Human-Centered Security • Developer Experience*

---

## 1. Project Objective & Identity
**Policy-to-Code Mapper** is a native Visual Studio Code extension built in TypeScript that brings relevant organizational security policies and supporting regulatory context directly into the developer's coding environment. Operating as a local-first behavioral intervention, the extension detects policy-relevant code patterns in real time and presents context-aware, traceable, non-blocking guidance at the point of action.

### Primary Artifact
The primary artifact of this project is the **native VS Code extension**. The extension functions entirely locally in VS Code without requiring external cloud services, API endpoints, LLMs, or vector databases.

---

## 2. Problem Statement
Security, privacy, and compliance requirements are traditionally maintained in static PDF documents, intranet pages, spreadsheet matrices, or GRC ticketing platforms. Developers rarely consult these disconnected sources during daily coding due to workflow friction, search cost, non-actionable legal phrasing, and pressure to deliver.

Consequently, policy awareness arrives too late—often during code review, security audits, penetration testing, or after security incidents. Policy-to-Code Mapper bridges this operational gap by embedding non-intrusive policy guidance into the IDE as code is being written ("shift-left policy awareness").

---

## 3. Guiding Principles & Core Workflow
The system operates on the core principle:
> **Code analysis is the trigger. Policy guidance is the product. Developer understanding is the desired outcome.**

### Core User Scenario
1. **Developer writes code:**
   ```python
   def login(username, password):
       logger.info("Login attempt for %s with password %s", username, password)
   ```
2. **Extension detects context:** Identifies sensitive credential logging pattern.
3. **Presents policy guidance:**
   - **Potential Policy Consideration:** Sensitive credential logging detected.
   - **Relevant Policy:** `SEC-LOG-001 — Sensitive Data Must Not Be Logged`
   - **Why It Matters:** Unmasked credentials in logs risk exposure in log aggregators, monitoring tools, or backups.
   - **Supporting Regulatory Context:** GDPR Article 32 (Security of processing).
   - **Suggested Action:** Remove the password from the log statement; log non-sensitive operational metadata instead.
   - **Safer Implementation:** `logger.info("Login attempt received for user_id=%s", user_id)`
4. **Developer remains in control:** The warning is advisory and non-blocking, allowing full developer autonomy.

---

## 4. Scope (Initial Research Prototype)
- **Target IDE:** Visual Studio Code (Extension API)
- **Programming Language:** Python (`.py`)
- **Policy Focus:** Secure logging and privacy-aware data minimization
  - `SEC-LOG-001`: Sensitive Data Must Not Be Logged
  - `SEC-LOG-002`: Personal Data in Logs Must Be Minimized
- **Supported Contexts:** `print()`, `logging.*()`, `logger.*()`
- **Operation:** Local TypeScript pattern detection and JSON policy store.

---

## 5. Non-Goals & Safety Disclaimer
To establish clear legal and operational boundaries:
- **NOT a Legal Compliance Engine:** The extension does not certify legal compliance or declare code "legal" or "illegal".
- **NOT a Blocking Linter:** The system does not prevent compiling, saving, building, or committing code.
- **NOT an External SAAS:** The extension operates locally and does not transmit source code externally.

> **Safety Disclaimer:**
> *Policy-to-Code Mapper provides automated developer guidance and policy awareness for educational and security research purposes only. It does not provide legal advice, formal compliance determinations, or legal status certifications.*

---

## 6. Technology Stack
- **Language & Runtime:** TypeScript, Node.js LTS
- **IDE Framework:** VS Code Extension API
- **Data Model:** Local JSON Policy Records (`resources/policies.json`)
- **Package Manager:** `npm`
- **Build System:** `tsc` (TypeScript Compiler)
- **Documentation:** Markdown & Mermaid.js diagrams

---

## 7. Development Roadmap
- **Phase 0:** Extension Scaffold & Research Foundation *(Completed)*
- **Phase 1:** Local Policy Knowledge Base
- **Phase 2:** Analyze Current File Command
- **Phase 3:** Editor Diagnostics & Hover Guidance
- **Phase 4:** Policy-to-Code Sidebar & Traceability View
- **Phase 5:** Developer Feedback & Policy Awareness Evaluation
- **Phase 6:** Optional Advanced Enhancements
- **Phase 7:** Final Documentation & Demo Package
