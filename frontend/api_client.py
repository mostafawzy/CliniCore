import httpx
import streamlit as st

import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"
TIMEOUT = 60.0


def _base() -> str:
    """
    Returns API base URL (no trailing slash)
    Example: http://localhost:8000
    """
    return st.session_state.get("api_base_url", "http://localhost:8000").rstrip("/")


def _request(method: str, path: str, **kwargs) -> dict:
    """
    Centralized request handler with proper error handling
    """
    url = f"{_base()}{path}"

    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.request(method, url, **kwargs)
            r.raise_for_status()
            return r.json()

    except httpx.HTTPStatusError as e:
        try:
            detail = e.response.json()
        except Exception:
            detail = e.response.text

        raise Exception(f"API Error {e.response.status_code}: {detail}")

    except Exception as e:
        raise Exception(f"Request failed: {str(e)}")


# ── RAG ───────────────────────────────────────────────────────────────────────



def rag_query(query: str, top_k: int = 5):
    response = requests.post(
        f"{BASE_URL}/rag/query",
        json={"query": query, "top_k": top_k},
        timeout=60
    )
    return response.json()


def rag_upload(file_bytes: bytes, filename: str):
    files = {"file": (filename, file_bytes, "application/pdf")}

    response = requests.post(
        f"{BASE_URL}/rag/upload",
        files=files,
        timeout=120
    )
    return response.json()


def rag_list_docs():
    response = requests.get(
        f"{BASE_URL}/rag/documents",
        timeout=30
    )
    return response.json()

# ── NER ───────────────────────────────────────────────────────────────────────

def ner_extract(text: str) -> dict:
    print("🔥 USING NEW NER FUNCTION")
    print("URL:", f"{BASE_URL}/ner/extract")

    response = requests.post(
        f"{BASE_URL}/ner/extract",
        json={"text": text},
        timeout=60
    )
    return response.json()  


# ── Vision ────────────────────────────────────────────────────────────────────

def vision_classify(
    image_bytes: bytes,
    filename: str,
    content_type: str,
) -> dict:
    return _request(
        "POST",
        "/api/v1/vision/classify",
        files={
            "file": (
                filename,
                image_bytes,
                content_type,
            )
        },
    )




# ── Health ────────────────────────────────────────────────────────────────────


def health_check():
    try:
        r = httpx.get("http://localhost:8000/", timeout=5.0)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "offline", "error": str(e)}