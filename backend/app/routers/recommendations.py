from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models import Movie
from ..schemas import MovieResponse
from ..services.recommendation_engine import recommendation_engine
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/recommendations", tags=["recommendations"])


@router.get("/", response_model=List[MovieResponse])
def get_recommendations(
    movie_id: int = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized recommendations for the current user"""
    
    # Get hybrid recommendations
    movie_ids = recommendation_engine.get_hybrid_recommendations(
        db, current_user.id, movie_id=movie_id, n=20
    )
    
    # If no recommendations, fall back to popular movies
    if not movie_ids:
        preferred_genres = []
        if current_user.preferences and current_user.preferences.preferred_genres:
            preferred_genres = current_user.preferences.preferred_genres
        
        movie_ids = recommendation_engine.get_popular_recommendations(
            db, genres=preferred_genres, n=20
        )
    
    # Fetch movie details
    movies = db.query(Movie).filter(Movie.id.in_(movie_ids)).all()
    
    # Sort by the order of movie_ids
    movie_dict = {movie.id: movie for movie in movies}
    sorted_movies = [movie_dict[mid] for mid in movie_ids if mid in movie_dict]
    
    return sorted_movies


@router.get("/popular", response_model=List[MovieResponse])
def get_popular_movies(
    genre: str = None,
    db: Session = Depends(get_db)
):
    """Get popular movies (for cold start or guest users)"""
    genres = [genre] if genre else None
    movie_ids = recommendation_engine.get_popular_recommendations(db, genres=genres, n=20)
    
    movies = db.query(Movie).filter(Movie.id.in_(movie_ids)).all()
    
    return movies
