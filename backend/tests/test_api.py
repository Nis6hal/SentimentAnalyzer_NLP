"""
Integration tests for SentimentIQ FastAPI endpoints using FastAPI TestClient.
Tests health, single analysis, batch analysis, history, analytics, model info, and feedback.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app


@pytest.fixture(scope="module")
def client():
    """Initializes TestClient which triggers the FastAPI lifespan events."""
    with TestClient(app) as c:
        yield c


def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "inference_engine" in data
    assert data["inference_engine"] == "loaded"


def test_model_info_endpoint(client):
    response = client.get("/api/v1/model/info")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "model_id" in data
    assert "benchmark" in data
    assert "test_macro_f1" in data["benchmark"]
    assert set(data["classes"]) == {"NEGATIVE", "NEUTRAL", "POSITIVE"}


def test_single_analyze_positive(client):
    payload = {"text": "Absolutely fantastic customer experience! The interface is swift and intuitive."}
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    result = data["result"]
    assert result["sentiment"] == "POSITIVE"
    assert result["confidence"] > 0.5
    assert result["probabilities"]["positive"] > 0.5
    assert "id" in result
    assert result["id"] is not None


def test_single_analyze_negative(client):
    payload = {"text": "Worst purchase I have ever made. Complete waste of money and broke in a day."}
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    result = data["result"]
    assert result["sentiment"] == "NEGATIVE"
    assert result["probabilities"]["negative"] > 0.5


def test_single_analyze_invalid_empty(client):
    payload = {"text": "   "}
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 400


def test_batch_analyze(client):
    payload = {
        "texts": [
            "We enjoyed our stay very much, hotel staff was delightful.",
            "The flight was canceled without prior notice, outrageous!",
            "Flight AA120 departs at 10:45 AM from Gate 14."
        ]
    }
    response = client.post("/api/v1/analyze/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["total_processed"] == 3
    assert len(data["results"]) == 3
    assert data["results"][0]["sentiment"] == "POSITIVE"
    assert data["results"][1]["sentiment"] == "NEGATIVE"


def test_history_and_pagination(client):
    response = client.get("/api/v1/history?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["total"] >= 5
    assert len(data["items"]) <= 10


def test_analytics_metrics(client):
    response = client.get("/api/v1/analytics")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    summary = data["summary"]
    assert summary["total"] >= 5
    assert "percentages" in data
    assert "timeline" in data
    assert "recent_activity" in data


def test_feedback_submission(client):
    # First analyze something
    analyze_res = client.post("/api/v1/analyze", json={"text": "The battery life is acceptable."})
    analysis_id = analyze_res.json()["result"]["id"]

    # Submit feedback
    feedback_payload = {
        "analysis_id": analysis_id,
        "is_correct": True,
        "actual_sentiment": "NEUTRAL",
        "comment": "Accurately classified as neutral."
    }
    fb_res = client.post("/api/v1/feedback", json=feedback_payload)
    assert fb_res.status_code == 200
    assert fb_res.json()["success"] is True
