from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models import Rating
from ..schemas import RatingCreate, RatingResponse
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/ratings", tags=["ratings"])


@router.post("/", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
def create_rating(
    rating_data: RatingCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if rating already exists
    existing_rating = db.query(Rating).filter(
        Rating.user_id == current_user.id,
        Rating.movie_id == rating_data.movie_id
    ).first()
    
    if existing_rating:
        # Update existing rating
        existing_rating.rating = rating_data.rating
        existing_rating.review_text = rating_data.review_text
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    
    # Create new rating
    new_rating = Rating(
        user_id=current_user.id,
        movie_id=rating_data.movie_id,
        rating=rating_data.rating,
        review_text=rating_data.review_text
    )
    
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    
    return new_rating


@router.get("/my-ratings", response_model=List[RatingResponse])
def get_my_ratings(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ratings = db.query(Rating).filter(Rating.user_id == current_user.id).all()
    return ratings


@router.get("/movie/{movie_id}", response_model=RatingResponse)
def get_user_rating_for_movie(
    movie_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rating = db.query(Rating).filter(
        Rating.user_id == current_user.id,
        Rating.movie_id == movie_id
    ).first()
    
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    return rating
