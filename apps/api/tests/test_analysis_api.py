from fastapi.testclient import TestClient

from cybersafe_api.main import app

client = TestClient(app)


def test_create_analysis_returns_analysis_result() -> None:
    response = client.post(
        "/api/v1/analysis",
        json={
            "score": 30,
            "summary": "The analyzed asset presents a moderate security risk.",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "score": 30,
        "risk_level": "medium",
        "summary": "The analyzed asset presents a moderate security risk.",
    }


def test_create_analysis_accepts_critical_score() -> None:
    response = client.post(
        "/api/v1/analysis",
        json={
            "score": 90,
            "summary": "The analyzed asset presents a critical security risk.",
        },
    )

    assert response.status_code == 200
    assert response.json()["risk_level"] == "critical"


def test_create_analysis_rejects_score_above_hundred() -> None:
    response = client.post(
        "/api/v1/analysis",
        json={
            "score": 150,
            "summary": "Invalid score.",
        },
    )

    assert response.status_code == 422


def test_create_analysis_rejects_empty_summary() -> None:
    response = client.post(
        "/api/v1/analysis",
        json={
            "score": 50,
            "summary": "",
        },
    )

    assert response.status_code == 422
