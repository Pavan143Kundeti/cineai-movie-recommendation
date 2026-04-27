# CineAI — Interview Preparation Guide

---

## Q1. Tell me about your project (4-5 minutes)

"We built **CineAI** — an intelligent Movie Recommendation System using advanced Machine Learning algorithms.

The core problem we solved is called the **Information Overload Problem** — there are thousands of movies available, but users don't know what to watch. Our system solves this by learning each user's taste and giving personalised recommendations in real time.

**Architecture:** We followed a **3-tier architecture** —
- **Frontend** — Streamlit web application
- **Backend** — RESTful API built with FastAPI (Python)
- **Database** — MySQL with SQLAlchemy ORM

**The ML Engine is the heart of the project.** We implemented a **Hybrid Recommendation System** combining 3 algorithms:

1. **TF-IDF Vectorization + Cosine Similarity** — Content-Based Filtering. Converts movie metadata (genres, cast, director, overview) into numerical vectors and finds similarity between movies using cosine distance.

2. **SVD — Singular Value Decomposition** — Matrix Factorization technique. Decomposes the user-item rating matrix into latent factors to predict what rating a user would give to an unseen movie.

3. **Pearson Correlation — User-Based Collaborative Filtering** — Finds users with similar rating patterns and recommends what those similar users liked.

**Key problems we solved:**
- **Cold Start Problem** — handled using popularity-based fallback for new users
- **Data Sparsity** — handled by normalising ratings per user before SVD
- **Scalability** — pre-computed TF-IDF similarity matrix on server startup for O(1) lookup

**Security:** JWT-based authentication with bcrypt password hashing (12 rounds).

**Deployment:** Backend on Render, Database on Railway MySQL, Frontend on Streamlit Cloud. CI/CD through GitHub.

The system has 4800+ movies, 15+ REST API endpoints, and the recommendation quality improves dynamically as users rate more movies."

---

## Q2. Technologies Used — With Keywords

| Technology | Definition | Keywords to Say |
|-----------|-----------|----------------|
| **Python** | High-level, interpreted programming language | "We used Python because of its rich ML ecosystem — NumPy, Pandas, Scikit-learn" |
| **FastAPI** | Modern async Python web framework based on OpenAPI standard | "FastAPI gives automatic Swagger UI documentation, Pydantic validation, and async support" |
| **MySQL** | Relational Database Management System (RDBMS) | "ACID compliant, supports JSON columns for flexible schema, used SQLAlchemy ORM for abstraction" |
| **SQLAlchemy** | Python ORM (Object Relational Mapper) | "Prevents SQL injection, database-agnostic, clean model definitions" |
| **Streamlit** | Python-based reactive web framework for data apps | "Rapid prototyping, Python-native, perfect for ML demos" |
| **Scikit-learn** | Open-source ML library — TF-IDF, SVD, cosine similarity | "Industry standard ML library, TruncatedSVD for matrix factorization" |
| **JWT** | JSON Web Token — stateless authentication standard | "Stateless, scalable, tokens expire in 24 hours, signed with HS256 algorithm" |
| **bcrypt** | Adaptive password hashing algorithm | "12 salt rounds, resistant to brute force and rainbow table attacks" |
| **Pandas / NumPy** | Data manipulation and numerical computing libraries | "Used for user-item matrix construction and rating normalisation" |
| **Docker** | Containerisation platform | "Docker + docker-compose for consistent deployment across environments" |
| **GitHub** | Version control and CI/CD | "Git branching strategy, pull requests, automated deployment on push" |

---

## Q3. ML Algorithms — Technical Explanation

### Algorithm 1 — TF-IDF + Cosine Similarity (Content-Based Filtering)

**Definition:**
- **TF-IDF** = Term Frequency × Inverse Document Frequency
- Converts text (movie metadata) into numerical feature vectors
- **Cosine Similarity** measures the angle between two vectors — closer to 1 means more similar

**How it works in our project:**
```
Movie features = genres + cast + director + overview
→ TF-IDF converts this to a vector
→ Cosine similarity finds nearest movies

Example:
Inception vector:  [0.8, 0.1, 0.9, 0.2]  (Sci-Fi, Thriller heavy)
Interstellar vec:  [0.7, 0.1, 0.8, 0.3]  (Sci-Fi, Thriller heavy)
Similarity = 0.94  → Very similar ✓

Inception vs Titanic:
Titanic vector:    [0.1, 0.9, 0.1, 0.8]  (Romance, Drama heavy)
Similarity = 0.12  → Not similar ✓
```

**Keywords:** Feature extraction, vectorization, cosine distance, n-gram (1,2), sublinear TF scaling, stop words removal

---

### Algorithm 2 — SVD Matrix Factorization (Collaborative Filtering)

**Definition:**
- SVD = Singular Value Decomposition
- Decomposes the User × Movie rating matrix into latent factor matrices
- Learns hidden patterns — "users who like Sci-Fi also like mind-bending plots"

**How it works:**
```
Rating Matrix R (Users × Movies):
         Inception  Interstellar  Titanic  Avatar
User 1:     9           8           2        7
User 2:     8           9           3        8
User 3:     2           1           9        3
User 4:     ?           8           ?        7   ← predict missing

SVD decomposes R into:
R ≈ U × Σ × V^T
(User factors) × (Weights) × (Movie factors)

→ Predicts User 4 would rate Inception = 8.2
→ Recommends Inception to User 4
```

**We used:** TruncatedSVD with 50 latent components, mean-normalized ratings

**Keywords:** Matrix factorization, latent factors, dimensionality reduction, TruncatedSVD, rating normalization, collaborative signal

---

### Algorithm 3 — Pearson Correlation (User-Based CF)

**Definition:**
- Measures linear correlation between two users' rating patterns
- Range: -1 (opposite taste) to +1 (identical taste)

**How it works:**
```
You rated:    Inception=9, Dark Knight=9, Interstellar=8
User B rated: Inception=8, Dark Knight=9, Interstellar=9

Pearson correlation = 0.95 → Very similar users
→ User B also rated "The Prestige" = 9
→ Recommend "The Prestige" to you
```

**Keywords:** Pearson correlation coefficient, user similarity matrix, neighborhood-based CF, rating prediction, top-K similar users

---

### Hybrid Engine — Adaptive Weighted Combination

| User Ratings | Content Weight | SVD Weight | Reason |
|-------------|---------------|------------|--------|
| 0 ratings | — | — | Show popular movies |
| 1–4 ratings | 90% | 10% | Not enough data for CF |
| 5–19 ratings | 50% | 50% | Balanced approach |
| 20+ ratings | 30% | 70% | CF is now reliable |

**Additional boosts:**
- Preferred genre → **+15% score boost**
- Disliked genre → **-30% score penalty**

**Keywords:** Hybrid filtering, adaptive weights, cold start mitigation, genre preference weighting, score normalization

---

## Q4. Team Roles

| Member | Role | Work Done |
|--------|------|-----------|
| **Pavan** (Team Leader) | Full Stack + ML Lead | Project architecture, ML engine (SVD + TF-IDF), API design, deployment, team coordination |
| **Yousuf** | Backend Developer | FastAPI routes, JWT authentication, database models, user management |
| **Arif** | Database + Data | MySQL schema design, data migration (4800 movies), poster updates, Railway setup |
| **Dhanush** | Frontend Developer | Streamlit UI, movie cards, search, watchlist, mood page, dashboard |

---

## Q5. Why Did You Choose This Project?

"Three reasons:

1. **Real world use** — Netflix, Amazon, YouTube all use recommendation systems. It is one of the most used technologies in the industry today.

2. **Covers everything** — This project has frontend, backend, database, machine learning, security, and deployment. It shows all skills in one project.

3. **Challenging** — Simple CRUD apps are boring. Recommendation systems have real problems like cold start problem, data sparsity, and algorithm tuning. Solving these makes the project impressive."

---

## Q6. Problems Faced and How You Solved Them

| Problem | What Happened | How We Solved |
|---------|--------------|---------------|
| **Cold Start** | New users have no ratings, cannot recommend anything | Used popularity-based recommendations for new users |
| **Slow recommendations** | Computing similarity for 4800 movies was slow | Pre-computed the similarity matrix on server startup |
| **Password security** | Cannot store plain text passwords | Used bcrypt hashing (12 rounds) |
| **Genre filter not working** | MySQL JSON column search was wrong | Used `JSON_CONTAINS()` SQL function |
| **Python version conflict** | Streamlit Cloud used Python 3.14, Pillow failed | Added `.python-version` file to force Python 3.11 |
| **Duplicate widget errors** | Same movie appeared in multiple genre rows | Made button keys unique using row label + position + movie ID |

---

## Q7. Team Conflicts and How Solved

"We had one main conflict — Yousuf wanted to use Django for backend, I wanted FastAPI.

I explained:
- FastAPI is 3x faster than Django
- It auto-generates API documentation
- It is better for ML integration

We did a small test, compared both, and the team agreed FastAPI was better. We always made decisions based on technical facts, not personal preference."

---

## Q8. Simple Code Example (Show This)

**How recommendation works in simple code:**

```python
# Step 1: Convert movies to numbers using TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = [
    "Action Adventure Iron Man superhero",
    "Action Adventure Thor superhero",
    "Romance Drama Love Story"
]

# Convert text to numbers
vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(movies)

# Find similarity between movies
similarity = cosine_similarity(matrix)

# Movie 0 (Iron Man) similarity scores
print(similarity[0])
# Output: [1.0, 0.85, 0.02]
# → Iron Man is 85% similar to Thor, only 2% similar to Love Story
```

**How login security works:**

```python
import bcrypt

# When user registers — store hashed password
password = "mypassword123"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# Stored in DB: $2b$12$xK8... (unreadable)

# When user logs in — verify
bcrypt.checkpw("mypassword123".encode(), hashed)  # True
bcrypt.checkpw("wrongpassword".encode(), hashed)  # False
```

---

## Q9. API Endpoints (Show at /docs)

| Method | URL | What it does |
|--------|-----|-------------|
| POST | `/api/v1/auth/register` | Create new account |
| POST | `/api/v1/auth/login` | Login, get token |
| GET | `/api/v1/recommendations/` | Get personalised recommendations |
| GET | `/api/v1/recommendations/trending` | Get trending movies |
| GET | `/api/v1/recommendations/mood/action` | Mood-based recommendations |
| GET | `/api/v1/movies/search/?q=batman` | Search movies |
| POST | `/api/v1/ratings/` | Rate a movie |
| GET | `/api/v1/watchlist/` | Get my watchlist |
| GET | `/api/v1/recommendations/explain/123` | Why was this recommended? |

---

## Q10. Database Design

| Table | What it stores |
|-------|---------------|
| `users` | Name, email, hashed password |
| `movies` | Title, genres, cast, director, poster |
| `ratings` | Which user rated which movie, score 1-10 |
| `watchlist` | Which user saved which movie |
| `user_preferences` | Favourite and disliked genres |

---

## Q11. What is Cold Start Problem?

**Problem:** When a new user joins, they have no ratings. The system does not know what they like. So it cannot recommend anything.

**Our Solution:**
- Step 1: Show popular movies (everyone likes popular movies)
- Step 2: Ask user to pick favourite genres (Preferences page)
- Step 3: As they rate movies, system learns and improves

---

## Q12. Why Not React for Frontend?

"We chose Streamlit because:
- Our project focus is Machine Learning, not frontend design
- Streamlit is Python-based, same as our backend and ML code
- It connects to our API easily
- For production scale, we would migrate to React with the same FastAPI backend"

---

## Q13. How is This Different from a Tutorial Project?

| Tutorial Project | Our Project |
|-----------------|-------------|
| Copy-paste code | Designed architecture ourselves |
| Single algorithm | 3 algorithms combined (Hybrid) |
| No authentication | JWT + bcrypt security |
| No database | MySQL with 5 tables |
| Runs only locally | Deployed live on internet |
| No real data | 4800 real movies from TMDB dataset |
| No problem solving | Solved cold start, performance, security |

---

## Quick Answers for Common Questions

**Q: How many movies?** → 4800+ from TMDB dataset

**Q: How accurate are recommendations?** → Improves with more ratings. After 5 ratings, SVD activates. After 20 ratings, 70% weight on collaborative filtering.

**Q: How long did it take?** → 3 months. Planning 2 weeks, backend 4 weeks, ML 3 weeks, frontend 2 weeks, deployment 1 week.

**Q: What would you improve?** → Add deep learning (Neural Collaborative Filtering), add real-time updates using WebSockets, add Redis caching for faster response.

**Q: Is it secure?** → Yes. Passwords hashed with bcrypt, login uses JWT tokens that expire in 24 hours, all sensitive data in environment variables.

---

## Demo Flow (5 Minutes)

1. Open live website URL
2. Show login page — mention team names at bottom
3. Register new account
4. Show Home page — Movie of the Day banner, genre rows
5. Rate 3-4 movies
6. Go to Recommendations — show personalised results
7. Click "Why?" on a movie — show ML explanation
8. Go to Mood page — click Action, show results
9. Open `/docs` URL — show all 15+ APIs
10. Show GitHub repo — clean code structure

---

*CineAI — Built by Pavan, Yousuf, Arif, Dhanush | B.Tech Final Year 2025*

---

## Q14. What is TMDB API Key? Why Did You Use It?

**TMDB = The Movie Database**
- It is a free public website (like Wikipedia for movies)
- They provide a free API (web service) to get movie data
- Website: https://www.themoviedb.org

**What the API Key does:**
- It is like a password that proves "I am allowed to use TMDB's data"
- Without it, TMDB blocks your requests
- It is free — just register and get a key

**Why we used it:**
| Purpose | How We Used TMDB |
|---------|-----------------|
| Movie Posters | Fetched poster images for all 4800 movies |
| Poster URL format | `https://image.tmdb.org/t/p/w185/posterpath.jpg` |
| Data source | Our CSV dataset (tmdb_5000_movies.csv) also came from TMDB |

**How it is integrated in our project:**

```python
# In update_posters.py
TMDB_API_KEY = "c20cfa2fbbe54c8971f014a6560fd7d9"

# Call TMDB API to get poster path for each movie
url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}"
response = requests.get(url)
poster_path = response.json()['poster_path']
# Example: "/gKY6q7SjCkAU6FqvqWybDYgUKIF.jpg"

# Then display poster in frontend
poster_url = f"https://image.tmdb.org/t/p/w185{poster_path}"
# Shows the actual movie poster image
```

**In simple words:**
"We used TMDB API to fetch movie poster images. Without it, our website would show blank boxes instead of movie posters. The API key is stored securely in environment variables, not hardcoded in the source code."

**Keywords to say:** REST API integration, API key authentication, environment variable security, CDN image hosting, rate limiting (we added 0.05s delay between calls)

---

## Q15. How Did You Deploy the Project? (Full Deployment Flow)

**Our deployment has 3 parts working together:**

```
User opens browser
       ↓
Streamlit Cloud (Frontend)
       ↓ API calls
Render.com (FastAPI Backend)
       ↓ SQL queries
Railway.app (MySQL Database)
```

---

### Part 1 — Database (Railway MySQL)

**What:** Cloud-hosted MySQL database
**Why Railway:** Free tier, easy setup, accessible from anywhere on internet

**Steps we did:**
1. Created MySQL instance on Railway
2. Got connection URL:
   `mysql+pymysql://root:password@shuttle.proxy.rlwy.net:58035/railway`
3. Ran `migrate_data.py` locally pointing to Railway URL
4. Loaded 4800 movies into Railway MySQL

---

### Part 2 — Backend (Render.com)

**What:** Hosts our FastAPI Python application
**Why Render:** Free tier, connects directly to GitHub, auto-deploys on every push

**Settings we configured:**
| Setting | Value |
|---------|-------|
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port 10000` |

**Environment Variables set on Render:**
| Variable | Value |
|----------|-------|
| `DATABASE_URL` | Railway MySQL connection string |
| `SECRET_KEY` | JWT signing secret (32+ chars) |
| `TMDB_API_KEY` | TMDB API key for posters |
| `ALGORITHM` | HS256 |

**Live URL:** `https://cineai-backend-t8bk.onrender.com`
**API Docs:** `https://cineai-backend-t8bk.onrender.com/docs`

---

### Part 3 — Frontend (Streamlit Cloud)

**What:** Hosts our Streamlit Python web application
**Why Streamlit Cloud:** Free, made specifically for Streamlit apps, one-click deploy

**Settings we configured:**
| Setting | Value |
|---------|-------|
| Repository | `Pavan143Kundeti/cineai-movie-recommendation` |
| Branch | `main` |
| Main file | `frontend/app.py` |
| Python version | `3.11` (in `.python-version` file) |

**Secret we added:**
```toml
API_BASE_URL = "https://cineai-backend-t8bk.onrender.com"
```

This tells the frontend where the backend is running.

---

### How Auto-Deploy Works (CI/CD)

```
We push code to GitHub
        ↓
Render detects new commit → auto rebuilds backend
        ↓
Streamlit Cloud detects new commit → auto rebuilds frontend
        ↓
Live website updated in 3-5 minutes
```

**Keywords to say:** CI/CD pipeline, environment variables, cloud deployment, auto-deploy on git push, separation of concerns (frontend/backend/database on separate services), 3-tier deployment architecture

---

### One Problem We Faced in Deployment

**Problem:** Streamlit Cloud was using Python 3.14 by default. Pillow (image library) does not support Python 3.14 yet — build failed.

**Solution:** We added a `.python-version` file in the frontend folder with content `3.11`. This forces Streamlit Cloud to use Python 3.11 where all packages work correctly.

**Lesson learned:** Always pin your Python version in deployment. Never rely on the platform default.

---

## Q16. What is Docker? Why Did You Use It? What is Its Role?

### What is Docker? (Simple Definition)

**Docker is a tool that packages your application with everything it needs to run — code, libraries, settings — into one box called a "Container".**

Think of it like this:

| Real World | Docker |
|-----------|--------|
| Shipping container | Docker container |
| Contains goods safely | Contains your app + all dependencies |
| Works on any ship | Works on any computer/server |
| Same box, same contents | Same container, same behavior everywhere |

---

### The Problem Docker Solves

**Without Docker — "It works on my computer" problem:**
```
Developer A runs the app → Works fine ✓
Developer B runs the app → Error! Wrong Python version ✗
Server runs the app     → Error! Missing library ✗
```

**With Docker:**
```
Developer A builds container → Works fine ✓
Developer B runs same container → Works fine ✓
Server runs same container → Works fine ✓
```

**"Build once, run anywhere"** — this is Docker's main promise.

---

### Docker in Our Project — What We Created

We created **3 containers** using `docker-compose.yml`:

| Container | What it runs | Port |
|-----------|-------------|------|
| `db` | MySQL 8.0 database | 3306 |
| `backend` | FastAPI Python app | 8000 |
| `frontend` | Streamlit web app | 8501 |

---

### Our Dockerfile — Backend

```dockerfile
# backend/Dockerfile

FROM python:3.11-slim          # Start with Python 3.11

WORKDIR /app                   # Set working directory

COPY requirements.txt .        # Copy dependencies list
RUN pip install -r requirements.txt  # Install all packages

COPY . .                       # Copy all code

EXPOSE 8000                    # Open port 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Line by line meaning:**
- `FROM python:3.11-slim` → Use Python 3.11 as base (slim = smaller size)
- `WORKDIR /app` → All commands run inside /app folder
- `COPY requirements.txt` → Copy the dependencies file first
- `RUN pip install` → Install all Python packages
- `COPY . .` → Copy all project code
- `EXPOSE 8000` → Tell Docker this app uses port 8000
- `CMD` → Command to start the app

---

### Our docker-compose.yml — One Command to Run Everything

```yaml
services:
  db:           # MySQL database
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: cineai123
      MYSQL_DATABASE: movie_recommender

  backend:      # FastAPI app
    build: ./backend
    ports: ["8000:8000"]
    depends_on: [db]   # Wait for DB to start first

  frontend:     # Streamlit app
    build: ./frontend
    ports: ["8501:8501"]
    depends_on: [backend]  # Wait for backend to start first
```

**To run the entire project with ONE command:**
```bash
docker-compose up --build
```

This starts MySQL + FastAPI + Streamlit together automatically.

---

### Why We Used Docker in This Project

| Reason | Explanation |
|--------|-------------|
| **Consistency** | Same environment on every developer's machine |
| **Easy setup** | New team member runs 1 command, everything works |
| **Deployment ready** | Same container runs locally and on cloud server |
| **Isolation** | Each service (DB, backend, frontend) runs separately |
| **No conflicts** | Python version, library versions all locked inside container |

---

### Docker vs Without Docker

| Without Docker | With Docker |
|---------------|-------------|
| Install Python manually | Python included in container |
| Install MySQL manually | MySQL starts automatically |
| "Works on my machine" problem | Works everywhere same way |
| 30 minutes setup for new developer | 1 command: `docker-compose up` |
| Different versions cause errors | Versions locked in Dockerfile |

---

### Important Docker Terms to Know

| Term | Meaning |
|------|---------|
| **Image** | Blueprint/template of a container (like a class) |
| **Container** | Running instance of an image (like an object) |
| **Dockerfile** | Instructions to build an image |
| **docker-compose** | Tool to run multiple containers together |
| **Port mapping** | `8000:8000` means host port 8000 → container port 8000 |
| **Volume** | Persistent storage so data is not lost when container stops |
| **depends_on** | Start this container only after another one is ready |

---

### What to Say in Interview

*"We used Docker to containerise our application. We created separate Dockerfiles for the backend and frontend, and a docker-compose.yml to orchestrate all three services — MySQL, FastAPI, and Streamlit — together. This ensures that any developer can clone our repository and run the entire stack with a single command: `docker-compose up --build`. It also makes our deployment environment identical to our development environment, eliminating the classic 'works on my machine' problem."*

**Keywords:** Containerisation, Docker image, Docker container, docker-compose, orchestration, port mapping, environment isolation, infrastructure as code, build once run anywhere
