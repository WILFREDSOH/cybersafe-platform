from dataclasses import dataclass

from cybersafe_api.domain.analysis.value_objects.risk_level import RiskLevel


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """Represents the result produced by a CyberSafe security analysis."""

    score: int
    risk_level: RiskLevel
    summary: str

    def __post_init__(self) -> None:
        if not 0 <= self.score <= 100:
            raise ValueError("Analysis score must be between 0 and 100.")

        if not self.summary.strip():
            raise ValueError("Analysis summary cannot be empty.")
