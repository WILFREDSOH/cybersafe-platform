from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RiskFactor:
    """Represents a weighted factor contributing to a security risk score."""

    name: str
    score: int
    weight: float

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Risk factor name cannot be empty.")

        if not 0 <= self.score <= 100:
            raise ValueError("Risk factor score must be between 0 and 100.")

        if not 0 <= self.weight <= 1:
            raise ValueError("Risk factor weight must be between 0 and 1.")
