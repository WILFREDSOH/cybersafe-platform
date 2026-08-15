import pytest

from cybersafe_api.domain.analysis.value_objects.risk_factor import RiskFactor


def test_risk_factor_accepts_valid_values() -> None:
    factor = RiskFactor(
        name="password_security",
        score=30,
        weight=0.25,
    )

    assert factor.name == "password_security"
    assert factor.score == 30
    assert factor.weight == 0.25


def test_risk_factor_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="name cannot be empty"):
        RiskFactor(
            name="   ",
            score=30,
            weight=0.25,
        )


def test_risk_factor_rejects_score_below_zero() -> None:
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        RiskFactor(
            name="password_security",
            score=-1,
            weight=0.25,
        )


def test_risk_factor_rejects_score_above_hundred() -> None:
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        RiskFactor(
            name="password_security",
            score=101,
            weight=0.25,
        )


def test_risk_factor_rejects_negative_weight() -> None:
    with pytest.raises(ValueError, match="weight must be between 0 and 1"):
        RiskFactor(
            name="password_security",
            score=30,
            weight=-0.1,
        )


def test_risk_factor_rejects_weight_above_one() -> None:
    with pytest.raises(ValueError, match="weight must be between 0 and 1"):
        RiskFactor(
            name="password_security",
            score=30,
            weight=1.1,
        )
