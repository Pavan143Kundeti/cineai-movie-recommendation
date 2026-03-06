import pandas as pd
import pickle
import sys
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models import Movie
import json
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

def get_tmdb_poster(tmdb_id, api_key):
    """Fetch poster path from TMDB API"""
    if not api_key:
        return None, None
    
    try:
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster = data.get('poster_path')
            backdrop = data.get('backdrop_path')
            return poster, backdrop
    except:
        pass
    return None, None


def migrate_movies_from_csv():
    """Migrate movies from CSV files to database"""
    db = SessionLocal()
    
    # Get TMDB API key from environment
    tmdb_api_key = os.getenv('TMDB_API_KEY')
    if tmdb_api_key:
        print(f"TMDB API key found - will fetch poster images")
    else:
        print("No TMDB API key - using placeholder images")
    
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Load CSV files
        print("Loading CSV files...")
        movies_df = pd.read_csv('../tmdb_5000_movies.csv')
        credits_df = pd.read_csv('../tmdb_5000_credits.csv')
        
        # Merge dataframes
        movies_df = movies_df.merge(credits_df, left_on='id', right_on='movie_id', how='left')
        
        print(f"Found {len(movies_df)} movies to migrate")
        
        migrated_count = 0
        error_count = 0
        
        # Migrate each movie
        for idx, row in movies_df.iterrows():
            try:
                # Check if movie already exists
                existing = db.query(Movie).filter(Movie.tmdb_id == int(row['id'])).first()
                if existing:
                    continue
                
                # Parse genres
                genres = []
                try:
                    if pd.notna(row['genres']):
                        genres_data = json.loads(row['genres'])
                        genres = [g['name'] for g in genres_data if 'name' in g]
                except:
                    pass
                
                # Parse cast
                cast = []
                try:
                    if pd.notna(row['cast']):
                        cast_data = json.loads(row['cast'])
                        cast = [c['name'] for c in cast_data[:10] if 'name' in c]
                except:
                    pass
                
                # Parse crew for director
                director = None
                try:
                    if pd.notna(row['crew']):
                        crew_data = json.loads(row['crew'])
                        directors = [c['name'] for c in crew_data if c.get('job') == 'Director' and 'name' in c]
                        if directors:
                            director = directors[0]
                except:
                    pass
                
                # Get title safely
                title = str(row.get('title', row.get('original_title', 'Unknown')))
                if not title or title == 'nan':
                    continue
                
                # Fetch poster from TMDB API
                poster_path = None
                backdrop_path = None
                if tmdb_api_key and migrated_count < 500:  # Limit API calls
                    poster_path, backdrop_path = get_tmdb_poster(int(row['id']), tmdb_api_key)
                    time.sleep(0.05)  # Rate limiting
                
                # Create movie
                movie = Movie(
                    tmdb_id=int(row['id']),
                    title=title[:500],
                    genres=genres if genres else None,
                    overview=str(row['overview'])[:1000] if pd.notna(row['overview']) else None,
                    release_date=str(row['release_date']) if pd.notna(row['release_date']) else None,
                    poster_path=poster_path,
                    backdrop_path=backdrop_path,
                    vote_average=float(row['vote_average']) if pd.notna(row['vote_average']) else 0.0,
                    vote_count=int(row['vote_count']) if pd.notna(row['vote_count']) else 0,
                    popularity=float(row['popularity']) if pd.notna(row['popularity']) else 0.0,
                    runtime=int(row['runtime']) if pd.notna(row['runtime']) and str(row['runtime']) != 'nan' else None,
                    cast=cast if cast else None,
                    director=director
                )
                
                db.add(movie)
                migrated_count += 1
                
                if (migrated_count) % 100 == 0:
                    try:
                        db.commit()
                        print(f"Migrated {migrated_count} movies...")
                    except Exception as commit_error:
                        print(f"Commit error: {commit_error}")
                        db.rollback()
                    
            except Exception as e:
                error_count += 1
                if error_count < 10:
                    print(f"Error migrating movie: {e}")
                db.rollback()
                continue
        
        try:
            db.commit()
        except:
            db.rollback()
        print(f"\nMigration completed!")
        print(f"Successfully migrated: {migrated_count} movies")
        print(f"Errors: {error_count}")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting database migration...")
    migrate_movies_from_csv()
