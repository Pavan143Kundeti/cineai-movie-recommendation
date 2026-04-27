import requests
import time
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import Movie
from dotenv import load_dotenv

load_dotenv()

def update_posters():
    """Update poster paths for existing movies"""
    db = SessionLocal()
    tmdb_api_key = os.getenv('TMDB_API_KEY')
    
    if not tmdb_api_key:
        print("No TMDB API key found!")
        return
    
    print(f"Updating posters using TMDB API...")
    
    try:
        # Get top 60 most popular movies without posters
        movies = db.query(Movie).filter(Movie.poster_path == None).order_by(Movie.popularity.desc()).limit(60).all()
        print(f"Found {len(movies)} movies without posters")
        
        updated = 0
        for movie in movies:
            try:
                url = f"https://api.themoviedb.org/3/movie/{movie.tmdb_id}?api_key={tmdb_api_key}"
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    poster = data.get('poster_path')
                    backdrop = data.get('backdrop_path')
                    
                    if poster:
                        movie.poster_path = poster
                        movie.backdrop_path = backdrop
                        updated += 1
                        
                        if updated % 50 == 0:
                            db.commit()
                            print(f"Updated {updated} posters...")
                
                time.sleep(0.05)  # Rate limiting
                
            except Exception as e:
                print(f"Error updating movie {movie.tmdb_id}: {e}")
                continue
        
        db.commit()
        print(f"\nCompleted! Updated {updated} movie posters")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_posters()
