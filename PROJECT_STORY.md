# CineAI — The Full Story (Beginning to End)

*How we built a Movie Recommendation System from scratch — explained simply, step by step.*

---

## Chapter 1 — The Idea

We wanted to build something that is used in real life.

Netflix shows you movies you like. Amazon recommends products. YouTube suggests videos. All of these use **Recommendation Systems** behind the scenes.

We thought — why not build one ourselves for movies?

That is how CineAI started.

---

## Chapter 2 — Where Did We Get the Movie Data?

The first question was — where do we get 4800+ movies with all details like title, genres, cast, director, ratings?

We found a free dataset on **Kaggle** (a data science website) called the **TMDB 5000 Movie Dataset**.

It came as two CSV files:

### File 1 — `tmdb_5000_movies.csv`
Contains movie details:
```
id | title          | genres              | overview        | vote_average | popularity
---|----------------|---------------------|-----------------|--------------|----------
19 | Inception      | [Sci-Fi, Thriller]  | A thief who...  | 8.3          | 724.2
27 | Interstellar   | [Sci-Fi, Drama]     | A team of...    | 8.1          | 612.4
```

### File 2 — `tmdb_5000_credits.csv`
Contains cast and crew:
```
movie_id | cast                              | crew
---------|-----------------------------------|------------------
19       | [Leonardo DiCaprio, Joseph...]    | [Christopher Nolan (Director)...]
27       | [Matthew McConaughey, Anne...]    | [Christopher Nolan (Director)...]
```

**Why two files?** Because movie details and cast/crew are stored separately. We had to **join** (merge) them using the movie ID.

---

## Chapter 3 — Reading and Processing the Data (Pandas + NumPy)

The CSV files are just text files. We needed Python to read them and make sense of them.

We used **Pandas** for this.

**Why Pandas?**
- It reads CSV files in one line
- It can merge two files easily
- It handles missing values
- It is the standard tool for data processing in Python

```python
import pandas as pd

# Read both files
movies_df  = pd.read_csv('tmdb_5000_movies.csv')
credits_df = pd.read_csv('tmdb_5000_credits.csv')

# Merge them on movie ID
movies_df = movies_df.merge(credits_df, left_on='id', right_on='movie_id')
```

Now we had one big table with everything — title, genres, cast, director, ratings.

**Why NumPy?**
- Pandas uses NumPy underneath
- We used NumPy for the ML matrix calculations (user-rating matrix, similarity scores)
- NumPy handles large number arrays very fast

---

## Chapter 4 — The Genres Problem

The genres column in the CSV looked like this:
```
[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}]
```

It was a **JSON string inside a CSV cell** — not a clean list.

We had to extract just the names:
```python
import json

genres_raw = '[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}]'
genres_data = json.loads(genres_raw)
genres = [g['name'] for g in genres_data]
# Result: ["Action", "Adventure"]
```

Same thing for cast and crew. We extracted:
- Top 10 cast member names
- Director name (from crew where job == "Director")

---

## Chapter 5 — Why Database First?

Before building any website, we needed a place to **permanently store** the data.

Think of it like building a house — you lay the foundation first, then build walls.

**Database = Foundation**

If we built the website first without a database:
- Data would be lost every time the server restarts
- Multiple users cannot share the same data
- No way to store user accounts, ratings, watchlists

So we designed the **MySQL database first**.

**Why MySQL?**
- It is a **Relational Database** — data is stored in tables with relationships
- It is the most widely used database in the industry
- It supports **JSON columns** — perfect for storing genres and cast as arrays
- It is **ACID compliant** — data is never corrupted even if something crashes

---

## Chapter 6 — Database Design (5 Tables)

We designed 5 tables:

```
users
├── id (primary key)
├── username
├── email
└── password_hash (encrypted)

movies
├── id (primary key)
├── tmdb_id (original ID from TMDB)
├── title
├── genres (JSON array)
├── cast (JSON array)
├── director
├── overview
├── poster_path
├── vote_average
└── popularity

ratings
├── id
├── user_id → links to users table
├── movie_id → links to movies table
└── rating (1.0 to 10.0)

watchlist
├── id
├── user_id → links to users table
└── movie_id → links to movies table

user_preferences
├── id
├── user_id → links to users table
├── preferred_genres (JSON array)
└── disliked_genres (JSON array)
```

**Relationships:**
- One user can have many ratings (one-to-many)
- One user can have many watchlist items (one-to-many)
- One movie can have many ratings from different users (one-to-many)

We used **SQLAlchemy** (Python library) to define these tables in Python code instead of writing raw SQL. This is called an **ORM — Object Relational Mapper**.

---

## Chapter 7 — Loading Movies into Database (Migration)

We wrote a script called `migrate_data.py`.

It reads the CSV files and inserts each movie into the MySQL database:

```python
for each movie in CSV:
    1. Parse genres from JSON string → clean list
    2. Parse cast from JSON string → top 10 names
    3. Extract director from crew JSON
    4. Create Movie object
    5. Insert into MySQL database
    6. Every 100 movies → commit (save) to database
```

This loaded **4803 movies** into MySQL.

---

## Chapter 8 — Where Did the Posters Come From?

The CSV files had a column called `poster_path` — but it was empty for most movies.

The actual poster images are hosted on **TMDB's servers** (The Movie Database website).

To get the poster paths, we needed to call the **TMDB API**.

**What is an API?**
An API is like a waiter in a restaurant. You give an order (request), the waiter goes to the kitchen (server), and brings back food (response).

We called TMDB's API for each movie:
```python
# Ask TMDB: "Give me details for movie with ID 19"
url = f"https://api.themoviedb.org/3/movie/19?api_key=OUR_KEY"
response = requests.get(url)
poster_path = response.json()['poster_path']
# Returns: "/gKY6q7SjCkAU6FqvqWybDYgUKIF.jpg"
```

Then we saved this path in our database.

**How posters are displayed:**
The path is just a filename. The full URL is:
```
https://image.tmdb.org/t/p/w185/gKY6q7SjCkAU6FqvqWybDYgUKIF.jpg
```
- `image.tmdb.org` = TMDB's image server (CDN)
- `w185` = image width 185 pixels
- `/gKY6q7...jpg` = the poster filename

So we never store the actual image — just the filename. The browser fetches the image directly from TMDB's servers.

**Why TMDB API Key?**
TMDB gives free access but requires an API key to:
- Track who is using their service
- Prevent abuse (too many requests)
- It is free to get — just register on their website

---

## Chapter 9 — Building the Backend (FastAPI)

Now we had data in the database. Next step — build the backend.

**What is a Backend?**
The backend is the brain of the website. It:
- Receives requests from the frontend
- Talks to the database
- Runs the ML algorithms
- Sends back results

**Why FastAPI?**
- It is a modern Python framework
- Very fast (uses async programming)
- Automatically creates API documentation at `/docs`
- Uses **Pydantic** for data validation — wrong data is rejected automatically

We organised the backend into layers:

```
frontend sends request
        ↓
Router (decides which function to call)
        ↓
Service (business logic + ML)
        ↓
Model (talks to database)
        ↓
Database (MySQL)
        ↓
Response sent back to frontend
```

---

## Chapter 10 — How Login and Security Works

When a user registers:
1. They send username, email, password
2. We **hash** the password using **bcrypt**
   - Hashing = converting password to unreadable text
   - `"mypassword"` → `"$2b$12$xK8mN..."`
   - Even we cannot read it back
3. We store the hashed password in database

When a user logs in:
1. They send email + password
2. We fetch their hashed password from database
3. bcrypt checks if the password matches the hash
4. If yes → we create a **JWT Token**

**What is JWT?**
JWT = JSON Web Token. It is like a temporary ID card.
- Contains: user ID, expiry time
- Signed with a secret key so nobody can fake it
- Expires in 24 hours
- Frontend stores this token and sends it with every request

```
User logs in → Gets token → Sends token with every API call
Backend checks token → If valid → Allow access
```

---

## Chapter 11 — The ML Engine (Heart of the Project)

This is the most important part.

### Step 1 — Build Content Model (on server startup)

When the backend starts, it immediately:
1. Loads all 4803 movies from database
2. For each movie, creates a text string:
   ```
   "Action Action Action Overview text Cast names Director"
   (genres repeated 3x to give them more weight)
   ```
3. Runs **TF-IDF** on all these strings → converts to number vectors
4. Computes **Cosine Similarity** between all pairs → 4803 × 4803 matrix
5. Stores this matrix in memory

Now finding similar movies is instant — just look up the matrix.

### Step 2 — SVD Model (built when enough ratings exist)

When 20+ ratings exist in the database:
1. Build a User × Movie matrix
   ```
         Inception  Interstellar  Titanic
   User1:    9           8          2
   User2:    8           9          3
   User3:    ?           7          9   ← predict this
   ```
2. Subtract each user's average rating (normalise)
3. Run **TruncatedSVD** with 50 components
4. This creates a "taste profile" for every user
5. Multiply user profile × movie profiles → predicted ratings

### Step 3 — Hybrid Recommendation

When a user asks for recommendations:
```
If user has < 5 ratings:
    → Show popular movies

If user has 5-19 ratings:
    → 50% SVD predictions + 50% content similarity

If user has 20+ ratings:
    → 70% SVD predictions + 30% content similarity

Apply genre boosts:
    → Preferred genre: score × 1.15
    → Disliked genre: score × 0.70

Sort by final score → Return top 20
```

---

## Chapter 12 — Building the Frontend (Streamlit)

**Why Streamlit?**
- It is Python — same language as our backend and ML code
- No need to learn HTML, CSS, JavaScript separately
- We can connect to our API with simple `requests.get()` calls
- Perfect for data/ML applications
- Deploys for free on Streamlit Cloud

**How frontend connects to backend:**

Every action on the website makes an API call:

```python
# User clicks "Get Recommendations"
response = requests.get(
    "http://backend:8000/api/v1/recommendations/",
    headers={"Authorization": f"Bearer {token}"}
)
movies = response.json()
# Display movies on screen
```

The frontend never touches the database directly. It always goes through the backend API. This is the correct way to build web applications — **separation of concerns**.

---

## Chapter 13 — How All Three Are Connected

```
STREAMLIT FRONTEND
(runs on port 8501)
User clicks button
        ↓
HTTP Request with JWT token
        ↓
FASTAPI BACKEND
(runs on port 8000)
Validates token
Runs ML algorithm
        ↓
SQL Query via SQLAlchemy
        ↓
MYSQL DATABASE
(runs on port 3306)
Returns data
        ↓
Backend processes data
        ↓
JSON Response
        ↓
Frontend displays to user
```

**The API is the bridge** between frontend and database. Frontend never talks to database directly. Backend never talks to user directly. Each layer has one job.

---

## Chapter 14 — Deployment (Making It Live on Internet)

Local development works on our computer. But for the world to access it, we need to put it on the internet.

We used 3 free cloud services:

### Railway (Database)
- Created a MySQL database on Railway's servers
- Got a connection URL
- Ran our migration script pointing to Railway
- Now our 4803 movies are on Railway's servers permanently

### Render (Backend)
- Connected our GitHub repository to Render
- Told Render: "Go to `backend` folder, install requirements, run uvicorn"
- Set environment variables (DATABASE_URL, SECRET_KEY, TMDB_API_KEY)
- Render builds and runs our FastAPI app
- Every time we push to GitHub → Render automatically redeploys

### Streamlit Cloud (Frontend)
- Connected GitHub repository to Streamlit Cloud
- Told it: "Run `frontend/app.py`"
- Set secret: `API_BASE_URL = "https://cineai-backend.onrender.com"`
- Streamlit Cloud runs our app
- Every push to GitHub → auto redeploys

**The connection:**
```
User opens Streamlit URL
    → Streamlit app loads
    → App calls Render backend URL
    → Backend queries Railway MySQL
    → Data flows back to user
```

---

## Chapter 15 — Docker (For Easy Setup)

We also created Docker files so anyone can run the entire project with one command.

Docker packages everything — Python, libraries, settings — into a container. Like a box that contains everything needed to run the app.

```bash
docker-compose up --build
```

This one command:
1. Downloads MySQL image
2. Builds backend container (installs all Python packages)
3. Builds frontend container
4. Starts all three together
5. They can talk to each other automatically

---

## Chapter 16 — The Complete Flow (User's Journey)

```
1. User opens website
   → Streamlit loads login page

2. User registers
   → Frontend sends POST /api/v1/auth/register
   → Backend hashes password with bcrypt
   → Saves user to MySQL
   → Returns success

3. User logs in
   → Frontend sends POST /api/v1/auth/login
   → Backend verifies password
   → Creates JWT token
   → Frontend stores token

4. User browses Home page
   → Frontend sends GET /api/v1/recommendations/popular
   → Backend queries MySQL for top movies
   → Returns movie list with poster paths
   → Frontend builds poster URLs from TMDB CDN
   → Displays movie cards

5. User rates a movie (e.g., Inception = 9)
   → Frontend sends POST /api/v1/ratings/
   → Backend saves rating to MySQL

6. User asks for recommendations
   → Frontend sends GET /api/v1/recommendations/
   → Backend checks: how many ratings does this user have?
   → Runs SVD + Content-Based hybrid
   → Applies genre preferences
   → Returns top 20 personalised movies
   → Frontend displays them

7. User clicks "Why?" on a movie
   → Frontend sends GET /api/v1/recommendations/explain/123
   → Backend explains: "Because you liked Inception" / "Matches your Sci-Fi preference"
   → Frontend shows explanation
```

---

## Summary — Why Each Technology Was Chosen

| Technology | Why Here |
|-----------|---------|
| Python | ML libraries, same language for everything |
| Pandas | Read and process CSV files easily |
| NumPy | Fast matrix calculations for ML |
| Scikit-learn | TF-IDF, SVD, cosine similarity — all in one library |
| MySQL | Permanent storage, relationships between tables |
| SQLAlchemy | Write Python instead of SQL, prevents SQL injection |
| FastAPI | Fast, auto-docs, modern, perfect for ML APIs |
| JWT + bcrypt | Industry standard security |
| Streamlit | Python-native UI, no HTML/CSS needed |
| TMDB API | Free movie data and poster images |
| Docker | One command setup, consistent environment |
| GitHub | Version control, auto-deploy trigger |
| Render | Free backend hosting |
| Railway | Free MySQL hosting |
| Streamlit Cloud | Free frontend hosting |

---

*This is the complete story of CineAI — from a CSV file to a live deployed website with machine learning.*

*Built by Pavan, Yousuf, Arif, Dhanush — B.Tech Final Year 2025*
