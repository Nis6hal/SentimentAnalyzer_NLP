# 📊 Sentify AI - Intelligent Sentiment Analyzer

Sentify AI is an end-to-end Machine Learning sentiment intelligence platform engineered with Python, Scikit-Learn, and Streamlit. It delivers real-time polarity prediction, batch inference for CSV datasets, and interactive probability distributions.

---

## 🌟 Key Features

- **🎯 Real-Time Sentiment Polarity:** Instant analysis classifying text into Positive 😊, Neutral 😐, or Negative 😠.
- **📈 Multi-Class Confidence Breakdown:** Complete probability distribution and confidence score calculated using calibrated Linear SVM.
- **🧠 Token & Vocabulary Explainability:** Dynamic extraction and display of sentiment-influencing vocabulary features.
- **📁 High-Throughput Bulk Processing:** Vectorized batch inference supporting CSV uploads of up to 10,000 records with auto-discovery of text columns and downloadable annotated results.
- **🛡️ Enterprise-Grade Security:**
  - Input sanitization and HTML entity escaping to safeguard against stored and reflected Cross-Site Scripting (XSS).
  - Configurable string length bounds (`MAX_TEXT_LENGTH = 15,000`) and batch processing row caps to prevent Denial-of-Service (DoS) and RAM exhaustion.
  - Safe model deserialization supporting compressed `.joblib` format alongside legacy `.pkl`.
- **🎨 Glassmorphic Ambient Design System:** Modern UI with custom CSS, typography, responsive cards, and dynamic dark/light mode compatibility.

---

## 🏗️ Project Architecture

```
Sentiment Analyzer/
├── app.py                    # Streamlit web application & multi-tab UI
├── training.py               # Model training, validation, & artifact serialization
├── utils.py                  # NLP text sanitization, tokenization, & inference engine
├── styles.py                 # Modern design system & HTML/CSS layout templates
├── requirements.txt          # Python runtime dependencies
├── samples.csv               # Ground truth training dataset
├── sentiment_model.joblib    # High-performance compressed SVM model artifact
└── vectorizer.joblib         # Fitted TF-IDF (Unigram + Bigram) vectorizer artifact
```

---

## 🚀 Getting Started

### 1. Prerequisites & Virtual Environment
Ensure you have Python 3.10+ installed.

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate.bat
# Linux / macOS:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Train or Retrain the Model (Optional)
The project comes with pre-trained artifacts. To retrain on your dataset:
```bash
python training.py
```

### 4. Run the Web Application
```bash
streamlit run app.py
```
The application will launch automatically in your default browser at `http://localhost:8501`.

---

## 🧪 Model Details
- **Algorithm:** Support Vector Classifier (`SVC`) with a Linear kernel and probability calibration.
- **Feature Extraction:** TF-IDF Vectorizer with Sublinear Term Frequency (`ngram_range=(1, 2)` unigrams and bigrams).
- **Text Processing:** NLTK tokenization, WordNet lemmatization, contraction normalization, and negation-preserving stopword filtration.

---

## 👨‍💻 Author
**Nischal Bhandari**  
School of Engineering (SOE), Pokhara University
