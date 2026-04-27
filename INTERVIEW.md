# CineAI — Interview Preparation Guide

---

## Q1. Tell me about your project (4-5 minutes)

"We built **CineAI** — a Movie Recommendation System.

The idea is simple. When you open Netflix or Amazon Prime, it shows you movies you will like. But how does it know? That is what we built from scratch.

Our system has 4800+ movies. A user registers, rates movies they have watched, and our system learns their taste. Then it recommends movies they will enjoy.

We used **3 machine learning algorithms** working together:
- First it looks at what kind of movies you like (genres, directors, cast)
- Then it finds other users who have similar taste to you
- Then it combines both to give the best recommendation

We built a full website with login, search, watchlist, trending movies, mood-based recommendations, and a movie detail page with trailer link.

The backend is built with Python FastAPI, database is MySQL, and the frontend is Streamlit. The website is deployed live on the internet."

---

## Q2. Technologies Used

| Technology | What it is | Why we used it |
|-----------|-----------|----------------|
| **Python** | Programming language | Easy for ML, everyone knows it |
| **FastAPI** | Tool to build APIs (web services) | Fast, modern, auto-generates documentation |
| **MySQL** | Database to store data | Stores users, movies, ratings permanently |
| **Streamlit** | Tool to build web UI using Python | Quick to build, no need to learn HTML/CSS separately |
| **Scikit-learn** | ML library | Has all algorithms ready to use |
| **Pandas** | Data handling library | Read and process CSV files easily |
| **JWT** | Security token for login | Industry standard, secure |
| **bcrypt** | Password encryption | Passwords stored safely, not as plain text |
| **Railway** | Cloud MySQL hosting | Free, easy to set up |
| **Render** | Cloud backend hosting | Free, connects to GitHub automatically |
| **Streamlit Cloud** | Frontend hosting | Free, one-click deploy |

---

## Q3. ML Algorithms — Simple Explanation

### Algorithm 1 — TF-IDF + Cosine Similarity (Content-Based)

**What it means:**
- TF-IDF = Term Frequency - Inverse Document Frequency
- It converts movie descriptions into numbers
- Then finds movies that are similar to each other

**Simple example:**
```
Movie A: "Action, Adventure, Iron Man, Robert Downey"
Movie B: "Action, Adventure, Thor, Chris Hemsworth"
Movie C: "Romance, Drama, Love Story"

→ A and B are similar (both Action/Adventure)
→ C is different
```

**When used:** When a user clicks "Find Similar" on a movie

---

### Algorithm 2 — SVD (Singular Value Decomposition)

**What it means:**
- SVD = Matrix Factorization
- It creates a "taste profile" for every user
- Learns hidden patterns from ratings

**Simple example:**
```
User 1 rated: Action=9, Comedy=3, Horror=2
User 2 rated: Action=8, Comedy=4, Horror=1

→ Both users have similar taste
→ If User 1 liked Movie X, recommend X to User 2
```

**When used:** After a user rates 5+ movies

---

### Algorithm 3 — Pearson Collaborative Filtering

**What it means:**
- Finds users who rated movies similarly to you
- Recommends what those similar users liked

**Simple example:**
```
You liked: Inception(9), Interstellar(9), Dark Knight(8)
User B liked: Inception(8), Interstellar(9), Dark Knight(9)

→ You and User B have similar taste
→ User B also liked "The Prestige" → Recommend it to you
```

---

### Hybrid Engine (All 3 Combined)

| User History | Algorithm Used |
|-------------|----------------|
| 0 ratings | Popular movies (trending) |
| 1-4 ratings | 90% Content-Based, 10% SVD |
| 5-19 ratings | 50% Content-Based, 50% SVD |
| 20+ ratings | 30% Content-Based, 70% SVD |

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
