import re
import html
import joblib
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Ensure required NLTK resources are available
for package in ['stopwords', 'wordnet', 'omw-1.4', 'punkt', 'punkt_tab']:
    try:
        nltk.data.find(f"tokenizers/{package}" if 'punkt' in package else f"corpora/{package}")
    except LookupError:
        nltk.download(package, quiet=True)

# Preserve negation and sentiment-bearing modifiers
NEGATION_WORDS = {
    'no', 'not', 'nor', 'neither', 'never', 'none',
    'hardly', 'scarcely', 'barely', "n't", "don't", "doesn't",
    "didn't", "won't", "wouldn't", "can't", "cannot", "couldn't"
}
STOP_WORDS = set(stopwords.words('english')) - NEGATION_WORDS
LEMMATIZER = WordNetLemmatizer()

# Max text length for security / DoS protection (15,000 chars per single submission)
MAX_TEXT_LENGTH = 15000

def sanitize_text(text: str) -> str:
    """Sanitizes user input by escaping HTML and enforcing length limits."""
    if not isinstance(text, str):
        text = str(text)
    # Strip dangerous null bytes and excess whitespace
    text = text.replace('\x00', '')
    if len(text) > MAX_TEXT_LENGTH:
        text = text[:MAX_TEXT_LENGTH]
    # Clean HTML escaping
    return html.escape(text.strip())

def preprocess_text(text: str) -> str:
    """Preprocesses raw text: lowercase, contraction normalization, tokenization, lemmatization."""
    if not isinstance(text, str):
        text = str(text)
    
    text = text.lower()
    # Normalize standard contractions
    text = re.sub(r"n't\b", " not", text)
    text = re.sub(r"'re\b", " are", text)
    text = re.sub(r"'s\b", "", text)
    text = re.sub(r"'d\b", " would", text)
    text = re.sub(r"'ll\b", " will", text)
    text = re.sub(r"'t\b", " not", text)
    text = re.sub(r"'ve\b", " have", text)
    text = re.sub(r"'m\b", " am", text)

    # Replace URLs and emails with generic tags
    text = re.sub(r"https?://\S+|www\.\S+", " url ", text)
    text = re.sub(r"\S+@\S+\.\S+", " email ", text)

    # Keep alphanumerics and spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    
    # Tokenize
    words = word_tokenize(text)
    
    # Remove stopwords (preserving negations) & lemmatize
    cleaned_tokens = [LEMMATIZER.lemmatize(w) for w in words if w not in STOP_WORDS and len(w) > 1]
    return ' '.join(cleaned_tokens)

def predict_sentiment(text: str, vectorizer, classifier):
    """
    Predicts sentiment for a single text input.
    Returns:
        label (str): Predicted sentiment class ('positive', 'neutral', 'negative')
        confidence (float): Confidence score of the predicted class (0.0 to 1.0)
        breakdown (dict): Probability distribution across all available classes
        word_highlights (list): Top influential words detected in input
    """
    cleaned = preprocess_text(text)
    if not cleaned.strip():
        return "neutral", 0.5, {"positive": 0.33, "neutral": 0.34, "negative": 0.33}, []

    vec = vectorizer.transform([cleaned])
    probs = classifier.predict_proba(vec)[0]
    classes = list(classifier.classes_)
    breakdown = {cls: float(prob) for cls, prob in zip(classes, probs)}
    
    # Select label matching highest probability
    label = max(breakdown, key=breakdown.get)
    confidence = breakdown[label]

    # Extract detected vocabulary tokens for explainability
    words = cleaned.split()
    vocab = vectorizer.vocabulary_
    matched_words = [w for w in set(words) if w in vocab]

    return label, confidence, breakdown, matched_words

def predict_sentiment_batch(texts: list, vectorizer, classifier, max_rows: int = 10000):
    """
    Secure high-performance vectorized batch prediction for uploaded files.
    Enforces row limits to prevent DoS memory overflow.
    """
    if len(texts) > max_rows:
        texts = texts[:max_rows]
        
    cleaned_texts = [preprocess_text(str(t)[:MAX_TEXT_LENGTH]) for t in texts]
    vecs = vectorizer.transform(cleaned_texts)
    
    preds = classifier.predict(vecs)
    probs = classifier.predict_proba(vecs)
    
    classes = list(classifier.classes_)
    class_to_idx = {cls: idx for idx, cls in enumerate(classes)}
    
    confidences = [float(prob[class_to_idx[pred]]) for pred, prob in zip(preds, probs)]
    return list(preds), confidences
