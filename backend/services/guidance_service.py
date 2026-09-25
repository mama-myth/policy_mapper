import uuid
from typing import Any, Dict, List
from pydantic import BaseModel, Field
from backend.policies.policy_mapper import policy_mapper
from backend.policies.policy_loader import PolicyRecordModel


class CodeEvidenceModel(BaseModel):
    line_start: int
    line_end: int
    function_called: str
    sensitive_identifier: str
    snippet: str


class PolicyReferenceModel(BaseModel):
    id: str
    title: str
    category: str


class RegulatoryContextModel(BaseModel):
    framework: str
    article: str
    title: str
    relationship: str


class ConfidenceModel(BaseModel):
    label: str  # high, medium, low
    basis: str


class TraceabilityModel(BaseModel):
    code_to_pattern: str
    pattern_to_policy: str
    policy_to_context: str


class FindingGuidanceModel(BaseModel):
    finding_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    guidance_type: str = "policy_awareness"
    severity: str = "high"  # low, medium, high
    title: str
    potential_policy_consideration: str
    code_evidence: CodeEvidenceModel
    observed_pattern: str
    policy_reference: PolicyReferenceModel
    supporting_regulatory_context: List[RegulatoryContextModel]
    why_this_matters: str
    recommended_action: str
    safer_example: str
    confidence: ConfidenceModel
    traceability: TraceabilityModel
    disclaimer: str = "This is automated developer guidance, not legal advice or a legal-compliance determination."


class AnalysisResponseModel(BaseModel):
    analysis_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    language: str = "python"
    file_name: str
    findings: List[FindingGuidanceModel] = Field(default_factory=list)


class GuidanceService:

    def __init__(self, mapper=policy_mapper):
        self.mapper = mapper

    def generate_guidance_for_pattern(
            self, pattern_record: Dict[str, Any],
            file_name: str) -> FindingGuidanceModel:
        obs_pattern = pattern_record["observed_pattern"]
        sens_id = pattern_record["sensitive_identifier"]
        func_called = pattern_record["function_called"]

        policy: PolicyRecordModel = self.mapper.map_pattern_to_policy(
            obs_pattern, sens_id)

        if not policy:
            # Fallback policy
            policy_id = "SEC-LOG-001"
            policy_title = "Sensitive Data Must Not Be Logged"
            category = "Secure Logging"
            risk = "Sensitive data logged to application output may be exposed."
            action = "Remove sensitive values from logging output."
            reg_list = [{
                "framework": "GDPR",
                "article": "Article 32",
                "title": "Security of processing",
                "relationship": "supporting_security_context"
            }]
        else:
            policy_id = policy.id
            policy_title = policy.title
            category = policy.category
            risk = policy.risk_explanation
            action = policy.developer_guidance
            reg_list = [
                {
                    "framework": r.framework,
                    "article": r.article,
                    "title": r.title,
                    "relationship": r.relationship
                } for r in policy.supporting_regulatory_context
            ]

        # Determine severity & safer example
        severity = "high" if policy_id == "SEC-LOG-001" else "medium"
        safer_example = f'{func_called}("Event processed for user_id=%s", user_id)'

        primary_reg = reg_list[0]["article"] if reg_list else "Article 32"

        return FindingGuidanceModel(
            severity=severity,
            title=
            f"Potential sensitive {'credential' if policy_id=='SEC-LOG-001' else 'personal data'} logging",
            potential_policy_consideration=
            f"This code appears to pass sensitive attribute '{sens_id}' to output function '{func_called}'.",
            code_evidence=CodeEvidenceModel(
                line_start=pattern_record["line_start"],
                line_end=pattern_record["line_end"],
                function_called=func_called,
                sensitive_identifier=sens_id,
                snippet=pattern_record["snippet"],
            ),
            observed_pattern=obs_pattern,
            policy_reference=PolicyReferenceModel(
                id=policy_id, title=policy_title, category=category),
            supporting_regulatory_context=[
                RegulatoryContextModel(**r) for r in reg_list
            ],
            why_this_matters=risk,
            recommended_action=action,
            safer_example=safer_example,
            confidence=ConfidenceModel(
                label="high",
                basis=
                "A deterministic AST rule detected a sensitive identifier passed to a recognized logging function."
            ),
            traceability=TraceabilityModel(
                code_to_pattern=f"{sens_id} → {func_called}()",
                pattern_to_policy=
                f"sensitive logging pattern → {policy_id}",
                policy_to_context=f"{policy_id} → GDPR {primary_reg}",
            ),
        )


guidance_service = GuidanceService()
