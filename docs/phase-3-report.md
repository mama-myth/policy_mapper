# Phase 3 Visual Progression & Completion Report — Policy Mapping & Guidance Generation

## 1. Overview
In **Phase 3**, Policy-to-Code Mapper built the deterministic Policy Mapping engine and Guidance Generation service (`backend/policies/policy_mapper.py` and `backend/services/guidance_service.py`). This layer takes observed AST code patterns from Phase 2 and maps them to curated organizational policy rules (`SEC-LOG-001` and `SEC-LOG-002`) and supporting regulatory context (`GDPR Article 32` and `GDPR Article 5(1)(c)`).

---

## 2. End-to-End Traceability Chain Flow

```text
               1. SOURCE CODE EVIDENCE
  `logger.info("Login attempt with password %s", password)`
                          │
                          ▼
             2. OBSERVED CODE PATTERN (AST)
  sensitive_value_passed_to_logging_function (password -> logger.info)
                          │
                          ▼
             3. INTERNAL POLICY MAPPING
  SEC-LOG-001 — Sensitive Data Must Not Be Logged
                          │
                          ▼
            4. SUPPORTING REGULATORY CONTEXT
  GDPR Article 32 — Security of processing
                          │
                          ▼
          5. DEVELOPER-FACING ADVISORY GUIDANCE
  "Credentials in logs can be exposed through monitoring tools...
   Remove the password from the log message. Log only a non-sensitive event."
```

---

## 3. Sample Generated Structured Finding JSON Payload

When processing `examples/unsafe_credential_logging.py`, the Guidance Service generates:

```json
{
  "analysis_id": "c71a39f0-32b0-4fdf-9730-8a6210f13a30",
  "language": "python",
  "file_name": "unsafe_credential_logging.py",
  "findings": [
    {
      "finding_id": "8f8888b1-5e2a-4318-a664-df0a1969e46a",
      "guidance_type": "policy_awareness",
      "severity": "high",
      "title": "Potential sensitive credential logging",
      "potential_policy_consideration": "This code appears to pass sensitive attribute 'password' to output function 'logger.info'.",
      "code_evidence": {
        "line_start": 8,
        "line_end": 8,
        "function_called": "logger.info",
        "sensitive_identifier": "password",
        "snippet": "logger.info(\"Login attempt for %s with password %s\", username, password)"
      },
      "observed_pattern": "sensitive_value_passed_to_logging_function",
      "policy_reference": {
        "id": "SEC-LOG-001",
        "title": "Sensitive Data Must Not Be Logged",
        "category": "Secure Logging"
      },
      "supporting_regulatory_context": [
        {
          "framework": "GDPR",
          "article": "Article 32",
          "title": "Security of processing",
          "relationship": "supporting_security_context"
        }
      ],
      "why_this_matters": "Passwords, authentication tokens, API keys... must not be written to application logs.",
      "recommended_action": "Remove sensitive values from output statements.",
      "safer_example": "logger.info(\"Event processed for user_id=%s\", user_id)",
      "confidence": {
        "label": "high",
        "basis": "A deterministic AST rule detected a sensitive identifier passed to a recognized logging function."
      },
      "traceability": {
        "code_to_pattern": "password → logger.info()",
        "pattern_to_policy": "sensitive logging pattern → SEC-LOG-001",
        "policy_to_context": "SEC-LOG-001 → GDPR Article 32"
      },
      "disclaimer": "This is automated developer guidance, not legal advice or a legal-compliance determination."
    }
  ]
}
```

---

## 4. Test Suite Execution & Verification

All mapping, guidance generation, and regulatory attribution components were verified via `pytest`:

```text
============================= test session starts ==============================
rootdir: /app
configfile: pyproject.toml
collected 16 items

tests/test_api.py .                                                      [  6%]
tests/test_guidance_service.py ..                                        [ 18%]
tests/test_logging_detector.py .......                                   [ 62%]
tests/test_mock_prototype.py ...                                         [ 81%]
tests/test_policy_mapper.py ...                                          [100%]

======================== 16 passed in 1.04s =========================
```

### Verified Criteria:
- `test_map_credential_identifier_to_sec_log_001`: Confirms password/API key patterns map strictly to `SEC-LOG-001`.
- `test_map_email_identifier_to_sec_log_002`: Confirms personal data patterns map to `SEC-LOG-002`.
- `test_guidance_service_generation_for_credential_logging`: Verifies full finding JSON generation, including GDPR Article 32 context and explicit legal disclaimers.
