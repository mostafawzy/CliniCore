from core.config import get_settings


def get_vectorstore_path():
    return get_settings().vector_store_path