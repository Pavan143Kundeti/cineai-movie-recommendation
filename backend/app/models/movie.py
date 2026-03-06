from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, unique=True, index=True, nullable=False)
    title = Column(String(500), nullable=False, index=True)
    genres = Column(JSON, nullable=True)
    overview = Column(Text, nullable=True)
    release_date = Column(String(50), nullable=True)
    poster_path = Column(String(500), nullable=True)
    backdrop_path = Column(String(500), nullable=True)
    vote_average = Column(Float, default=0.0)
    vote_count = Column(Integer, default=0)
    popularity = Column(Float, default=0.0)
    runtime = Column(Integer, nullable=True)
    cast = Column(JSON, nullable=True)
    director = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")
    watchlist = relationship("Watchlist", back_populates="movie", cascade="all, delete-orphan")
