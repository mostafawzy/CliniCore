from typing import List
from loguru import logger

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from core.llm import get_llm
from api.v1.ner.schemas import NERRequest, NERResponse, NEREntity


class NERService:
    def __init__(self):
        self._llm = get_llm()
        self._parser = JsonOutputParser(pydantic_object=NERResponse)

        self._prompt = ChatPromptTemplate.from_template("""
You are a clinical Named Entity Recognition system.

Extract entities using ONLY these labels:
DISEASE, SYMPTOM, MEDICATION, VACCINE, PROCEDURE, ANATOMY, DOSAGE, AGE_GROUP.

Return strict JSON only.
Do not hallucinate entities.
Keep exact spans.
Skip uncertain cases.

Text:
{text}

{format_instructions}
""")

    def _normalize(self, entity: NEREntity) -> NEREntity:
        """Light rule-based normalization layer"""

        mapping = {
            "hpv": "Human Papillomavirus Vaccine",
            "mmr": "Measles Mumps Rubella Vaccine",
            "hep b": "Hepatitis B Vaccine",
        }

        key = entity.text.lower()

        if key in mapping:
            entity.normalized = mapping[key]

        return entity

    async def extract(self, request: NERRequest) -> NERResponse:
        logger.info("NER extraction started")

        chain = self._prompt | self._llm | self._parser

        raw = await chain.ainvoke({
            "text": request.text,
            "format_instructions": self._parser.get_format_instructions(),
        })

        try:
            result = NERResponse.model_validate(raw)
        except Exception:
            logger.error(f"Invalid NER output: {raw}")
            raise ValueError("NER output parsing failed")

        entities: List[NEREntity] = [
            self._normalize(ent) for ent in result.entities
        ]

        return NERResponse(
            text=request.text,
            entities=entities,
            entity_count=len(entities),
        )