# Phase 2 Visual Progression & Completion Report — Deterministic AST Detection

## 1. Overview
In **Phase 2**, Policy-to-Code Mapper implemented deterministic Python AST (Abstract Syntax Tree) analysis using Python's built-in `ast` module. The AST engine scans Python source code to detect logging/output function calls (`print()`, `logging.*`, `logger.*`) when sensitive identifiers (`password`, `token`, `api_key`, `credentials`, `email`, etc.) are passed as arguments.

---

## 2. Visual Code-to-Pattern Evidence Chain

```text
               SOURCE CODE INPUT
 ┌───────────────────────────────────────────────────┐
 │ def login(username, password):                    │
 │     logger.info("Login for %s: %s", user, password)│
 └─────────────────────────┬─────────────────────────┘
                           │
                           ▼
                 DETERMINISTIC AST PARSER
         (backend/analyzer/logging_detector.py)
                           │
                           ▼
              STRUCTURED PATTERN DISCOVERY
 ┌───────────────────────────────────────────────────┐
 │ Pattern ID: sensitive_value_passed_to_logging_func│
 │ Function Called: logger.info                      │
 │ Sensitive Identifier: password                    │
 │ Line: 3                                           │
 └───────────────────────────────────────────────────┘
```

---

## 3. Sample Observed Pattern JSON Payload

When running AST analysis on `examples/unsafe_credential_logging.py`, the AST detector generates the following structured record:

```json
{
  "file_name": "examples/unsafe_credential_logging.py",
  "patterns": [
    {
      "observed_pattern": "sensitive_value_passed_to_logging_function",
      "function_called": "logger.info",
      "sensitive_identifier": "password",
      "line_start": 8,
      "line_end": 8,
      "snippet": "logger.info(\"Login attempt for %s with password %s\", username, password)"
    },
    {
      "observed_pattern": "sensitive_value_passed_to_logging_function",
      "function_called": "print",
      "sensitive_identifier": "password",
      "line_start": 9,
      "line_end": 9,
      "snippet": "print(f\"Debug auth token: {password}\")"
    }
  ]
}
```

---

## 4. Test Suite Execution & Precision Evidence

The AST detector was verified against positive, negative, safe, and invalid syntax examples using `pytest`:

```text
============================= test session starts ==============================
rootdir: /app
configfile: pyproject.toml
collected 11 items

tests/test_api.py .                                                      [  9%]
tests/test_logging_detector.py .......                                   [ 72%]
tests/test_mock_prototype.py ...                                         [100%]

======================== 11 passed in 0.67s =========================
```

### Verified Test Cases:
1. `test_positive_credential_logging`: Correctly flags `logger.info(..., password)`.
2. `test_positive_api_key_logging`: Correctly flags `print("Key:", api_key)`.
3. `test_positive_token_attribute_logging`: Correctly flags `logging.warning(..., request.access_token)`.
4. `test_safe_logging`: Confirms `logger.info("... user_id=%s", user_id)` produces 0 findings.
5. `test_sensitive_variable_used_without_logging`: Confirms hashing `password` without logging produces 0 findings.
6. `test_benign_substring_not_flagged`: Confirms benign variables like `category = "general_announcement"` produce 0 findings.
7. `test_invalid_python_syntax`: Confirms syntax errors return structured `SyntaxError` details rather than crashing.
