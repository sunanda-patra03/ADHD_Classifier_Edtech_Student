from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter(prefix="/adapt", tags=["Adaptive Generation"])


class AdaptInput(BaseModel):
    engagement_label: str
    content: List[Dict]


@router.post("/content")
def adapt_content(data: AdaptInput):
    label = data.engagement_label
    content = data.content

    if label == "Confused":
        content.append({
            "type": "hint",
            "content": "💡 Hint: Think of sunlight as energy for plants."
        })

    elif label == "Bored":
        content.append({
            "type": "question",
            "content": "🤔 What would happen if there was no sunlight?"
        })

    elif label == "Frustrated":
        content.append({
            "type": "encouragement",
            "content": "💙 Take a breath. You're doing well."
        })

    return {
        "engagement": label,
        "adapted_content": content
    }