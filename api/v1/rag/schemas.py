from pydantic import BaseModel, Field


class RAGRequest(BaseModel):
    query: str = Field(..., min_length=3)
    top_k: int = Field(default=5, ge=1, le=20)


class RAGSource(BaseModel):
    content: str
    source: str
    page: int | None = None


class RAGResponse(BaseModel):
    answer: str
    sources: list[RAGSource]
    query: str