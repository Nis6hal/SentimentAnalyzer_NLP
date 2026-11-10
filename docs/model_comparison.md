# 🏆 SentimentIQ — Model Comparison & Selection Report

## 1. Overview
In accordance with Sections 5, 7, and 8, this report presents an empirical, evidence-based evaluation comparing **Model A (TF-IDF + Logistic Regression)** against **Model C (Pretrained RoBERTa - CardiffNLP Twitter Sentiment)** on identical held-out test splits and the curated Challenge Evaluation Suite.

## 2. Test Set Benchmark Comparison (TweetEval 3-Class)

| Evaluation Metric | Model A: Logistic Regression | Model C: RoBERTa | Delta / Advantage |
| :--- | :--- | :--- | :--- |
| **Macro F1-Score (Primary)** | **0.5837** | **0.7043** | **+0.1206 (RoBERTa)** |
| **Overall Accuracy** | 0.5868 | 0.6990 | +0.1122 |
| **Weighted F1-Score** | 0.5865 | 0.6985 | +0.1120 |
| **F1 Negative (Minority)** | 0.5998 | 0.7009 | +0.1011 |
| **F1 Neutral** | 0.5860 | 0.6861 | +0.1002 |
| **F1 Positive** | 0.5655 | 0.7259 | +0.1604 |

## 3. Challenge Suite Performance
- **Baseline Accuracy**: 37.5% (6/16 cases)
- **RoBERTa Accuracy**: 75.0% (12/16 cases)

### Challenge Test Breakdown

| ID | Category | Sentence | Ground Truth | Baseline | RoBERTa |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `neg_01` | negation | "The movie was not bad at all, in fact I ..." | **positive** | ❌ negative | ✅ positive |
| `neg_02` | negation | "I can not say that I am satisfied with t..." | **negative** | ✅ negative | ✅ negative |
| `neg_03` | negation | "The hotel was by no means luxurious, but..." | **neutral** | ❌ negative | ✅ neutral |
| `neg_04` | negation | "Never disappointed by their punctual del..." | **positive** | ❌ negative | ✅ positive |
| `sarc_01` | sarcasm | "Oh fantastic, another software crash rig..." | **negative** | ❌ positive | ✅ negative |
| `sarc_02` | sarcasm | "Just wonderful, my flight was delayed fo..." | **negative** | ❌ positive | ❌ positive |
| `sarc_03` | sarcasm | "What a genius idea to schedule a mandato..." | **negative** | ❌ neutral | ❌ neutral |
| `mix_01` | mixed_sentiment | "The display and camera are absolutely st..." | **neutral** | ❌ negative | ❌ negative |
| `mix_02` | mixed_sentiment | "Customer support was polite and responsi..." | **neutral** | ❌ negative | ❌ positive |
| `info_01` | informal_slang | "Bro this new track is straight heat, tot..." | **positive** | ✅ positive | ✅ positive |
| `info_02` | informal_slang | "Ngl the food was mid and the wait time w..." | **negative** | ❌ positive | ✅ negative |
| `neu_01` | neutral_fact | "Pokhara University conducted the semeste..." | **neutral** | ✅ neutral | ✅ neutral |
| `neu_02` | neutral_fact | "The package arrived at 2:15 PM and was s..." | **neutral** | ✅ neutral | ✅ neutral |
| `neu_03` | neutral_fact | "This notebook contains 120 pages of rule..." | **neutral** | ✅ neutral | ✅ neutral |
| `long_01` | long_form | "Having tested dozens of wireless headpho..." | **positive** | ❌ neutral | ✅ positive |
| `long_02` | long_form | "We booked a three-night stay based on gl..." | **negative** | ✅ negative | ✅ negative |

## 4. Final Champion Model Selection
> **Selection Decision: RoBERTa (`cardiffnlp/twitter-roberta-base-sentiment-latest`)**
>
> RoBERTa substantially outperforms the baseline across all metrics—especially in context-dependent categories including **sarcasm**, **double negations** (*'not bad at all'*), and **informal expressions** (*'straight heat'*). The inference engine and FastAPI backend will package both models, designating RoBERTa as the champion model with graceful fallback to the lightweight baseline.
