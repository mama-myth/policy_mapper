from typing import List, Optional, Any
from pydantic import BaseModel, Field


class ObservedCodeEvidence(BaseModel):
    line_start: int
    line_end: int
    function_called: str
    sensitive_identifier: str
    snippet: str


class ObservedCodePatternRecord(BaseModel):
    pattern_id: str = "sensitive_value_passed_to_logging_function"
    file_name: str
    code_evidence: ObservedCodeEvidence
    raw_pattern: str = "Sensitive identifier passed to logging function"


class DetectionResult(BaseModel):
    file_name: str
    patterns: List[ObservedCodePatternRecord] = Field(default_factory=list)
    syntax_error: Optional[dict] = None
