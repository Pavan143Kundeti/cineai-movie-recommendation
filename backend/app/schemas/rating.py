from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RatingCreate(BaseModel):
    movie_id: int
    rating: float = Field(..., ge=1.0, le=10.0)
    review_text: Optional[str] = Field(None, max_length=1000)


class RatingUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=1.0, le=10.0)
    review_text: Optional[str] = Field(None, max_length=1000)


class RatingResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: float
    review_text: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
