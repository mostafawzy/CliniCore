from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from loguru import logger

from .schemas import VisionResponse
from .service import VisionService, get_vision_service

router = APIRouter()

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


@router.post(
    "/classify",
    response_model=VisionResponse,
    summary="Classify a skin lesion image",
)
async def classify_lesion(
    file: UploadFile = File(...),
    service: VisionService = Depends(get_vision_service),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported file type '{file.content_type}'. "
                "Use JPEG, PNG, or WebP."
            ),
        )

    try:
        image_bytes = await file.read()

        result = await service.classify(image_bytes)

        return VisionResponse(**result)

    except Exception as e:
        logger.exception("Vision classification failed")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Classification failed: {str(e)}",
        )