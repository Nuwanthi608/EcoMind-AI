from pydantic import BaseModel
from datetime import datetime

class PredictionResponse(BaseModel):
    id: int
    filename: str
    category: str
    confidence: float
    disposal_advice: str
    impact_estimate: str
    created_at: datetime

    class Config:
        from_attributes = True
