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
    page_title="Sentify AI - Neomorphic Sentiment Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Neomorphic Design System
apply_styles()

# ---------------------------------------------------------
# Session State Management
# ---------------------------------------------------------
if 'history' not in st.session_state:
    st.session_state.history = []

if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# ---------------------------------------------------------
# Artifact Loading (Cached & Resilient)
# ---------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_model_artifacts():
    """Loads vectorized models with fallback checks across joblib and pickle formats."""
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
# Sidebar (Neomorphic Dashboard & History)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ Sentify Core")
    
    if classifier is not None and vectorizer is not None:
        st.markdown("""
            <div class="neu-well" style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                <span class="neu-pulse-dot"></span>
                <div>
                    <strong style="color: var(--text-primary); font-size: 0.95rem;">Model Status: Active</strong><br>
                    <small style="color: var(--text-secondary);">Linear SVM • Calibrated</small>
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("ℹ️ Model Architecture"):
            st.markdown(f"""
            - **Algorithm:** Linear SVM (`C=1.0`)
            - **Vectorizer:** TF-IDF (Unigram + Bigram)
            - **Vocabulary:** `{len(vectorizer.vocabulary_):,}` tokens
            - **Classes:** `{', '.join(classifier.classes_)}`
            """)
    else:
        st.error("🔴 Model Status: Offline. Run `python training.py` first.")

    st.markdown("### 🕒 Session History")
    
    if not st.session_state.history:
        st.markdown("""
            <div class="neu-well" style="text-align: center; color: var(--text-muted); font-size: 0.9rem;">
                No inquiries recorded yet.<br>Analyze a text to populate history.
            </div>
        """, unsafe_allow_html=True)
    else:
        color_map = {
            "positive": "var(--pos-color)",
            "neutral": "var(--neu-color)",
            "negative": "var(--neg-color)"
        }
        for item in reversed(st.session_state.history[-8:]):
            border_col = color_map.get(item['sentiment'], "var(--primary)")
            st.markdown(f"""
                <div class="neu-history-item" style="border-left-color: {border_col};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <strong style="color: {border_col}; font-size: 0.85rem; letter-spacing: 0.04em;">
                            {item['sentiment'].upper()}
                        </strong>
                        <span style="font-size: 0.8rem; font-family: var(--font-code); color: var(--text-muted);">
                            {item['confidence']:.1%}
                        </span>
                    </div>
                    <div style="font-size: 0.85rem; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        {item['preview']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        if st.button("🗑️ Clear Session History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

# ---------------------------------------------------------
# Main UI Presentation
# ---------------------------------------------------------
st.markdown(hero_html(), unsafe_allow_html=True)

if classifier is None or vectorizer is None:
    st.error("⚠️ **Model Artifacts Missing!** Execute `python training.py` in your terminal to train and serialize the model.")
    st.stop()

tabs = st.tabs([
    "🎯 Instant Real-Time Analysis",
    "📊 High-Throughput Bulk Engine",
    "🧪 Model Architecture & Data"
])

# ---------------------------------------------------------
# TAB 1: Instant Real-Time Analysis
# ---------------------------------------------------------
with tabs[0]:
    st.markdown('<div class="neu-card">', unsafe_allow_html=True)
    st.markdown("### 💬 Real-Time Polarity Evaluator")
    st.caption("Input text to predict emotional valence, compute multi-class probabilities, and extract key vocabulary signals.")
    
    # Tactile Sample Presets
    st.markdown("<p style='font-size: 0.85rem; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;'>Quick Test Presets:</p>", unsafe_allow_html=True)
    sample_col1, sample_col2, sample_col3 = st.columns(3)
    with sample_col1:
        if st.button("😊 Positive Sample", use_container_width=True):
            st.session_state.input_text = "The solution saved a lot of time and worked perfectly."
    with sample_col2:
        if st.button("😐 Neutral Sample", use_container_width=True):
            st.session_state.input_text = "Rishi is reading a book at the desk."
    with sample_col3:
        if st.button("😠 Negative Sample", use_container_width=True):
            st.session_state.input_text = "I am deeply disappointed with the service."

    user_input = st.text_area(
        label="Enter sentence, tweet, or review below:",
        value=st.session_state.input_text,
        placeholder="How do you feel about this today? Type here...",
        height=140,
        max_chars=MAX_TEXT_LENGTH,
        help=f"Enforced limit: {MAX_TEXT_LENGTH:,} characters. Protected against XSS injection."
    )

    # Live Text Telemetry
    chars_count = len(user_input)
    words_count = len(user_input.split()) if user_input.strip() else 0
    sentences_count = len([s for s in user_input.split('.') if s.strip()]) if user_input.strip() else 0
    reading_time_sec = max(1, round(words_count / 3.5)) if words_count > 0 else 0

    st.markdown(f"""
        <div class="neu-well" style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 10px; margin-top: 0.75rem; padding: 0.8rem 1.2rem;">
            <div style="text-align: center;">
                <span style="font-size: 0.78rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Characters</span><br>
                <strong style="font-size: 1rem; color: var(--text-primary); font-family: var(--font-code);">{chars_count}</strong>
            </div>
            <div style="text-align: center;">
                <span style="font-size: 0.78rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Words</span><br>
                <strong style="font-size: 1rem; color: var(--text-primary); font-family: var(--font-code);">{words_count}</strong>
            </div>
            <div style="text-align: center;">
                <span style="font-size: 0.78rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Sentences</span><br>
                <strong style="font-size: 1rem; color: var(--text-primary); font-family: var(--font-code);">{sentences_count}</strong>
            </div>
            <div style="text-align: center;">
                <span style="font-size: 0.78rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Read Time</span><br>
                <strong style="font-size: 1rem; color: var(--text-primary); font-family: var(--font-code);">~{reading_time_sec}s</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        analyze_clicked = st.button("🚀 Analyze Polarity", use_container_width=True, type="primary")

    if analyze_clicked or (user_input and user_input != st.session_state.input_text):
        st.session_state.input_text = user_input

    if user_input.strip() and analyze_clicked:
        sanitized_input = sanitize_text(user_input)
        with st.spinner("Calculating sentiment vectors..."):
            label, confidence, breakdown, tokens = predict_sentiment(sanitized_input, vectorizer, classifier)
            
            # Save into session history
            st.session_state.history.append({
                "preview": user_input[:45] + ("..." if len(user_input) > 45 else ""),
                "sentiment": label,
                "confidence": confidence
            })
            
            # Render Neomorphic Result Card
            st.markdown(result_card_html(label, confidence, breakdown, tokens), unsafe_allow_html=True)
            
            # Probability Breakdown
            st.markdown("<h4 style='color: var(--text-primary); margin-top: 1.5rem; margin-bottom: 0.75rem;'>📈 Calibrated Probability Distribution</h4>", unsafe_allow_html=True)
            m_col1, m_col2, m_col3 = st.columns(3)
            
            p_pos = breakdown.get("positive", 0.0)
            p_neu = breakdown.get("neutral", 0.0)
            p_neg = breakdown.get("negative", 0.0)

            with m_col1:
                st.markdown(f"""
                    <div class="neu-stat-tile" style="border-top: 4px solid var(--pos-color);">
                        <div class="neu-stat-num" style="color: var(--pos-color);">{p_pos:.1%}</div>
                        <div class="neu-stat-lbl">Positive Probability</div>
                    </div>
                """, unsafe_allow_html=True)
                st.progress(p_pos)

            with m_col2:
                st.markdown(f"""
                    <div class="neu-stat-tile" style="border-top: 4px solid var(--neu-color);">
                        <div class="neu-stat-num" style="color: var(--neu-color);">{p_neu:.1%}</div>
                        <div class="neu-stat-lbl">Neutral Probability</div>
                    </div>
                """, unsafe_allow_html=True)
                st.progress(p_neu)

            with m_col3:
                st.markdown(f"""
                    <div class="neu-stat-tile" style="border-top: 4px solid var(--neg-color);">
                        <div class="neu-stat-num" style="color: var(--neg-color);">{p_neg:.1%}</div>
                        <div class="neu-stat-lbl">Negative Probability</div>
                    </div>
                """, unsafe_allow_html=True)
                st.progress(p_neg)
                
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: High-Throughput Bulk Engine
# ---------------------------------------------------------
with tabs[1]:
    st.markdown('<div class="neu-card">', unsafe_allow_html=True)
    st.markdown("### 📁 High-Throughput Dataset Ingestion")
    st.caption("Upload CSV datasets for vectorized batch classification with automated visualization and report export.")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file for batch processing",
        type=["csv"],
        help="Max file limit: 10,000 rows. Auto-detects columns: Sentence, text, Content, sentence, comment, review."
    )
    
    if uploaded_file is not None:
        try:
            df_bulk = pd.read_csv(uploaded_file, nrows=10000)
            candidate_cols = ['Sentence', 'text', 'Content', 'sentence', 'comment', 'review', 'Text', 'feedback']
            text_col = next((c for c in candidate_cols if c in df_bulk.columns), None)
            
            if not text_col:
                st.error(f"❌ Could not find a text column. Available columns: `{list(df_bulk.columns)}`. Please include one of: {candidate_cols}")
            else:
                st.markdown(f"""
                    <div class="neu-well" style="display: flex; align-items: center; justify-content: space-between;">
                        <span>Target column identified: <strong>`{text_col}`</strong></span>
                        <span class="neu-token-tag">{len(df_bulk):,} Rows Loaded</span>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("⚡ Run Vectorized Batch Inference", type="primary", use_container_width=True):
                    with st.spinner(f"Vectorizing & classifying {len(df_bulk):,} entries..."):
                        texts = df_bulk[text_col].fillna("").astype(str).tolist()
                        preds, confs = predict_sentiment_batch(texts, vectorizer, classifier)
                        
                        df_bulk['Predicted_Sentiment'] = preds
                        df_bulk['Confidence'] = [round(c, 4) for c in confs]
                        
                        total_count = len(df_bulk)
                        counts = df_bulk['Predicted_Sentiment'].value_counts().to_dict()
                        pos_c = counts.get("positive", 0)
                        neu_c = counts.get("neutral", 0)
                        neg_c = counts.get("negative", 0)
                        
                        st.markdown("<h4 style='color: var(--text-primary); margin-top: 1.5rem;'>📊 Batch Inference Overview</h4>", unsafe_allow_html=True)
                        b1, b2, b3, b4 = st.columns(4)
                        with b1:
                            st.markdown(f"""
                                <div class="neu-stat-tile">
                                    <div class="neu-stat-num">{total_count:,}</div>
                                    <div class="neu-stat-lbl">Total Processed</div>
                                </div>
                            """, unsafe_allow_html=True)
                        with b2:
                            st.markdown(f"""
                                <div class="neu-stat-tile" style="border-top: 4px solid var(--pos-color);">
                                    <div class="neu-stat-num" style="color: var(--pos-color);">{pos_c:,}</div>
                                    <div class="neu-stat-lbl">Positive ({pos_c/total_count:.1%})</div>
                                </div>
                            """, unsafe_allow_html=True)
                        with b3:
                            st.markdown(f"""
                                <div class="neu-stat-tile" style="border-top: 4px solid var(--neu-color);">
                                    <div class="neu-stat-num" style="color: var(--neu-color);">{neu_c:,}</div>
                                    <div class="neu-stat-lbl">Neutral ({neu_c/total_count:.1%})</div>
                                </div>
                            """, unsafe_allow_html=True)
                        with b4:
                            st.markdown(f"""
                                <div class="neu-stat-tile" style="border-top: 4px solid var(--neg-color);">
                                    <div class="neu-stat-num" style="color: var(--neg-color);">{neg_c:,}</div>
                                    <div class="neu-stat-lbl">Negative ({neg_c/total_count:.1%})</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Charts and Table
                        chart_col, table_col = st.columns([1, 2])
                        with chart_col:
                            st.markdown("##### Class Distribution")
                            st.bar_chart(df_bulk['Predicted_Sentiment'].value_counts())
                        with table_col:
                            st.markdown("##### Annotated Dataset Sample")
                            st.dataframe(df_bulk[[text_col, 'Predicted_Sentiment', 'Confidence']].head(10), use_container_width=True)
                            
                        # Download Button
                        csv_data = df_bulk.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Classified Dataset (CSV)",
                            data=csv_data,
                            file_name="sentify_batch_predictions.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")
            
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 3: Model Architecture & Insights
# ---------------------------------------------------------
with tabs[2]:
    st.markdown('<div class="neu-card">', unsafe_allow_html=True)
    st.markdown("### 🧠 AI Engine Architecture & Training Profile")
    st.caption("Inspect underlying model parameters, feature extraction pipelines, and dataset balance.")
    
    data_path = 'samples.csv' if os.path.exists('samples.csv') else os.path.join('data', 'samples.csv')
    if os.path.exists(data_path):
        raw_df = pd.read_csv(data_path)
        
        stat1, stat2, stat3 = st.columns(3)
        with stat1:
            st.markdown(f"""
                <div class="neu-stat-tile">
                    <div class="neu-stat-num">{len(raw_df):,}</div>
                    <div class="neu-stat-lbl">Training Samples</div>
                </div>
            """, unsafe_allow_html=True)
        with stat2:
            st.markdown(f"""
                <div class="neu-stat-tile">
                    <div class="neu-stat-num">{raw_df['Sentiment'].nunique()}</div>
                    <div class="neu-stat-lbl">Sentiment Classes</div>
                </div>
            """, unsafe_allow_html=True)
        with stat3:
            st.markdown(f"""
                <div class="neu-stat-tile">
                    <div class="neu-stat-num">{len(vectorizer.vocabulary_):,}</div>
                    <div class="neu-stat-lbl">TF-IDF Features</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<h4 style='color: var(--text-primary); margin-top: 1rem;'>📊 Ground Truth Label Distribution</h4>", unsafe_allow_html=True)
        st.bar_chart(raw_df['Sentiment'].value_counts())
        
        with st.expander("🔎 Browse Ground Truth Dataset Sample"):
            st.dataframe(raw_df.head(20), use_container_width=True)
    else:
        st.info("Dataset file `samples.csv` not found in workspace.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown(footer_html(), unsafe_allow_html=True)
