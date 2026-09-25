import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_post_analyze_unsafe_credential_logging():
    payload = {
        "language":
        "python",
        "file_name":
        "auth.py",
        "code":
        "def login(user, password):\n    logger.info('User login %s password %s', user, password)\n"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "findings" in data
    assert len(data["findings"]) == 1

    finding = data["findings"][0]
    assert finding["policy_reference"]["id"] == "SEC-LOG-001"
    assert finding["code_evidence"]["sensitive_identifier"] == "password"
    assert finding["supporting_regulatory_context"][0][
        "framework"] == "GDPR"
    assert finding["supporting_regulatory_context"][0][
        "article"] == "Article 32"


def test_post_analyze_safe_logging():
    payload = {
        "language": "python",
        "file_name": "safe.py",
        "code": "logger.info('Process completed for user_id=%s', user_id)"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["findings"]) == 0


def test_post_analyze_unsupported_language_error():
    payload = {
        "language": "javascript",
        "file_name": "app.js",
        "code": "console.log(password)"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["error"] == "UnsupportedLanguage"


def test_post_analyze_empty_code_error():
    payload = {"language": "python", "file_name": "empty.py", "code": "   "}
    response = client.post("/analyze", json=payload)
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["error"] == "EmptyCode"


def test_post_analyze_syntax_error():
    payload = {
        "language": "python",
        "file_name": "invalid.py",
        "code": "def invalid_func(:"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["error"] == "SyntaxError"
