import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from utils import preprocess_text

def train_and_save():
    # Resolve dataset path safely
    dataset_path = 'samples.csv' if os.path.exists('samples.csv') else os.path.join('data', 'samples.csv')
    print(f"Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    df = df.dropna(subset=['Sentence', 'Sentiment'])

    print(f"Dataset shape: {df.shape}")
    print("Class distribution:\n", df['Sentiment'].value_counts())

    print("\nPreprocessing sentences...")
    df['Sentence_Cleaned'] = df['Sentence'].apply(preprocess_text)
    # Remove any empty cleaned sentences
    df = df[df['Sentence_Cleaned'].str.strip() != ""]

    print("Fitting TF-IDF Vectorizer (ngram_range=(1,2))...")
    # Using unigrams and bigrams with sublinear tf scaling for better generalization
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        sublinear_tf=True
    )
    X = vectorizer.fit_transform(df['Sentence_Cleaned'])
    y = df['Sentiment']

    # Stratified split to maintain balance across classes
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training Linear SVM with probability calibration...")
    classifier = SVC(
        kernel='linear',
        C=1.0,
        probability=True,
        random_state=42
    )
    classifier.fit(X_train, y_train)

    # Evaluate model
    y_pred = classifier.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nTest Accuracy: {acc:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Save artifacts using joblib
    print("Saving artifacts with joblib...")
    joblib.dump(classifier, "sentiment_model.joblib", compress=3)
    joblib.dump(vectorizer, "vectorizer.joblib", compress=3)

    # Also maintain .pkl for legacy compatibility
    joblib.dump(classifier, "sentiment_model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")
    
    print("Training and serialization completed successfully!")

if __name__ == "__main__":
    train_and_save()
