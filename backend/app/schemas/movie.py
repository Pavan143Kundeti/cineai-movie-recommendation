from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MovieBase(BaseModel):
    tmdb_id: int
    title: str
    genres: Optional[List[str]] = None
    overview: Optional[str] = None
    release_date: Optional[str] = None
    poster_path: Optional[str] = None
    vote_average: Optional[float] = 0.0
    popularity: Optional[float] = 0.0


class MovieResponse(MovieBase):
    id: int
    vote_count: int
    runtime: Optional[int] = None
    cast: Optional[List[str]] = None
    director: Optional[str] = None
    
    class Config:
        from_attributes = True


class MovieSearch(BaseModel):
    query: Optional[str] = None
    genres: Optional[List[str]] = None
    min_rating: Optional[float] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None
