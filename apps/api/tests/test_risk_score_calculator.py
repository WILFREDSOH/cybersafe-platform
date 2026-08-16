import pytest

from cybersafe_api.domain.analysis.services.risk_score_calculator import (
    RiskScoreCalculator,
)
from cybersafe_api.domain.analysis.value_objects.risk_factor import RiskFactor


def test_calculate_weighted_score_returns_expected_score() -> None:
    factors = [
        RiskFactor("password_security", 20, 0.20),
        RiskFactor("network_exposure", 80, 0.25),
        RiskFactor("configuration", 30, 0.20),
        RiskFactor("software_security", 70, 0.20),
        RiskFactor("data_protection", 40, 0.15),
    ]

    score = RiskScoreCalculator.calculate_weighted_score(factors)

    assert score == 50


def test_calculate_weighted_score_accepts_zero_score() -> None:
    factors = [
        RiskFactor("password_security", 0, 0.5),
        RiskFactor("network_exposure", 0, 0.5),
    ]

    score = RiskScoreCalculator.calculate_weighted_score(factors)

    assert score == 0


def test_calculate_weighted_score_accepts_maximum_score() -> None:
    factors = [
        RiskFactor("password_security", 100, 0.5),
        RiskFactor("network_exposure", 100, 0.5),
    ]

    score = RiskScoreCalculator.calculate_weighted_score(factors)

    assert score == 100


def test_calculate_weighted_score_requires_at_least_one_factor() -> None:
    with pytest.raises(ValueError, match="At least one factor"):
        RiskScoreCalculator.calculate_weighted_score([])


def test_calculate_weighted_score_requires_weights_to_sum_to_one() -> None:
    factors = [
        RiskFactor("password_security", 20, 0.2),
        RiskFactor("network_exposure", 80, 0.2),
    ]

    with pytest.raises(ValueError, match="sum to 1"):
        RiskScoreCalculator.calculate_weighted_score(factors)


def test_calculate_weighted_score_accepts_zero_weight() -> None:
    factors = [
        RiskFactor("password_security", 100, 0.0),
        RiskFactor("network_exposure", 50, 1.0),
    ]

    score = RiskScoreCalculator.calculate_weighted_score(factors)

    assert score == 50
