import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
        
        :root {
            --font-main: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            --font-code: 'JetBrains Mono', monospace;
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
            --card-glass: rgba(255, 255, 255, 0.05);
            --border-glass: rgba(255, 255, 255, 0.1);
        }

        html, body, [class*="css"] {
            font-family: var(--font-main) !important;
        }

        /* Ambient Hero Header */
        .hero-banner {
            position: relative;
            text-align: center;
            padding: 3.5rem 1.5rem 2.5rem 1.5rem;
            background: radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.18) 0%, rgba(139, 92, 246, 0.04) 60%, transparent 100%);
            border-radius: 28px;
            border: 1px solid rgba(128, 128, 128, 0.15);
            backdrop-filter: blur(16px);
            margin-bottom: 2rem;
            overflow: hidden;
        }

        .hero-title {
            background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: clamp(2.4rem, 5vw, 3.8rem);
            font-weight: 800;
            letter-spacing: -0.04em;
            margin-bottom: 0.75rem;
            line-height: 1.1;
        }

        .hero-tagline {
            font-size: 1.15rem;
            color: var(--text-color);
            opacity: 0.85;
            max-width: 640px;
            margin: 0 auto 1.25rem auto;
            line-height: 1.6;
        }

        .badge-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 14px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            background: rgba(99, 102, 241, 0.12);
            border: 1px solid rgba(99, 102, 241, 0.25);
            color: #818cf8;
            margin-bottom: 0.75rem;
        }

        /* Glassmorphic Content Card */
        .glass-card {
            background: rgba(128, 128, 128, 0.04);
            border-radius: 22px;
            padding: 2rem;
            border: 1px solid rgba(128, 128, 128, 0.12);
            backdrop-filter: blur(12px);
            margin-bottom: 1.5rem;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        .glass-card:hover {
            border-color: rgba(99, 102, 241, 0.3);
            box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.15);
        }

        /* Result Cards */
        .result-container {
            border-radius: 20px;
            padding: 1.75rem;
            margin-top: 1.5rem;
            border: 1px solid;
            animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(16px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .result-positive {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.12) 0%, rgba(16, 185, 129, 0.04) 100%);
            border-color: rgba(34, 197, 94, 0.35);
            color: #22c55e;
        }

        .result-neutral {
            background: linear-gradient(135deg, rgba(148, 163, 184, 0.12) 0%, rgba(100, 116, 139, 0.04) 100%);
            border-color: rgba(148, 163, 184, 0.35);
            color: #94a3b8;
        }

        .result-negative {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(220, 38, 38, 0.04) 100%);
            border-color: rgba(239, 68, 68, 0.35);
            color: #ef4444;
        }

        .result-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
        }

        .result-title {
            font-size: 1.6rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 0;
        }

        .confidence-chip {
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 700;
            background: rgba(0, 0, 0, 0.2);
        }

        /* Token Pills */
        .token-tag {
            display: inline-block;
            padding: 3px 10px;
            margin: 3px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-family: var(--font-code);
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: #818cf8;
        }

        /* Metric cards */
        .metric-box {
            text-align: center;
            padding: 1.2rem;
            border-radius: 16px;
            background: rgba(128, 128, 128, 0.05);
            border: 1px solid rgba(128, 128, 128, 0.1);
        }
        .metric-val {
            font-size: 1.7rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }
        .metric-lbl {
            font-size: 0.8rem;
            opacity: 0.7;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* History items */
        .history-card {
            padding: 0.85rem 1rem;
            border-radius: 12px;
            margin-bottom: 0.6rem;
            border-left: 4px solid;
            background: rgba(128, 128, 128, 0.06);
            transition: transform 0.15s ease;
        }
        .history-card:hover {
            transform: translateX(4px);
        }

        /* Streamlit widget tweaks */
        .stTextArea textarea {
            border-radius: 14px !important;
            border: 1px solid rgba(128, 128, 128, 0.2) !important;
            padding: 1rem !important;
            font-size: 1rem !important;
            background: rgba(128, 128, 128, 0.03) !important;
        }
        .stButton button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }

        /* Footer */
        .premium-footer {
            text-align: center;
            padding: 3.5rem 1rem 2rem 1rem;
            margin-top: 3rem;
            border-top: 1px solid rgba(128, 128, 128, 0.12);
            color: var(--text-color);
            opacity: 0.75;
            font-size: 0.9rem;
        }
        .premium-footer strong {
            color: #818cf8;
        }
        </style>
    """, unsafe_allow_html=True)

def hero_html():
    return """
        <div class="hero-banner">
            <div class="badge-pill">⚡ Powered by Scikit-Learn Linear SVM + TF-IDF</div>
            <h1 class="hero-title">Sentify AI</h1>
            <p class="hero-tagline">
                State-of-the-art sentiment intelligence engine designed to analyze sentiment polarity with fine-grained probability distributions.
            </p>
        </div>
    """

def result_card_html(label: str, confidence: float, breakdown: dict, matched_tokens: list):
    icons = {"positive": "😊", "neutral": "😐", "negative": "😠"}
    icon = icons.get(label, "🔍")
    css_class = f"result-{label}"

    tokens_html = "".join([f'<span class="token-tag">{token}</span>' for token in matched_tokens]) if matched_tokens else "<span style='opacity:0.6;font-size:0.85rem;'>None detected in vocabulary</span>"

    return f"""
        <div class="result-container {css_class}">
            <div class="result-header">
                <div class="result-title">{icon} {label.upper()}</div>
                <div class="confidence-chip">{confidence:.1%} Match</div>
            </div>
            <div style="margin-top: 1rem; margin-bottom: 0.5rem; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.8;">
                Key Vocabulary Signals Detected:
            </div>
            <div>{tokens_html}</div>
        </div>
    """

def footer_html():
    return """
        <div class="premium-footer">
            Designed & Engineered with ❤️ by <strong>Nischal Bhandari</strong><br>
            School of Engineering (SOE) • Pokhara University
        </div>
    """
