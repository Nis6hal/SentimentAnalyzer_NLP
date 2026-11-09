import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

        /* -------------------------------------------------------------
           NEUMORPHIC DESIGN SYSTEM TOKENS (LIGHT & DARK ADAPTIVE)
        ------------------------------------------------------------- */
        :root {
            --font-main: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            --font-code: 'JetBrains Mono', monospace;

            /* Light Neumorphism Default */
            --bg-base: #e8ecf2;
            --neu-surface: #e8ecf2;
            --neu-dark: #c2cbd6;
            --neu-light: #ffffff;
            --neu-dark-rgb: 194, 203, 214;
            --neu-light-rgb: 255, 255, 255;

            /* Shadows */
            --shadow-raised: 8px 8px 18px var(--neu-dark), -8px -8px 18px var(--neu-light);
            --shadow-raised-sm: 4px 4px 10px var(--neu-dark), -4px -4px 10px var(--neu-light);
            --shadow-raised-lg: 14px 14px 28px var(--neu-dark), -14px -14px 28px var(--neu-light);
            --shadow-inset: inset 4px 4px 8px var(--neu-dark), inset -4px -4px 8px var(--neu-light);
            --shadow-inset-sm: inset 2px 2px 5px var(--neu-dark), inset -2px -2px 5px var(--neu-light);

            /* Typography & Colors */
            --text-primary: #2d3748;
            --text-secondary: #64748b;
            --text-muted: #94a3b8;

            /* Accents */
            --primary: #6366f1;
            --primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            --primary-glow: rgba(99, 102, 241, 0.35);

            /* Sentiment Accents */
            --pos-color: #10b981;
            --pos-bg: rgba(16, 185, 129, 0.12);
            --pos-glow: 0 4px 16px rgba(16, 185, 129, 0.28);

            --neu-color: #0ea5e9;
            --neu-bg: rgba(14, 165, 233, 0.12);
            --neu-glow: 0 4px 16px rgba(14, 165, 233, 0.28);

            --neg-color: #f43f5e;
            --neg-bg: rgba(244, 63, 94, 0.12);
            --neg-glow: 0 4px 16px rgba(244, 63, 94, 0.28);
        }

        /* Dark Neumorphic Palette */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-base: #181b20;
                --neu-surface: #181b20;
                --neu-dark: #101216;
                --neu-light: #242931;
                --neu-dark-rgb: 16, 18, 22;
                --neu-light-rgb: 36, 41, 49;

                --shadow-raised: 8px 8px 18px var(--neu-dark), -8px -8px 18px var(--neu-light);
                --shadow-raised-sm: 4px 4px 10px var(--neu-dark), -4px -4px 10px var(--neu-light);
                --shadow-raised-lg: 14px 14px 28px var(--neu-dark), -14px -14px 28px var(--neu-light);
                --shadow-inset: inset 4px 4px 8px var(--neu-dark), inset -4px -4px 8px var(--neu-light);
                --shadow-inset-sm: inset 2px 2px 5px var(--neu-dark), inset -2px -2px 5px var(--neu-light);

                --text-primary: #f1f5f9;
                --text-secondary: #94a3b8;
                --text-muted: #64748b;

                --primary: #818cf8;
                --primary-gradient: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
                --primary-glow: rgba(129, 140, 248, 0.4);

                --pos-color: #34d399;
                --pos-bg: rgba(52, 211, 153, 0.16);
                --pos-glow: 0 4px 20px rgba(52, 211, 153, 0.35);

                --neu-color: #38bdf8;
                --neu-bg: rgba(56, 189, 248, 0.16);
                --neu-glow: 0 4px 20px rgba(56, 189, 248, 0.35);

                --neg-color: #fb7185;
                --neg-bg: rgba(251, 113, 133, 0.16);
                --neg-glow: 0 4px 20px rgba(251, 113, 133, 0.35);
            }
        }

        /* Streamlit UI Theme Sync */
        [data-theme="dark"], .stApp[data-theme="dark"] {
            --bg-base: #181b20;
            --neu-surface: #181b20;
            --neu-dark: #101216;
            --neu-light: #242931;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
        }

        [data-theme="light"], .stApp[data-theme="light"] {
            --bg-base: #e8ecf2;
            --neu-surface: #e8ecf2;
            --neu-dark: #c2cbd6;
            --neu-light: #ffffff;
            --text-primary: #2d3748;
            --text-secondary: #64748b;
            --text-muted: #94a3b8;
        }

        /* -------------------------------------------------------------
           GLOBAL CANVAS & TYPOGRAPHY
        ------------------------------------------------------------- */
        html, body, [class*="css"] {
            font-family: var(--font-main) !important;
        }

        .stApp {
            background-color: var(--bg-base) !important;
            color: var(--text-primary) !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: var(--bg-base) !important;
            border-right: 1px solid rgba(128, 128, 128, 0.12) !important;
            box-shadow: 4px 0 20px rgba(0, 0, 0, 0.04) !important;
        }

        section[data-testid="stSidebar"] .stMarkdown h3 {
            color: var(--text-primary) !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }

        /* -------------------------------------------------------------
           NEUMORPHIC CARDS & CONTAINERS
        ------------------------------------------------------------- */
        .neu-card {
            background: var(--neu-surface);
            border-radius: 26px;
            padding: 2.2rem;
            box-shadow: var(--shadow-raised);
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin-bottom: 1.8rem;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .neu-card:hover {
            box-shadow: var(--shadow-raised-lg);
            transform: translateY(-2px);
        }

        .neu-well {
            background: var(--neu-surface);
            border-radius: 18px;
            padding: 1.25rem;
            box-shadow: var(--shadow-inset);
            border: none;
            margin-bottom: 1.2rem;
        }

        /* -------------------------------------------------------------
           NEUMORPHIC HERO BANNER
        ------------------------------------------------------------- */
        .neu-hero {
            position: relative;
            text-align: center;
            padding: 3.5rem 2rem 2.8rem 2rem;
            background: var(--neu-surface);
            border-radius: 32px;
            box-shadow: var(--shadow-raised);
            margin-bottom: 2.5rem;
            border: 1px solid rgba(255, 255, 255, 0.4);
            overflow: hidden;
        }

        .neu-pill-tag {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 18px;
            border-radius: 9999px;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            background: var(--neu-surface);
            box-shadow: var(--shadow-raised-sm);
            color: var(--primary);
            margin-bottom: 1.25rem;
            transition: all 0.2s ease;
        }

        .neu-pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--pos-color);
            box-shadow: 0 0 10px var(--pos-color);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.3); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }

        .neu-hero-title {
            font-size: clamp(2.6rem, 5.5vw, 4rem);
            font-weight: 800;
            letter-spacing: -0.04em;
            margin-bottom: 0.75rem;
            color: var(--text-primary);
            text-shadow: 2px 2px 4px rgba(var(--neu-dark-rgb), 0.6);
            line-height: 1.1;
        }

        .neu-hero-title span {
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .neu-hero-subtitle {
            font-size: 1.15rem;
            color: var(--text-secondary);
            max-width: 650px;
            margin: 0 auto;
            line-height: 1.6;
            font-weight: 400;
        }

        /* -------------------------------------------------------------
           STREAMLIT NATIVE INPUTS (TEXTAREA & INPUTS)
        ------------------------------------------------------------- */
        div[data-baseweb="textarea"] {
            background-color: transparent !important;
            border: none !important;
        }

        .stTextArea textarea {
            background: var(--neu-surface) !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 1.25rem !important;
            font-size: 1.05rem !important;
            font-family: var(--font-main) !important;
            color: var(--text-primary) !important;
            box-shadow: var(--shadow-inset) !important;
            transition: all 0.25s ease !important;
            line-height: 1.5 !important;
        }

        .stTextArea textarea:focus {
            box-shadow: var(--shadow-inset), 0 0 0 2px var(--primary) !important;
            outline: none !important;
        }

        /* -------------------------------------------------------------
           STREAMLIT BUTTONS (TACTILE NEUMORPHIC)
        ------------------------------------------------------------- */
        .stButton > button {
            background: var(--neu-surface) !important;
            color: var(--text-primary) !important;
            border: none !important;
            border-radius: 16px !important;
            padding: 0.65rem 1.4rem !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            box-shadow: var(--shadow-raised-sm) !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            letter-spacing: 0.01em !important;
        }

        .stButton > button:hover {
            box-shadow: var(--shadow-raised) !important;
            transform: translateY(-2px) !important;
            color: var(--primary) !important;
        }

        .stButton > button:active {
            box-shadow: var(--shadow-inset-sm) !important;
            transform: translateY(1px) !important;
        }

        /* Primary Call-To-Action Button */
        .stButton > button[kind="primary"],
        .stButton > button[data-testid="baseButton-primary"] {
            background: var(--primary-gradient) !important;
            color: #ffffff !important;
            box-shadow: 6px 6px 16px var(--neu-dark), -6px -6px 16px var(--neu-light), 0 0 20px var(--primary-glow) !important;
            font-weight: 700 !important;
        }

        .stButton > button[kind="primary"]:hover,
        .stButton > button[data-testid="baseButton-primary"]:hover {
            box-shadow: 8px 8px 20px var(--neu-dark), -8px -8px 20px var(--neu-light), 0 0 26px var(--primary-glow) !important;
            transform: translateY(-2px) scale(1.01) !important;
            color: #ffffff !important;
        }

        .stButton > button[kind="primary"]:active,
        .stButton > button[data-testid="baseButton-primary"]:active {
            box-shadow: inset 3px 3px 6px rgba(0,0,0,0.4), inset -3px -3px 6px rgba(255,255,255,0.2) !important;
            transform: translateY(1px) !important;
        }

        /* Download Button */
        .stDownloadButton > button {
            background: var(--neu-surface) !important;
            color: var(--primary) !important;
            border: none !important;
            border-radius: 16px !important;
            padding: 0.75rem 1.6rem !important;
            font-weight: 700 !important;
            box-shadow: var(--shadow-raised-sm) !important;
            transition: all 0.2s ease !important;
        }

        .stDownloadButton > button:hover {
            box-shadow: var(--shadow-raised) !important;
            transform: translateY(-2px) !important;
        }

        .stDownloadButton > button:active {
            box-shadow: var(--shadow-inset-sm) !important;
            transform: translateY(1px) !important;
        }

        /* -------------------------------------------------------------
           STREAMLIT TABS (NEUMORPHIC SEGMENTED CONTROL)
        ------------------------------------------------------------- */
        div[data-testid="stTabs"] {
            margin-top: 1rem;
        }

        div[data-baseweb="tab-list"] {
            background: var(--neu-surface) !important;
            padding: 8px !important;
            border-radius: 20px !important;
            box-shadow: var(--shadow-inset-sm) !important;
            gap: 10px !important;
            border-bottom: none !important;
            margin-bottom: 1.8rem !important;
        }

        button[data-baseweb="tab"] {
            border: none !important;
            border-radius: 14px !important;
            padding: 10px 22px !important;
            color: var(--text-secondary) !important;
            background: transparent !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            transition: all 0.25s ease !important;
        }

        button[data-baseweb="tab"]:hover {
            color: var(--text-primary) !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            background: var(--neu-surface) !important;
            box-shadow: var(--shadow-raised-sm) !important;
            color: var(--primary) !important;
            font-weight: 700 !important;
        }

        div[data-baseweb="tab-highlight"] {
            display: none !important;
        }

        /* -------------------------------------------------------------
           NEUMORPHIC RESULT DISPLAY CARD
        ------------------------------------------------------------- */
        .neu-result-card {
            background: var(--neu-surface);
            border-radius: 24px;
            padding: 2rem;
            box-shadow: var(--shadow-raised);
            margin-top: 1.6rem;
            margin-bottom: 1.6rem;
            border: 1px solid rgba(255, 255, 255, 0.4);
            animation: neuFadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes neuFadeIn {
            from { opacity: 0; transform: translateY(14px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .neu-result-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 1.4rem;
        }

        .neu-badge {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 10px 22px;
            border-radius: 9999px;
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            background: var(--neu-surface);
            box-shadow: var(--shadow-raised-sm);
        }

        .neu-badge-pos {
            color: var(--pos-color);
            border-left: 4px solid var(--pos-color);
        }
        .neu-badge-neu {
            color: var(--neu-color);
            border-left: 4px solid var(--neu-color);
        }
        .neu-badge-neg {
            color: var(--neg-color);
            border-left: 4px solid var(--neg-color);
        }

        .neu-confidence-meter {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px 18px;
            border-radius: 9999px;
            background: var(--neu-surface);
            box-shadow: var(--shadow-inset-sm);
            font-family: var(--font-code);
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        /* Detected Vocabulary Token Chips */
        .neu-token-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 0.75rem;
        }

        .neu-token-tag {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 5px 14px;
            border-radius: 12px;
            font-size: 0.85rem;
            font-family: var(--font-code);
            font-weight: 600;
            background: var(--neu-surface);
            box-shadow: 3px 3px 7px var(--neu-dark), -3px -3px 7px var(--neu-light);
            color: var(--primary);
            transition: all 0.2s ease;
        }

        .neu-token-tag:hover {
            box-shadow: 1px 1px 3px var(--neu-dark), -1px -1px 3px var(--neu-light);
            transform: scale(1.04);
        }

        /* -------------------------------------------------------------
           STAT TILES & MINI METRICS
        ------------------------------------------------------------- */
        .neu-stat-tile {
            background: var(--neu-surface);
            border-radius: 20px;
            padding: 1.4rem;
            box-shadow: var(--shadow-raised-sm);
            text-align: center;
            transition: all 0.25s ease;
            margin-bottom: 1rem;
        }

        .neu-stat-tile:hover {
            box-shadow: var(--shadow-raised);
            transform: translateY(-2px);
        }

        .neu-stat-num {
            font-size: 1.85rem;
            font-weight: 800;
            color: var(--text-primary);
            letter-spacing: -0.02em;
            line-height: 1.1;
        }

        .neu-stat-lbl {
            font-size: 0.82rem;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 0.4rem;
        }

        /* -------------------------------------------------------------
           TACTILE HISTORY CARDS (SIDEBAR)
        ------------------------------------------------------------- */
        .neu-history-item {
            background: var(--neu-surface);
            padding: 0.9rem 1.1rem;
            border-radius: 16px;
            box-shadow: var(--shadow-raised-sm);
            margin-bottom: 0.75rem;
            border-left: 4px solid var(--primary);
            transition: all 0.2s ease;
        }

        .neu-history-item:hover {
            box-shadow: var(--shadow-raised);
            transform: translateX(3px);
        }

        /* -------------------------------------------------------------
           FILE UPLOADER OVERRIDES
        ------------------------------------------------------------- */
        div[data-testid="stFileUploader"] {
            background: var(--neu-surface);
            border-radius: 22px;
            padding: 1.5rem;
            box-shadow: var(--shadow-inset-sm);
            border: 2px dashed rgba(var(--neu-dark-rgb), 0.7);
        }

        /* -------------------------------------------------------------
           PROGRESS BARS & PROGRESS METERS
        ------------------------------------------------------------- */
        div[data-testid="stProgress"] > div {
            background: var(--neu-surface) !important;
            border-radius: 9999px !important;
            box-shadow: var(--shadow-inset-sm) !important;
            height: 12px !important;
            overflow: hidden !important;
        }

        div[data-testid="stProgress"] > div > div {
            background: var(--primary-gradient) !important;
            border-radius: 9999px !important;
        }

        /* -------------------------------------------------------------
           EXPANDER & FOOTER
        ------------------------------------------------------------- */
        div[data-testid="stExpander"] {
            background: var(--neu-surface) !important;
            border-radius: 18px !important;
            box-shadow: var(--shadow-raised-sm) !important;
            border: none !important;
            margin-top: 1rem;
        }

        .neu-footer {
            text-align: center;
            padding: 3.5rem 1rem 2rem 1rem;
            margin-top: 3.5rem;
            border-top: 1px solid rgba(128, 128, 128, 0.12);
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .neu-footer-pill {
            display: inline-block;
            margin-top: 0.75rem;
            padding: 8px 22px;
            border-radius: 9999px;
            background: var(--neu-surface);
            box-shadow: var(--shadow-raised-sm);
            font-weight: 600;
            color: var(--primary);
        }
        </style>
    """, unsafe_allow_html=True)

def hero_html():
    return """
        <div class="neu-hero">
            <div class="neu-pill-tag">
                <span class="neu-pulse-dot"></span>
                SVM AI Core Online • TF-IDF Vectorized
            </div>
            <h1 class="neu-hero-title">Sentify <span>AI</span></h1>
            <p class="neu-hero-subtitle">
                Tactile Neomorphic sentiment intelligence engine. Experience fine-grained polarity classification with calibrated multi-class probabilities and keyword explainability.
            </p>
        </div>
    """

def result_card_html(label: str, confidence: float, breakdown: dict, matched_tokens: list):
    meta = {
        "positive": {"icon": "😊", "class": "neu-badge-pos", "title": "POSITIVE", "accent": "var(--pos-color)"},
        "neutral": {"icon": "😐", "class": "neu-badge-neu", "title": "NEUTRAL", "accent": "var(--neu-color)"},
        "negative": {"icon": "😠", "class": "neu-badge-neg", "title": "NEGATIVE", "accent": "var(--neg-color)"}
    }
    current = meta.get(label, meta["neutral"])

    tokens_html = "".join([f'<span class="neu-token-tag">#{t}</span>' for t in matched_tokens]) if matched_tokens else "<span style='color: var(--text-muted); font-size: 0.85rem;'>No strong vocabulary triggers matched</span>"

    return f"""
        <div class="neu-result-card">
            <div class="neu-result-header">
                <div class="neu-badge {current['class']}">
                    <span>{current['icon']}</span>
                    <span>{current['title']}</span>
                </div>
                <div class="neu-confidence-meter">
                    <span style="color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase;">Confidence</span>
                    <span style="color: {current['accent']}; font-size: 1.15rem;">{confidence:.1%}</span>
                </div>
            </div>
            <div style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin-bottom: 0.4rem;">
                Detected Vocabulary Signals:
            </div>
            <div class="neu-token-container">
                {tokens_html}
            </div>
        </div>
    """

def footer_html():
    return """
        <div class="neu-footer">
            Designed & Engineered with Neomorphic Precision by
            <br>
            <div class="neu-footer-pill">
                <strong>Nischal Bhandari</strong> • School of Engineering (SOE), Pokhara University
            </div>
        </div>
    """
