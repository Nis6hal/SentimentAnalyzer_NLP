# 🧠 SentimentIQ — Enterprise NLP Sentiment Intelligence Platform

A production-grade, end-to-end sentiment analysis platform classifying English text into **POSITIVE**, **NEGATIVE**, and **NEUTRAL** using fine-tuned transformer models. Built with PyTorch, Hugging Face Transformers, FastAPI, React, TypeScript, and Tailwind CSS.

> **No mockups. No external sentiment APIs. Every prediction runs against real trained model weights with full Softmax probability distributions.**

---

## 📊 Live Benchmark Results

| Metric | Baseline (TF-IDF + LogReg) | Champion (RoBERTa) | Delta |
|:---|:---|:---|:---|
| **Macro F1-Score** | 0.5837 | **0.7043** | +12.06% |
| **Overall Accuracy** | 0.5868 | **0.6990** | +11.22% |
| **Challenge Suite (16 cases)** | 37.5% (6/16) | **75.0% (12/16)** | +37.5% |
| F1 Positive | 0.5655 | 0.7259 | +16.04% |
| F1 Neutral | 0.5860 | 0.6861 | +10.02% |
| F1 Negative | 0.5998 | 0.7009 | +10.11% |

---

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                        SentimentIQ Platform                      │
├──────────────┬──────────────────┬────────────────────────────────┤
│   Frontend   │     Backend      │         ML Pipeline            │
│              │                  │                                │
│  React 18    │  FastAPI         │  Dataset Acquisition           │
│  TypeScript  │  Pydantic        │  Preprocessing / EDA           │
│  Vite        │  SQLAlchemy      │  TF-IDF + LogReg Baseline      │
│  Tailwind    │  PostgreSQL      │  DistilBERT Fine-tuning        │
│  Recharts    │  SQLite fallback │  RoBERTa Champion Model        │
│  Lucide      │  Async Sessions  │  Challenge Evaluation Suite    │
│              │  CORS / Logging  │  MLflow Experiment Tracking    │
└──────────────┴──────────────────┴────────────────────────────────┘
```

---

## 📂 Repository Structure

```
SentimentIQ/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/     # health.py, sentiment.py
│   │   ├── core/config.py        # pydantic-settings configuration
│   │   ├── db/                   # session.py, base.py, migrations/
│   │   ├── models/entities.py    # SQLAlchemy ORM entities
│   │   ├── schemas/sentiment.py  # Pydantic request/response schemas
│   │   ├── services/             # Business logic + DB persistence
│   │   └── main.py               # FastAPI application entry point
│   ├── tests/test_api.py         # 9 integration tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/           # Navbar, SentimentBadge, ProbabilityBar
│   │   ├── pages/                # 9 pages (Landing → Settings)
│   │   ├── services/api.ts       # Axios API client
│   │   ├── types/sentiment.ts    # TypeScript interfaces
│   │   ├── App.tsx               # Root SPA router
│   │   └── main.tsx              # React DOM entry
│   ├── Dockerfile
│   ├── nginx.conf
│   └── vite.config.ts
├── ml/
│   ├── artifacts/
│   │   ├── baseline/             # Serialized TF-IDF + LogReg model
│   │   └── eda/                  # EDA plots (class & length distributions)
│   ├── data/
│   │   ├── processed/            # Parquet splits (train/val/test)
│   │   └── challenge_dataset.json
│   ├── evaluation/
│   │   ├── compare_models.py     # Model A vs C comparison + challenge suite
│   │   └── eda.py                # Exploratory data analysis
│   ├── inference/engine.py       # Dual-tier inference engine (RoBERTa + Baseline)
│   ├── preprocessing/
│   │   ├── cleaner.py            # Text normalization (HTML, contractions, Twitter)
│   │   └── pipeline.py           # Schema validation, dedup, split, parquet export
│   └── training/
│       ├── train_baseline.py     # TF-IDF + Logistic Regression
│       └── train_transformer.py  # DistilBERT / RoBERTa fine-tuning
├── tests/
│   ├── test_preprocessing.py     # 7 unit tests
│   └── test_inference.py         # 6 unit tests
├── docs/
│   ├── exploratory_data_analysis.md
│   └── model_comparison.md       # Empirical champion selection report
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** with pip
- **Node.js 18+** with npm
- (Optional) Docker & Docker Compose for containerized deployment

### 1. Clone the Repository

```bash
git clone https://github.com/Nis6hal/SentimentAnalyzer_NLP.git
cd SentimentAnalyzer_NLP
```

### 2. Install Python Dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Run the ML Pipeline (First Time Only)

```bash
# Preprocess TweetEval dataset
python -m ml.preprocessing.pipeline

# Train TF-IDF baseline
python -m ml.training.train_baseline

# Run model comparison (downloads RoBERTa checkpoint ~500MB)
python -m ml.evaluation.compare_models
```

### 4. Start the FastAPI Backend

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with interactive docs at `/docs`.

### 5. Start the React Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

---

## 🐳 Docker Compose (Full Stack)

```bash
docker-compose up --build
```

| Service | URL |
|:---|:---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |
| MLflow UI | http://localhost:5000 |
| PostgreSQL | localhost:5432 |

---

## 🔌 REST API Reference

### `POST /api/v1/analyze` — Single Text Analysis

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Absolutely fantastic experience!"}'
```

```json
{
  "success": true,
  "result": {
    "sentiment": "POSITIVE",
    "confidence": 0.9821,
    "probabilities": {
      "positive": 0.9821,
      "negative": 0.0054,
      "neutral": 0.0125
    },
    "model_version": "1.0.0",
    "model_id": "roberta-sentiment-v1.0",
    "latency_ms": 14.8
  }
}
```

### `POST /api/v1/analyze/batch` — Batch Processing (up to 500 texts)

```bash
curl -X POST http://localhost:8000/api/v1/analyze/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Great product", "Terrible service", "Meeting at 3 PM"]}'
```

### `GET /api/v1/history` — Paginated Analysis History

```bash
curl "http://localhost:8000/api/v1/history?page=1&page_size=20&sentiment=POSITIVE"
```

### `GET /api/v1/analytics` — Aggregate Intelligence Metrics

### `GET /api/v1/model/info` — Active Model Metadata & Benchmarks

### `POST /api/v1/feedback` — Submit Ground-Truth Correction

### `GET /api/v1/health` — Infrastructure Health Check

Full OpenAPI documentation: `http://localhost:8000/docs`

---

## 🧪 Testing

```bash
# Run entire test suite (22 tests)
python -m pytest tests/ backend/tests/ -v

# Preprocessing tests only
python -m pytest tests/test_preprocessing.py -v

# Inference engine tests only
python -m pytest tests/test_inference.py -v

# Backend API integration tests only
python -m pytest backend/tests/test_api.py -v
```

---

## 🤖 ML Models

### Model A: TF-IDF + Logistic Regression (Baseline)
- **Architecture:** TF-IDF (1–3 word n-grams, max 60k features) → Scikit-learn Logistic Regression with balanced class weights
- **Training Data:** TweetEval 3-class sentiment (45,583 samples)
- **Test Macro F1:** 0.5837
- **Strengths:** Ultra-fast CPU inference (<1ms), interpretable feature weights, zero GPU dependency
- **Weaknesses:** Cannot resolve negation inversions, sarcasm, or informal slang

### Model C: CardiffNLP RoBERTa (Champion)
- **Architecture:** 12-layer bidirectional RoBERTa transformer (`cardiffnlp/twitter-roberta-base-sentiment-latest`)
- **Pre-training:** Multi-domain conversational corpora (Twitter, reviews, social media)
- **Test Macro F1:** 0.7043
- **Challenge Suite:** 75.0% accuracy (negation, sarcasm, slang, mixed sentiment, long-form)
- **Inference:** Softmax-normalized 3-class probabilities with calibrated confidence scoring

### Selection Rationale

RoBERTa outperforms the baseline by **+12.06% Macro F1** and **2x** on the challenge suite. The inference engine loads RoBERTa as the champion model with graceful fallback to the baseline if transformer loading fails.

---

## 🎨 Frontend Pages

| # | Page | Description |
|:--|:-----|:------------|
| 1 | **Landing Page** | Hero section with key metrics, feature grid, and challenge suite demonstration |
| 2 | **Sentiment Analyzer** | Single-text input with presets, probability bars, confidence score, and feedback loop |
| 3 | **Batch Processor** | CSV upload/paste, bulk analysis table, downloadable annotated CSV export |
| 4 | **Executive Dashboard** | KPI cards, donut chart, live analysis stream, model health summary |
| 5 | **Analytics** | Temporal sentiment trajectory (area chart), volume breakdown (bar chart), ratio cards |
| 6 | **Audit History** | Paginated table with sentiment filter, inspection modal, full-text drill-down |
| 7 | **Model Intelligence** | Benchmark matrix, challenge suite showcase, architecture specifications |
| 8 | **API Reference** | Interactive endpoint documentation with cURL snippets and JSON responses |
| 9 | **Settings** | Infrastructure health diagnostics, inference engine preference, API URL configuration |

---

## 📦 Technology Stack

| Layer | Technologies |
|:------|:-------------|
| **Machine Learning** | Python, PyTorch, Hugging Face Transformers, Scikit-learn, Pandas, NumPy, Matplotlib |
| **Backend** | FastAPI, Pydantic, SQLAlchemy 2.0 (Async), PostgreSQL / SQLite |
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS v4, Recharts, Lucide Icons, Axios |
| **DevOps** | Docker, Docker Compose, MLflow, Pytest |

---

## 📜 Dataset Provenance

| Dataset | Source | Classes | Usage |
|:--------|:-------|:--------|:------|
| **TweetEval Sentiment** | `cardiffnlp/tweet_eval` (sentiment) | Positive, Negative, Neutral | Primary 3-class training, validation, and test |
| **SST-2** | `stanfordnlp/sst2` | Positive, Negative | Short-text binary evaluation |
| **IMDb** | `stanfordnlp/imdb` | Positive, Negative | Long-form binary baseline |
| **Challenge Suite** | Hand-curated (16 samples) | All 3 classes | Negation, sarcasm, slang, mixed sentiment |

---

## 📄 License

This project is for educational and research purposes. Model weights from Hugging Face Hub are subject to their respective licenses.

---

**Built with ❤️ by Nischal**
