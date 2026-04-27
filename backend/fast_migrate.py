"""Fast migration — no TMDB API calls, just CSV data"""
import pandas as pd
import json
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models import Movie
from dotenv import load_dotenv

load_dotenv()

def fast_migrate():
    db = SessionLocal()
    Base.metadata.create_all(bind=engine)

    print("Loading CSV files...")
    movies_df = pd.read_csv('../tmdb_5000_movies.csv')
    credits_df = pd.read_csv('../tmdb_5000_credits.csv')
    movies_df = movies_df.merge(credits_df, left_on='id', right_on='movie_id', how='left')
    print(f"Found {len(movies_df)} movies")

    migrated = errors = 0
    for _, row in movies_df.iterrows():
        try:
            if db.query(Movie).filter(Movie.tmdb_id == int(row['id'])).first():
                continue

            genres, cast, director = [], [], None
            try:
                if pd.notna(row['genres']):
                    genres = [g['name'] for g in json.loads(row['genres'])]
            except: pass
            try:
                if pd.notna(row['cast']):
                    cast = [c['name'] for c in json.loads(row['cast'])[:10]]
            except: pass
            try:
                if pd.notna(row['crew']):
                    dirs = [c['name'] for c in json.loads(row['crew']) if c.get('job') == 'Director']
                    director = dirs[0] if dirs else None
            except: pass

            title = str(row.get('title', row.get('original_title', 'Unknown')))
            if not title or title == 'nan': continue

            db.add(Movie(
                tmdb_id=int(row['id']), title=title[:500],
                genres=genres or None, overview=str(row['overview'])[:1000] if pd.notna(row['overview']) else None,
                release_date=str(row['release_date']) if pd.notna(row['release_date']) else None,
                poster_path=None, backdrop_path=None,
                vote_average=float(row['vote_average']) if pd.notna(row['vote_average']) else 0.0,
                vote_count=int(row['vote_count']) if pd.notna(row['vote_count']) else 0,
                popularity=float(row['popularity']) if pd.notna(row['popularity']) else 0.0,
                runtime=int(row['runtime']) if pd.notna(row['runtime']) and str(row['runtime']) != 'nan' else None,
                cast=cast or None, director=director
            ))
            migrated += 1
            if migrated % 200 == 0:
                db.commit()
                print(f"Migrated {migrated}...")
        except Exception as e:
            errors += 1
            db.rollback()

    db.commit()
    print(f"Done! Migrated: {migrated}, Errors: {errors}")
    db.close()

if __name__ == "__main__":
    fast_migrate()
