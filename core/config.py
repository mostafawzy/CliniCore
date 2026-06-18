from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    groq_api_key: SecretStr | None = None

    # RAG
    groq_model: str = "llama-3.3-70b-versatile"

       
    chunk_size: int = 500
    chunk_overlap: int = 50
    vector_store_path: str = "data"

    model_config = {
        "env_file": ".env"
    }


def get_settings():
    settings = Settings()

    if settings.groq_api_key is None:
        raise ValueError("GROQ_API_KEY is not set")

    return settings


