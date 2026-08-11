from enum import StrEnum


class RiskLevel(StrEnum):
    """Represents the severity level of a security analysis."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
