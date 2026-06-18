"""Medical NER page — entity extraction with interactive highlighting."""

import streamlit as st
from api_client import ner_extract

# ─────────────────────────────────────────────────────────────
# Sample Data
# ─────────────────────────────────────────────────────────────

SAMPLE_TEXTS = [
    "The patient was diagnosed with type 2 diabetes mellitus and prescribed metformin 500mg twice daily. She also has a history of hypertension managed with lisinopril.",
    "A 45-year-old male presents with acute myocardial infarction. He has a history of hyperlipidaemia and was on atorvastatin 40mg. ECG shows ST elevation in leads II, III and aVF.",
    "Child presents with fever, rhinorrhoea and productive cough. Suspected community-acquired pneumonia. Prescribed amoxicillin 250mg three times daily for 7 days.",
]

# ─────────────────────────────────────────────────────────────
# Label UI Meta
# ─────────────────────────────────────────────────────────────

LABEL_META = {
    "DISEASE":  {"color": "#F87171", "bg": "rgba(244,63,94,0.15)",  "border": "rgba(244,63,94,0.35)",  "icon": "🦠"},
    "MEDICATION": {"color": "#60A5FA", "bg": "rgba(59,130,246,0.15)", "border": "rgba(59,130,246,0.35)", "icon": "💊"},
    "SYMPTOM":  {"color": "#FCD34D", "bg": "rgba(251,191,36,0.15)", "border": "rgba(251,191,36,0.35)", "icon": "🌡️"},
    "ANATOMY":  {"color": "#A78BFA", "bg": "rgba(139,92,246,0.15)", "border": "rgba(139,92,246,0.35)", "icon": "🫀"},
    "VACCINE":  {"color": "#34D399", "bg": "rgba(16,185,129,0.15)", "border": "rgba(16,185,129,0.35)", "icon": "💉"},
    "DOSAGE":   {"color": "#FBBF24", "bg": "rgba(251,191,36,0.15)", "border": "rgba(251,191,36,0.35)", "icon": "📏"},
    "AGE_GROUP":{"color": "#38BDF8", "bg": "rgba(56,189,248,0.15)", "border": "rgba(56,189,248,0.35)", "icon": "👤"},
    "PROCEDURE":{"color": "#FB7185", "bg": "rgba(244,63,94,0.15)", "border": "rgba(244,63,94,0.35)", "icon": "🏥"},
}

LABEL_DESCRIPTIONS = {
    "DISEASE": "Conditions, disorders, syndromes",
    "MEDICATION": "Drugs, prescriptions, therapies",
    "SYMPTOM": "Clinical signs, complaints",
    "ANATOMY": "Body parts, organs",
    "VACCINE": "Immunizations, vaccines",
    "DOSAGE": "Dose amounts (mg, ml, etc.)",
    "AGE_GROUP": "Patient age categories",
    "PROCEDURE": "Medical procedures",
}

# ─────────────────────────────────────────────────────────────
# Highlight Logic
# ─────────────────────────────────────────────────────────────

import re

def _highlight_text(text: str, entities: list) -> str:
    if not entities:
        return f'<span style="color:#94A3B8;">{text}</span>'

    # sort longest first to avoid partial overwrite issues
    entities = sorted(entities, key=lambda x: len(x.get("text", "")), reverse=True)

    for ent in entities:
        label = ent.get("label")
        entity_text = ent.get("text")

        if not entity_text:
            continue

        m = LABEL_META.get(label, {
            "color": "#CBD5E1",
            "bg": "rgba(255,255,255,0.08)",
            "border": "rgba(255,255,255,0.15)",
            "icon": "•"
        })

        confidence = ent.get("confidence") or 0.0

        pattern = r"\b" + re.escape(entity_text) + r"\b"

        replacement = (
            f'<span title="{label} ({confidence*100:.0f}%)" '
            f'style="background:{m["bg"]};color:{m["color"]};'
            f'border:1px solid {m["border"]};border-radius:6px;'
            f'padding:2px 6px;font-weight:600;">'
            f'{entity_text}'
            f'<sup style="font-size:9px;opacity:0.7;margin-left:3px;">{m["icon"]}</sup>'
            f'</span>'
        )

        text = re.sub(pattern, replacement, text)

    return f'<span style="color:#E2E8F0;">{text}</span>'

# ─────────────────────────────────────────────────────────────
# Page Renderer
# ─────────────────────────────────────────────────────────────

def render():
    st.markdown(
        """
        <div style="padding:32px 0 20px;">
            <div class="gradient-title" style="font-size:2rem;">🔬 Medical NER</div>
            <div class="subtitle">
                Paste any clinical text and extract structured medical entities
                using a fine-tuned model.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([3, 2], gap="large")

    # ───────────────── LEFT PANEL ─────────────────
    with left:

        # Samples
        st.markdown('<div style="font-size:12px;color:#8892B0;margin-bottom:8px;">Load a sample:</div>', unsafe_allow_html=True)
        cols = st.columns(3)

        for i, s in enumerate(SAMPLE_TEXTS):
            with cols[i]:
                if st.button(f"Sample {i+1}", key=f"sample_{i}", use_container_width=True):
                    st.session_state["ner_text"] = s
                    

        

        text_input = st.text_area(
    "Clinical text",
    
    height=140,
    placeholder="Paste clinical notes...",
    key="ner_text",
    label_visibility="collapsed",
)

        run_btn = st.button("Extract Entities 🔬", use_container_width=True)
        clean_text = (text_input or "").strip()

        # ───────── RESULTS ─────────
        if run_btn and clean_text:
            with st.spinner("Running NER model…"):
                try:
                    st.write("🔍 Sending request...")
                    result = ner_extract(clean_text)
                    #st.write("✅ Response:", result)
                    entities = result.get("entities", [])
                    # Highlighted text
                    st.markdown(
    f"""
    <div style="
        background:#303443;
        padding:16px;
        border-radius:12px;
        border:1px solid #1E293B;
        line-height:2.0;
        font-size:14px;
        color:#E2E8F0;
    ">
        <div style="font-size:11px;color:#dae0e8;font-weight:600;margin-bottom:10px;">
            ✦ Annotated Text
        </div>
        {_highlight_text(clean_text, entities)}
    </div>
    """,
    unsafe_allow_html=True,
)
                    #st.write("✅ Response:", result)
                    
                    

                    # Group entities
                    if entities:
                        st.markdown(
                            f'<div style="font-size:12px;color:#8892B0;margin-top:10px;">{len(entities)} entities found</div>',
                            unsafe_allow_html=True,
                        )

                        groups = {}
                        for e in entities:
                            groups.setdefault(e["label"], []).append(e)

                        for label, ents in groups.items():
                            m = LABEL_META.get(label, {"color": "#8892B0", "icon": "•"})

                            chips = " ".join(
                                f'<span class="entity-chip">'
                                f'{e["text"]} ({((e.get("confidence") or 0.0) * 100):.0f}%)'
                                f'</span>'
                                for e in ents
                            )

                            st.markdown(
                                f"""
                                <div style="margin-top:10px;">
                                    <div style="color:{m["color"]};font-weight:600;">
                                        {m["icon"]} {label}
                                    </div>
                                    <div>{chips}</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    else:
                        st.info("No entities detected.")

                except Exception as e:
                    st.error(f"NER failed: {e}")

    # ───────────────── RIGHT PANEL ─────────────────
    with right:
        st.markdown("### Entity Legend")

        for label, m in LABEL_META.items():
            desc = LABEL_DESCRIPTIONS.get(label, "")

            st.markdown(
                f"""
                <div style="padding:12px;border-radius:10px;
                            background:{m['bg']};
                            border:1px solid {m['border']};
                            margin-bottom:8px;">
                    <b>{m['icon']} {label}</b><br>
                    <span style="font-size:12px;color:#8892B0;">{desc}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )