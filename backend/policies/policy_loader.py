import json
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

POLICIES_JSON_PATH = Path(__file__).parent.parent / "data" / "policies.json"


class SupportingRegulatoryContextModel(BaseModel):
    framework: str
    article: str
    title: str
    relationship: str
    note: Optional[str] = None


class PolicyRecordModel(BaseModel):
    id: str
    title: str
    category: str
    requirement: str
    risk_explanation: str
    developer_guidance: str
    relevant_code_contexts: List[str]
    supporting_regulatory_context: List[SupportingRegulatoryContextModel]


class PolicyLoader:

    def __init__(self, json_path: Path = POLICIES_JSON_PATH):
        self.json_path = json_path
        self._policies: Dict[str, PolicyRecordModel] = {}
        self.load_policies()

    def load_policies(self) -> Dict[str, PolicyRecordModel]:
        if not self.json_path.exists():
            raise FileNotFoundError(
                f"Policy JSON file not found at {self.json_path}")

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._policies = {}
        for item in data:
            policy = PolicyRecordModel(**item)
            self._policies[policy.id] = policy

        return self._policies

    def get_policy(self, policy_id: str) -> Optional[PolicyRecordModel]:
        return self._policies.get(policy_id)

    def list_policies(self) -> List[PolicyRecordModel]:
        return list(self._policies.values())


# Global singleton instance for efficient cached lookup
policy_loader = PolicyLoader()
