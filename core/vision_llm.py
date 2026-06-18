from groq import Groq

from core.config import get_settings


def get_vision_client():
    settings = get_settings()

    api_key = settings.groq_api_key
    assert api_key is not None

    return Groq(
        api_key=api_key.get_secret_value()
    )
    
    