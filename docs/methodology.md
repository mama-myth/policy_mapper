# Research Methodology — Policy-to-Code Mapper

## 1. Primary Research Objectives
Policy-to-Code Mapper investigates the effectiveness of **point-of-action policy interventions** in software development. The central hypothesis is that presenting contextual, traceable, non-blocking policy guidance directly inside the IDE at the time of code creation reduces security risks (such as sensitive data logging) compared to traditional post-hoc security audits or disconnected documentation.

## 2. Intended Target Users
- **Primary Users:** Software developers writing Python code in Visual Studio Code.
- **Secondary Stakeholders:** Security engineers, DevSecOps leads, and GRC professionals seeking transparent policy adoption without degrading developer velocity.

## 3. Core Intervention Mechanism
The intervention operates on five key human-centered principles:
1. **Advisory & Educational:** Guidance is supportive and educational rather than punitive or blocking.
2. **Contextual Timeliness:** Information is delivered at the exact point of action (inside the IDE diagnostic/hover UI).
3. **Explainable Traceability:** Every prompt establishes a transparent chain:
   $$\text{Code Evidence} \rightarrow \text{Observed Pattern} \rightarrow \text{Internal Policy} \rightarrow \text{Supporting Regulation} \rightarrow \text{Actionable Suggestion}$$
4. **Developer Autonomy:** Developers retain full authority to dismiss guidance, view details, or follow suggested safe alternatives.
5. **Zero Friction:** Non-blocking diagnostics ensure building, committing, and saving code are never interrupted.

## 4. Policy-to-Code Traceability Model
To prevent "black-box" warnings, each finding produced by the system includes explicit traceability fields:
- `code_to_pattern`: Explains how the AST detected the specific variable/call combination.
- `pattern_to_policy`: Identifies the exact internal security policy requirement (`SEC-LOG-001`).
- `policy_to_context`: Links the policy requirement to relevant supporting regulatory context (e.g., GDPR Article 32).

## 5. Evaluation Strategy
The prototype's effectiveness and usability will be evaluated through a two-fold approach:
1. **Technical Precision & Recall:** Benchmark against a curated dataset of positive, negative, safe, and ambiguous code snippets to evaluate detection accuracy and false-positive rates.
2. **Human-Centered Usability Evaluation:** User feedback surveys assessing:
   - Perceived usefulness and clarity of policy guidance.
   - Developer trust and perceived non-intrusiveness.
   - Learning impact regarding secure logging practices.
