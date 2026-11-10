"""
SentimentIQ - Exploratory Data Analysis (EDA) Module
Adheres to Milestone 3:
- Class distribution analysis across all splits
- Sequence length & word count distributions
- Top n-grams per sentiment class
- Export of metrics and charts into docs/ and ml/artifacts/eda/
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

from ml.preprocessing.cleaner import clean_text_baseline

# Target directories
ARTIFACTS_DIR = "ml/artifacts/eda"
DOCS_DIR = "docs"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

ID2LABEL = {0: "negative", 1: "neutral", 2: "positive"}
CLASS_COLORS = {"negative": "#e11d48", "neutral": "#0284c7", "positive": "#059669"}


def run_eda(data_dir: str = "ml/data/processed"):
    print("Loading processed splits...")
    train_df = pd.read_parquet(os.path.join(data_dir, "tweeteval_3class_train.parquet"))
    val_df = pd.read_parquet(os.path.join(data_dir, "tweeteval_3class_validation.parquet"))
    test_df = pd.read_parquet(os.path.join(data_dir, "tweeteval_3class_test.parquet"))

    # Map labels
    for df in [train_df, val_df, test_df]:
        df["sentiment_name"] = df["label_id"].map(ID2LABEL)

    # 1. Class Distribution Analysis
    print("Generating class distribution plots...")
    split_summary = []
    for name, df in [("Train", train_df), ("Validation", val_df), ("Test", test_df)]:
        counts = df["sentiment_name"].value_counts()
        total = len(df)
        for sentiment, count in counts.items():
            split_summary.append({
                "Split": name,
                "Sentiment": sentiment,
                "Count": count,
                "Percentage": (count / total) * 100
            })
    
    summary_df = pd.DataFrame(split_summary)
    
    plt.figure(figsize=(9, 5))
    palette = [CLASS_COLORS[s] for s in ["negative", "neutral", "positive"]]
    sns.barplot(data=summary_df, x="Split", y="Count", hue="Sentiment", palette=palette)
    plt.title("SentimentIQ - Class Distribution Across Dataset Splits", fontsize=13, fontweight="bold")
    plt.xlabel("Split", fontsize=11)
    plt.ylabel("Sample Count", fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    class_dist_plot = os.path.join(ARTIFACTS_DIR, "class_distribution.png")
    plt.savefig(class_dist_plot, dpi=200)
    plt.close()

    # 2. Sequence Length Distribution
    print("Analyzing sequence length distributions...")
    plt.figure(figsize=(10, 5))
    for sentiment, color in CLASS_COLORS.items():
        subset = train_df[train_df["sentiment_name"] == sentiment]
        sns.kdeplot(subset["word_len"], label=f"{sentiment.capitalize()} (Words)", color=color, fill=True, alpha=0.2)
    
    plt.title("Kernel Density Estimation of Word Counts per Sentiment Class (Train)", fontsize=13, fontweight="bold")
    plt.xlabel("Word Count", fontsize=11)
    plt.ylabel("Density", fontsize=11)
    plt.xlim(0, 45)
    plt.legend(frameon=True)
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    length_dist_plot = os.path.join(ARTIFACTS_DIR, "length_distribution.png")
    plt.savefig(length_dist_plot, dpi=200)
    plt.close()

    # 3. Top N-Grams per Class
    print("Extracting top n-grams per sentiment class...")
    ngram_stats = {}
    for sentiment in ["negative", "neutral", "positive"]:
        texts = train_df[train_df["sentiment_name"] == sentiment]["text_baseline"].tolist()
        words = []
        for t in texts:
            words.extend([w for w in t.split() if len(w) > 2 and w not in ["the", "and", "for", "that", "this", "with", "have", "are", "you", "user", "http"]])
        counter = Counter(words)
        ngram_stats[sentiment] = counter.most_common(12)

    # 4. Generate Comprehensive Markdown EDA Report
    report_path = os.path.join(DOCS_DIR, "exploratory_data_analysis.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 📊 SentimentIQ — Exploratory Data Analysis (EDA) Report\n\n")
        f.write("## 1. Overview & Provenance\n")
        f.write("- **Primary Benchmark Dataset**: `cardiffnlp/tweet_eval` (sentiment subset)\n")
        f.write(f"- **Total Samples Audited**: {len(train_df) + len(val_df) + len(test_df):,} samples\n")
        f.write(f"- **Splits**: Train ({len(train_df):,}), Validation ({len(val_df):,}), Test ({len(test_df):,})\n\n")
        
        f.write("## 2. Split Composition & Class Balance\n\n")
        f.write("| Split | Negative Count (%) | Neutral Count (%) | Positive Count (%) | Total |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        for split_name, df in [("Train", train_df), ("Validation", val_df), ("Test", test_df)]:
            counts = df["sentiment_name"].value_counts().to_dict()
            tot = len(df)
            f.write(f"| **{split_name}** | {counts.get('negative', 0):,} ({counts.get('negative',0)/tot*100:.1f}%) | {counts.get('neutral', 0):,} ({counts.get('neutral',0)/tot*100:.1f}%) | {counts.get('positive', 0):,} ({counts.get('positive',0)/tot*100:.1f}%) | {tot:,} |\n")

        f.write("\n> [!NOTE]\n")
        f.write("> **Class Imbalance Observation**: In the training split, `negative` samples constitute ~15.6% of the dataset, whereas `neutral` and `positive` comprise ~45.3% and ~39.1% respectively. Consequently, **Macro F1-score** is strictly mandated as the primary evaluation metric (Section 8) to penalize models that neglect minority negative expressions.\n\n")

        f.write("## 3. Sequence Length Characteristics\n\n")
        f.write("| Metric | Train Words | Train Chars | Validation Words | Test Words |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        f.write(f"| **Mean** | {train_df['word_len'].mean():.2f} | {train_df['char_len'].mean():.2f} | {val_df['word_len'].mean():.2f} | {test_df['word_len'].mean():.2f} |\n")
        f.write(f"| **Median** | {train_df['word_len'].median():.1f} | {train_df['char_len'].median():.1f} | {val_df['word_len'].median():.1f} | {test_df['word_len'].median():.1f} |\n")
        f.write(f"| **95th Percentile** | {train_df['word_len'].quantile(0.95):.1f} | {train_df['char_len'].quantile(0.95):.1f} | {val_df['word_len'].quantile(0.95):.1f} | {test_df['word_len'].quantile(0.95):.1f} |\n")
        f.write(f"| **Max** | {train_df['word_len'].max()} | {train_df['char_len'].max()} | {val_df['word_len'].max()} | {test_df['word_len'].max()} |\n\n")

        f.write("## 4. Top Vocabulary Signals per Sentiment Class\n\n")
        for sentiment, top_words in ngram_stats.items():
            words_str = ", ".join([f"`{w}` ({c})" for w, c in top_words])
            f.write(f"- **{sentiment.capitalize()}**: {words_str}\n")

        f.write("\n## 5. Artifacts Generated\n")
        f.write(f"- `ml/artifacts/eda/class_distribution.png`\n")
        f.write(f"- `ml/artifacts/eda/length_distribution.png`\n")

    print(f"EDA successfully completed! Report written to {report_path}")


if __name__ == "__main__":
    run_eda()

