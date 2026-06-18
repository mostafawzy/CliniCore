from langchain_groq import ChatGroq
from core.config import get_settings


def get_llm():
    settings = get_settings()

    return ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0.1
    )