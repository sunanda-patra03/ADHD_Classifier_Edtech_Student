from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.ml_client import call_ml_service
from app.adapters.passthrough_adapter import adapt

router = APIRouter(prefix="/process", tags=["Content Processing"])

ML_SIMPLIFY_URL = "http://<ML_IP>:8001/simplify"


class ContentInput(BaseModel):
    text: Optional[str] = None
    image_base64: Optional[str] = None


@router.post("/content")
def process_content(data: ContentInput):
    # ✅ Validation: at least one input required
    if not data.text and not data.image_base64:
        raise HTTPException(
            status_code=400,
            detail="Either text or image must be provided"
        )

    payload = {
        "text": data.text,
        "image_base64": data.image_base64
    }

    raw_ml_output = call_ml_service(
        ML_SIMPLIFY_URL,
        payload=payload
    )

    return adapt(raw_ml_output)