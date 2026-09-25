import pytest
from backend.llm.explanation_service import format_explanation


def test_llm_explanation_fallback_when_disabled():
    finding = {
        "policy_reference": {"id": "SEC-LOG-001", "title": "Sensitive Data Must Not Be Logged"},
        "code_evidence": {
            "function_called": "logger.info",
            "sensitive_identifier": "password",
            "snippet": "logger.info(password)"
        },
        "why_this_matters": "Credentials in logs can be exposed.",
        "recommended_action": "Remove password from log statement."
    }

    result = format_explanation(finding, "Passwords must not be logged.", "GDPR Article 32")
    assert result["llm_used"] is False
    assert result["why_this_matters"] == "Credentials in logs can be exposed."
    assert result["recommended_action"] == "Remove password from log statement."
