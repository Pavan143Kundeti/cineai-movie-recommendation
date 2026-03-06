from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models import Watchlist, Movie
from ..schemas import MovieResponse
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/watchlist", tags=["watchlist"])


@router.post("/{movie_id}", status_code=status.HTTP_201_CREATED)
def add_to_watchlist(
    movie_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if already in watchlist
    existing = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.id,
        Watchlist.movie_id == movie_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Movie already in watchlist")
    
    # Add to watchlist
    watchlist_item = Watchlist(user_id=current_user.id, movie_id=movie_id)
    db.add(watchlist_item)
    db.commit()
    
    return {"message": "Movie added to watchlist"}


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_watchlist(
    movie_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    watchlist_item = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.id,
        Watchlist.movie_id == movie_id
    ).first()
    
    if not watchlist_item:
        raise HTTPException(status_code=404, detail="Movie not in watchlist")
    
    db.delete(watchlist_item)
    db.commit()
    
    return None


@router.get("/", response_model=List[MovieResponse])
def get_watchlist(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    watchlist_items = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.id
    ).order_by(Watchlist.added_at.desc()).all()
    
    movie_ids = [item.movie_id for item in watchlist_items]
    movies = db.query(Movie).filter(Movie.id.in_(movie_ids)).all()
    
    # Sort by watchlist order
    movie_dict = {movie.id: movie for movie in movies}
    sorted_movies = [movie_dict[mid] for mid in movie_ids if mid in movie_dict]
    
    return sorted_movies
