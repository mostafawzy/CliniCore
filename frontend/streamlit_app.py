"""
MediAssist AI — Streamlit Frontend (Light Mode)
Entry point: streamlit run frontend/streamlit_app.py
"""

import streamlit as st

# ── Must be first Streamlit call ──────────────────────────────────────────────
st.set_page_config(
    page_title="ClinCore",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject Global CSS (LIGHT + GLASS THEME) ───────────────────────────────────
def inject_css():
    
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

        /* ── Root (LIGHT THEME) ───────────────────────────────────────────── */
        :root {
            --bg-primary:    #F7FAFC;
            --bg-secondary:  #FFFFFF;
            --bg-card:       rgba(255,255,255,0.72);
            --bg-card-hover: #F0F7FF;

            --accent-teal:   #14B8A6;
            --accent-blue:   #3B82F6;
            --accent-purple: #7C3AED;
            --accent-rose:   #F43F5E;

            --text-primary:  #0F172A;
            --text-muted:    #64748B;

            --border:        rgba(15, 23, 42, 0.08);

            --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
            --shadow-md: 0 10px 30px rgba(15, 23, 42, 0.08);
        }

        /* ── Global background ────────────────────────────────────────────── */
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #F7FAFC 0%, #EEF6FF 100%) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', sans-serif;
        }

        /* ── Sidebar ──────────────────────────────────────────────────────── */
        [data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        rgba(255, 255, 255, 0.92) 0%,
        rgba(247, 250, 252, 0.96) 50%,
        rgba(238, 246, 255, 0.98) 100%
    ) !important;

    border-right: 1px solid rgba(20, 184, 166, 0.10);

    backdrop-filter: blur(14px);

    box-shadow:
        4px 0 20px rgba(15, 23, 42, 0.04);
}
        
        /* ── Sidebar navigation buttons ── */

/* ── Sidebar Buttons (REFINED NAV SYSTEM) ───────────────────── */
section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(
        135deg,
       rgba(20, 184, 166, 0.18),
        rgba(59, 130, 246, 0.10)
    ) !important;

    color: #0F172A !important;

    border: 1px solid rgba(20, 184, 166, 0.18) !important;
    border-radius: 12px !important;

    font-weight: 600 !important;

    box-shadow:
        0 2px 8px rgba(15, 23, 42, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.5);

    transition: all 0.22s ease !important;
}

/* hover */
/* ── Sidebar Buttons (REFINED NAV SYSTEM) ───────────────────── */
section[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(
        135deg,
        rgba(20, 184, 166, 0.18),
        rgba(59, 130, 246, 0.10)
    ) !important;

    transform: translateX(.5px);

    border: 1px solid rgba(20, 184, 166, 0.30) !important;

    box-shadow:
        0 6px 6px rgba(15, 23, 42, 0.08),
        0 0 2px rgba(20, 20, 20, 0.12);
        transform: translateY(.5px);
}

/* active/pressed button (Streamlit adds aria attribute) */

section[data-testid="stSidebar"] .stButton > button[aria-pressed="true"] {
    background: linear-gradient(135deg, #14B8A6, #3B82F6) !important;
    color: white !important;

    border: 1px solid rgba(20, 184, 166, 0.40) !important;

    box-shadow:
        0 10px 24px rgba(20, 184, 166, 0.20);
}

        /* ── Cards (GLASS STYLE) ─────────────────────────────────────────── */
        .medi-card {
            background: var(--bg-card);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 24px;
            margin-bottom: 16px;
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
        }

        .medi-card:hover {
            transform: translateY(.5px);
            
        }
        
        [data-testid="stSidebarNav"] {
    display: none !important;
}
section[data-testid="stSidebarNav"] {
    display: none !important;
}

        /* ── Titles ──────────────────────────────────────────────────────── */
        .gradient-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.4rem;
            font-weight: 700;
            background: linear-gradient(135deg, #0EA5E9, #14B8A6, #6366F1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .section-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.4rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .subtitle {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-bottom: 24px;
        }

        /* ── Buttons ─────────────────────────────────────────────────────── */
      /* ── Buttons (REFINED PREMIUM GLASS SYSTEM) ───────────────────────── */
/* ── Buttons (REFINED ACCENT SYSTEM) ─────────────────────────── */
.stButton > button {
    background: linear-gradient(
        135deg,
        rgba(20, 184, 166, 0.14),
        rgba(59, 130, 246, 0.10)
    ) !important;

    color: #0F172A !important;
    font-weight: 600 !important;

    border: 1px solid rgba(20, 184, 166, 0.22) !important;
    border-radius: 12px !important;

    padding: 10px 22px !important;

    box-shadow:
        0 6px 18px rgba(15, 23, 42, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.6);

    backdrop-filter: blur(10px);

    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(
        135deg,
        rgba(20, 184, 166, 0.22),
        rgba(59, 130, 246, 0.14)
    ) !important;

    transform: translateY(-2px);

    box-shadow:
        0 10px 26px rgba(15, 23, 42, 0.10),
        0 0 0 1px rgba(20, 184, 166, 0.18);

    border: 1px solid rgba(20, 184, 166, 0.35) !important;
}
     .stButton > button:active {
    transform: scale(0.98);
    background: rgba(20, 184, 166, 0.12) !important;
}

        /* ── Inputs ──────────────────────────────────────────────────────── */
        .stTextArea textarea,
        .stTextInput input {
            background: white !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
        }

        .stTextArea textarea:focus,
        .stTextInput input:focus {
            border-color: var(--accent-teal) !important;
            box-shadow: 0 0 0 3px rgba(20,184,166,0.15) !important;
        }

        /* ── Sidebar nav links (LIGHT STYLE) ─────────────────────────────── */
        .nav-link {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            border-radius: 10px;
            margin-bottom: 6px;
            cursor: pointer;
            color: var(--text-muted);
            transition: all 0.2s ease;
        }

        .nav-link:hover {
            background: rgba(20,184,166,0.08);
            color: var(--accent-teal);
        }

        .nav-link.active {
            background: rgba(59,130,246,0.10);
            color: var(--accent-blue);
        }

        /* ── Stat pills ──────────────────────────────────────────────────── */
        .stat-pill {
            display: inline-flex;
            align-items: center;
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 600;
        }

        .pill-teal { background: rgba(20,184,166,0.12); color: #0F766E; }
        .pill-blue { background: rgba(59,130,246,0.12); color: #1D4ED8; }
        .pill-purple { background: rgba(124,58,237,0.12); color: #5B21B6; }

        /* ── Entity chips ────────────────────────────────────────────────── */
        .entity-chip {
            display: inline-flex;
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 13px;
            margin: 3px;
        }

        .entity-DISEASE { background: rgba(244,63,94,0.12); color: #BE123C; }
        .entity-DRUG    { background: rgba(59,130,246,0.12); color: #1D4ED8; }
        .entity-SYMPTOM { background: rgba(245,158,11,0.12); color: #B45309; }
        .entity-ANATOMY { background: rgba(124,58,237,0.12); color: #6D28D9; }

        /* ── Confidence bar ─────────────────────────────────────────────── */
        .conf-bar-wrap {
            background: rgba(0,0,0,0.05);
            border-radius: 999px;
            height: 8px;
            overflow: hidden;
        }

        .conf-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #14B8A6, #3B82F6);
        }

        /* ── Divider ─────────────────────────────────────────────────────── */
        .medi-divider {
            border-top: 1px solid var(--border);
            margin: 20px 0;
        }

        /* ── Hide Streamlit UI ───────────────────────────────────────────── */
       #MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

        </style>
        """,
        unsafe_allow_html=True,
    )


# ── Page Registry ────────────────────────────────────────────────────────────
PAGES = {
    " Home":         "home",
    " Document Q&A": "rag",
    "  Medical NER":  "ner",
    "  Skin Vision":  "vision",
}


def sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div style="padding: 18px 8px 26px;">
                <div style="display:flex;align-items:center;gap:10px;">
                    <span style="font-size:28px;"><svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 48 48"><path fill="#000000" fill-rule="evenodd" d="M34 16c0 5.523-4.477 10-10 10s-10-4.477-10-10S18.477 6 24 6s10 4.477 10 10Zm-2 0a8 8 0 1 1-16 0a8 8 0 0 1 16 0ZM17.914 28.855l.011.022l.075.147h11.749c.229-.434.748-1.126 1.251-1.011c1.13.257 2.268.615 3.361 1.056l.033-.016l.011.022l.008.015C38.528 30.762 42 33.596 42 36.57V42H6v-5.43c0-3.775 5.596-7.327 11-8.557c.441-.1.703.42.914.842Zm14.79 1.728a20.33 20.33 0 0 0-1.301-.407l-.446.848H16.793l-.414-.787l-.36.108c-.007.066-.013.14-.016.224c-.013.345.013.754.07 1.17a8.087 8.087 0 0 0 .28 1.281a3 3 0 1 1-1.957.444l-.008-.028a10.082 10.082 0 0 1-.297-1.426a9.987 9.987 0 0 1-.084-.928c-1.236.528-2.389 1.166-3.355 1.87C8.73 34.356 8 35.668 8 36.57V40h32v-3.43c0-.903-.73-2.215-2.652-3.617a16.564 16.564 0 0 0-2.666-1.562A10.446 10.446 0 0 1 34.434 33H35a1 1 0 0 1 .894.553l1 2c.07.139.106.292.106.447v2a1 1 0 0 1-1 1h-2v-2h1v-.764L34.382 35h-2.764L31 36.236V37h1v2h-2a1 1 0 0 1-1-1v-2c0-.155.036-.308.106-.447l1-2A1 1 0 0 1 31 33h1.362c.012-.04.025-.08.037-.124c.094-.321.178-.72.235-1.136c.056-.412.082-.815.07-1.157ZM17 36c0 .574-.462 1.015-1 1.015s-1-.44-1-1.015c0-.574.462-1.015 1-1.015s1 .44 1 1.015Z" clip-rule="evenodd"/></svg></span>
                    <span style="font-family:'Space Grotesk';font-size:1.2rem;font-weight:700;">
                        CliniCore<span style="color:#14B8A6;"></span>
                    </span>
                </div>
                <div style="font-size:11px;color:#64748B;letter-spacing:0.06em;text-transform:uppercase;padding-left:38px;">
                    Healthcare Intelligence
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if "page" not in st.session_state:
            st.session_state.page = "home"

        for label, key in PAGES.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()

        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown(
            """
            <div 
            </div>
            """,
            unsafe_allow_html=True,
        )


def main():
    inject_css()
    sidebar()

    page = st.session_state.get("page", "home")

    if page == "home":
        from pages.home import render
    elif page == "rag":
        from pages.rag import render
    elif page == "ner":
        from pages.ner import render
    elif page == "vision":
        from pages.vision import render

    else:
        from pages.home import render

    render()


if __name__ == "__main__":
    main()