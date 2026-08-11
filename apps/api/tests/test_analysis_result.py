import pytest

from cybersafe_api.domain.analysis.entities.analysis_result import AnalysisResult
from cybersafe_api.domain.analysis.value_objects.risk_level import RiskLevel


def test_analysis_result_accepts_valid_score() -> None:
    result = AnalysisResult(
        score=25,
        risk_level=RiskLevel.LOW,
        summary="The analyzed asset presents a low security risk.",
    )

    assert result.score == 25
    assert result.risk_level == RiskLevel.LOW
    assert result.summary == "The analyzed asset presents a low security risk."


def test_analysis_result_rejects_score_below_zero() -> None:
    with pytest.raises(ValueError, match="between 0 and 100"):
        AnalysisResult(
            score=-1,
            risk_level=RiskLevel.LOW,
            summary="Invalid score.",
        )


def test_analysis_result_rejects_score_above_hundred() -> None:
    with pytest.raises(ValueError, match="between 0 and 100"):
        AnalysisResult(
            score=101,
            risk_level=RiskLevel.HIGH,
            summary="Invalid score.",
        )


def test_analysis_result_rejects_empty_summary() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        AnalysisResult(
            score=50,
            risk_level=RiskLevel.MEDIUM,
            summary="   ",
        )
