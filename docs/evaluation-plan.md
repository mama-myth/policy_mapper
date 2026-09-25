# Evaluation & Usability Study Plan — Policy-to-Code Mapper

## 1. Evaluation Methodology Overview
Policy-to-Code Mapper evaluates both technical detection accuracy and human-centered developer experience using a mixed-methods research design:
1. **Technical Accuracy Benchmark:** Quantitative precision, recall, F1 score, policy-mapping accuracy, and traceability completeness on a curated evaluation dataset (`data/evaluation/test_cases.json`).
2. **Exploratory Usability Study:** Human-centered evaluation measuring clarity, usefulness, trust, perceived intrusiveness, and learning value among developers.

---

## 2. Technical Evaluation Benchmark Results

The automated benchmark tool (`backend/evaluation/benchmark.py`) evaluates the system against positive credential logging, positive personal data logging, safe operational logging, non-logging sensitive variable usage, and benign substrings:

```json
{
  "total_test_cases": 8,
  "true_positives": 4,
  "false_positives": 0,
  "true_negatives": 4,
  "false_negatives": 0,
  "precision": 1.0,
  "recall": 1.0,
  "f1_score": 1.0,
  "policy_mapping_accuracy": 1.0,
  "traceability_completeness": 1.0
}
```

---

## 3. Exploratory Usability Study Design

### Participants & Target Demographic
- **Sample Size:** 5–10 software developers or computer science students writing Python code.
- **Task Procedure:**
  1. Open a sample Python repository containing unsafe logging (`examples/unsafe_credential_logging.py`) in VS Code.
  2. Invoke `Policy-to-Code: Analyze Current File`.
  3. Inspect diagnostic warnings, hover cards, and safer code suggestions.
  4. Invoke `Policy-to-Code: View Traceability`.
  5. Provide feedback using IDE feedback actions (`Helpful` / `Not Helpful` / `Dismiss`).

### Likert Survey Metrics (1 = Strongly Disagree, 5 = Strongly Agree)
- **Clarity:** "The policy guidance clearly explained why the code pattern mattered."
- **Actionability:** "The suggested developer action and safer example were immediately useful."
- **Non-Intrusiveness:** "The guidance was non-blocking and did not interrupt my coding velocity."
- **Trust & Transparency:** "The traceability chain (Code ➔ Policy ➔ GDPR) helped me trust the recommendation."
- **Perceived Learning Value:** "I learned a secure logging principle that I will apply in future development."

---

## 4. Threats to Validity & Limitations
- **Sample Size:** The usability study is exploratory and designed for small qualitative feedback rather than large statistical conclusions.
- **Dataset Scope:** Benchmarks focus on secure logging (`SEC-LOG-001` and `SEC-LOG-002`) and Python language AST rules.
