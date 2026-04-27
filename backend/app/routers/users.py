from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import UserPreference
from ..schemas import UserPreferenceUpdate, UserResponse
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/stats")
def get_user_stats(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from ..models import Rating, Movie
    from sqlalchemy import func
    ratings = db.query(Rating).filter(Rating.user_id == current_user.id).all()
    if not ratings:
        return {"total_ratings": 0, "avg_rating": 0, "fav_genre": "N/A", "top_movie": None}

    avg = round(sum(r.rating for r in ratings) / len(ratings), 1)

    # Find favourite genre
    genre_count = {}
    for r in ratings:
        movie = db.query(Movie).filter(Movie.id == r.movie_id).first()
        if movie and movie.genres:
            for g in movie.genres:
                genre_count[g] = genre_count.get(g, 0) + 1
    fav_genre = max(genre_count, key=genre_count.get) if genre_count else "N/A"

    # Top rated movie
    top = max(ratings, key=lambda r: r.rating)
    top_movie = db.query(Movie).filter(Movie.id == top.movie_id).first()

    return {
        "total_ratings": len(ratings),
        "avg_rating": avg,
        "fav_genre": fav_genre,
        "top_movie": top_movie.title if top_movie else None,
        "top_rating": top.rating,
    }


@router.post("/preferences")
def update_preferences(
    prefs: UserPreferenceUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    preference = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()

    if preference:
        if prefs.preferred_genres is not None:
            preference.preferred_genres = prefs.preferred_genres
        if prefs.disliked_genres is not None:
            preference.disliked_genres = prefs.disliked_genres
    else:
        preference = UserPreference(
            user_id=current_user.id,
            preferred_genres=prefs.preferred_genres,
            disliked_genres=prefs.disliked_genres
        )
        db.add(preference)

    db.commit()
    return {"message": "Preferences updated", "preferred_genres": preference.preferred_genres}


@router.get("/preferences")
def get_preferences(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pref = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()
    if not pref:
        return {"preferred_genres": [], "disliked_genres": []}
    return {
        "preferred_genres": pref.preferred_genres or [],
        "disliked_genres": pref.disliked_genres or []
    }
