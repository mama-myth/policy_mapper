# Policy Representation Model — Policy-to-Code Mapper

## 1. Overview
The Policy Knowledge Base in Policy-to-Code Mapper provides a curated, machine-readable, and explainable representation of organizational security requirements and supporting regulatory references. Policy data is represented in structured JSON records (`backend/data/policies.json`) and validated via Pydantic models (`backend/policies/policy_loader.py`).

---

## 2. Policy Record Schema

Each policy record contains the following mandatory fields:

```json
{
  "id": "SEC-LOG-001",
  "title": "Sensitive Data Must Not Be Logged",
  "category": "Secure Logging",
  "requirement": "Passwords, authentication tokens, API keys, session identifiers, credentials, and other secrets must not be written to application logs, console output, debug output, or error messages.",
  "risk_explanation": "Sensitive values written to logs can be exposed through log storage, monitoring systems, error-reporting platforms, backups, support tools, or unauthorized access.",
  "developer_guidance": "Remove sensitive values from output statements. Log non-sensitive operational data only when necessary. Use event IDs, correlation IDs, or masked values where appropriate.",
  "relevant_code_contexts": [
    "Sensitive identifier passed to print()",
    "Sensitive identifier passed to logging function",
    "Sensitive identifier passed to logger method"
  ],
  "supporting_regulatory_context": [
    {
      "framework": "GDPR",
      "article": "Article 32",
      "title": "Security of processing",
      "relationship": "supporting_security_context",
      "note": "This is supporting context, not a legal conclusion."
    }
  ]
}
```

---

## 3. Curated Policy Records

### A. SEC-LOG-001: Sensitive Data Must Not Be Logged
- **Category:** Secure Logging
- **Target Identifiers:** `password`, `passwd`, `pwd`, `token`, `access_token`, `refresh_token`, `api_key`, `secret`, `credential`, `credentials`.
- **Supporting Regulation:** GDPR Article 32 (Security of processing).

### B. SEC-LOG-002: Personal Data in Logs Must Be Minimized
- **Category:** Data Privacy
- **Target Identifiers:** `email`, `user.email`, `phone`, `address`, `dob`.
- **Supporting Regulation:** GDPR Article 5(1)(c) (Data minimisation).

---

## 4. Binding Rules & Non-Legal Context Association
- **Code Context Binding:** AST pattern `sensitive_value_passed_to_logging_function` maps code elements (`password → logger.info()`) directly to policy requirements.
- **Supporting Context Rule:** Regulatory frameworks (GDPR) are explicitly mapped as **supporting context**, ensuring the tool educates developers without declaring legal non-compliance or legal violations.
