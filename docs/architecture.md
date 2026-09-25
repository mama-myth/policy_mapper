# System Architecture: Policy-to-Code Mapper

## 1. Local-First Architecture Overview
Policy-to-Code Mapper is designed as an extension-first, local IDE assistant. All detection logic, policy mapping, hover guidance rendering, diagnostics, and local state management run entirely within the VS Code Extension Host process.

```mermaid
graph TD
    subgraph VS Code IDE
        DEV[Developer Writes Code] -->|Edits Python File| VS_EDITOR[VS Code Active Editor]

        subgraph Policy-to-Code Mapper Extension
            VS_EDITOR -->|Invoke Analysis / On Edit| DETECTOR[Code-Context Detector]

            subgraph Extension Core
                DETECTOR -->|Detected Context| MATCHER[Policy Matcher]
                POLICY_STORE[(Local Policy KB JSON)] -->|Load Policies| MATCHER
                MATCHER -->|Guidance Model| BUILDER[Guidance & Traceability Builder]
            end

            BUILDER -->|Diagnostics Warnings| DIAG[VS Code Diagnostics API]
            BUILDER -->|Hover Cards| HOVER[VS Code Hover Provider]
            BUILDER -->|Sidebar Items| TREEVIEW[VS Code Activity Bar TreeView]
            BUILDER -->|Full Guidance Detail| WEBVIEW[Webview Panel / Traceability View]

            FEEDBACK[User Action: Helpful/Dismiss] -->|Store Feedback| LOCAL_STATE[(VS Code Workspace/Global State)]
        end

        DIAG -->|Yellow Underline| DEV
        HOVER -->|Advisory Guidance| DEV
        TREEVIEW -->|Active Policy List| DEV
    end
```

---

## 2. Component Descriptions

### A. Code-Context Detector (`src/analyzer/`)
- Evaluates active Python file buffers for target logging and output function calls (`print`, `logging.*`, `logger.*`).
- Inspects function parameters and line expressions against sensitive variable/identifier names (`password`, `token`, `api_key`, `email`, etc.).
- Produces structured `DetectedCodeContext` instances detailing line numbers, code snippets, matched identifiers, and function names.

### B. Local Policy Knowledge Base (`src/policies/`)
- Maintained as local JSON (`resources/policies.json`).
- Stores curated organizational policies containing policy IDs, descriptions, risk explanations, mapped sensitive identifiers, suggested actions, safer code examples, and supporting regulatory references (e.g., GDPR Article 32).

### C. Guidance & Traceability Builder (`src/guidance/`)
- Maps detected code contexts to relevant policy records.
- Constructs structured `GuidanceItem` objects including potential considerations, policy citations, explanation, regulatory references, safer code examples, and standard advisory disclaimers.
- Generates full traceability chains connecting `Source Code Evidence → Observed Pattern → Internal Policy → Regulatory Context → Suggested Action`.

### D. User Interface & Presentation Layer (`src/views/` & `src/guidance/`)
- **Diagnostics Provider:** Underlines policy-relevant lines in yellow (warning severity).
- **Hover Provider:** Displays formatted Markdown popups containing full advisory guidance on hover.
- **Activity Bar View:** Hosts an "Active Policy Guidance" tree view listing all findings in the workspace.
- **Traceability / Details View:** Interactive panel showing end-to-end policy traceability and safe code examples.

### E. Local Feedback Store (`src/feedback/`)
- Captures developer feedback (e.g., "Helpful", "Not helpful", "Dismiss") locally using VS Code's `globalState` or `workspaceState`.
- Does not collect personal data or transmit feedback externally.

---

## 3. Data Isolation & Privacy Guarantee
- **Zero External Egress:** Source code and telemetry never leave the local machine.
- **No Cloud Dependencies:** Operates without mandatory API keys, external cloud backends, LLMs, or remote vector stores.
