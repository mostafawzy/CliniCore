"""Home / landing page."""

import streamlit as st
from api_client import health_check


def render():
    # ── Hero ──────────────────────────────────────────────────────────────────
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(
            """
            <div style="padding: 48px 0 10px;">
                <div class="gradient-title">CliniCore</div>
                <div style="font-family:'Space Grotesk',sans-serif;font-size:1.1rem;
                            color:#8892B0;max-width:560px;line-height:1.6;margin-bottom:10px;">
                    An AI-powered platform for retrieving medical knowledge, analyzing clinical text, and interpreting diagnostic images.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
   
    
  

    # ── Module cards ──────────────────────────────────────────────────────────
    #st.markdown('<div class="section-title">Platform Modules</div>', unsafe_allow_html=True)
    #st.markdown('<div class="subtitle">Click any card to navigate to that module.</div>', unsafe_allow_html=True)


    modules = [
    {
        "icon": "",
        "title": "Document Q&A",
        "desc": "Ask clinical questions and receive answers grounded in verified medical documents and guidelines.",
        "pill": "pill-blue",
        "pill_label": "Clinical Q&A · Evidence Retrieval",
        "page": "rag",
    },
    {
        "icon": "",
        "title": "Medical NER",
        "desc": "Extract structured medical entities such as conditions, medications, and symptoms from clinical text.",
        "pill": "pill-purple",
        "pill_label": "Clinical NLP · Entity Extraction",
        "page": "ner",
    },
    {
        "icon": "",
        "title": "Skin Vision",
        "desc": "Support dermatological screening through AI-based analysis of skin lesion images.",
        "pill": "pill-teal",
        "pill_label": "Dermatology AI · Imaging Support",
        "page": "vision",
    },
]
    cols = st.columns(2)
    for i, m in enumerate(modules):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="medi-card">
                    <div style="font-size:32px;margin-bottom:10px;">{m["icon"]}</div>
                    <div class="section-title" style="font-size:1.1rem;">{m["title"]}</div>
                    <div style="color:#8892B0;font-size:13px;line-height:1.55;
                                margin:8px 0 14px;">{m["desc"]}</div>
                    <span class="stat-pill {m['pill']}">{m["pill_label"]}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Open {m['title']} →", key=f"home_nav_{m['page']}"):
                st.session_state.page = m["page"]
                st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)

  # ── API Status ────────────────────────────────────────────────────────────
    with st.spinner("Checking API…"):
        status = health_check()

    online = status.get("status") == "ok"
    status_color  = "#00D4AA" if online else "#F43F5E"
    status_dot    = "●" if online else "●"
    status_label  = "API Online" if online else "API Offline — start FastAPI first"

    st.markdown(
        f"""
        <div class="medi-card" style="display:flex;align-items:center;gap:12px;padding:16px 24px;">
            <span style="color:{status_color};font-size:20px;">{status_dot}</span>
            <span style="font-weight:600;color:{status_color};">{status_label}</span>
            {"<span style='color:#8892B0;font-size:13px;margin-left:auto;'>" + status.get("version","") + " · " + status.get("environment","") + "</span>" if online else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br/>", unsafe_allow_html=True)