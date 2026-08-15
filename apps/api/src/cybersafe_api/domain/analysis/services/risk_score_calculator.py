class RiskScoreCalculator:
    """Calculate a global security risk score from weighted factors."""

    @staticmethod
    def calculate_weighted_score(
        factors: dict[str, int],
        weights: dict[str, float],
    ) -> int:
        """Calculate a weighted risk score from individual security factors."""
        if set(factors) != set(weights):
            raise ValueError("Factors and weights must contain the same factors.")

        if not factors:
            raise ValueError("At least one factor is required.")

        for name, score in factors.items():
            if not 0 <= score <= 100:
                raise ValueError(
                    f"Factor '{name}' score must be between 0 and 100."
                )

        for name, weight in weights.items():
            if not 0 <= weight <= 1:
                raise ValueError(
                    f"Factor '{name}' weight must be between 0 and 1."
                )

        total_weight = sum(weights.values())

        if abs(total_weight - 1.0) > 1e-9:
            raise ValueError("Weights must sum to 1.")

        weighted_score = sum(
            factors[name] * weights[name]
            for name in factors
        )

        return round(weighted_score)
