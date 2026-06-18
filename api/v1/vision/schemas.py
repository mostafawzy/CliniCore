from typing import Any
from pydantic import BaseModel


class VisionResponse(BaseModel):
    predicted_class: str
    confidence: float
    top_predictions: list[dict[str, Any]]

    disclaimer: str = (
        "This is a research tool only. "
        "Always consult a qualified dermatologist."
    )