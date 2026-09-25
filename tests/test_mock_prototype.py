import json
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
ROOT_DIR = Path(__file__).parent.parent


def test_policies_json_validity():
    policy_file = ROOT_DIR / "backend" / "data" / "policies.json"
    assert policy_file.exists()
    with open(policy_file, "r", encoding="utf-8") as f:
        policies = json.load(f)
    assert isinstance(policies, list)
    assert len(policies) >= 1
    sec_log_001 = next((p for p in policies if p["id"] == "SEC-LOG-001"), None)
    assert sec_log_001 is not None
    assert sec_log_001["title"] == "Sensitive Data Must Not Be Logged"


def test_mock_analysis_endpoint():
    response = client.get("/mock-analysis")
    assert response.status_code == 200
    data = response.json()
    assert "findings" in data
    assert len(data["findings"]) == 1
    finding = data["findings"][0]
    assert finding["policy_reference"]["id"] == "SEC-LOG-001"
    assert finding["guidance_type"] == "policy_awareness"


def test_mock_guidance_endpoint():
    response = client.get("/mock-guidance")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    html = response.text
    assert "Policy-to-Code Guidance" in html
    assert "SEC-LOG-001" in html
    assert "GDPR" in html
    assert "Advisory" in html
