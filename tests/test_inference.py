"""
Unit tests for SentimentIQ Inference Engine.
"""

import pytest
from ml.inference.engine import SentimentInferenceEngine


@pytest.fixture(scope="module")
def baseline_engine():
    """Load baseline engine for rapid unit testing without transformer overhead."""
    return SentimentInferenceEngine(model_type="baseline")


def test_input_validation_empty(baseline_engine):
    with pytest.raises(ValueError, match="Input text must not be empty"):
        baseline_engine.predict("")

    with pytest.raises(ValueError, match="Input text must not be empty"):
        baseline_engine.predict("   \n\t  ")


def test_input_validation_type(baseline_engine):
    with pytest.raises(ValueError, match="Input text must be a string"):
        baseline_engine.predict(12345)


def test_single_prediction_format(baseline_engine):
    sample = "The customer support team resolved my billing issue in five minutes! Excellent service."
    response = baseline_engine.predict(sample)

    assert response["success"] is True
    assert "result" in response
    result = response["result"]

    assert result["sentiment"] in ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    assert 0.0 <= result["confidence"] <= 1.0
    assert "probabilities" in result

    probs = result["probabilities"]
    assert "positive" in probs
    assert "negative" in probs
    assert "neutral" in probs
    total_prob = sum(probs.values())
    assert 0.99 <= total_prob <= 1.01
    assert "model_version" in result
    assert "latency_ms" in result


def test_batch_prediction(baseline_engine):
    samples = [
        "I love this software! It is fast and reliable.",
        "Terrible experience, completely broken on arrival.",
        "The package arrived on Tuesday at 2 PM."
    ]
    batch_res = baseline_engine.predict_batch(samples)

    assert len(batch_res) == 3
    for res in batch_res:
        assert res["success"] is True
        assert res["result"]["sentiment"] in ["POSITIVE", "NEGATIVE", "NEUTRAL"]
        assert res["result"]["confidence"] > 0


def test_model_info(baseline_engine):
    info = baseline_engine.get_model_info()
    assert info["is_loaded"] is True
    assert info["model_type"] == "baseline"
    assert "version" in info
    assert set(info["classes"]) == {"POSITIVE", "NEGATIVE", "NEUTRAL"}


def test_champion_engine_inference():
    # Instantiate champion engine (RoBERTa)
    champion_engine = SentimentInferenceEngine(model_type="champion")
    assert champion_engine.is_loaded is True
    res = champion_engine.predict("This product is absolutely amazing and exceeded my expectations!")
    assert res["success"] is True
    assert res["result"]["sentiment"] == "POSITIVE"
    assert res["result"]["probabilities"]["positive"] > 0.8

