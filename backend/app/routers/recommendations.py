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
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    import json
    from sqlalchemy import text
    query = db.query(Movie).filter(Movie.vote_count >= 50)
    if genre:
        query = query.filter(text(f"JSON_CONTAINS(genres, '{json.dumps(genre)}')"))
    movies = (
        query.order_by((Movie.vote_average * 0.7 + Movie.popularity * 0.3).desc())
        .offset(skip).limit(limit).all()
    )
    return movies


@router.get("/popular/count")
def get_popular_count(genre: str = None, db: Session = Depends(get_db)):
    import json
    from sqlalchemy import text
    query = db.query(Movie).filter(Movie.vote_count >= 50)
    if genre:
        query = query.filter(text(f"JSON_CONTAINS(genres, '{json.dumps(genre)}')"))
    return {"count": query.count()}


@router.get("/trending", response_model=List[MovieResponse])
def get_trending(db: Session = Depends(get_db)):
    """Trending = high vote_average × popularity, recently active"""
    movies = (
        db.query(Movie)
        .filter(Movie.vote_count >= 100)
        .order_by((Movie.vote_average * Movie.popularity).desc())
        .limit(20).all()
    )
    return movies


@router.get("/mood/{mood}", response_model=List[MovieResponse])
def get_by_mood(
    mood: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Personalised mood-based recommendations — blends user taste with mood genre filter"""
    import json
    from sqlalchemy import text

    mood_map = {
        "action":      ["Action", "Adventure", "Thriller"],
        "comedy":      ["Comedy", "Animation", "Family"],
        "feelgood":    ["Romance", "Drama", "Music"],
        "mindbending": ["Science Fiction", "Mystery", "Fantasy"],
        "horror":      ["Horror", "Thriller", "Crime"],
        "classic":     ["Drama", "History", "War"],
    }
    genres = mood_map.get(mood.lower(), ["Action"])
    conditions = " OR ".join(
        [f"JSON_CONTAINS(genres, '{json.dumps(g)}')" for g in genres]
    )

    # Get user's rated movie IDs to exclude already-seen
    from ..models import Rating
    rated_ids = {r.movie_id for r in db.query(Rating).filter(Rating.user_id == current_user.id).all()}

    # Try personalised: get hybrid recs then filter by mood genres
    hybrid_ids = recommendation_engine.get_hybrid_recommendations(
        db, current_user.id, n=100
    )

    # Filter hybrid results by mood genres
    personalised = []
    for mid in hybrid_ids:
        movie = db.query(Movie).filter(Movie.id == mid).first()
        if movie and movie.genres:
            if any(g in movie.genres for g in genres):
                personalised.append(movie)
        if len(personalised) >= 20:
            break

    # If not enough personalised results, fill with top mood movies
    if len(personalised) < 10:
        existing_ids = {m.id for m in personalised} | rated_ids
        fallback = (
            db.query(Movie)
            .filter(Movie.vote_count >= 100)
            .filter(text(f"({conditions})"))
            .filter(Movie.id.notin_(existing_ids) if existing_ids else text("1=1"))
            .order_by((Movie.vote_average * 0.7 + Movie.popularity * 0.3).desc())
            .limit(20 - len(personalised))
            .all()
        )
        personalised.extend(fallback)

    return personalised[:20]


@router.get("/explain/{movie_id}")
def explain_recommendation(
    movie_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Explain why a movie was recommended to the user"""
    return recommendation_engine.explain_recommendation(db, current_user.id, movie_id)
