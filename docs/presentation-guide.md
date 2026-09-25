# Final Presentation Outline & Viva / Interview Guide — Policy-to-Code Mapper

## 1. Presentation Outline (10-Minute Technical Briefing)

### Slide 1: Introduction & Domain
- **Title:** Policy-to-Code Mapper: A Context-Aware IDE Assistant for Real-Time Security and Policy Guidance
- **Domain:** DevSecOps, Governance, Risk and Compliance (GRC), Human-Centered Security, AI-Assisted Development.

### Slide 2: Problem Statement
- Security and compliance policies trapped in intranet wikis or long PDFs.
- Developers rarely consult policies during active coding due to search friction and pressure.
- Shift-left policy awareness: Surfacing guidance at the **point of action**.

### Slide 3: Core Contribution & Non-Goals
- **Contribution:** Real-time, traceable, advisory guidance in VS Code when sensitive coding patterns occur.
- **Strict Non-Goals:** NOT a legal audit tool, NOT a GDPR compliance checker, does NOT declare code legal/illegal.

### Slide 4: Target System Architecture
- VS Code Extension (TypeScript) ➔ FastAPI Backend (Python AST) ➔ Curated Policy KB (JSON) ➔ Traceable Hover Guidance.

### Slide 5: Point-of-Action Developer Workflow
- Demonstration of `logger.info("Pass: %s", password)` trigger, diagnostic warning, hover policy card, and traceability chain.

### Slide 6: Evaluation & Results
- Benchmark precision, recall, and F1 score on test dataset.
- Exploratory developer usability study design.

---

## 2. Viva / Interview Questions & Concise Answers

### Q1: Why build an AST-based analyzer instead of relying entirely on an LLM?
**Answer:**
> "AST analysis is deterministic, fast, runs 100% locally with zero cloud privacy risk, and guarantees zero false positives from comments or strings. In our architecture, AST is the primary trigger, while LLM/RAG is strictly an optional layer for explanation formatting."

### Q2: How does Policy-to-Code Mapper avoid making unsupported legal claims?
**Answer:**
> "Every finding uses advisory language ('Potential policy consideration', 'Suggested developer action'), explicitly presents GDPR Article 32 as supporting context rather than a legal conclusion, and includes a mandatory disclaimer stating it is technical guidance, not legal advice."

### Q3: How does the system balance security awareness with developer velocity?
**Answer:**
> "Guidance is non-blocking. Warnings appear as subtle diagnostics and hovers without interrupting builds, saves, or git commits. Developers retain full autonomy to inspect safer code examples or dismiss prompts."
