from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    predicted_class: str
    confidence: float
    created_at: datetime

class PredictionListResponse(BaseModel):
    predictions: list[PredictionResponse]