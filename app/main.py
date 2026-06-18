# app/main.py

from fastapi import FastAPI

from api.v1.rag.router import router as rag_router
from api.v1.ner.router import router as ner_router
from api.v1.vision.router import router as vision_router

app = FastAPI(title="ClinCore")


# Register routers
app.include_router(rag_router, prefix="/api/v1/rag", tags=["RAG"])
app.include_router(ner_router, prefix="/api/v1/ner", tags=["NER"])
app.include_router(vision_router, prefix="/api/v1/vision", tags=["Vision"])

@app.get("/")
def root():
    return {
        "message": "ClinCore is running",
        "status": "ok"
    }
    
    