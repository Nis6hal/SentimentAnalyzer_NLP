"""
SentimentIQ - Baseline Model Training (Model A: TF-IDF + Logistic Regression)
Adheres to Section 5, 7, & 8:
- TF-IDF representation with sublinear TF & unigram + bigrams
- Class-weighted Logistic Regression to mitigate class imbalance
- Rigorous evaluation on validation & held-out test sets
- Macro F1 primary metric tracking
- MLflow experiment logging and artifact serialization
"""

import os
import json
import logging
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
import mlflow

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SentimentIQ.Baseline")

ID2LABEL = {0: "negative", 1: "neutral", 2: "positive"}
LABEL_NAMES = ["negative", "neutral", "positive"]


def train_baseline(
    data_dir: str = "ml/data/processed",
    artifacts_dir: str = "ml/artifacts/baseline",
    max_features: int = 15000,
    c_param: float = 1.0,
    random_seed: int = 42
):
    os.makedirs(artifacts_dir, exist_ok=True)
    
    # Configure MLflow with robust SQLite backend
    db_path = os.path.abspath("ml/experiments/mlflow.db")
    mlflow.set_tracking_uri(f"sqlite:///{db_path}")
    mlflow.set_experiment("SentimentIQ_Baseline")

    logger.info("Loading preprocessed training and evaluation data...")
    train_df = pd.read_parquet(os.path.join(data_dir, "tweeteval_3class_train.parquet"))
    val_df = pd.read_parquet(os.path.join(data_dir, "tweeteval_3class_validation.parquet"))
    test_df = pd.read_parquet(os.path.join(data_dir, "tweeteval_3class_test.parquet"))

    X_train_raw = train_df["text_baseline"]
    y_train = train_df["label_id"]

    X_val_raw = val_df["text_baseline"]
    y_val = val_df["label_id"]

    X_test_raw = test_df["text_baseline"]
    y_test = test_df["label_id"]

    with mlflow.start_run(run_name="TFIDF_LogisticRegression_Baseline"):
        mlflow.log_params({
            "model_architecture": "TF-IDF + LogisticRegression",
            "ngram_range": "(1, 2)",
            "max_features": max_features,
            "C": c_param,
            "class_weight": "balanced",
            "solver": "lbfgs",
            "random_seed": random_seed
        })

        logger.info(f"Fitting TF-IDF Vectorizer (max_features={max_features:,}, ngram_range=(1,2))...")
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=max_features,
            sublinear_tf=True
        )
        X_train = vectorizer.fit_transform(X_train_raw)
        X_val = vectorizer.transform(X_val_raw)
        X_test = vectorizer.transform(X_test_raw)

        logger.info("Training Logistic Regression classifier with balanced class weights...")
        classifier = LogisticRegression(
            C=c_param,
            class_weight="balanced",
            max_iter=1000,
            solver="lbfgs",
            random_state=random_seed
        )
        classifier.fit(X_train, y_train)

        # 1. Validation Set Evaluation
        y_val_pred = classifier.predict(X_val)
        val_acc = accuracy_score(y_val, y_val_pred)
        val_macro_f1 = f1_score(y_val, y_val_pred, average="macro")
        val_weighted_f1 = f1_score(y_val, y_val_pred, average="weighted")
        
        # 2. Independent Test Set Evaluation
        y_test_pred = classifier.predict(X_test)
        test_acc = accuracy_score(y_test, y_test_pred)
        test_macro_f1 = f1_score(y_test, y_test_pred, average="macro")
        test_weighted_f1 = f1_score(y_test, y_test_pred, average="weighted")
        test_macro_precision = precision_score(y_test, y_test_pred, average="macro")
        test_macro_recall = recall_score(y_test, y_test_pred, average="macro")
        per_class_f1 = f1_score(y_test, y_test_pred, average=None)

        logger.info(f"Validation Macro F1: {val_macro_f1:.4f} | Validation Acc: {val_acc:.4f}")
        logger.info(f"Test Macro F1: {test_macro_f1:.4f} | Test Acc: {test_acc:.4f}")

        # Log metrics to MLflow
        mlflow.log_metrics({
            "val_accuracy": val_acc,
            "val_macro_f1": val_macro_f1,
            "val_weighted_f1": val_weighted_f1,
            "test_accuracy": test_acc,
            "test_macro_f1": test_macro_f1,
            "test_weighted_f1": test_weighted_f1,
            "test_macro_precision": test_macro_precision,
            "test_macro_recall": test_macro_recall,
            "test_f1_negative": per_class_f1[0],
            "test_f1_neutral": per_class_f1[1],
            "test_f1_positive": per_class_f1[2]
        })

        # Generate Confusion Matrix Heatmap
        cm = confusion_matrix(y_test, y_test_pred)
        plt.figure(figsize=(6, 5))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=LABEL_NAMES,
            yticklabels=LABEL_NAMES
        )
        plt.title("Baseline Logistic Regression — Test Confusion Matrix", fontsize=11, fontweight="bold")
        plt.xlabel("Predicted Sentiment")
        plt.ylabel("True Sentiment")
        plt.tight_layout()
        cm_path = os.path.join(artifacts_dir, "confusion_matrix.png")
        plt.savefig(cm_path, dpi=200)
        plt.close()
        mlflow.log_artifact(cm_path)

        # Save Metrics & Artifacts
        metrics = {
            "model_type": "LogisticRegression_Baseline",
            "val_accuracy": round(float(val_acc), 4),
            "val_macro_f1": round(float(val_macro_f1), 4),
            "test_accuracy": round(float(test_acc), 4),
            "test_macro_f1": round(float(test_macro_f1), 4),
            "test_weighted_f1": round(float(test_weighted_f1), 4),
            "per_class_f1": {
                "negative": round(float(per_class_f1[0]), 4),
                "neutral": round(float(per_class_f1[1]), 4),
                "positive": round(float(per_class_f1[2]), 4)
            },
            "classification_report": classification_report(y_test, y_test_pred, target_names=LABEL_NAMES, output_dict=True)
        }

        metrics_file = os.path.join(artifacts_dir, "baseline_metrics.json")
        with open(metrics_file, "w") as f:
            json.dump(metrics, f, indent=2)

        model_file = os.path.join(artifacts_dir, "baseline_model.joblib")
        vec_file = os.path.join(artifacts_dir, "baseline_vectorizer.joblib")

        joblib.dump(classifier, model_file, compress=3)
        joblib.dump(vectorizer, vec_file, compress=3)

        logger.info(f"Baseline artifacts serialized to {artifacts_dir}")
        print("\n=== BASELINE TEST CLASSIFICATION REPORT ===")
        print(classification_report(y_test, y_test_pred, target_names=LABEL_NAMES))


if __name__ == "__main__":
    train_baseline()
