from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class EntityLabel(str, Enum):
    DISEASE = "DISEASE"
    SYMPTOM = "SYMPTOM"
    MEDICATION = "MEDICATION"
    VACCINE = "VACCINE"
    PROCEDURE = "PROCEDURE"
    ANATOMY = "ANATOMY"
    DOSAGE = "DOSAGE"
    AGE_GROUP = "AGE_GROUP"


class NERRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=5
    )


class NEREntity(BaseModel):
    text: str
    label: EntityLabel

    start: Optional[int] = None
    end: Optional[int] = None
    normalized: Optional[str] = None
    confidence: float


class NERResponse(BaseModel):
    text: str
    entities: List[NEREntity]
    entity_count: int