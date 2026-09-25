import pytest
from backend.services.analysis_service import analysis_service


def test_guidance_service_generation_for_credential_logging():
    code = """
def login(username, password):
    logger.info("Login for username=%s password=%s", username, password)
"""
    response = analysis_service.analyze_code(code, "auth.py")
    assert response.file_name == "auth.py"
    assert len(response.findings) == 1

    finding = response.findings[0]
    assert finding.policy_reference.id == "SEC-LOG-001"
    assert finding.severity == "high"
    assert finding.code_evidence.sensitive_identifier == "password"
    assert "GDPR" in finding.supporting_regulatory_context[0].framework
    assert "Article 32" in finding.supporting_regulatory_context[0].article
    assert "password → logger.info()" in finding.traceability.code_to_pattern
    assert "SEC-LOG-001 → GDPR Article 32" in finding.traceability.policy_to_context
    assert "automated developer guidance" in finding.disclaimer.lower()


def test_guidance_service_generation_for_personal_data_logging():
    code = """
def process_user(user):
    logger.info("User registered email: %s", user.email)
"""
    response = analysis_service.analyze_code(code, "user.py")
    assert len(response.findings) == 1

    finding = response.findings[0]
    assert finding.policy_reference.id == "SEC-LOG-002"
    assert finding.severity == "medium"
    assert "Article 5(1)(c)" in finding.supporting_regulatory_context[
        0].article
