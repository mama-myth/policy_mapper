import pytest
from backend.rag.retrieval import retrieve_policy_context


def test_rag_retrieval_credential_logging():
    results = retrieve_policy_context("sensitive_value_passed_to_logging_function", "password")
    assert len(results) >= 1
    top_policy = results[0]["policy"]
    assert top_policy.id == "SEC-LOG-001"


def test_rag_retrieval_email_logging():
    results = retrieve_policy_context("sensitive_value_passed_to_logging_function", "email")
    assert len(results) >= 1
    policy_ids = [r["policy_id"] for r in results]
    assert "SEC-LOG-002" in policy_ids or "SEC-LOG-001" in policy_ids
