from cybersafe_api.domain.analysis.entities.analysis_result import AnalysisResult
from cybersafe_api.domain.analysis.value_objects.risk_level import RiskLevel


class AnalysisService:
    """Provides domain logic for evaluating security analysis scores."""

    @staticmethod
    def determine_risk_level(score: int) -> RiskLevel:
        """Determine the risk level associated with a security score."""
        if not 0 <= score <= 100:
            raise ValueError("Analysis score must be between 0 and 100.")

        if score < 25:
            return RiskLevel.LOW

        if score < 50:
            return RiskLevel.MEDIUM

        if score < 75:
            return RiskLevel.HIGH

        return RiskLevel.CRITICAL

    @classmethod
    def create_result(cls, score: int, summary: str) -> AnalysisResult:
        """Create an analysis result from a score and a summary."""
        risk_level = cls.determine_risk_level(score)

        return AnalysisResult(
            score=score,
            risk_level=risk_level,
            summary=summary,
        )
