from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from loguru import logger

from .schemas import RAGRequest, RAGResponse
from .service import RAGService, get_rag_service

router = APIRouter(tags=["RAG"])


@router.post("/query", response_model=RAGResponse, summary="Query medical documents")
async def query_documents(
    request: RAGRequest,
    service: RAGService = Depends(get_rag_service),
):
    try:
        return await service.query(
            question=request.query,
            top_k=request.top_k
        )
    except Exception as e:
        logger.exception("Query failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/upload", summary="Upload a medical PDF")
async def upload_document(
    file: UploadFile = File(...),
    service: RAGService = Depends(get_rag_service),
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )

    try:
        content = await file.read()

        result = await service.ingest_pdf(
            pdf_bytes=content,
            filename=file.filename
        )

        return {
            "message": f"Indexed {result['chunks']} chunks from '{file.filename}'"
        }

    except Exception as e:
        logger.exception("Upload failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/documents", summary="List indexed documents")
async def list_documents(
    service: RAGService = Depends(get_rag_service)
):
    return await service.list_documents()