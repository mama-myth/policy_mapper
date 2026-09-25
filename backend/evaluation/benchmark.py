import json
from pathlib import Path
from backend.services.analysis_service import analysis_service

EVAL_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "evaluation" / "test_cases.json"


def run_benchmark():
    if not EVAL_DATA_PATH.exists():
        raise FileNotFoundError(f"Evaluation dataset not found at {EVAL_DATA_PATH}")

    with open(EVAL_DATA_PATH, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    tp = 0
    fp = 0
    fn = 0
    tn = 0
    correct_policy_mappings = 0
    traceability_complete_count = 0

    for tc in test_cases:
        expected_findings = tc["expected_finding_count"]
        expected_policy_id = tc["expected_policy_id"]
        code = tc["code"]

        response = analysis_service.analyze_code(code, f"{tc['id']}.py")
        actual_findings_count = len(response.findings)

        if expected_findings > 0:
            if actual_findings_count > 0:
                tp += 1
                finding = response.findings[0]
                if finding.policy_reference.id == expected_policy_id:
                    correct_policy_mappings += 1
                if finding.traceability and finding.traceability.code_to_pattern and finding.traceability.policy_to_context:
                    traceability_complete_count += 1
            else:
                fn += 1
        else:
            if actual_findings_count > 0:
                fp += 1
            else:
                tn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    mapping_accuracy = correct_policy_mappings / tp if tp > 0 else 1.0
    traceability_completeness = traceability_complete_count / tp if tp > 0 else 1.0

    results = {
        "total_test_cases": len(test_cases),
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "policy_mapping_accuracy": round(mapping_accuracy, 4),
        "traceability_completeness": round(traceability_completeness, 4)
    }

    return results


if __name__ == "__main__":
    metrics = run_benchmark()
    print(json.dumps(metrics, indent=2))
