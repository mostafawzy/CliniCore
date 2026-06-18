"""Skin Vision page — dermoscopy image classification with EfficientNet-B0."""

import io
import streamlit as st
from api_client import vision_classify

# ISIC 2019 class metadata
ISIC_CLASSES = {
    "MEL":  {"name": "Melanoma",                    "icon": "🔴", "risk": "High",   "color": "#F43F5E"},
    "NV":   {"name": "Melanocytic Nevus",            "icon": "🟢", "risk": "Low",    "color": "#22C55E"},
    "BCC":  {"name": "Basal Cell Carcinoma",         "icon": "🟠", "risk": "Medium", "color": "#F97316"},
    "AK":   {"name": "Actinic Keratosis",            "icon": "🟡", "risk": "Medium", "color": "#EAB308"},
    "BKL":  {"name": "Benign Keratosis",             "icon": "🟢", "risk": "Low",    "color": "#22C55E"},
    "DF":   {"name": "Dermatofibroma",               "icon": "🟢", "risk": "Low",    "color": "#22C55E"},
    "VASC": {"name": "Vascular Lesion",              "icon": "🟡", "risk": "Low-Med","color": "#A3E635"},
    "SCC":  {"name": "Squamous Cell Carcinoma",      "icon": "🔴", "risk": "High",   "color": "#EF4444"},
}

RISK_COLOR = {"High": "#F43F5E", "Medium": "#F97316", "Low-Med": "#A3E635", "Low": "#22C55E"}


def _confidence_bar(pct: float, color: str) -> str:
    return f"""
    <div class="conf-bar-wrap">
        <div class="conf-bar-fill" style="width:{pct:.1f}%;background:{color};"></div>
    </div>
    """


def render():
    st.markdown(
        """
        <div style="padding:32px 0 20px;">
            <div class="gradient-title" style="font-size:2rem;">🔭 Skin Vision</div>
            <div class="subtitle">
                Upload a dermoscopy or clinical skin image and classify it across
                8 ISIC lesion types using a fine-tuned EfficientNet-B0 model.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([2, 3], gap="large")

    # ── LEFT: Upload ──────────────────────────────────────────────────────────
    with left:
        st.markdown('<div class="section-title">Upload Image</div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="medi-card" style="text-align:center;padding:32px 20px;
                                           border-style:dashed;border-color:rgba(0,212,170,0.3);">
                <div style="font-size:48px;margin-bottom:10px;">🩺</div>
                <div style="font-size:13px;color:#8892B0;line-height:1.6;">
                    Accepts dermoscopy or clinical photos.<br/>
                    JPEG · PNG · WebP
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        uploaded = st.file_uploader(
            "Skin image",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
        )

        if uploaded:
            st.image(uploaded, caption="Uploaded image", use_container_width=True)
            classify_btn = st.button("Classify Lesion ", use_container_width=True)

            if classify_btn:
                with st.spinner("Classifying lesion…"):
                    try:
                        image_bytes = uploaded.getvalue()
                        result = vision_classify(
                            image_bytes=image_bytes,
                            filename=uploaded.name,
                            content_type=uploaded.type or "image/jpeg",
                        )
                        st.session_state["vision_result"] = result
                        st.rerun()
                    except Exception as e:
                        st.error(f"Classification failed: {e}")

        # Class reference
        st.markdown("<hr class='medi-divider'/>", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:12px;font-weight:600;color:#8892B0;'
            'text-transform:uppercase;letter-spacing:0.05em;margin-bottom:10px;">ISIC Classes</div>',
            unsafe_allow_html=True,
        )
        for code, meta in ISIC_CLASSES.items():
            risk_c = RISK_COLOR.get(meta["risk"], "#8892B0")
            st.markdown(
                f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:6px 10px;border-radius:7px;margin-bottom:4px;
                            background:rgba(255,255,255,0.02);">
                    <div style="font-size:12px;">
                        <span style="color:{meta['color']};margin-right:6px;">{meta['icon']}</span>
                        <span style="color:#CBD5E0;font-weight:500;">{code}</span>
                        <span style="color:#4A5568;margin-left:4px;">{meta['name']}</span>
                    </div>
                    <span style="font-size:10px;font-weight:600;color:{risk_c};">{meta['risk']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── RIGHT: Results ────────────────────────────────────────────────────────
    with right:
        result = st.session_state.get("vision_result")

        if not result:
            # Placeholder state
            st.markdown(
                """
                <div class="medi-card" style="text-align:center;padding:60px 40px;
                                               border-style:dashed;min-height:300px;
                                               display:flex;flex-direction:column;
                                               align-items:center;justify-content:center;">
                    <div style="font-size:64px;margin-bottom:16px;opacity:0.3;">🔭</div>
                    <div style="color:#4A5568;font-size:14px;max-width:280px;line-height:1.6;">
                        Upload a skin image on the left and click
                        <strong style="color:#8892B0;">Classify Lesion</strong>
                        to see predictions here.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            pred_class = result.get("predicted_class", "UNK")
            confidence = result.get("confidence", 0.0) * 100
            top_preds  = result.get("top_predictions", [])
            meta       = ISIC_CLASSES.get(pred_class, {"name": pred_class, "icon": "•", "risk": "Unknown", "color": "#8892B0"})
            risk_c     = RISK_COLOR.get(meta["risk"], "#8892B0")

            # Primary result card
            st.markdown(
                f"""
                <div class="medi-card" style="border-color:{meta['color']}44;padding:28px;">
                    <div style="font-size:11px;color:#8892B0;font-weight:600;
                                text-transform:uppercase;letter-spacing:0.06em;margin-bottom:16px;">
                        ✦ Primary Prediction
                    </div>
                    <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;">
                        <div style="font-size:52px;">{meta['icon']}</div>
                        <div>
                            <div style="font-family:'Space Grotesk',sans-serif;font-size:1.6rem;
                                        font-weight:700;color:{meta['color']};">{pred_class}</div>
                            <div style="font-size:14px;color:#CBD5E0;margin-top:2px;">{meta['name']}</div>
                            <div style="margin-top:8px;">
                                <span style="font-size:11px;font-weight:700;padding:3px 10px;
                                             border-radius:999px;color:{risk_c};
                                             background:{risk_c}18;border:1px solid {risk_c}44;">
                                    {meta['risk']} Risk
                                </span>
                            </div>
                        </div>
                        <div style="margin-left:auto;text-align:right;">
                            <div style="font-family:'Space Grotesk',sans-serif;font-size:2rem;
                                        font-weight:700;color:{meta['color']};">{confidence:.1f}%</div>
                            <div style="font-size:11px;color:#8892B0;">confidence</div>
                        </div>
                    </div>
                    {_confidence_bar(confidence, meta['color'])}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Top-N predictions
            if top_preds:
                st.markdown(
                    '<div style="font-size:12px;font-weight:600;color:#8892B0;'
                    'text-transform:uppercase;letter-spacing:0.05em;margin:16px 0 10px;">All Predictions</div>',
                    unsafe_allow_html=True,
                )
                for p in top_preds:
                    pc  = p.get("label", p.get("class", "?"))
                    pct = p.get("score", p.get("confidence", 0)) * 100
                    pm  = ISIC_CLASSES.get(pc, {"color": "#8892B0", "name": pc})
                    st.markdown(
                        f"""
                        <div style="margin-bottom:10px;">
                            <div style="display:flex;justify-content:space-between;
                                        font-size:13px;margin-bottom:4px;">
                                <span style="color:{pm['color']};font-weight:600;">{pc}</span>
                                <span style="color:#8892B0;">{pm['name']}</span>
                                <span style="color:{pm['color']};font-weight:600;">{pct:.1f}%</span>
                            </div>
                            {_confidence_bar(pct, pm['color'])}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            # Disclaimer
            st.markdown(
                f'<div class="disclaimer">'
                f'{result.get("disclaimer", "Research tool only — not a substitute for clinical diagnosis.")}'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Clear button
            if st.button("← Classify another image", use_container_width=True):
                if "vision_result" in st.session_state:
                    del st.session_state["vision_result"]
                st.rerun()
