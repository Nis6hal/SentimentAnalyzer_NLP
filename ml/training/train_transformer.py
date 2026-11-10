"""
SentimentIQ - Transformer Fine-Tuning Module (Model B: DistilBERT / Model C: RoBERTa)
Adheres to Section 5, 7, & 8:
- Pretrained distilbert-base-uncased or roberta-base
- Sequence length capped at 128 (covering 99.5% of tweets)
- AdamW optimizer, lr 2e-5, weight decay 0.01
- Early stopping & best-model checkpointing on validation Macro F1
- MLflow tracking integration
"""

import os
import json
import logging
import argparse
from typing import Dict, Any
import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback
)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SentimentIQ.Transformer")

ID2LABEL = {0: "negative", 1: "neutral", 2: "positive"}
LABEL2ID = {"negative": 0, "neutral": 1, "positive": 2}


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    
    acc = accuracy_score(labels, preds)
    macro_f1 = f1_score(labels, preds, average="macro")
    weighted_f1 = f1_score(labels, preds, average="weighted")
    macro_prec = precision_score(labels, preds, average="macro", zero_division=0)
    macro_rec = recall_score(labels, preds, average="macro", zero_division=0)

    return {
        "accuracy": acc,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "macro_precision": macro_prec,
        "macro_recall": macro_rec
    }


def train_transformer(
    model_name: str = "distilbert-base-uncased",
    data_dir: str = "ml/data/processed",
    output_dir: str = "ml/artifacts/transformer",
    max_length: int = 128,
    batch_size: int = 16,
    num_epochs: int = 3,
    learning_rate: float = 2e-5,
    sample_limit: int = 3000
):
    os.makedirs(output_dir, exist_ok=True)
    
    # Configure MLflow SQLite backend
    db_path = os.path.abspath("ml/experiments/mlflow.db")
    mlflow.set_tracking_uri(f"sqlite:///{db_path}")
    mlflow.set_experiment("SentimentIQ_Transformers")

    logger.info(f"Loading data from {data_dir}...")
    train_df = pd.read_parquet(os.path.join(data_dir, "tweeteval_3class_train.parquet"))
    val_df = pd.read_parquet(os.path.join(data_dir, "tweeteval_3class_validation.parquet"))

    # Stratified sub-sample if on constrained CPU environment
    if sample_limit and sample_limit < len(train_df):
        logger.info(f"Subsampling {sample_limit:,} stratified training samples for CPU fine-tuning...")
        train_df = train_df.groupby("label_id", group_keys=False).apply(
            lambda x: x.sample(int(sample_limit * len(x) / len(train_df)), random_state=42)
        )

    logger.info(f"Final training set: {len(train_df):,} samples | Val set: {len(val_df):,} samples")

    logger.info(f"Loading tokenizer & model: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=3,
        id2label=ID2LABEL,
        label2id=LABEL2ID
    )

    def tokenize_fn(examples):
        return tokenizer(
            examples["text_clean"],
            padding="max_length",
            truncation=True,
            max_length=max_length
        )

    # Convert to Hugging Face Dataset format
    train_ds = Dataset.from_pandas(train_df[["text_clean", "label_id"]].rename(columns={"label_id": "label"}))
    val_ds = Dataset.from_pandas(val_df[["text_clean", "label_id"]].rename(columns={"label_id": "label"}))

    train_tokenized = train_ds.map(tokenize_fn, batched=True)
    val_tokenized = val_ds.map(tokenize_fn, batched=True)

    checkpoint_dir = os.path.join(output_dir, "checkpoints")

    training_args = TrainingArguments(
        output_dir=checkpoint_dir,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=learning_rate,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=num_epochs,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        logging_dir=os.path.join(output_dir, "logs"),
        logging_steps=50,
        save_total_limit=2,
        seed=42,
        report_to=[]  # Using native MLflow logger below
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_tokenized,
        eval_dataset=val_tokenized,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )

    with mlflow.start_run(run_name=f"FineTune_{model_name.replace('/', '_')}"):
        mlflow.log_params({
            "model_name": model_name,
            "max_length": max_length,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "num_epochs": num_epochs,
            "training_samples": len(train_df)
        })

        logger.info("Beginning transformer fine-tuning loop...")
        train_result = trainer.train()

        logger.info("Evaluating best model checkpoint on validation set...")
        eval_metrics = trainer.evaluate()
        logger.info(f"Validation Metrics: {eval_metrics}")

        # Log metrics to MLflow
        for k, v in eval_metrics.items():
            if isinstance(v, (int, float)):
                mlflow.log_metric(k, v)

        # Save Final Best Model Artifacts
        best_model_dir = os.path.join(output_dir, "best_model")
        trainer.save_model(best_model_dir)
        tokenizer.save_pretrained(best_model_dir)

        # Save metadata summary
        summary = {
            "model_name": model_name,
            "train_loss": train_result.training_loss,
            "eval_macro_f1": eval_metrics.get("eval_macro_f1"),
            "eval_accuracy": eval_metrics.get("eval_accuracy"),
            "best_checkpoint": trainer.state.best_model_checkpoint
        }
        with open(os.path.join(output_dir, "training_summary.json"), "w") as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Model and tokenizer successfully saved to {best_model_dir}")
        return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Transformer Sentiment Model")
    parser.add_argument("--model", type=str, default="distilbert-base-uncased")
    parser.add_argument("--samples", type=int, default=1500)
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch_size", type=int, default=16)
    args = parser.parse_args()

    train_transformer(
        model_name=args.model,
        sample_limit=args.samples,
        num_epochs=args.epochs,
        batch_size=args.batch_size
    )

