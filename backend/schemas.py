from typing import List, Optional, Any
from pydantic import BaseModel, Field
from backend.services.guidance_service import AnalysisResponseModel


class AnalyzeRequest(BaseModel):
    language: str = Field(
        default="python",
        description="Programming language of the source file (currently Python supported).",
        examples=["python"]
    )
    file_name: str = Field(
        default="sample.py",
        description="Name or relative path of the file being analyzed.",
        examples=["auth.py"]
    )
    code: str = Field(
        ...,
        description="Source code content to be analyzed.",
        examples=["logger.info('Login for %s with pass %s', username, password)"]
    )


class ErrorResponseModel(BaseModel):
    error: str
    message: str
    details: Optional[Any] = None
