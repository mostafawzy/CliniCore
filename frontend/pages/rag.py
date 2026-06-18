"""Document Q&A page — RAG with source attribution."""

import streamlit as st
from api_client import rag_query, rag_upload, rag_list_docs

EXAMPLE_QUESTIONS = [
    "What are the contraindications for aspirin?",
    "Summarise the treatment steps for type 2 diabetes.",
    "What does the guideline say about blood pressure targets?",
    "List recommended vaccines for adults over 50.",
]


def render():
    st.markdown(
        """
        <div style="padding:32px 0 20px;">
            <div class="gradient-title" style="font-size:2rem;">📄 Document Q&A</div>
            <div class="subtitle">
                Upload clinical PDFs — drug sheets, WHO guidelines, discharge summaries —
                and ask questions grounded in your documents.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([3, 2], gap="large")

    # ── LEFT: Q&A panel ───────────────────────────────────────────────────────
    with left:
        st.markdown('<div class="section-title">Ask a Question</div>', unsafe_allow_html=True)

    

        query = st.text_area(
            "Question",
            value= "",
            placeholder="What does the guideline recommend for…",
            height=100,
            label_visibility="collapsed",
        )

        col_k, col_btn = st.columns([3, 2])
        with col_k:
            top_k = st.slider("Sources to retrieve", 1, 10, 5)

        with col_btn:
            ask = st.button("Search Documents ", use_container_width=True)

        # ── RESULT ────────────────────────────────────────────────────────────
        if ask and query and query.strip():
            clean_query = query.strip()

            with st.spinner("Retrieving and generating…"):
                try:
                    result = rag_query(clean_query, top_k=top_k)

                    st.markdown(
                        f"""
                        <div class="medi-card" style="border-color:rgba(0,212,170,0.3);">
                            <div style="font-size:11px;color:#00D4AA;font-weight:600;
                                        text-transform:uppercase;letter-spacing:0.06em;
                                        margin-bottom:10px;">✦ Answer</div>
                              <div style="
                                  font-size:14px;
                                  line-height:1.7;
                                  color:#1F2937;
                                  font-weight:500;
                              ">
                                {result.get("answer","")}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    sources = result.get("sources", [])

                    if sources:
                        st.markdown(
                            f'<div style="font-size:12px;color:#8892B0;margin-bottom:10px;">'
                            f'📎 {len(sources)} source chunk(s) retrieved</div>',
                            unsafe_allow_html=True,
                        )

                        for i, src in enumerate(sources):
                            with st.expander(
                                f"Source {i+1} — {src.get('source', 'unknown')}"
                            ):
                                pg = src.get("page")
                                if pg:
                                    st.markdown(
                                        f'<span class="stat-pill pill-blue">Page {pg}</span>',
                                        unsafe_allow_html=True,
                                    )

                                st.markdown(
                                    f'<div class="source-box">{src.get("content","")}</div>',
                                    unsafe_allow_html=True,
                                )

                except Exception as e:
                    st.error(f"Query failed: {e}")

    # ── RIGHT: Upload + doc list ───────────────────────────────────────────────
    with right:
        st.markdown('<div class="section-title">Knowledge Base</div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="medi-card" style="text-align:center;padding:32px 24px;">
                <div style="font-size:36px;margin-bottom:10px;">📂</div>
                <div style="font-size:13px;color:#64748B;margin-bottom:16px;">
                    Upload clinical PDFs to expand the knowledge base.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        uploaded = st.file_uploader(
            " ",
            type=["pdf"],
            label_visibility="collapsed"
        )
        
        st.markdown("""
        <style>
        [data-testid="stFileUploader"] {
            margin-top: -18px;
        }
        
        [data-testid="stFileUploaderDropzone"] {
            border: 1px dashed rgba(20,184,166,0.35) !important;
            background: rgba(20,184,166,0.04) !important;
            border-radius: 12px !important;
            padding: 14px !important;
        }
        </style>
        """, unsafe_allow_html=True)


        if uploaded:
            if st.button("Index Document ", use_container_width=True):
                with st.spinner(f"Indexing {uploaded.name}…"):
                    try:
                        res = rag_upload(uploaded.read(), uploaded.name)
                        st.success(res.get("message", "Indexed!"))
                    except Exception as e:
                        st.error(f"Upload failed: {e}")

        st.markdown("<hr class='medi-divider'/>", unsafe_allow_html=True)

        st.markdown(
            '<div style="font-size:13px;font-weight:600;color:#F0F4FF;margin-bottom:10px;">'
            "Indexed Documents</div>",
            unsafe_allow_html=True,
        )


        try:
            docs = rag_list_docs()
            doc_list = docs.get("documents", [])

            if doc_list:
                for doc in doc_list:
                    st.markdown(
                        f"""
                        <div class="doc-item">
                            📄 <span class="doc-name">{doc}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    '<div style="color:#4A5568;font-size:13px;padding:12px;">'
                    "No documents indexed yet. Upload a PDF to get started.</div>",
                    unsafe_allow_html=True,
                )

        except Exception:
            st.markdown(
                '<div style="color:#4A5568;font-size:13px;">API offline — document list unavailable.</div>',
                unsafe_allow_html=True,
            )
            
            
            