import pytest
from backend.analyzer.logging_detector import detect_sensitive_logging


def test_positive_credential_logging():
    code = """
def login(username, password):
    logger.info("User login with password %s", password)
"""
    result = detect_sensitive_logging(code, "auth.py")
    assert "error" not in result
    patterns = result["patterns"]
    assert len(patterns) == 1
    assert patterns[0]["function_called"] == "logger.info"
    assert patterns[0]["sensitive_identifier"] == "password"
    assert patterns[0]["line_start"] == 3


def test_positive_api_key_logging():
    code = """
import logging

def fetch_data(api_key):
    print("Connecting using key:", api_key)
"""
    result = detect_sensitive_logging(code, "api.py")
    patterns = result["patterns"]
    assert len(patterns) == 1
    assert patterns[0]["function_called"] == "print"
    assert patterns[0]["sensitive_identifier"] == "api_key"


def test_positive_token_attribute_logging():
    code = """
def authenticate(request):
    logging.warning("Failed auth for token %s", request.access_token)
"""
    result = detect_sensitive_logging(code, "auth.py")
    patterns = result["patterns"]
    assert len(patterns) == 1
    assert patterns[0]["function_called"] == "logging.warning"
    assert patterns[0]["sensitive_identifier"] == "request.access_token"


def test_safe_logging():
    code = """
def login(username, user_id):
    logger.info("User login attempt for user_id=%s", user_id)
"""
    result = detect_sensitive_logging(code, "safe.py")
    assert len(result["patterns"]) == 0


def test_sensitive_variable_used_without_logging():
    code = """
def hash_pass(password):
    hashed = make_hash(password)
    return hashed
"""
    result = detect_sensitive_logging(code, "hash.py")
    assert len(result["patterns"]) == 0


test_benign_variable_containing_substring = """
def process():
    logger.info("Processing complete")
    category = "general_announcement"
    print(category)
"""


def test_benign_substring_not_flagged():
    result = detect_sensitive_logging(
        test_benign_variable_containing_substring, "benign.py")
    assert len(result["patterns"]) == 0


def test_invalid_python_syntax():
    code = "def invalid_func(:"
    result = detect_sensitive_logging(code, "invalid.py")
    assert "error" in result
    assert result["error"]["error"] == "SyntaxError"
