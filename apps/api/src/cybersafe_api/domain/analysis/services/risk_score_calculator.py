from cybersafe_api.domain.analysis.value_objects.risk_factor import RiskFactor


class RiskScoreCalculator:
    """Calculate a global security risk score from weighted factors."""

    @staticmethod
    def calculate_weighted_score(factors: list[RiskFactor]) -> int:
        """Calculate a weighted risk score from risk factors."""
        if not factors:
            raise ValueError("At least one factor is required.")

        total_weight = sum(factor.weight for factor in factors)

        if abs(total_weight - 1.0) > 1e-9:
            raise ValueError("Weights must sum to 1.")

        weighted_score = sum(
            factor.score * factor.weight
            for factor in factors
        )

        return round(weighted_score)
