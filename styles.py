import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

        /* -------------------------------------------------------------
           HIGH-CONTRAST NEUMORPHIC DESIGN SYSTEM
        ------------------------------------------------------------- */
        :root {
            --font-main: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            --font-code: 'JetBrains Mono', monospace;

            /* Crisp Light Porcelain Neumorphism */
            --bg-base: #eef2f7;
            --neu-surface: #eef2f7;
            --neu-shadow-dark: #bac7d6;
            --neu-shadow-light: #ffffff;
            --neu-border: rgba(255, 255, 255, 0.85);

            /* High-Contrast Typography */
            --text-primary: #0f172a;       /* slate-900 (ultra-crisp) */
            --text-secondary: #334155;     /* slate-700 (sharp & clear) */
            --text-muted: #64748b;         /* slate-500 */

            /* Neomorphic Shadows */
            --shadow-raised: 8px 8px 18px var(--neu-shadow-dark), -8px -8px 18px var(--neu-shadow-light);
            --shadow-raised-sm: 4px 4px 10px var(--neu-shadow-dark), -4px -4px 10px var(--neu-shadow-light);
            --shadow-raised-lg: 12px 12px 26px var(--neu-shadow-dark), -12px -12px 26px var(--neu-shadow-light);
            --shadow-inset: inset 4px 4px 8px var(--neu-shadow-dark), inset -4px -4px 8px var(--neu-shadow-light);
            --shadow-inset-sm: inset 2px 2px 5px var(--neu-shadow-dark), inset -2px -2px 5px var(--neu-shadow-light);

            /* Accents */
            --primary: #4f46e5;
            --primary-gradient: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
            --primary-glow: rgba(79, 70, 229, 0.3);

            /* Sentiment Tokens */
            --pos-color: #059669;          /* emerald-600 */
            --pos-bg: rgba(5, 150, 105, 0.12);
            --neu-color: #0284c7;          /* sky-600 */
            --neu-bg: rgba(2, 132, 199, 0.12);
            --neg-color: #e11d48;          /* rose-600 */
            --neg-bg: rgba(225, 29, 72, 0.12);
        }

        /* Dark Neumorphic Palette */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-base: #181b20;
                --neu-surface: #181b20;
                --neu-shadow-dark: #0d0f12;
                --neu-shadow-light: #23272f;
                --neu-border: rgba(255, 255, 255, 0.08);

                --text-primary: #f8fafc;
                --text-secondary: #cbd5e1;
                --text-muted: #94a3b8;

                --shadow-raised: 8px 8px 18px var(--neu-shadow-dark), -8px -8px 18px var(--neu-shadow-light);
                --shadow-raised-sm: 4px 4px 10px var(--neu-shadow-dark), -4px -4px 10px var(--neu-shadow-light);
                --shadow-raised-lg: 12px 12px 26px var(--neu-shadow-dark), -12px -12px 26px var(--neu-shadow-light);
                --shadow-inset: inset 4px 4px 8px var(--neu-shadow-dark), inset -4px -4px 8px var(--neu-shadow-light);
                --shadow-inset-sm: inset 2px 2px 5px var(--neu-shadow-dark), inset -2px -2px 5px var(--neu-shadow-light);

                --primary: #818cf8;
                --primary-gradient: linear-gradient(135deg, #6366f1 0%, #818cf8 100%);
                --primary-glow: rgba(129, 140, 248, 0.35);

                --pos-color: #10b981;
                --pos-bg: rgba(16, 185, 129, 0.18);
                --neu-color: #38bdf8;
                --neu-bg: rgba(56, 189, 248, 0.18);
                --neg-color: #fb7185;
                --neg-bg: rgba(251, 113, 133, 0.18);
            }
        }

        [data-theme="dark"], .stApp[data-theme="dark"] {
            --bg-base: #181b20;
            --neu-surface: #181b20;
            --neu-shadow-dark: #0d0f12;
            --neu-shadow-light: #23272f;
            --neu-border: rgba(255, 255, 255, 0.08);
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
        }

        [data-theme="light"], .stApp[data-theme="light"] {
            --bg-base: #eef2f7;
            --neu-surface: #eef2f7;
            --neu-shadow-dark: #bac7d6;
            --neu-shadow-light: #ffffff;
            --neu-border: rgba(255, 255, 255, 0.85);
            --text-primary: #0f172a;
            --text-secondary: #334155;
            --text-muted: #64748b;
        }

        /* -------------------------------------------------------------
           CANVAS & STREAMLIT CONTAINER OVERRIDES
        ------------------------------------------------------------- */
        html, body, [class*="css"] {
            font-family: var(--font-main) !important;
        }

        .stApp {
            background-color: var(--bg-base) !important;
            color: var(--text-primary) !important;
        }

        /* Real Streamlit Container Wrapping */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--neu-surface) !important;
            border: 1px solid var(--neu-border) !important;
            border-radius: 22px !important;
            box-shadow: var(--shadow-raised) !important;
            padding: 1.6rem !important;
            margin-bottom: 1.5rem !important;
            transition: box-shadow 0.25s ease, transform 0.25s ease !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            box-shadow: var(--shadow-raised-lg) !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: var(--bg-base) !important;
            border-right: 1px solid var(--neu-border) !important;
            box-shadow: 4px 0 16px rgba(0, 0, 0, 0.03) !important;
        }

        section[data-testid="stSidebar"] h3 {
            color: var(--text-primary) !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em !important;
        }

        /* -------------------------------------------------------------
           STREAMLIT NATIVE INPUTS (TEXTAREA)
        ------------------------------------------------------------- */
        div[data-baseweb="textarea"] {
            background-color: transparent !important;
            border: none !important;
        }

        .stTextArea textarea {
            background: var(--neu-surface) !important;
            border: none !important;
            border-radius: 16px !important;
            padding: 1.1rem 1.25rem !important;
            font-size: 1rem !important;
            font-family: var(--font-main) !important;
            color: var(--text-primary) !important;
            box-shadow: var(--shadow-inset) !important;
            transition: all 0.2s ease !important;
            line-height: 1.5 !important;
        }

        .stTextArea textarea:focus {
            box-shadow: var(--shadow-inset), 0 0 0 2px var(--primary) !important;
            outline: none !important;
        }

        /* -------------------------------------------------------------
           TACTILE NEUMORPHIC BUTTONS
        ------------------------------------------------------------- */
        .stButton > button {
            background: var(--neu-surface) !important;
            color: var(--text-primary) !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 0.65rem 1.25rem !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            box-shadow: var(--shadow-raised-sm) !important;
            transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
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

        /* Primary Call-to-Action */
        .stButton > button[kind="primary"],
        .stButton > button[data-testid="baseButton-primary"] {
            background: var(--primary-gradient) !important;
            color: #ffffff !important;
            box-shadow: 4px 4px 14px var(--neu-shadow-dark), -4px -4px 14px var(--neu-shadow-light), 0 0 16px var(--primary-glow) !important;
            font-weight: 700 !important;
        }

        .stButton > button[kind="primary"]:hover,
        .stButton > button[data-testid="baseButton-primary"]:hover {
            box-shadow: 6px 6px 18px var(--neu-shadow-dark), -6px -6px 18px var(--neu-shadow-light), 0 0 22px var(--primary-glow) !important;
            transform: translateY(-2px) !important;
            color: #ffffff !important;
        }

        .stButton > button[kind="primary"]:active,
        .stButton > button[data-testid="baseButton-primary"]:active {
            box-shadow: inset 3px 3px 6px rgba(0,0,0,0.35) !important;
            transform: translateY(1px) !important;
        }

        /* Download Button */
        .stDownloadButton > button {
            background: var(--neu-surface) !important;
            color: var(--primary) !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 0.75rem 1.4rem !important;
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
           STREAMLIT TABS (SEGMENTED NEUMORPHIC CONTROL)
        ------------------------------------------------------------- */
        div[data-baseweb="tab-list"] {
            background: var(--neu-surface) !important;
            padding: 6px !important;
            border-radius: 16px !important;
            box-shadow: var(--shadow-inset-sm) !important;
            gap: 8px !important;
            border-bottom: none !important;
            margin-bottom: 1.5rem !important;
        }

        button[data-baseweb="tab"] {
            border: none !important;
            border-radius: 12px !important;
            padding: 9px 20px !important;
            color: var(--text-secondary) !important;
            background: transparent !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            transition: all 0.2s ease !important;
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
           PROGRESS BARS & INSET TRACKS
        ------------------------------------------------------------- */
        div[data-testid="stProgress"] > div {
            background: var(--neu-surface) !important;
            border-radius: 9999px !important;
            box-shadow: var(--shadow-inset-sm) !important;
            height: 10px !important;
            overflow: hidden !important;
        }

        div[data-testid="stProgress"] > div > div {
            background: var(--primary-gradient) !important;
            border-radius: 9999px !important;
        }

        /* -------------------------------------------------------------
           CUSTOM NEUMORPHIC HTML MODULES
        ------------------------------------------------------------- */
        .neu-hero-container {
            text-align: center;
            padding: 2.4rem 1.5rem 1.8rem 1.5rem;
            background: var(--neu-surface);
            border-radius: 26px;
            box-shadow: var(--shadow-raised);
            border: 1px solid var(--neu-border);
            margin-bottom: 1.8rem;
        }

        .neu-pill-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            background: var(--neu-surface);
            box-shadow: var(--shadow-raised-sm);
            color: var(--primary);
            margin-bottom: 1rem;
        }

        .neu-led-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--pos-color);
            box-shadow: 0 0 8px var(--pos-color);
            animation: neuBreathe 2s infinite ease-in-out;
        }

        @keyframes neuBreathe {
            0%, 100% { opacity: 0.8; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.25); }
        }

        .neu-hero-h1 {
            font-size: clamp(2.2rem, 4.5vw, 3.2rem);
            font-weight: 800;
            letter-spacing: -0.03em;
            margin: 0 0 0.5rem 0;
            color: var(--text-primary);
            line-height: 1.15;
        }

        .neu-hero-h1 span {
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .neu-hero-desc {
            font-size: 1.05rem;
            color: var(--text-secondary);
            max-width: 620px;
            margin: 0 auto;
            line-height: 1.55;
        }

        /* Result Card */
        .neu-result-box {
            background: var(--neu-surface);
            border-radius: 20px;
            padding: 1.6rem;
            box-shadow: var(--shadow-raised);
            border: 1px solid var(--neu-border);
            margin-top: 1.4rem;
            margin-bottom: 1.4rem;
            animation: neuSlideIn 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes neuSlideIn {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .neu-result-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 1.2rem;
        }

        .neu-sentiment-pill {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 9px 20px;
            border-radius: 9999px;
            font-size: 1.15rem;
            font-weight: 800;
            background: var(--neu-surface);
            box-shadow: var(--shadow-raised-sm);
        }

        .neu-pill-pos { color: var(--pos-color); border-left: 4px solid var(--pos-color); }
        .neu-pill-neu { color: var(--neu-color); border-left: 4px solid var(--neu-color); }
        .neu-pill-neg { color: var(--neg-color); border-left: 4px solid var(--neg-color); }

        .neu-conf-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            border-radius: 9999px;
            background: var(--neu-surface);
            box-shadow: var(--shadow-inset-sm);
            font-family: var(--font-code);
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .neu-token-chip {
            display: inline-flex;
            align-items: center;
            padding: 4px 12px;
            border-radius: 10px;
            font-size: 0.82rem;
            font-family: var(--font-code);
            font-weight: 600;
            background: var(--neu-surface);
            box-shadow: 2px 2px 5px var(--neu-shadow-dark), -2px -2px 5px var(--neu-shadow-light);
            color: var(--primary);
            margin: 3px;
            transition: all 0.15s ease;
        }

        .neu-token-chip:hover {
            transform: translateY(-1px);
            box-shadow: 3px 3px 7px var(--neu-shadow-dark), -3px -3px 7px var(--neu-shadow-light);
        }

        /* Stat Tile */
        .neu-card-tile {
            background: var(--neu-surface);
            border-radius: 18px;
            padding: 1.25rem;
            box-shadow: var(--shadow-raised-sm);
            text-align: center;
            border: 1px solid var(--neu-border);
            transition: transform 0.2s ease;
        }

        .neu-card-tile:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-raised);
        }

        .neu-tile-val {
            font-size: 1.65rem;
            font-weight: 800;
            color: var(--text-primary);
            font-family: var(--font-code);
            line-height: 1.1;
        }

        .neu-tile-lbl {
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-top: 0.35rem;
        }

        /* Sidebar History Card */
        .neu-history-card {
            background: var(--neu-surface);
            padding: 0.85rem 1rem;
            border-radius: 14px;
            box-shadow: var(--shadow-raised-sm);
            margin-bottom: 0.65rem;
            border-left: 4px solid var(--primary);
            transition: transform 0.15s ease;
        }

        .neu-history-card:hover {
            transform: translateX(3px);
            box-shadow: var(--shadow-raised);
        }

        /* Telemetry Inset Bar */
        .neu-inset-bar {
            background: var(--neu-surface);
            border-radius: 16px;
            padding: 0.75rem 1rem;
            box-shadow: var(--shadow-inset-sm);
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 0.6rem;
            margin-bottom: 0.6rem;
        }

        /* Footer */
        .neu-footer-bar {
            text-align: center;
            padding: 3rem 1rem 1.8rem 1rem;
            margin-top: 3rem;
            border-top: 1px solid var(--neu-border);
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .neu-footer-pill {
            display: inline-block;
            margin-top: 0.65rem;
            padding: 7px 20px;
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
        <div class="neu-hero-container">
            <div class="neu-pill-badge">
                <span class="neu-led-dot"></span>
                AI Core Online • Linear SVM & TF-IDF
            </div>
            <h1 class="neu-hero-h1">Sentify <span>AI</span></h1>
            <p class="neu-hero-desc">
                High-precision sentiment intelligence engine with calibrated multi-class probability scoring, instant telemetry, and vocabulary explainability.
            </p>
        </div>
    """

def telemetry_bar_html(chars: int, words: int, sentences: int, read_time_sec: int):
    return f"""
        <div class="neu-inset-bar">
            <div style="text-align: center;">
                <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Characters</span><br>
                <strong style="font-size: 0.95rem; color: var(--text-primary); font-family: var(--font-code);">{chars}</strong>
            </div>
            <div style="text-align: center;">
                <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Words</span><br>
                <strong style="font-size: 0.95rem; color: var(--text-primary); font-family: var(--font-code);">{words}</strong>
            </div>
            <div style="text-align: center;">
                <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Sentences</span><br>
                <strong style="font-size: 0.95rem; color: var(--text-primary); font-family: var(--font-code);">{sentences}</strong>
            </div>
            <div style="text-align: center;">
                <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Est. Read Time</span><br>
                <strong style="font-size: 0.95rem; color: var(--text-primary); font-family: var(--font-code);">~{read_time_sec}s</strong>
            </div>
        </div>
    """

def result_card_html(label: str, confidence: float, breakdown: dict, matched_tokens: list):
    meta = {
        "positive": {"icon": "😊", "pill_class": "neu-pill-pos", "title": "POSITIVE", "accent": "var(--pos-color)"},
        "neutral": {"icon": "😐", "pill_class": "neu-pill-neu", "title": "NEUTRAL", "accent": "var(--neu-color)"},
        "negative": {"icon": "😠", "pill_class": "neu-pill-neg", "title": "NEGATIVE", "accent": "var(--neg-color)"}
    }
    current = meta.get(label, meta["neutral"])

    tokens_html = "".join([f'<span class="neu-token-chip">#{t}</span>' for t in matched_tokens]) if matched_tokens else "<span style='color: var(--text-muted); font-size: 0.85rem;'>No strong vocabulary signals detected</span>"

    return f"""
        <div class="neu-result-box">
            <div class="neu-result-row">
                <div class="neu-sentiment-pill {current['pill_class']}">
                    <span>{current['icon']}</span>
                    <span>{current['title']}</span>
                </div>
                <div class="neu-conf-pill">
                    <span style="color: var(--text-muted); font-size: 0.78rem; text-transform: uppercase;">Confidence</span>
                    <span style="color: {current['accent']}; font-size: 1.1rem;">{confidence:.1%}</span>
                </div>
            </div>
            <div style="font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin-bottom: 0.35rem;">
                Detected Vocabulary Triggers:
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                {tokens_html}
            </div>
        </div>
    """

def probability_cards_html(p_pos: float, p_neu: float, p_neg: float):
    return f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin-top: 1rem; margin-bottom: 1.2rem;">
            <div class="neu-card-tile" style="border-top: 4px solid var(--pos-color);">
                <div class="neu-tile-val" style="color: var(--pos-color);">{p_pos:.1%}</div>
                <div class="neu-tile-lbl">Positive Likelihood</div>
            </div>
            <div class="neu-card-tile" style="border-top: 4px solid var(--neu-color);">
                <div class="neu-tile-val" style="color: var(--neu-color);">{p_neu:.1%}</div>
                <div class="neu-tile-lbl">Neutral Likelihood</div>
            </div>
            <div class="neu-card-tile" style="border-top: 4px solid var(--neg-color);">
                <div class="neu-tile-val" style="color: var(--neg-color);">{p_neg:.1%}</div>
                <div class="neu-tile-lbl">Negative Likelihood</div>
            </div>
        </div>
    """

def footer_html():
    return """
        <div class="neu-footer-bar">
            Engineered with Neomorphic Precision by
            <br>
            <div class="neu-footer-pill">
                <strong>Nischal Bhandari</strong> • School of Engineering (SOE), Pokhara University
            </div>
        </div>
    """
