import pytest
from backend.policies.policy_mapper import policy_mapper


def test_map_credential_identifier_to_sec_log_001():
    policy = policy_mapper.map_pattern_to_policy(
        "sensitive_value_passed_to_logging_function", "password")
    assert policy is not None
    assert policy.id == "SEC-LOG-001"
    assert policy.title == "Sensitive Data Must Not Be Logged"


def test_map_api_key_identifier_to_sec_log_001():
    policy = policy_mapper.map_pattern_to_policy(
        "sensitive_value_passed_to_logging_function", "request.api_key")
    assert policy is not None
    assert policy.id == "SEC-LOG-001"


def test_map_email_identifier_to_sec_log_002():
    policy = policy_mapper.map_pattern_to_policy(
        "sensitive_value_passed_to_logging_function", "user.email")
    assert policy is not None
    assert policy.id == "SEC-LOG-002"
    assert policy.title == "Personal Data in Logs Must Be Minimized"
