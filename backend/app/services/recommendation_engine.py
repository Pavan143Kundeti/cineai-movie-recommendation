import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler
from typing import List, Tuple, Dict
from sqlalchemy.orm import Session
from ..models import Movie, Rating, User
import logging

logger = logging.getLogger(__name__)


class RecommendationEngine:
    def __init__(self):
        # Content-based
        self.similarity_matrix = None
        self.movie_indices = {}
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=10000,
            sublinear_tf=True
        )
        # SVD / Matrix Factorization
        self.svd_model = None
        self.svd_user_factors = None
        self.svd_movie_factors = None
        self.svd_user_index = {}
        self.svd_movie_index = {}
        self.svd_movie_ids = []
        self.n_components = 50

    # ------------------------------------------------------------------
    # Content-Based Model  (TF-IDF + Cosine Similarity)
    # ------------------------------------------------------------------
    def build_content_based_model(self, db: Session):
        """Build TF-IDF content model on genres, overview, cast, director."""
        movies = db.query(Movie).all()
        if not movies:
            logger.warning("No movies found — skipping content model build.")
            return

        features, movie_ids = [], []
        for movie in movies:
            genres_str  = ' '.join(movie.genres) if movie.genres else ''
            cast_str    = ' '.join(movie.cast[:5]) if movie.cast else ''
            director    = movie.director or ''
            overview    = movie.overview or ''
            # Weight genres 3x — most important signal
            feat = f"{genres_str} {genres_str} {genres_str} {overview} {cast_str} {director}"
            features.append(feat)
            movie_ids.append(movie.id)
            self.movie_indices[movie.id] = len(movie_ids) - 1

        tfidf_matrix = self.tfidf_vectorizer.fit_transform(features)
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        logger.info(f"Content model built for {len(movies)} movies.")

    def get_content_based_recommendations(self, movie_id: int, n: int = 20) -> List[Tuple[int, float]]:
        if self.similarity_matrix is None or movie_id not in self.movie_indices:
            return []
        idx = self.movie_indices[movie_id]
        scores = list(enumerate(self.similarity_matrix[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:n + 1]
        id_list = list(self.movie_indices.keys())
        return [(id_list[i], s) for i, s in scores]

    # ------------------------------------------------------------------
    # SVD Matrix Factorization  (Collaborative)
    # ------------------------------------------------------------------
    def build_svd_model(self, db: Session):
        """Build SVD latent-factor model from user-rating matrix."""
        ratings = db.query(Rating).all()
        if len(ratings) < 20:
            logger.info("Not enough ratings for SVD — need at least 20.")
            return

        data = [(r.user_id, r.movie_id, r.rating) for r in ratings]
        df = pd.DataFrame(data, columns=['user_id', 'movie_id', 'rating'])

        # Normalise ratings per user (subtract mean)
        user_means = df.groupby('user_id')['rating'].mean()
        df['rating_norm'] = df.apply(
            lambda row: row['rating'] - user_means[row['user_id']], axis=1
        )

        users   = df['user_id'].unique()
        movies  = df['movie_id'].unique()
        self.svd_user_index  = {u: i for i, u in enumerate(users)}
        self.svd_movie_index = {m: i for i, m in enumerate(movies)}
        self.svd_movie_ids   = list(movies)

        R = np.zeros((len(users), len(movies)))
        for _, row in df.iterrows():
            ui = self.svd_user_index[row['user_id']]
            mi = self.svd_movie_index[row['movie_id']]
            R[ui, mi] = row['rating_norm']

        n_comp = min(self.n_components, min(R.shape) - 1)
        svd = TruncatedSVD(n_components=n_comp, random_state=42)
        self.svd_user_factors  = svd.fit_transform(R)
        self.svd_movie_factors = svd.components_.T
        self.svd_model = svd
        logger.info(f"SVD model built: {len(users)} users × {len(movies)} movies, {n_comp} components.")

    def get_svd_recommendations(self, db: Session, user_id: int, n: int = 20) -> List[Tuple[int, float]]:
        """Predict ratings via SVD latent factors."""
        if self.svd_user_factors is None or user_id not in self.svd_user_index:
            return self.get_collaborative_recommendations(db, user_id, n)

        ui = self.svd_user_index[user_id]
        scores = self.svd_user_factors[ui] @ self.svd_movie_factors.T

        # Exclude already-rated movies
        rated = {r.movie_id for r in db.query(Rating).filter(Rating.user_id == user_id).all()}
        results = []
        for mi, score in enumerate(scores):
            mid = self.svd_movie_ids[mi]
            if mid not in rated:
                results.append((mid, float(score)))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:n]

    # ------------------------------------------------------------------
    # User-Based Collaborative Filtering  (Pearson)
    # ------------------------------------------------------------------
    def get_collaborative_recommendations(self, db: Session, user_id: int, n: int = 20) -> List[Tuple[int, float]]:
        ratings = db.query(Rating).all()
        if len(ratings) < 10:
            return []

        df = pd.DataFrame(
            [(r.user_id, r.movie_id, r.rating) for r in ratings],
            columns=['user_id', 'movie_id', 'rating']
        )
        matrix = df.pivot_table(index='user_id', columns='movie_id', values='rating')
        if user_id not in matrix.index:
            return []

        filled = matrix.fillna(0)
        user_sim = filled.T.corr()
        if user_id not in user_sim.columns:
            return []

        similar_users = user_sim[user_id].sort_values(ascending=False)[1:51]
        rated_by_user = set(matrix.loc[user_id].dropna().index)

        recs: Dict[int, float] = {}
        for sim_uid, sim_score in similar_users.items():
            if sim_score <= 0:
                continue
            for mid, rating in matrix.loc[sim_uid].dropna().items():
                if mid not in rated_by_user:
                    recs[mid] = recs.get(mid, 0) + rating * sim_score

        return sorted(recs.items(), key=lambda x: x[1], reverse=True)[:n]

    # ------------------------------------------------------------------
    # Hybrid  (SVD + Content-Based + Preferences)
    # ------------------------------------------------------------------
    def get_hybrid_recommendations(
        self, db: Session, user_id: int, movie_id: int = None, n: int = 20
    ) -> List[int]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return []

        rating_count = db.query(Rating).filter(Rating.user_id == user_id).count()

        # Adaptive weights
        if rating_count < 5:
            svd_w, content_w = 0.1, 0.9
        elif rating_count < 20:
            svd_w, content_w = 0.5, 0.5
        else:
            svd_w, content_w = 0.7, 0.3

        recs: Dict[int, float] = {}

        # SVD collaborative
        if rating_count >= 5:
            for mid, score in self.get_svd_recommendations(db, user_id, n=40):
                recs[mid] = recs.get(mid, 0) + score * svd_w

        # Content-based (from a seed movie or user's top-rated)
        seed_id = movie_id
        if not seed_id and rating_count > 0:
            top = (
                db.query(Rating)
                .filter(Rating.user_id == user_id)
                .order_by(Rating.rating.desc())
                .first()
            )
            if top:
                seed_id = top.movie_id

        if seed_id:
            for mid, score in self.get_content_based_recommendations(seed_id, n=40):
                recs[mid] = recs.get(mid, 0) + score * content_w

        # Genre preference boost / penalty
        if user.preferences:
            preferred = user.preferences.preferred_genres or []
            disliked  = user.preferences.disliked_genres or []
            for mid in list(recs.keys()):
                movie = db.query(Movie).filter(Movie.id == mid).first()
                if movie and movie.genres:
                    if any(g in preferred for g in movie.genres):
                        recs[mid] *= 1.15
                    if any(g in disliked for g in movie.genres):
                        recs[mid] *= 0.7

        sorted_recs = sorted(recs.items(), key=lambda x: x[1], reverse=True)
        return [mid for mid, _ in sorted_recs[:n]]

    # ------------------------------------------------------------------
    # Popularity-Based  (cold start)
    # ------------------------------------------------------------------
    def get_popular_recommendations(
        self, db: Session, genres: List[str] = None, n: int = 20
    ) -> List[int]:
        query = db.query(Movie).filter(Movie.vote_count >= 100)
        if genres:
            query = query.filter(Movie.genres.contains(genres[0]))
        movies = (
            query.order_by(
                (Movie.vote_average * 0.7 + Movie.popularity * 0.3).desc()
            )
            .limit(n)
            .all()
        )
        return [m.id for m in movies]

    # ------------------------------------------------------------------
    # Explanation  (for /recommendations/explain endpoint)
    # ------------------------------------------------------------------
    def explain_recommendation(self, db: Session, user_id: int, movie_id: int) -> Dict:
        rating_count = db.query(Rating).filter(Rating.user_id == user_id).count()
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        reasons = []

        if rating_count >= 5 and self.svd_user_factors is not None:
            reasons.append("Predicted high rating based on your taste profile (SVD Matrix Factorization)")

        if movie and movie.genres:
            reasons.append(f"Matches genres you enjoy: {', '.join(movie.genres[:3])}")

        if movie and movie.vote_average and movie.vote_average >= 7.0:
            reasons.append(f"Highly rated by the community ({movie.vote_average}/10)")

        if not reasons:
            reasons.append("Popular among users with similar taste")

        return {
            "movie_id": movie_id,
            "movie_title": movie.title if movie else "Unknown",
            "reasons": reasons,
            "algorithm": "Hybrid (SVD + TF-IDF Content-Based)" if rating_count >= 5 else "Content-Based (TF-IDF Cosine Similarity)"
        }


# Global singleton
recommendation_engine = RecommendationEngine()
