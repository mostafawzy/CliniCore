from fastapi import APIRouter

from api.v1.ner.schemas import NERRequest, NERResponse
from api.v1.ner.service import NERService

router = APIRouter(tags=["NER"])


service = NERService()


@router.post("/extract", response_model=NERResponse)
async def extract_entities(request: NERRequest):
    """
    Extract clinical named entities from text.
    """
    return await service.extract(request)