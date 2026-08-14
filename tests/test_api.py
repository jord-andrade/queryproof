from fastapi.testclient import TestClient

from api.index import app

client = TestClient(app)


def test_api_index_links_to_public_contract() -> None:
    response = client.get("/api")

    assert response.status_code == 200
    assert response.json()["documentation"] == "/api/docs"


def test_health_discloses_synthetic_mode() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["dataset"]["synthetic"] is True
    assert response.headers["x-content-type-options"] == "nosniff"


def test_analyze_validates_and_returns_trace() -> None:
    response = client.post(
        "/api/analyze",
        json={"question": "How has CSAT changed week over week?"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "csat_weekly_trend"
    assert len(payload["trace"]) == 4
    assert payload["evidence"]["source"] == "data/support_tickets.csv"


def test_question_length_is_bounded() -> None:
    response = client.post("/api/analyze", json={"question": "x" * 301})

    assert response.status_code == 422
