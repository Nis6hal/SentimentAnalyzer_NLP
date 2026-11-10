"""
SentimentIQ - Unit Tests for Text Preprocessing and Data Pipeline
Adheres to Section 6 and 13.
"""

import pytest
import pandas as pd
from ml.preprocessing.cleaner import (
    clean_html,
    normalize_whitespace,
    normalize_twitter_artifacts,
    expand_contractions,
    clean_text_transformer,
    clean_text_baseline,
)
from ml.preprocessing.pipeline import DatasetPipeline


def test_clean_html():
    raw = "<p>The product is <b>extraordinary</b> &amp; fast!</p>"
    cleaned = clean_html(raw)
    assert "<p>" not in cleaned
    assert "<b>" not in cleaned
    assert "&amp;" not in cleaned
    assert "extraordinary & fast!" in cleaned


def test_negation_preservation_baseline():
    text_neg = "I didn't like the performance, it wasn't good at all."
    cleaned = clean_text_baseline(text_neg)
    # Ensure negation words are preserved and expanded
    assert "not" in cleaned
    assert "like" in cleaned
    assert "good" in cleaned


def test_negation_preservation_transformer():
    text = "We cannot recommend this product; it never works."
    cleaned = clean_text_transformer(text)
    assert "cannot" in cleaned or "can not" in cleaned
    assert "never" in cleaned


def test_twitter_artifacts_normalization():
    tweet = "Great job @elonmusk checking the update at https://x.com/post/123"
    cleaned = clean_text_transformer(tweet)
    assert "@elonmusk" not in cleaned
    assert "@user" in cleaned
    assert "https://x.com/post/123" not in cleaned
    assert "http" in cleaned


def test_whitespace_and_null_bytes():
    raw = "Hello \x00 world!   \n\n  Multiple    spaces.  "
    cleaned = clean_text_transformer(raw)
    assert "\x00" not in cleaned
    assert cleaned == "Hello world! Multiple spaces."


def test_empty_and_invalid_inputs():
    assert clean_text_transformer(None) == ""
    assert clean_text_transformer("") == ""
    assert clean_text_baseline(None) == ""
    assert clean_text_baseline(12345) == "12345"


def test_dataset_pipeline_conflict_resolution():
    pipeline = DatasetPipeline(output_dir="ml/data/processed")
    # DataFrame with duplicate text having conflicting labels
    data = {
        "text": ["Movie was awful", "Movie was awful", "Great movie", "Neutral comment"],
        "label_id": [0, 2, 2, 1]  # First two have identical text but labels 0 and 2
    }
    df = pd.DataFrame(data)
    clean_df, stats = pipeline.validate_and_clean_df(df)
    
    # Conflicting text 'Movie was awful' must be excluded
    assert len(clean_df) == 2
    assert "Movie was awful" not in clean_df["text_clean"].values
    assert stats["conflicts_dropped"] == 1

