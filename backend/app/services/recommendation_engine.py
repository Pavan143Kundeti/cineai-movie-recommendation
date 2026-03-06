import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from ..models import Movie, Rating, User


class RecommendationEngine:
    def __init__(self):
        self.similarity_matrix = None
        self.movie_indices = {}
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        
    def build_content_based_model(self, db: Session):
        """Build content-based filtering model using TF-IDF and cosine similarity"""
        movies = db.query(Movie).all()
        
        if not movies:
            return
        
        # Create feature strings combining genres, overview, cast, director
        features = []
        movie_ids = []
        
        for movie in movies:
            genres_str = ' '.join(movie.genres) if movie.genres else ''
            cast_str = ' '.join(movie.cast[:5]) if movie.cast else ''
            director_str = movie.director if movie.director else ''
            overview_str = movie.overview if movie.overview else ''
            
            feature = f"{genres_str} {genres_str} {overview_str} {cast_str} {director_str}"
            features.append(feature)
            movie_ids.append(movie.id)
            self.movie_indices[movie.id] = len(movie_ids) - 1
        
        # Compute TF-IDF matrix
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(features)
        
        # Compute cosine similarity
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
    def get_content_based_recommendations(self, movie_id: int, n: int = 20) -> List[Tuple[int, float]]:
        """Get content-based recommendations for a movie"""
        if self.similarity_matrix is None or movie_id not in self.movie_indices:
            return []
        
        idx = self.movie_indices[movie_id]
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1]  # Exclude the movie itself
        
        # Convert indices back to movie IDs
        movie_ids_list = list(self.movie_indices.keys())
        recommendations = [(movie_ids_list[i], score) for i, score in sim_scores]
        
        return recommendations
    
    def get_collaborative_recommendations(self, db: Session, user_id: int, n: int = 20) -> List[Tuple[int, float]]:
        """Get collaborative filtering recommendations using user-based CF"""
        # Get all ratings
        ratings = db.query(Rating).all()
        
        if len(ratings) < 10:
            return []
        
        # Create user-item matrix
        rating_data = [(r.user_id, r.movie_id, r.rating) for r in ratings]
        df = pd.DataFrame(rating_data, columns=['user_id', 'movie_id', 'rating'])
        
        user_movie_matrix = df.pivot_table(index='user_id', columns='movie_id', values='rating')
        
        if user_id not in user_movie_matrix.index:
            return []
        
        # Fill NaN with 0
        user_movie_matrix_filled = user_movie_matrix.fillna(0)
        
        # Compute user similarity using Pearson correlation
        user_similarity = user_movie_matrix_filled.T.corr()
        
        if user_id not in user_similarity.columns:
            return []
        
        # Get similar users
        similar_users = user_similarity[user_id].sort_values(ascending=False)[1:51]
        
        # Get movies rated by similar users but not by target user
        user_rated_movies = set(user_movie_matrix.loc[user_id].dropna().index)
        
        recommendations = {}
        for similar_user_id, similarity_score in similar_users.items():
            if similarity_score <= 0:
                continue
                
            similar_user_ratings = user_movie_matrix.loc[similar_user_id].dropna()
            
            for movie_id, rating in similar_user_ratings.items():
                if movie_id not in user_rated_movies:
                    if movie_id not in recommendations:
                        recommendations[movie_id] = 0
                    recommendations[movie_id] += rating * similarity_score
        
        # Sort and return top N
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:n]
        
        return sorted_recs
    
    def get_hybrid_recommendations(self, db: Session, user_id: int, movie_id: int = None, n: int = 20) -> List[int]:
        """Get hybrid recommendations combining content-based and collaborative filtering"""
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return []
        
        # Get user's rating count
        rating_count = db.query(Rating).filter(Rating.user_id == user_id).count()
        
        # Adjust weights based on user history
        if rating_count < 5:
            collab_weight = 0.2
            content_weight = 0.8
        else:
            collab_weight = 0.6
            content_weight = 0.4
        
        recommendations = {}
        
        # Get collaborative recommendations
        if rating_count >= 5:
            collab_recs = self.get_collaborative_recommendations(db, user_id, n=30)
            for movie_id_rec, score in collab_recs:
                recommendations[movie_id_rec] = score * collab_weight
        
        # Get content-based recommendations
        if movie_id and self.similarity_matrix is not None:
            content_recs = self.get_content_based_recommendations(movie_id, n=30)
            for movie_id_rec, score in content_recs:
                if movie_id_rec in recommendations:
                    recommendations[movie_id_rec] += score * content_weight
                else:
                    recommendations[movie_id_rec] = score * content_weight
        
        # Apply user preferences boost
        if user.preferences:
            preferred_genres = user.preferences.preferred_genres or []
            disliked_genres = user.preferences.disliked_genres or []
            
            for movie_id_rec in list(recommendations.keys()):
                movie = db.query(Movie).filter(Movie.id == movie_id_rec).first()
                if movie and movie.genres:
                    # Boost for preferred genres
                    if any(genre in preferred_genres for genre in movie.genres):
                        recommendations[movie_id_rec] *= 1.1
                    
                    # Penalize for disliked genres
                    if any(genre in disliked_genres for genre in movie.genres):
                        recommendations[movie_id_rec] *= 0.8
        
        # Sort and return top N
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:n]
        
        return [movie_id for movie_id, _ in sorted_recs]
    
    def get_popular_recommendations(self, db: Session, genres: List[str] = None, n: int = 20) -> List[int]:
        """Get popular movies for cold start users"""
        query = db.query(Movie).filter(Movie.vote_count >= 100)
        
        if genres:
            # Filter by genres (this is simplified, you may need JSON query for MySQL)
            query = query.filter(Movie.genres.contains(genres[0]))
        
        movies = query.order_by(
            (Movie.vote_average * 0.7 + Movie.popularity * 0.3).desc()
        ).limit(n).all()
        
        return [movie.id for movie in movies]


# Global instance
recommendation_engine = RecommendationEngine()
