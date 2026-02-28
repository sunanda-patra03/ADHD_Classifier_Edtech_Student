from fastapi import APIRouter
from pydantic import BaseModel
import requests

router = APIRouter(prefix="/reaction", tags=["Reaction Analysis"])

ML_REACTION_URL = "http://<ML_IP>:8002/analyze"  # teammate ML service


class ReactionInput(BaseModel):
    image_base64: str
    interaction_metrics: dict


@router.post("/analyze")
def analyze_reaction(data: ReactionInput):
    """
    Frontend → Backend → ML → Backend
    """

    try:
        ml_response = requests.post(
            ML_REACTION_URL,
            json=data.dict(),
            timeout=10
        )
        ml_response.raise_for_status()
    except Exception as e:
        return {"error": "ML service unavailable", "details": str(e)}

    ml_data = ml_response.json()

    # Backend interpretation layer
    if ml_data["prediction"]["attention_level"] == "High":
        label = "Focused"
    elif ml_data["prediction"]["engagement_score"] < 0.4:
        label = "Distracted"
    else:
        label = "Confused"

    return {
        "engagement_label": label,
        "confidence": ml_data["prediction"]["confidence"],
        "model_version": ml_data.get("model_version")
    }