from fastapi import APIRouter

from cybersafe_api.api.v1.schemas.analysis import (
    AnalysisRequest,
    AnalysisResponse,
)
from cybersafe_api.domain.analysis.services.analysis_service import AnalysisService

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


@router.post(
    "",
    response_model=AnalysisResponse,
)
async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    """Analyze a security score and return the corresponding risk level."""
    result = AnalysisService.create_result(
        score=request.score,
        summary=request.summary,
    )

    return AnalysisResponse(
        score=result.score,
        risk_level=result.risk_level,
        summary=result.summary,
    )
