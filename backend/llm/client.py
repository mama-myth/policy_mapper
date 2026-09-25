from backend.config import settings


class LLMClient:

    def __init__(self):
        self.enabled = settings.LLM_ENABLED

    def generate_explanation(self, prompt: str) -> str:
        """Simulates LLM explanation generation if enabled, or raises ValueError to trigger fallback."""
        if not self.enabled:
            raise ValueError("LLM integration is disabled in settings.")

        # In production or when configured, calls OpenAI / HuggingFace API
        return "LLM generated developer guidance explanation."


llm_client = LLMClient()
