"""
SentimentIQ - Text Preprocessing & Cleaning Engine
Adheres to Section 6 of specification:
- Preserves negation tokens ('not', 'no', 'never', "n't")
- Preserves emotional punctuation (!, ?)
- Normalizes URLs, mentions, and HTML entities
- Avoids aggressive normalization for transformer tokenization
"""

import re
import html
import unicodedata
from typing import Union, List


# Common contractions expansion mapping for standardized baseline processing
CONTRACTION_MAP = {
    r"won\'t": "will not",
    r"can\'t": "can not",
    r"cannot": "can not",
    r"n\'t": " not",
    r"\'re": " are",
    r"\'s": " is",
    r"\'d": " would",
    r"\'ll": " will",
    r"\'t": " not",
    r"\'ve": " have",
    r"\'m": " am"
}


def clean_html(text: str) -> str:
    """Unescapes HTML entities, strips residual HTML tags, and collapses spaces."""
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    # Strip HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    return normalize_whitespace(text)


def normalize_whitespace(text: str) -> str:
    """Collapses multiple spaces, tabs, and newlines into single spaces."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def normalize_twitter_artifacts(text: str) -> str:
    """
    Standardizes Twitter/Social artifacts from TweetEval while keeping context:
    - Normalizes @user mentions to @user
    - Normalizes http URLs to http
    """
    # Standardize mentions
    text = re.sub(r"@\w+", "@user", text)
    # Standardize URLs
    text = re.sub(r"https?://\S+|www\.\S+", "http", text)
    return text


def expand_contractions(text: str) -> str:
    """Expands common English contractions while strictly preserving negations."""
    for pattern, replacement in CONTRACTION_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def clean_text_transformer(text: Union[str, float, None]) -> str:
    """
    Preprocessing pipeline specifically for Transformer models (DistilBERT / RoBERTa):
    - Preserves case (cased/uncased tokenizer handles this).
    - Preserves meaningful punctuation (!, ?, ..., quotes).
    - Preserves emojis and sentiment indicators.
    - Normalizes HTML and unicode abnormalities.
    - Strictly avoids stopword removal.
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)

    # Unicode normalization (NFC)
    text = unicodedata.normalize("NFC", text)
    # Unescape and strip HTML
    text = clean_html(text)
    # Normalize social artifacts
    text = normalize_twitter_artifacts(text)
    # Remove null bytes
    text = text.replace("\x00", "")
    # Normalize excessive spaces
    text = normalize_whitespace(text)

    return text


def clean_text_baseline(text: Union[str, float, None]) -> str:
    """
    Preprocessing pipeline for TF-IDF + Logistic Regression:
    - Lowers case.
    - Expands contractions (retaining negations).
    - Cleans HTML and URLs.
    - Retains letters, numbers, and basic sentiment punctuation (!, ?).
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)

    text = clean_html(text)
    text = expand_contractions(text)
    text = text.lower()
    text = normalize_twitter_artifacts(text)
    # Retain alphanumeric and critical sentiment punctuation
    text = re.sub(r"[^a-z0-9\s!\?]", " ", text)
    text = normalize_whitespace(text)
    return text
