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
from styles import (
    apply_styles,
    hero_html,
    telemetry_bar_html,
    result_card_html,
    probability_cards_html,
    footer_html
)

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sentify AI - Neomorphic Sentiment Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Neomorphic Styling
apply_styles()

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if 'history' not in st.session_state:
    st.session_state.history = []

if 'current_text' not in st.session_state:
    st.session_state.current_text = ""

# ---------------------------------------------------------
# Resilient Artifact Loader
# ---------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_model_artifacts():
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
        st.markdown("""
            <div style="background: var(--neu-surface); border-radius: 14px; padding: 10px 14px; box-shadow: var(--shadow-inset-sm); display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                <span class="neu-led-dot"></span>
                <div>
                    <strong style="color: var(--text-primary); font-size: 0.92rem;">Model Active</strong><br>
                    <small style="color: var(--text-secondary);">Linear SVM (Calibrated)</small>
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("ℹ️ Model Architecture"):
            st.markdown(f"""
            - **Classifier:** Linear SVM (`C=1.0`)
            - **Vectorizer:** TF-IDF (1-2 N-grams)
            - **Vocabulary Size:** `{len(vectorizer.vocabulary_):,}` tokens
            - **Target Classes:** `{', '.join(classifier.classes_)}`
            """)
    else:
        st.error("🔴 Model Offline. Run `python training.py`.")

    st.markdown("### 🕒 Session History")
    
    if not st.session_state.history:
        st.markdown("""
            <div style="background: var(--neu-surface); border-radius: 14px; padding: 14px; box-shadow: var(--shadow-inset-sm); text-align: center; color: var(--text-muted); font-size: 0.88rem;">
                No analyses recorded yet.<br>Test a sentence to populate history.
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
                <div class="neu-history-card" style="border-left-color: {border_col};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px;">
                        <strong style="color: {border_col}; font-size: 0.82rem; letter-spacing: 0.04em;">
                            {item['sentiment'].upper()}
                        </strong>
                        <span style="font-size: 0.78rem; font-family: var(--font-code); color: var(--text-muted);">
                            {item['confidence']:.1%}
                        </span>
                    </div>
                    <div style="font-size: 0.82rem; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        {item['preview']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        if st.button("🗑️ Clear Session History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

# ---------------------------------------------------------
# Hero Banner
# ---------------------------------------------------------
st.markdown(hero_html(), unsafe_allow_html=True)

if classifier is None or vectorizer is None:
    st.error("⚠️ **Model Artifacts Missing!** Execute `python training.py` in your terminal to build the model.")
    st.stop()

# ---------------------------------------------------------
# Tabs Navigation
# ---------------------------------------------------------
tabs = st.tabs([
    "🎯 Instant Real-Time Analysis",
    "📊 High-Throughput Bulk Engine",
    "🧪 Model Architecture & Data"
])

# ---------------------------------------------------------
# TAB 1: Instant Real-Time Analysis
# ---------------------------------------------------------
with tabs[0]:
    with st.container(border=True):
        st.markdown("### 💬 Single Sentence Analysis")
        st.caption("Input feedback, tweets, or sentences to evaluate emotional polarity and token explainability.")

        # Presets row
        st.markdown("<p style='font-size: 0.82rem; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;'>Quick Test Presets:</p>", unsafe_allow_html=True)
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            if st.button("😊 Positive Preset", use_container_width=True):
                st.session_state.current_text = "The solution saved a lot of time and worked perfectly."
        with col_p2:
            if st.button("😐 Neutral Preset", use_container_width=True):
                st.session_state.current_text = "Rishi is reading a book at the desk."
        with col_p3:
            if st.button("😠 Negative Preset", use_container_width=True):
                st.session_state.current_text = "I am deeply disappointed with the service."

        user_input = st.text_area(
            label="Enter text for sentiment analysis:",
            value=st.session_state.current_text,
            placeholder="Type or paste customer feedback, tweet, or statement here...",
            height=130,
            max_chars=MAX_TEXT_LENGTH,
            help=f"Character limit: {MAX_TEXT_LENGTH:,} characters. Protected against XSS."
        )

        # Real-time Telemetry Calculations
        chars_count = len(user_input)
        words_count = len(user_input.split()) if user_input.strip() else 0
        sentences_count = len([s for s in user_input.split('.') if s.strip()]) if user_input.strip() else 0
        reading_time_sec = max(1, round(words_count / 3.5)) if words_count > 0 else 0

        st.markdown(telemetry_bar_html(chars_count, words_count, sentences_count, reading_time_sec), unsafe_allow_html=True)

        col_run, _ = st.columns([1, 2])
        with col_run:
            analyze_clicked = st.button("🚀 Analyze Polarity", use_container_width=True, type="primary")

        if user_input and user_input != st.session_state.current_text:
            st.session_state.current_text = user_input

        if analyze_clicked:
            if not user_input.strip():
                st.warning("⚠️ Please provide non-empty text input.")
            else:
                sanitized_input = sanitize_text(user_input)
                with st.spinner("Evaluating sentiment vectors..."):
                    label, confidence, breakdown, tokens = predict_sentiment(sanitized_input, vectorizer, classifier)
                    
                    # Append to session history
                    st.session_state.history.append({
                        "preview": user_input[:45] + ("..." if len(user_input) > 45 else ""),
                        "sentiment": label,
                        "confidence": confidence
                    })
                    
                    # Render Neomorphic Result Card
                    st.markdown(result_card_html(label, confidence, breakdown, tokens), unsafe_allow_html=True)
                    
                    # Render Probability Distribution Cards
                    st.markdown("<h4 style='color: var(--text-primary); margin-top: 1rem; margin-bottom: 0.5rem;'>📈 Calibrated Class Probabilities</h4>", unsafe_allow_html=True)
                    p_pos = breakdown.get("positive", 0.0)
                    p_neu = breakdown.get("neutral", 0.0)
                    p_neg = breakdown.get("negative", 0.0)
                    st.markdown(probability_cards_html(p_pos, p_neu, p_neg), unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: High-Throughput Bulk Engine
# ---------------------------------------------------------
with tabs[1]:
    with st.container(border=True):
        st.markdown("### 📁 High-Throughput Bulk Analysis")
        st.caption("Upload CSV datasets for high-speed vectorized batch classification and export annotated reports.")

        uploaded_file = st.file_uploader(
            label="Upload CSV dataset",
            type=["csv"],
            help="Maximum limit: 10,000 rows. Auto-detects columns: Sentence, text, Content, comment, review."
        )

        if uploaded_file is not None:
            try:
                df_bulk = pd.read_csv(uploaded_file, nrows=10000)
                candidate_cols = ['Sentence', 'text', 'Content', 'sentence', 'comment', 'review', 'Text', 'feedback']
                text_col = next((c for c in candidate_cols if c in df_bulk.columns), None)

                if not text_col:
                    st.error(f"❌ Could not find a text column. Available columns: `{list(df_bulk.columns)}`. Please include one of: {candidate_cols}")
                else:
                    st.info(f"Target column detected: **`{text_col}`** ({len(df_bulk):,} rows loaded)")

                    if st.button("⚡ Run Batch Inference", type="primary", use_container_width=True):
                        with st.spinner(f"Classifying {len(df_bulk):,} entries..."):
                            texts = df_bulk[text_col].fillna("").astype(str).tolist()
                            preds, confs = predict_sentiment_batch(texts, vectorizer, classifier)

                            df_bulk['Predicted_Sentiment'] = preds
                            df_bulk['Confidence'] = [round(c, 4) for c in confs]

                            total = len(df_bulk)
                            counts = df_bulk['Predicted_Sentiment'].value_counts().to_dict()
                            pos_c = counts.get("positive", 0)
                            neu_c = counts.get("neutral", 0)
                            neg_c = counts.get("negative", 0)

                            st.markdown("<h4 style='color: var(--text-primary); margin-top: 1.2rem;'>📊 Batch Inference Overview</h4>", unsafe_allow_html=True)
                            
                            c1, c2, c3, c4 = st.columns(4)
                            with c1:
                                st.markdown(f"""
                                    <div class="neu-card-tile">
                                        <div class="neu-tile-val">{total:,}</div>
                                        <div class="neu-tile-lbl">Total Samples</div>
                                    </div>
                                """, unsafe_allow_html=True)
                            with c2:
                                st.markdown(f"""
                                    <div class="neu-card-tile" style="border-top: 4px solid var(--pos-color);">
                                        <div class="neu-tile-val" style="color: var(--pos-color);">{pos_c:,}</div>
                                        <div class="neu-tile-lbl">Positive ({pos_c/total:.1%})</div>
                                    </div>
                                """, unsafe_allow_html=True)
                            with c3:
                                st.markdown(f"""
                                    <div class="neu-card-tile" style="border-top: 4px solid var(--neu-color);">
                                        <div class="neu-tile-val" style="color: var(--neu-color);">{neu_c:,}</div>
                                        <div class="neu-tile-lbl">Neutral ({neu_c/total:.1%})</div>
                                    </div>
                                """, unsafe_allow_html=True)
                            with c4:
                                st.markdown(f"""
                                    <div class="neu-card-tile" style="border-top: 4px solid var(--neg-color);">
                                        <div class="neu-tile-val" style="color: var(--neg-color);">{neg_c:,}</div>
                                        <div class="neu-tile-lbl">Negative ({neg_c/total:.1%})</div>
                                    </div>
                                """, unsafe_allow_html=True)

                            col_chart, col_table = st.columns([1, 2])
                            with col_chart:
                                st.markdown("##### Distribution")
                                st.bar_chart(df_bulk['Predicted_Sentiment'].value_counts())
                            with col_table:
                                st.markdown("##### Annotated Sample (Top 10)")
                                st.dataframe(df_bulk[[text_col, 'Predicted_Sentiment', 'Confidence']].head(10), use_container_width=True)

                            csv_data = df_bulk.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="📥 Download Annotated CSV",
                                data=csv_data,
                                file_name="sentify_predictions.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
            except Exception as e:
                st.error(f"Error parsing CSV: {str(e)}")

# ---------------------------------------------------------
# TAB 3: Model Architecture & Data
# ---------------------------------------------------------
with tabs[2]:
    with st.container(border=True):
        st.markdown("### 🧠 AI Engine Architecture & Ground Truth")
        st.caption("Inspect underlying model parameters, feature extraction pipelines, and dataset balance.")

        data_path = 'samples.csv' if os.path.exists('samples.csv') else os.path.join('data', 'samples.csv')
        if os.path.exists(data_path):
            raw_df = pd.read_csv(data_path)

            stat1, stat2, stat3 = st.columns(3)
            with stat1:
                st.markdown(f"""
                    <div class="neu-card-tile">
                        <div class="neu-tile-val">{len(raw_df):,}</div>
                        <div class="neu-tile-lbl">Training Samples</div>
                    </div>
                """, unsafe_allow_html=True)
            with stat2:
                st.markdown(f"""
                    <div class="neu-card-tile">
                        <div class="neu-tile-val">{raw_df['Sentiment'].nunique()}</div>
                        <div class="neu-tile-lbl">Target Classes</div>
                    </div>
                """, unsafe_allow_html=True)
            with stat3:
                st.markdown(f"""
                    <div class="neu-card-tile">
                        <div class="neu-tile-val">{len(vectorizer.vocabulary_):,}</div>
                        <div class="neu-tile-lbl">TF-IDF Features</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<h4 style='color: var(--text-primary); margin-top: 1rem;'>📊 Training Label Balance</h4>", unsafe_allow_html=True)
            st.bar_chart(raw_df['Sentiment'].value_counts())

            with st.expander("🔎 Browse Ground Truth Dataset"):
                st.dataframe(raw_df.head(25), use_container_width=True)
        else:
            st.info("Dataset file `samples.csv` not found in workspace.")

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown(footer_html(), unsafe_allow_html=True)
