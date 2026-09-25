from typing import Optional
from backend.policies.policy_loader import PolicyRecordModel, policy_loader


class PolicyMapper:

    def __init__(self, loader=policy_loader):
        self.loader = loader

    def map_pattern_to_policy(
            self,
            observed_pattern: str,
            sensitive_identifier: str) -> Optional[PolicyRecordModel]:
        """Maps an observed AST pattern and sensitive identifier to internal policy requirement.

        """
        # Credentials, secrets, tokens, keys -> SEC-LOG-001
        credential_terms = {
            "password", "passwd", "pwd", "token", "access_token",
            "refresh_token", "api_key", "apikey", "secret", "credential",
            "credentials"
        }

        # Personal data (email, name, etc.) -> SEC-LOG-002
        privacy_terms = {
            "email", "user.email", "phone", "address", "dob", "birth"
        }

        sens_lower = sensitive_identifier.lower()

        if any(term in sens_lower for term in credential_terms):
            return self.loader.get_policy("SEC-LOG-001")

        if any(term in sens_lower for term in privacy_terms):
            # Fallback to SEC-LOG-002 if present, otherwise SEC-LOG-001
            policy_002 = self.loader.get_policy("SEC-LOG-002")
            if policy_002:
                return policy_002
            return self.loader.get_policy("SEC-LOG-001")

        # Default fallback for logging calls
        if observed_pattern == "sensitive_value_passed_to_logging_function":
            return self.loader.get_policy("SEC-LOG-001")

        return None


policy_mapper = PolicyMapper()
