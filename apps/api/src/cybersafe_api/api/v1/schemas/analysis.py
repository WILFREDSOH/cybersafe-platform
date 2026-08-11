from pydantic import BaseModel, Field

from cybersafe_api.domain.analysis.value_objects.risk_level import RiskLevel


class AnalysisRequest(BaseModel):
    """Request payload for a security analysis."""

    score: int = Field(ge=0, le=100)
    summary: str = Field(min_length=1)


class AnalysisResponse(BaseModel):
    """Response returned after a security analysis."""

    score: int
    risk_level: RiskLevel
    summary: str
