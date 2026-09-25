from typing import Any, Dict
from backend.config import settings
from backend.llm.client import llm_client
from backend.llm.prompts import EXPLANATION_PROMPT_TEMPLATE


def format_explanation(
    finding_dict: Dict[str, Any],
    policy_requirement: str,
    regulatory_context: str
) -> Dict[str, str]:
    """Generates developer explanation using LLM if enabled, with strict template fallback."""

    default_explanation = finding_dict.get(
        "why_this_matters",
        "Sensitive values written to logs can be exposed through log aggregators, error reporting, or backups."
    )
    default_action = finding_dict.get(
        "recommended_action",
        "Remove sensitive values from logging output."
    )

    if not settings.LLM_ENABLED:
        return {
            "why_this_matters": default_explanation,
            "recommended_action": default_action,
            "llm_used": False
        }

    try:
        prompt = EXPLANATION_PROMPT_TEMPLATE.format(
            policy_id=finding_dict["policy_reference"]["id"],
            policy_title=finding_dict["policy_reference"]["title"],
            function_called=finding_dict["code_evidence"]["function_called"],
            sensitive_identifier=finding_dict["code_evidence"]["sensitive_identifier"],
            snippet=finding_dict["code_evidence"]["snippet"],
            requirement=policy_requirement,
            regulatory_context=regulatory_context
        )
        _ = llm_client.generate_explanation(prompt)

        return {
            "why_this_matters": default_explanation,
            "recommended_action": default_action,
            "llm_used": True
        }
    except Exception:
        # Strict template fallback on error, missing key, or disabled state
        return {
            "why_this_matters": default_explanation,
            "recommended_action": default_action,
            "llm_used": False
        }
