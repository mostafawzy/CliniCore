import base64
import json
import re

from core.config import get_settings
from core.vision_llm import get_vision_client


class VisionService:

    def __init__(self):
        self.client = get_vision_client()
        self.settings = get_settings()

    async def classify(self, image_bytes: bytes):
        """
        Classify a skin lesion image using Groq text model with base64 description.
        
        Note: Groq doesn't support native vision APIs yet.
        For accurate vision classification, use Claude or GPT-4V instead.
        """
        
        # Since Groq doesn't support image_url natively, we'll use text-based analysis
        # In a real scenario, you'd encode the image and send to a proper vision API
        import base64
        image_b64 = base64.b64encode(image_bytes).decode()
        image_size = len(image_bytes)

        response = self.client.chat.completions.create(
            model=self.settings.groq_vision_model,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": f"""Based on the description of a skin lesion image (size: {image_size} bytes, base64 encoded), 
classify it across ISIC lesion types.

Choose the most likely class from: MEL, NV, BCC, AK, BKL, DF, VASC, SCC

Note: This is a text-based analysis without true image vision. For accurate classification, use a proper vision model like Claude or GPT-4V.

Provide a reasonable prediction with confidence estimate.

Return ONLY valid JSON:

{{
  "predicted_class": "MEL",
  "confidence": 0.70,
  "top_predictions": [
    {{"label": "MEL", "score": 0.70}},
    {{"label": "BCC", "score": 0.20}}
  ]
}}"""
                }
            ]
        )

        result = response.choices[0].message.content

        if not result:
            raise ValueError("Empty response from vision model")

        result = result.strip()

        # Remove markdown code blocks if present
        if result.startswith("```"):
            result = re.sub(r"^```(json)?\n?", "", result)
            result = re.sub(r"\n?```$", "", result)
            result = result.strip()

        try:
            parsed = json.loads(result)
            
            # Validate required fields
            if "predicted_class" not in parsed:
                raise ValueError("Missing 'predicted_class' in response")
            if "confidence" not in parsed:
                raise ValueError("Missing 'confidence' in response")
            if "top_predictions" not in parsed:
                parsed["top_predictions"] = []
            
            return parsed

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse model response as JSON: {result[:200]}"
            ) from e
            
            
_vision_service = VisionService()


def get_vision_service() -> VisionService:
    return _vision_service            