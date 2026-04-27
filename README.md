# 🎬 CineAI — Movie Recommendation System

A full-stack movie recommendation system using a **Hybrid ML engine** (SVD Matrix Factorization + TF-IDF Content-Based Filtering), FastAPI backend, MySQL database, and Streamlit frontend.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit (dark Netflix-style UI) |
| Backend | FastAPI + Python |
| Database | MySQL |
| ML | SVD Matrix Factorization + TF-IDF + Cosine Similarity + Pearson CF |

## ML Algorithms

- **SVD Matrix Factorization** — learns latent user/movie factors from ratings
- **TF-IDF Content-Based Filtering** — finds similar movies via genres, overview, cast, director
- **User-Based Collaborative Filtering** — Pearson correlation between users
- **Hybrid Engine** — adaptive weights (SVD-heavy for experienced users, content-heavy for new users)
- **Cold Start Handling** — popularity-based recommendations for new users

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register |
| POST | `/api/v1/auth/login` | Login (JWT) |
| GET | `/api/v1/movies/` | List movies |
| GET | `/api/v1/movies/search/` | Search movies |
| GET | `/api/v1/recommendations/` | Personalised recommendations |
| GET | `/api/v1/recommendations/popular` | Popular movies |
| GET | `/api/v1/recommendations/explain/{id}` | Explain why a movie was recommended |
| POST | `/api/v1/ratings/` | Rate a movie |
| GET | `/api/v1/watchlist/` | Get watchlist |
| POST | `/api/v1/users/preferences` | Set genre preferences |

Full interactive docs at `http://localhost:8000/docs`

## Run Locally

### 1. Setup database
```bash
mysql -u root -p
CREATE DATABASE movie_recommender;
EXIT;
```

### 2. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env       # then edit .env
python migrate_data.py       # import movies from CSV
uvicorn app.main:app --reload
```

### 3. Frontend
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

- Frontend: http://localhost:8501
- API docs: http://localhost:8000/docs

## Deploy with Docker

```bash
docker-compose up --build
```

Everything (MySQL + backend + frontend) starts with one command.

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in:

```
DATABASE_URL=mysql+pymysql://root:PASSWORD@localhost:3306/movie_recommender
SECRET_KEY=your-random-32-char-secret
TMDB_API_KEY=optional-for-posters
```
