# Research Methodology: Policy-to-Code Mapper

## 1. Research Objective & Context
Modern DevSecOps practices emphasize "shifting security left," but organizational governance, risk, and compliance (GRC) policies frequently remain isolated from daily software engineering workflows. Security policies are typically hosted in static repositories or GRC platforms that developers rarely consult while writing code.

**Policy-to-Code Mapper** investigates a human-centered security hypothesis:
> *Providing contextual, non-blocking policy guidance directly in the IDE at the moment code is written increases developer policy awareness and encourages safer coding choices without harming developer productivity or trust.*

---

## 2. Theoretical Framework: Behavioral Intervention in IDEs
The design of Policy-to-Code Mapper is grounded in developer experience (DevEx) and human-centered security research:

1. **Point-of-Action Intervention:** Interventions are most effective when delivered at the exact moment of decision-making rather than deferred to pull request reviews or post-commit security scans.
2. **Advisory, Non-Blocking Design:** Rigid blocking mechanisms generate developer frustration, leading to bypasses or disabled security tools. Policy-to-Code Mapper uses advisory warnings (`Warning` severity) that preserve developer autonomy.
3. **Transparent Traceability:** Developer trust requires explainability. Every policy guidance item explicitly links source code evidence to internal policies, risk justifications, and supporting regulatory references.
4. **Actionable Remediation:** Guidance includes concrete, safer implementation examples to reduce the cognitive burden on developers attempting to fix identified issues.

---

## 3. Disambiguation: Policy Guidance vs. Compliance Certification
Policy-to-Code Mapper is strictly an **educational and policy-awareness assistant**. It explicitly avoids declaring code as legally compliant or non-compliant.

| Dimension | Policy-to-Code Mapper (This Tool) | Traditional Legal/Compliance Tool |
| :--- | :--- | :--- |
| **Primary Goal** | Developer policy awareness & behavioral nudging | Formal legal risk audit or certification |
| **Output Wording** | "Potential policy consideration", "Consider whether..." | "Non-compliant", "Legal violation", "Illegal code" |
| **Enforcement** | Non-blocking IDE advice | Gating / Build failure / Legal determination |
| **Scope** | Local code context & developer guidance | Organizational legal liability assessment |

---

## 4. Evaluative Design & Usability Metrics
The prototype evaluates behavioral intervention efficacy across five key dimensions:
- **Clarity:** Is the policy explanation understandable to developers?
- **Actionability:** Does the safer example enable immediate remediation?
- **Intrusiveness:** Does the guidance disrupt coding flow?
- **Trust:** Is the policy mapping perceived as accurate and relevant?
- **Traceability:** Does linking internal policies to regulatory contexts improve understanding?
