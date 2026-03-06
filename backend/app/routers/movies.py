from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..models import Movie
from ..schemas import MovieResponse, MovieSearch

router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


@router.get("/", response_model=List[MovieResponse])
def get_movies(
    skip: int = 0,
    limit: int = 20,
    genre: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Movie)
    
    if genre:
        query = query.filter(Movie.genres.contains(genre))
    
    movies = query.offset(skip).limit(limit).all()
    return movies


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return movie


@router.get("/search/", response_model=List[MovieResponse])
def search_movies(
    q: Optional[str] = Query(None, min_length=1),
    genre: Optional[str] = None,
    min_rating: Optional[float] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(Movie)
    
    if q:
        query = query.filter(Movie.title.contains(q))
    
    if genre:
        query = query.filter(Movie.genres.contains(genre))
    
    if min_rating:
        query = query.filter(Movie.vote_average >= min_rating)
    
    movies = query.order_by(Movie.popularity.desc()).offset(skip).limit(limit).all()
    
    return movies
