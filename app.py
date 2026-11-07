import os
import joblib
import pandas as pd
import streamlit as st

from utils import (
    sanitize_text,
    predict_sentiment,
    predict_sentiment_batch,
    MAX_TEXT_LENGTH
)
from styles import apply_styles, hero_html, result_card_html, footer_html

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sentify AI - Advanced Sentiment Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom Design System
apply_styles()

# ---------------------------------------------------------
# State Management
# ---------------------------------------------------------
if 'history' not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------------
# Artifact Loading (Cached & Resilient)
# ---------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_model_artifacts():
    """Loads vectorized models with fallback checks across joblib and pickle formats."""
    # Priority: .joblib then .pkl
    model_paths = ["sentiment_model.joblib", "sentiment_model.pkl"]
    vec_paths = ["vectorizer.joblib", "vectorizer.pkl"]
    
    clf = None
    vec = None
    
    for mp in model_paths:
        if os.path.exists(mp):
            try:
                clf = joblib.load(mp)
                break
            except Exception:
                pass
                
    for vp in vec_paths:
        if os.path.exists(vp):
            try:
                vec = joblib.load(vp)
                break
            except Exception:
                pass
                
    return vec, clf

vectorizer, classifier = load_model_artifacts()

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ Sentify Engine")
    
    if classifier is not None and vectorizer is not None:
        st.success("🟢 Model Status: Active")
        with st.expander("ℹ️ Model Architecture"):
            st.markdown(f"""
            - **Classifier:** Linear SVM (`C=1.0`)
            - **Vectorizer:** TF-IDF (Unigram + Bigram)
            - **Vocabulary Size:** `{len(vectorizer.vocabulary_):,}` features
            - **Classes:** `{', '.join(classifier.classes_)}`
            """)
    else:
        st.error("🔴 Model Status: Offline. Run `python training.py`.")

    st.divider()
    st.markdown("### 🕒 Real-time Session History")
    
    if not st.session_state.history:
        st.caption("No inquiries analyzed yet in this session.")
    else:
        color_map = {
            "positive": "#22c55e",
            "neutral": "#94a3b8",
            "negative": "#ef4444"
        }
        for item in reversed(st.session_state.history[-10:]):
            border_color = color_map.get(item['sentiment'], "#6366f1")
            st.markdown(f"""
                <div class="history-card" style="border-left-color: {border_color};">
                    <strong style="color: {border_color};">{item['sentiment'].upper()}</strong>
                    <span style="float: right; font-size: 0.8rem; opacity: 0.7;">{item['confidence']:.1%}</span>
                    <div style="font-size: 0.85rem; margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        {item['preview']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

# ---------------------------------------------------------
# Main UI Presentation
# ---------------------------------------------------------
st.markdown(hero_html(), unsafe_allow_html=True)

if classifier is None or vectorizer is None:
    st.error("⚠️ **Model Artifacts Missing!** Please execute `python training.py` in your terminal to generate the trained classifier and vectorizer.")
    st.stop()

tabs = st.tabs(["🎯 Instant Real-Time Analysis", "📊 High-Throughput Bulk Engine", "🧪 Model Performance & Insights"])

# ---------------------------------------------------------
# TAB 1: Instant Analysis
# ---------------------------------------------------------
with tabs[0]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💬 Single Sentence / Review Analysis")
    
    sample_col1, sample_col2, sample_col3 = st.columns(3)
    preset_text = ""
    with sample_col1:
        if st.button("💡 Sample: Positive", use_container_width=True):
            preset_text = "The solution saved a lot of time and worked perfectly."
    with sample_col2:
        if st.button("💡 Sample: Neutral", use_container_width=True):
            preset_text = "Rishi is reading a book at the desk."
    with sample_col3:
        if st.button("💡 Sample: Negative", use_container_width=True):
            preset_text = "I am deeply disappointed with the service."

    user_input = st.text_area(
        "Enter text to evaluate sentiment:",
        value=preset_text,
        placeholder="Type or paste customer feedback, tweet, or statement...",
        height=140,
        max_chars=MAX_TEXT_LENGTH,
        help=f"Maximum allowed length: {MAX_TEXT_LENGTH:,} characters (input is sanitized against XSS attacks)."
    )
    
    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        analyze_clicked = st.button("🚀 Analyze Polarity", use_container_width=True, type="primary")

    if analyze_clicked:
        sanitized_input = sanitize_text(user_input)
        if not sanitized_input:
            st.warning("⚠️ Please provide non-empty text input.")
        else:
            with st.spinner("Classifying sentiment vectors..."):
                label, confidence, breakdown, tokens = predict_sentiment(user_input, vectorizer, classifier)
                
                # Push to session history
                st.session_state.history.append({
                    "preview": user_input[:45] + ("..." if len(user_input) > 45 else ""),
                    "sentiment": label,
                    "confidence": confidence
                })
                
                # Render Rich Result Card
                st.markdown(result_card_html(label, confidence, breakdown, tokens), unsafe_allow_html=True)
                
                # Detailed probability distribution columns
                st.markdown("#### 📈 Multi-Class Probability Distribution")
                m_col1, m_col2, m_col3 = st.columns(3)
                with m_col1:
                    p_pos = breakdown.get("positive", 0.0)
                    st.metric(label="Positive", value=f"{p_pos:.1%}")
                    st.progress(p_pos)
                with m_col2:
                    p_neu = breakdown.get("neutral", 0.0)
                    st.metric(label="Neutral", value=f"{p_neu:.1%}")
                    st.progress(p_neu)
                with m_col3:
                    p_neg = breakdown.get("negative", 0.0)
                    st.metric(label="Negative", value=f"{p_neg:.1%}")
                    st.progress(p_neg)
                    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: High-Throughput Bulk Engine
# ---------------------------------------------------------
with tabs[1]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📁 Batch Processing & CSV Ingestion")
    st.caption("Upload CSV datasets for vectorized bulk classification with automated visualization.")
    
    uploaded_file = st.file_uploader(
        "Upload dataset (CSV format)",
        type=["csv"],
        help="Max file limit: 10,000 rows. Supported columns: Sentence, text, Content, sentence, comment, review."
    )
    
    if uploaded_file is not None:
        try:
            # Security: limit read size to avoid memory exhaustion
            df_bulk = pd.read_csv(uploaded_file, nrows=10000)
            
            # Smart column discovery
            candidate_cols = ['Sentence', 'text', 'Content', 'sentence', 'comment', 'review', 'Text', 'feedback']
            text_col = next((c for c in candidate_cols if c in df_bulk.columns), None)
            
            if not text_col:
                st.error(f"❌ Could not automatically detect a text column. Available columns: `{list(df_bulk.columns)}`. Please ensure your file has one of: {candidate_cols}")
            else:
                st.info(f"Target text column identified: **`{text_col}`** ({len(df_bulk):,} rows)")
                
                if st.button("⚡ Execute Batch Classification", type="primary"):
                    with st.spinner(f"Vectorizing and classifying {len(df_bulk):,} rows..."):
                        texts = df_bulk[text_col].fillna("").astype(str).tolist()
                        preds, confs = predict_sentiment_batch(texts, vectorizer, classifier)
                        
                        df_bulk['Predicted_Sentiment'] = preds
                        df_bulk['Confidence'] = [round(c, 4) for c in confs]
                        
                        st.success(f"Successfully processed {len(df_bulk):,} items!")
                        
                        # Summary metrics
                        c1, c2, c3 = st.columns(3)
                        counts = df_bulk['Predicted_Sentiment'].value_counts().to_dict()
                        c1.metric("😊 Positive Count", counts.get("positive", 0))
                        c2.metric("😐 Neutral Count", counts.get("neutral", 0))
                        c3.metric("😠 Negative Count", counts.get("negative", 0))
                        
                        # Visual breakdown
                        chart_col, table_col = st.columns([1, 2])
                        with chart_col:
                            st.markdown("#### Sentiment Distribution")
                            st.bar_chart(df_bulk['Predicted_Sentiment'].value_counts())
                        with table_col:
                            st.markdown("#### Preview (Top 10)")
                            st.dataframe(df_bulk.head(10), use_container_width=True)
                            
                        # Download output
                        csv_data = df_bulk.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Annotated CSV",
                            data=csv_data,
                            file_name="sentify_predictions.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 3: Model Performance & Dataset Insights
# ---------------------------------------------------------
with tabs[2]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Model Architecture & Training Profile")
    
    data_path = 'samples.csv' if os.path.exists('samples.csv') else os.path.join('data', 'samples.csv')
    if os.path.exists(data_path):
        raw_df = pd.read_csv(data_path)
        
        stat1, stat2, stat3 = st.columns(3)
        stat1.metric("Total Training Samples", f"{len(raw_df):,}")
        stat2.metric("Classes Supported", f"{raw_df['Sentiment'].nunique()}")
        stat3.metric("Max TF-IDF Features", f"{len(vectorizer.vocabulary_):,}")
        
        st.markdown("#### Training Label Balance")
        st.bar_chart(raw_df['Sentiment'].value_counts())
        
        with st.expander("🔎 View Ground Truth Dataset Sample"):
            st.dataframe(raw_df.head(15), use_container_width=True)
    else:
        st.info("Training dataset `samples.csv` not found in workspace.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown(footer_html(), unsafe_allow_html=True)
