import pytest

from cybersafe_api.domain.analysis.services.risk_score_calculator import (
    RiskScoreCalculator,
)


def test_calculate_weighted_score_returns_expected_score() -> None:
    score = RiskScoreCalculator.calculate_weighted_score(
        factors={
            "password_security": 20,
            "network_exposure": 80,
            "configuration": 30,
            "software_security": 70,
            "data_protection": 40,
        },
        weights={
            "password_security": 0.20,
            "network_exposure": 0.25,
            "configuration": 0.20,
            "software_security": 0.20,
            "data_protection": 0.15,
        },
    )

    assert score == 50


def test_calculate_weighted_score_accepts_zero_score() -> None:
    score = RiskScoreCalculator.calculate_weighted_score(
        factors={
            "password_security": 0,
            "network_exposure": 0,
        },
        weights={
            "password_security": 0.5,
            "network_exposure": 0.5,
        },
    )

    assert score == 0


def test_calculate_weighted_score_accepts_maximum_score() -> None:
    score = RiskScoreCalculator.calculate_weighted_score(
        factors={
            "password_security": 100,
            "network_exposure": 100,
        },
        weights={
            "password_security": 0.5,
            "network_exposure": 0.5,
        },
    )

    assert score == 100


def test_calculate_weighted_score_rejects_factor_outside_range() -> None:
    with pytest.raises(ValueError, match="between 0 and 100"):
        RiskScoreCalculator.calculate_weighted_score(
            factors={
                "password_security": 120,
            },
            weights={
                "password_security": 1.0,
            },
        )


def test_calculate_weighted_score_rejects_negative_factor() -> None:
    with pytest.raises(ValueError, match="between 0 and 100"):
        RiskScoreCalculator.calculate_weighted_score(
            factors={
                "password_security": -1,
            },
            weights={
                "password_security": 1.0,
            },
        )


def test_calculate_weighted_score_requires_matching_factors_and_weights() -> None:
    with pytest.raises(ValueError, match="same factors"):
        RiskScoreCalculator.calculate_weighted_score(
            factors={
                "password_security": 20,
                "network_exposure": 80,
            },
            weights={
                "password_security": 1.0,
            },
        )


def test_calculate_weighted_score_requires_weights_to_sum_to_one() -> None:
    with pytest.raises(ValueError, match="sum to 1"):
        RiskScoreCalculator.calculate_weighted_score(
            factors={
                "password_security": 20,
                "network_exposure": 80,
            },
            weights={
                "password_security": 0.2,
                "network_exposure": 0.2,
            },
        )


def test_calculate_weighted_score_rejects_negative_weight() -> None:
    with pytest.raises(ValueError, match="between 0 and 1"):
        RiskScoreCalculator.calculate_weighted_score(
            factors={
                "password_security": 20,
            },
            weights={
                "password_security": -0.1,
            },
        )
