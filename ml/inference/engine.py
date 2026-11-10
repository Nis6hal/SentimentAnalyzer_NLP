"""
SentimentIQ - Production Inference Engine
Implements modular, low-latency sentiment inference supporting single and batch predictions,
softmax probability estimation, and graceful model fallbacks (Champion RoBERTa -> Baseline TF-IDF).
"""

import os
import time
import logging
from typing import List, Dict, Any, Union, Optional
import numpy as np

logger = logging.getLogger("sentimentiq.inference")
logging.basicConfig(level=logging.INFO)

# Normalized label mappings
LABEL_MAP = {
    0: "NEGATIVE",
    1: "NEUTRAL",
    2: "POSITIVE"
}

ID2LABEL_LOWER = {
    0: "negative",
    1: "neutral",
    2: "positive"
}


class SentimentInferenceEngine:
    """
    Singleton-capable inference engine loaded once at application startup.
    Encapsulates tokenization, inference, softmax probability computation,
    confidence scoring, and batch processing.
    """

    _instance: Optional["SentimentInferenceEngine"] = None

    def __init__(self, model_type: str = "champion", device: str = "cpu"):
        self.model_type = model_type
        self.device = device
        self.model_version = "1.0.0"
        self.model_id = ""
        self.is_loaded = False
        
        # RoBERTa components
        self.tokenizer = None
        self.transformer_model = None

        # Baseline components
        self.baseline_clf = None
        self.baseline_vec = None

        self._load_model()

    @classmethod
    def get_instance(cls, model_type: str = "champion", device: str = "cpu") -> "SentimentInferenceEngine":
        """Thread-safe / singleton access to avoid reloading heavy weights."""
        if cls._instance is None:
            cls._instance = SentimentInferenceEngine(model_type=model_type, device=device)
        return cls._instance

    def _load_model(self):
        """Loads model weights once into memory."""
        logger.info(f"Initializing SentimentIQ Inference Engine (requested: {self.model_type})...")
        
        if self.model_type == "champion":
            try:
                import torch
                from transformers import AutoTokenizer, AutoModelForSequenceClassification

                model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
                logger.info(f"Loading champion model: {model_name} onto {self.device}...")
                
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.transformer_model = AutoModelForSequenceClassification.from_pretrained(model_name)
                self.transformer_model.to(self.device)
                self.transformer_model.eval()
                
                self.model_id = "roberta-sentiment-v1.0"
                self.is_loaded = True
                logger.info("Champion RoBERTa model successfully loaded and ready for inference.")
                return
            except Exception as e:
                logger.error(f"Failed to load Champion RoBERTa model: {e}. Falling back to baseline model.")
                self.model_type = "baseline"

        # Baseline fallback or explicit selection
        self._load_baseline()

    def _load_baseline(self):
        """Loads serialized TF-IDF + Logistic Regression baseline."""
        import joblib
        model_path = os.path.join("ml", "artifacts", "baseline", "baseline_model.joblib")
        vec_path = os.path.join("ml", "artifacts", "baseline", "baseline_vectorizer.joblib")

        if not os.path.exists(model_path) or not os.path.exists(vec_path):
            raise FileNotFoundError(
                f"Baseline model artifacts not found at {model_path} / {vec_path}. "
                "Ensure train_baseline.py has been run."
            )

        logger.info("Loading Baseline TF-IDF + Logistic Regression model...")
        self.baseline_clf = joblib.load(model_path)
        self.baseline_vec = joblib.load(vec_path)
        self.model_id = "baseline-tfidf-logreg-v1.0"
        self.model_type = "baseline"
        self.is_loaded = True
        logger.info("Baseline model successfully loaded.")

    def _validate_input(self, text: Any) -> str:
        """Validates input string, rejecting non-strings or empty text."""
        if not isinstance(text, str):
            raise ValueError(f"Input text must be a string, got {type(text).__name__}.")
        cleaned = text.strip()
        if not cleaned:
            raise ValueError("Input text must not be empty or whitespace only.")
        if len(cleaned) > 20000:
            cleaned = cleaned[:20000]
        return cleaned

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Executes single-text sentiment prediction.
        Returns standardized dictionary:
        {
            "success": True,
            "result": {
                "sentiment": "POSITIVE" | "NEGATIVE" | "NEUTRAL",
                "confidence": float,
                "probabilities": { "positive": float, "negative": float, "neutral": float },
                "model_version": str,
                "model_id": str,
                "latency_ms": float
            }
        }
        """
        batch_res = self.predict_batch([text])
        return batch_res[0]

    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Executes batch sentiment prediction with vectorized / tensor operations.
        """
        if not texts:
            return []

        validated_texts = [self._validate_input(t) for t in texts]
        t0 = time.perf_counter()

        if self.model_type == "champion" and self.transformer_model is not None:
            results = self._predict_transformer_batch(validated_texts)
        else:
            results = self._predict_baseline_batch(validated_texts)

        total_latency = (time.perf_counter() - t0) * 1000.0
        per_item_latency = round(total_latency / len(validated_texts), 2)

        formatted_outputs = []
        for res in results:
            formatted_outputs.append({
                "success": True,
                "result": {
                    "sentiment": res["sentiment"],
                    "confidence": res["confidence"],
                    "probabilities": res["probabilities"],
                    "model_version": self.model_version,
                    "model_id": self.model_id,
                    "latency_ms": per_item_latency
                }
            })

        return formatted_outputs

    def _predict_transformer_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Batched forward pass through RoBERTa with Softmax conversion."""
        import torch

        # Tokenize with padding and truncation
        encoded = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=256,
            return_tensors="pt"
        )
        encoded = {k: v.to(self.device) for k, v in encoded.items()}

        with torch.no_grad():
            outputs = self.transformer_model(**encoded)
            logits = outputs.logits
            # Softmax across class dimension
            probs = torch.softmax(logits, dim=-1).cpu().numpy()

        results = []
        for p in probs:
            neg_p = float(p[0])
            neu_p = float(p[1])
            pos_p = float(p[2])
            
            # Prediction corresponds to argmax
            pred_idx = int(np.argmax(p))
            sentiment = LABEL_MAP[pred_idx]
            confidence = round(float(p[pred_idx]), 4)

            results.append({
                "sentiment": sentiment,
                "confidence": confidence,
                "probabilities": {
                    "negative": round(neg_p, 4),
                    "neutral": round(neu_p, 4),
                    "positive": round(pos_p, 4)
                }
            })

        return results

    def _predict_baseline_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Batched inference via TF-IDF Vectorizer + Logistic Regression predict_proba."""
        from ml.preprocessing.cleaner import clean_text_baseline
        cleaned_texts = [clean_text_baseline(t) for t in texts]
        features = self.baseline_vec.transform(cleaned_texts)
        probs = self.baseline_clf.predict_proba(features)

        results = []
        for p in probs:
            neg_p = float(p[0])
            neu_p = float(p[1])
            pos_p = float(p[2])

            pred_idx = int(np.argmax(p))
            sentiment = LABEL_MAP[pred_idx]
            confidence = round(float(p[pred_idx]), 4)

            results.append({
                "sentiment": sentiment,
                "confidence": confidence,
                "probabilities": {
                    "negative": round(neg_p, 4),
                    "neutral": round(neu_p, 4),
                    "positive": round(pos_p, 4)
                }
            })

        return results

    def get_model_info(self) -> Dict[str, Any]:
        """Returns metadata about the active inference engine."""
        return {
            "model_id": self.model_id,
            "model_type": self.model_type,
            "version": self.model_version,
            "classes": ["NEGATIVE", "NEUTRAL", "POSITIVE"],
            "device": self.device,
            "is_loaded": self.is_loaded,
            "champion_architecture": "RoBERTa (cardiffnlp/twitter-roberta-base-sentiment-latest)",
            "baseline_architecture": "TF-IDF (1-3 ngrams) + Logistic Regression"
        }

