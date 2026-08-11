import pytest

from cybersafe_api.domain.analysis.services.analysis_service import AnalysisService
from cybersafe_api.domain.analysis.value_objects.risk_level import RiskLevel


@pytest.mark.parametrize(
    ("score", "expected_level"),
    [
        (0, RiskLevel.LOW),
        (24, RiskLevel.LOW),
        (25, RiskLevel.MEDIUM),
        (49, RiskLevel.MEDIUM),
        (50, RiskLevel.HIGH),
        (74, RiskLevel.HIGH),
        (75, RiskLevel.CRITICAL),
        (100, RiskLevel.CRITICAL),
    ],
)
def test_determine_risk_level(score: int, expected_level: RiskLevel) -> None:
    assert AnalysisService.determine_risk_level(score) == expected_level


def test_determine_risk_level_rejects_invalid_score() -> None:
    with pytest.raises(ValueError, match="between 0 and 100"):
        AnalysisService.determine_risk_level(101)


def test_create_result_builds_analysis_result() -> None:
    result = AnalysisService.create_result(
        score=30,
        summary="The analyzed asset presents a moderate security risk.",
    )

    assert result.score == 30
    assert result.risk_level == RiskLevel.MEDIUM
    assert result.summary == (
        "The analyzed asset presents a moderate security risk."
    )
