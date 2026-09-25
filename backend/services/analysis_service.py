from typing import Any, Dict
from backend.analyzer.logging_detector import detect_sensitive_logging
from backend.services.guidance_service import (
    AnalysisResponseModel,
    guidance_service,
)


class AnalysisService:

    def __init__(self, g_service=guidance_service):
        self.g_service = g_service

    def analyze_code(self,
                     code: str,
                     file_name: str = "sample.py") -> AnalysisResponseModel:
        detection_result = detect_sensitive_logging(code, file_name)

        if "error" in detection_result:
            return AnalysisResponseModel(file_name=file_name, findings=[])

        patterns = detection_result.get("patterns", [])
        findings = []

        for p in patterns:
            finding = self.g_service.generate_guidance_for_pattern(p, file_name)
            findings.append(finding)

        return AnalysisResponseModel(file_name=file_name, findings=findings)


analysis_service = AnalysisService()
