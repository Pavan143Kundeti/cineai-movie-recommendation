# CineAI Project Story


---

*How we built CineAI — A Movie Recommendation System — from zero to a live deployed website. Written in simple words so that anyone can understand, even without a technical background.*

---

## Chapter 1 — How the Idea Started

Every one of us uses Netflix, Amazon Prime, or YouTube. When you open Netflix, it shows you movies that you might like. It does not show you random movies. It shows movies based on what you watched before, what you rated, and what people similar to you liked.

We always wondered — how does Netflix know what I like? How does it decide which movie to show first?

That question became our project idea.

We decided to build a system that does exactly this — recommends movies to users based on their taste. We called it **CineAI**.

The word "CineAI" comes from "Cinema" and "AI" (Artificial Intelligence). It means a cinema experience powered by artificial intelligence.

---

## Chapter 2 — Planning Before Writing Any Code

Before writing even one line of code, we sat together and planned the entire project.

We asked ourselves these questions:

- Where will we get movie data from?
- How will we store the data?
- How will the recommendation work?
- How will users interact with the system?
- How will we make it available on the internet?

After discussion, we decided the project will have three main parts:

**Part 1 — Database**
Store all movies, users, ratings permanently.

**Part 2 — Backend**
The brain of the system. Handles login, recommendations, search, all logic.

**Part 3 — Frontend**
The face of the system. What the user sees and clicks on.

We also decided the order of building:
Database first → Backend second → Frontend third.

**Why this order?**

Think of building a house. You cannot build walls before the foundation. You cannot put furniture before the walls are ready.

Similarly:
- Database is the foundation — stores all data
- Backend is the walls — uses the database to do work
- Frontend is the furniture — uses the backend to show things to users

If we built the frontend first, it would have nothing to connect to. So database first is always the correct approach.

---

## Chapter 3 — Finding Movie Data

The first big challenge was — where do we get data for 4000+ movies?

We cannot manually type movie names, genres, cast, directors for thousands of movies. That would take months.

We searched online and found a free dataset on a website called **Kaggle**.

**What is Kaggle?**
Kaggle is a website where data scientists share datasets (collections of data) for free. It is like a library but for data instead of books.

We found a dataset called **TMDB 5000 Movie Dataset**.

**What is TMDB?**
TMDB stands for **The Movie Database**. It is a website like Wikipedia but only for movies and TV shows. Anyone can go to www.themoviedb.org and find information about any movie.

The dataset came as two separate files:

---

### File 1 — tmdb_5000_movies.csv

This file had one row for each movie. Each row had:

| Column | What it means | Example |
|--------|--------------|---------|
| id | Unique number for each movie | 19 |
| title | Movie name | Inception |
| genres | List of genres | Action, Sci-Fi |
| overview | Short description | A thief who steals... |
| vote_average | Average rating out of 10 | 8.3 |
| vote_count | How many people rated it | 14075 |
| popularity | How popular it is | 724.2 |
| runtime | Length in minutes | 148 |
| release_date | When it released | 2010-07-16 |

---

### File 2 — tmdb_5000_credits.csv

This file had cast and crew information:

| Column | What it means | Example |
|--------|--------------|---------|
| movie_id | Links to the movie | 19 |
| cast | List of actors | Leonardo DiCaprio, Joseph Gordon-Levitt |
| crew | List of crew members | Christopher Nolan (Director) |

**Why two separate files?**

Because movie details and cast/crew are different types of information. Keeping them separate makes the data cleaner and easier to manage. We had to combine (merge) them later using the movie ID number.

---

## Chapter 4 — Reading the CSV Files with Python

A CSV file is just a text file where data is separated by commas. Like this:

```
id,title,genres,vote_average
19,Inception,"[Action,Sci-Fi]",8.3
27,Interstellar,"[Sci-Fi,Drama]",8.1
```

To read this in Python, we used a library called **Pandas**.

**What is Pandas?**
Pandas is a Python library (a collection of ready-made tools) that makes it very easy to work with data in tables. Think of it like Microsoft Excel but inside Python code.

**Why Pandas and not something else?**
- It reads CSV files in just one line of code
- It can combine two files easily
- It handles missing or empty values automatically
- It is the most popular data tool in Python — used by companies like Google, Facebook, Netflix

```python
import pandas as pd

# Read the movies file
movies_df = pd.read_csv('tmdb_5000_movies.csv')

# Read the credits file
credits_df = pd.read_csv('tmdb_5000_credits.csv')

# Combine both files using the movie ID
movies_df = movies_df.merge(credits_df, left_on='id', right_on='movie_id')
```

After this, we had one big table with all movie information in one place.

**Problem we faced here:**
When we first ran this code, we got an error:

```
FileNotFoundError: tmdb_5000_movies.csv not found
```

This happened because we were running the script from the wrong folder. The CSV files were in the main project folder but we were running the script from inside the `backend` folder.

**How we fixed it:**
We changed the file path in the code to go one level up:
```python
movies_df = pd.read_csv('../tmdb_5000_movies.csv')
```

The `..` means "go one folder up". This fixed the error.

---

## Chapter 5 — The Genres Problem (JSON inside CSV)

When we looked at the genres column, it looked like this:

```
[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 878, "name": "Science Fiction"}]
```

This is called **JSON format** (JavaScript Object Notation). It is a way to store structured data as text.

But we only needed the names — Action, Adventure, Science Fiction. Not the ID numbers.

We had to write code to extract just the names:

```python
import json

# The raw genres text from CSV
raw = '[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}]'

# Convert text to Python list
genres_data = json.loads(raw)

# Extract only the names
genres = [item['name'] for item in genres_data]

# Result: ["Action", "Adventure"]
```

We did the same thing for cast names and director names.

**Problem we faced here:**
Some movies had empty or broken genres data. When we tried to parse them, we got:

```
json.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

This means the JSON text was empty or invalid.

**How we fixed it:**
We added a check — if the value is empty or not valid, skip it and use an empty list:

```python
try:
    genres = [item['name'] for item in json.loads(raw)]
except:
    genres = []  # If anything goes wrong, use empty list
```

This is called **error handling** — we prepare for things going wrong and handle them gracefully instead of crashing.

---

## Chapter 6 — Why We Chose MySQL as the Database

After processing the data, we needed a place to store it permanently.

**What is a Database?**
A database is like a very organised filing cabinet. Instead of papers, it stores data in tables (like Excel sheets). The data stays there even when you turn off the computer.

**Why MySQL specifically?**

We had other options like:
- SQLite (simple file-based database)
- MongoDB (stores data differently, not in tables)
- PostgreSQL (another table-based database)

We chose MySQL because:

1. **It is the most widely used database in the world** — knowing MySQL is a valuable skill
2. **It stores data in tables** — our data (movies, users, ratings) naturally fits in table format
3. **It supports relationships** — a rating belongs to a user AND a movie. MySQL handles these connections perfectly
4. **It supports JSON columns** — we needed to store genres as a list. MySQL 8.0 supports JSON type columns
5. **ACID compliance** — this means data is never lost or corrupted even if the computer crashes suddenly

**What is ACID?**
- **A**tomicity — either all of a transaction saves, or none of it does
- **C**onsistency — data always follows the rules we set
- **I**solation — two users saving data at the same time do not interfere with each other
- **D**urability — once saved, data stays saved even after a crash

---

## Chapter 7 — Designing the Database Tables

We designed 5 tables. Think of each table like a sheet in an Excel workbook.

**Table 1 — users**
Stores everyone who registers on the website.

| Column | Type | Purpose |
|--------|------|---------|
| id | Number | Unique ID for each user |
| username | Text | Display name |
| email | Text | Login email (must be unique) |
| password_hash | Text | Encrypted password (never plain text) |
| created_at | Date/Time | When they registered |

**Table 2 — movies**
Stores all 4803 movies.

| Column | Type | Purpose |
|--------|------|---------|
| id | Number | Our internal ID |
| tmdb_id | Number | Original ID from TMDB website |
| title | Text | Movie name |
| genres | JSON | List of genres like ["Action", "Drama"] |
| cast | JSON | List of actor names |
| director | Text | Director name |
| overview | Long Text | Movie description |
| poster_path | Text | Path to poster image |
| vote_average | Decimal | Rating out of 10 |
| popularity | Decimal | Popularity score |

**Table 3 — ratings**
Stores every rating a user gives to a movie.

| Column | Type | Purpose |
|--------|------|---------|
| id | Number | Unique ID |
| user_id | Number | Which user gave this rating |
| movie_id | Number | Which movie was rated |
| rating | Decimal | Score from 1.0 to 10.0 |
| review_text | Text | Optional written review |

**Table 4 — watchlist**
Stores movies a user wants to watch later.

| Column | Type | Purpose |
|--------|------|---------|
| id | Number | Unique ID |
| user_id | Number | Which user saved this |
| movie_id | Number | Which movie was saved |
| added_at | Date/Time | When they saved it |

**Table 5 — user_preferences**
Stores each user's favourite and disliked genres.

| Column | Type | Purpose |
|--------|------|---------|
| id | Number | Unique ID |
| user_id | Number | Which user |
| preferred_genres | JSON | Genres they love |
| disliked_genres | JSON | Genres they dislike |

**The connections between tables:**

```
users ──────────── ratings ──────────── movies
  |                                       |
  └──────────── watchlist ────────────────┘
  |
  └──────────── user_preferences
```

One user can have many ratings. One movie can have many ratings. This is called a **one-to-many relationship**.

---

## Chapter 8 — SQLAlchemy (Writing Python Instead of SQL)

To create these tables and work with the database, we used a tool called **SQLAlchemy**.

**What is SQLAlchemy?**
Normally to talk to a database, you write SQL commands like:
```sql
SELECT * FROM movies WHERE vote_average > 8.0
```

SQLAlchemy lets you write Python code instead:
```python
movies = db.query(Movie).filter(Movie.vote_average > 8.0).all()
```

This is called an **ORM — Object Relational Mapper**. It maps Python objects to database tables.

**Why use SQLAlchemy instead of writing SQL directly?**

1. **Safer** — prevents SQL Injection attacks (hackers cannot break your database)
2. **Cleaner code** — Python is easier to read than SQL
3. **Database independent** — if we switch from MySQL to another database, most code stays the same
4. **Automatic table creation** — SQLAlchemy creates the tables for us

**Problem we faced:**
When we first tried to connect to MySQL, we got this error:

```
ModuleNotFoundError: No module named 'pymysql'
```

**What happened:** SQLAlchemy needs a separate driver to talk to MySQL. We forgot to install it.

**How we fixed it:**
```bash
pip install pymysql
```

And we changed the database URL format to include `+pymysql`:
```
mysql+pymysql://root:password@localhost:3306/movie_recommender
```

---

## Chapter 9 — Loading Movies into the Database (Migration)

Now we had the database ready and the CSV data processed. We needed to move all 4803 movies from the CSV files into the MySQL database.

This process is called **Data Migration** — moving data from one place to another.

We wrote a script called `migrate_data.py` that:

1. Opens the CSV files
2. Reads each movie one by one
3. Cleans the data (extracts genres, cast, director)
4. Creates a Movie object
5. Saves it to MySQL database
6. Every 100 movies, it saves (commits) to avoid losing data

```python
for each movie in the CSV file:
    Step 1: Get the title
    Step 2: Extract genres list from JSON text
    Step 3: Extract cast names from JSON text
    Step 4: Find director from crew list
    Step 5: Create Movie object with all this data
    Step 6: Add to database
    Step 7: Every 100 movies, save to database
```

**Problems we faced during migration:**

**Problem 1 — Duplicate movies**
When we ran the script twice by mistake, we got:
```
IntegrityError: Duplicate entry for key 'movies.ix_movies_tmdb_id'
```
This means we tried to insert the same movie twice. MySQL rejected it because we set `tmdb_id` as unique.

**Fix:** We added a check before inserting:
```python
# Check if movie already exists
existing = db.query(Movie).filter(Movie.tmdb_id == movie_id).first()
if existing:
    continue  # Skip this movie, already in database
```

**Problem 2 — Some movies had no title**
A few rows in the CSV had empty title fields. Inserting a movie with no title would cause problems.

**Fix:** We added a check:
```python
if not title or title == 'nan':
    continue  # Skip movies with no title
```

**Problem 3 — Runtime column had decimal values**
Some movies had runtime like `148.0` instead of `148`. When we tried to store it as an integer, it failed.

**Fix:** We converted it properly:
```python
runtime = int(float(row['runtime'])) if pd.notna(row['runtime']) else None
```

After fixing all these problems, the migration ran successfully and loaded **4803 movies** into MySQL.

---

## Chapter 10 — Getting Movie Posters (TMDB API)

The CSV files had a column called `poster_path` but it was empty for most movies. The actual poster images are stored on TMDB's servers.

To get the poster paths, we needed to call the **TMDB API**.

**What is an API?**
API stands for **Application Programming Interface**.

Think of it like ordering food at a restaurant:
- You (our code) are the customer
- The waiter is the API
- The kitchen is TMDB's server
- The food is the movie data

You tell the waiter what you want. The waiter goes to the kitchen. The kitchen prepares it. The waiter brings it back to you.

Similarly:
- Our code sends a request to TMDB's API
- TMDB's server finds the movie data
- TMDB sends back the data as JSON text
- Our code reads the poster path from the response

**What is an API Key?**
TMDB gives free access to their data, but they need to know who is using it. So they give each developer a unique key — like a password.

Without the key, TMDB blocks your request. With the key, it allows it.

Our API key: `c20cfa2fbbe54c8971f014a6560fd7d9`

**How we used it:**
```python
import requests

tmdb_id = 19  # Inception's ID
api_key = "c20cfa2fbbe54c8971f014a6560fd7d9"

# Ask TMDB for movie details
url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}"
response = requests.get(url)

# Get the poster path from the response
data = response.json()
poster_path = data['poster_path']
# Result: "/gKY6q7SjCkAU6FqvqWybDYgUKIF.jpg"
```

**How poster images are displayed:**
The poster_path is just a filename. The full image URL is:
```
https://image.tmdb.org/t/p/w185/gKY6q7SjCkAU6FqvqWybDYgUKIF.jpg
```
- `image.tmdb.org` = TMDB's image server
- `w185` = image width 185 pixels (we can change this for different sizes)
- The filename = the poster_path we stored

We never store the actual image file. We only store the filename. The browser fetches the image directly from TMDB's servers. This saves us storage space.

**Problems we faced:**

**Problem 1 — Too many API calls, too slow**
We had 4803 movies. Calling the API for each one would take hours.

**Fix:** We only fetched posters for the top 60 most popular movies first. The rest can be done later.

**Problem 2 — API rate limiting**
TMDB allows only a certain number of requests per second. If we send too many requests too fast, they block us temporarily.

**Fix:** We added a small delay between each request:
```python
import time
time.sleep(0.05)  # Wait 0.05 seconds between each request
```

**Problem 3 — API key in source code**
We accidentally put the API key directly in the code and pushed it to GitHub. This is a security risk — anyone can see it and use our key.

**Fix:** We moved it to an environment variable in the `.env` file. The `.env` file is listed in `.gitignore` so it never gets pushed to GitHub.

```python
import os
api_key = os.getenv('TMDB_API_KEY')  # Read from environment, not hardcoded
```


---

## Chapter 11 — Building the Backend with FastAPI

Now the database was ready with 4803 movies. Next step was to build the backend.

**What is a Backend?**
The backend is the invisible part of a website that does all the work. When you click "Get Recommendations", the frontend sends a message to the backend. The backend thinks, talks to the database, runs the ML algorithm, and sends back the answer.

Users never see the backend. They only see the result.

**Why FastAPI?**

We had choices like Django, Flask, FastAPI.

| Framework | Speed | Difficulty | Auto Documentation |
|-----------|-------|-----------|-------------------|
| Django | Medium | Hard | No |
| Flask | Medium | Easy | No |
| FastAPI | Very Fast | Easy | Yes — automatic! |

We chose FastAPI because:
1. It is the fastest Python web framework
2. It automatically creates a documentation page at `/docs` — you can test all APIs from the browser without writing any extra code
3. It validates data automatically — if someone sends wrong data, FastAPI rejects it before it reaches our code
4. It is modern and used by big companies like Uber, Microsoft

**How we organised the backend:**

```
backend/
├── app/
│   ├── main.py          ← Starting point, connects everything
│   ├── core/
│   │   ├── config.py    ← Settings (database URL, secret key)
│   │   ├── database.py  ← Database connection
│   │   └── security.py  ← Password hashing, JWT tokens
│   ├── models/          ← Database table definitions
│   ├── schemas/         ← What data looks like (input/output)
│   ├── routers/         ← API endpoints (URLs)
│   ├── services/        ← ML recommendation engine
│   └── utils/           ← Helper functions
```

**Problems we faced:**

**Problem 1 — CORS Error**
When the frontend (running on port 8501) tried to call the backend (running on port 8000), the browser blocked it with:
```
Access to fetch blocked by CORS policy
```

**What is CORS?**
CORS = Cross-Origin Resource Sharing. Browsers have a security rule — a website on one address cannot call another address unless that other address gives permission.

**Fix:** We added CORS middleware to FastAPI:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Problem 2 — Environment variables not loading**
Our `.env` file had the database URL and secret key. But when we ran the backend, it said:
```
ValidationError: DATABASE_URL field required
```

**Fix:** We needed to install `python-dotenv` and load the `.env` file:
```python
from dotenv import load_dotenv
load_dotenv()  # This reads the .env file
```

**Problem 3 — Database connection pool exhausted**
Under heavy use, we got:
```
TimeoutError: QueuePool limit of size 5 overflow 10 reached
```

This means too many parts of the code were trying to use the database at the same time.

**Fix:** We increased the connection pool size:
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,      # Keep 10 connections ready
    max_overflow=20    # Allow 20 extra if needed
)
```

---

## Chapter 12 — Login and Security (JWT + bcrypt)

**The Password Problem**

When a user registers with password "mypassword123", we cannot store it as plain text in the database. If a hacker steals our database, they would see everyone's passwords.

The solution is **hashing** — converting the password into a scrambled, unreadable text.

We used **bcrypt** for this.

**How bcrypt works:**
```
Original password: "mypassword123"
After bcrypt:      "$2b$12$xK8mNpLqRs7tUvWxYzAbCd..."

Properties:
- Cannot be reversed (you cannot get "mypassword123" back from the hash)
- Same password always gives different hash (because of random "salt")
- Slow by design (makes brute force attacks take years)
```

**12 rounds** means bcrypt runs the hashing process 2^12 = 4096 times. This makes it very slow for hackers to guess passwords.

**The Login Token Problem**

After login, how does the backend know who is making each request? The user cannot send their password with every request — that would be insecure.

The solution is **JWT — JSON Web Token**.

**How JWT works:**

Step 1 — User logs in with correct password
Step 2 — Backend creates a token:
```
Token contains: {user_id: 5, expires: tomorrow}
Token is signed with our secret key
Token looks like: eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1fQ.abc123
```

Step 3 — Frontend stores this token
Step 4 — Every request includes the token in the header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
```

Step 5 — Backend reads the token, verifies the signature, extracts user_id
Step 6 — Backend knows who is making the request

**The token expires in 24 hours.** After that, the user must log in again. This limits damage if a token is stolen.

**Problems we faced:**

**Problem 1 — bcrypt version conflict**
We got this error:
```
AttributeError: module 'bcrypt' has no attribute 'checkpw'
```

This happened because we had an old version of bcrypt installed.

**Fix:**
```bash
pip install bcrypt==4.1.2
```

**Problem 2 — JWT token not working**
We got:
```
JWTError: Signature verification failed
```

This happened because the SECRET_KEY in our `.env` file was too short (less than 32 characters).

**Fix:** We changed the secret key to a longer random string:
```
SECRET_KEY=cineai-jwt-secret-key-2024-minimum-32-characters-long
```

---

## Chapter 13 — The ML Engine (The Most Important Part)

This is the heart of the entire project. Everything else is just support for this.

### What Problem Are We Solving?

We have 4803 movies. A user has rated 10 of them. We need to predict which of the remaining 4793 movies they will like.

We cannot ask the user to rate all 4803 movies. We need to **predict** their preferences.

This is the **Recommendation Problem**.

---

### Algorithm 1 — TF-IDF + Cosine Similarity (Content-Based Filtering)

**The idea:** Find movies that are similar to each other based on their content (genres, cast, director, description).

**Step 1 — Create a text description for each movie**

For each movie, we combine all its features into one text string:
```
Inception:
"Sci-Fi Sci-Fi Sci-Fi Thriller Thriller Thriller
A thief who steals corporate secrets through dream-sharing technology...
Leonardo DiCaprio Joseph Gordon-Levitt Ellen Page
Christopher Nolan"
```

We repeat genres 3 times to give them more importance. This is called **feature weighting**.

**Step 2 — TF-IDF converts text to numbers**

Computers cannot understand text. They only understand numbers. TF-IDF converts each word into a number.

**TF = Term Frequency** — how often a word appears in this movie's description
**IDF = Inverse Document Frequency** — how rare this word is across all movies

A word that appears in many movies (like "the", "a") gets a low score. A word that appears in few movies (like "inception", "nolan") gets a high score.

Result: Each movie becomes a list of numbers (a vector):
```
Inception:     [0.8, 0.1, 0.9, 0.0, 0.7, ...]
Interstellar:  [0.7, 0.1, 0.8, 0.0, 0.6, ...]
Titanic:       [0.0, 0.9, 0.1, 0.8, 0.0, ...]
```

**Step 3 — Cosine Similarity finds similar movies**

Cosine similarity measures the angle between two vectors. If the angle is small (close to 0), the movies are similar. If the angle is large, they are different.

Result is a number between 0 and 1:
- 1.0 = identical
- 0.9 = very similar
- 0.5 = somewhat similar
- 0.0 = completely different

```
Inception vs Interstellar = 0.94  (very similar — both Sci-Fi)
Inception vs Titanic      = 0.08  (very different — different genres)
```

**Step 4 — Store the similarity matrix**

We compute similarity between ALL pairs of movies and store it in a big table (matrix). This is done once when the server starts.

When a user asks "find movies similar to Inception", we just look up Inception's row in the matrix and return the top results. This is very fast.

**Problems we faced:**

**Problem 1 — Memory error**
4803 × 4803 = 23 million similarity scores. This used too much memory.

**Fix:** We used `TruncatedSVD` to reduce dimensions before computing similarity. This reduced memory usage significantly.

**Problem 2 — Slow startup**
Building the similarity matrix took 45 seconds every time the server started.

**Fix:** We accepted this as a one-time cost. The matrix is built once at startup and stays in memory. All subsequent requests are instant.

---

### Algorithm 2 — SVD Matrix Factorization

**The idea:** Learn hidden patterns from user ratings. Find users with similar taste. Predict what rating a user would give to movies they have not seen.

**What is a Matrix?**
A matrix is just a table of numbers. Our user-movie rating matrix looks like this:

```
           Inception  Interstellar  Titanic  Avatar  Dark Knight
User Pavan:    9           8          2        7         9
User Yousuf:   8           9          3        8         8
User Arif:     2           1          9        3         2
User Dhanush:  ?           8          ?        7         ?   ← predict these
```

Most cells are empty (?) because users have not rated most movies. We need to fill in the blanks.

**What is SVD?**
SVD = Singular Value Decomposition.

It is a mathematical technique that breaks a big matrix into smaller pieces. These smaller pieces capture the hidden patterns.

For example, it might discover:
- Pattern 1: Users who like Sci-Fi also like mind-bending plots
- Pattern 2: Users who like Romance also like Drama
- Pattern 3: Users who like Action also like Adventure

These patterns are called **latent factors** — hidden characteristics that explain why users like certain movies.

**How it works:**
```
Big matrix (Users × Movies)
        ↓ SVD breaks it into
User factors × Weights × Movie factors

User factors = each user's taste profile
Movie factors = each movie's characteristics

To predict Dhanush's rating for Inception:
Dhanush's taste profile × Inception's characteristics = 8.7
→ Dhanush will probably like Inception
```

We used **50 latent factors** — meaning we find 50 hidden patterns in the data.

**Problems we faced:**

**Problem 1 — Not enough ratings**
SVD needs at least 20 ratings to work. When we first tested, we had only 5 ratings and got:
```
ValueError: n_components must be < min(n_samples, n_features)
```

**Fix:** We added a check — only build SVD model if there are 20+ ratings. Otherwise fall back to content-based.

**Problem 2 — Rating scale bias**
Some users always give high ratings (8, 9, 10). Others are strict and give low ratings (4, 5, 6). This makes comparison unfair.

**Fix:** We subtracted each user's average rating before running SVD. This is called **mean normalization**:
```
Pavan's average = 8.0
Pavan's rating for Inception = 9
Normalized = 9 - 8.0 = +1.0 (above average for Pavan)

Arif's average = 5.0
Arif's rating for Inception = 6
Normalized = 6 - 5.0 = +1.0 (also above average for Arif)

Now both are comparable!
```

---

### Algorithm 3 — Pearson Correlation (User-Based Collaborative Filtering)

**The idea:** Find users who have similar rating patterns to you. Recommend what those similar users liked.

**Pearson Correlation** is a number between -1 and +1:
- +1 = two users rate movies exactly the same way
- 0 = no relationship between their ratings
- -1 = they always disagree

```
You rated:    Inception=9, Dark Knight=9, Interstellar=8, Titanic=3
User B rated: Inception=8, Dark Knight=9, Interstellar=9, Titanic=2

Pearson correlation = 0.97 → Very similar taste!

User B also rated "The Prestige" = 9 (you have not seen it)
→ Recommend "The Prestige" to you
```

We look at the **top 50 most similar users** and combine their recommendations.

---

### The Hybrid Engine — Combining All Three

Using just one algorithm is not enough:
- Content-based alone: always recommends similar genres, no variety
- SVD alone: needs many ratings to work, fails for new users
- Pearson alone: needs many users with similar taste

Combining all three gives the best results.

**How we combine them:**

```
New user (0-4 ratings):
→ Show popular movies (everyone likes popular movies)
→ No personalisation yet

Getting started (5-19 ratings):
→ 50% SVD predictions
→ 50% Content similarity
→ Starting to personalise

Experienced user (20+ ratings):
→ 70% SVD predictions (now reliable)
→ 30% Content similarity
→ Fully personalised

Then apply preferences:
→ Preferred genre: multiply score by 1.15 (boost by 15%)
→ Disliked genre: multiply score by 0.70 (reduce by 30%)

Sort all movies by final score
Return top 20
```

This is called an **Adaptive Hybrid System** — it adapts based on how much data we have about the user.

---

## Chapter 14 — Building the Frontend with Streamlit

**What is a Frontend?**
The frontend is what the user sees. The buttons, the movie posters, the search box — all of this is the frontend.

**Why Streamlit?**

We had options like React, Vue.js, plain HTML/CSS.

| Option | Language | Difficulty | Good for ML? |
|--------|---------|-----------|-------------|
| React | JavaScript | Hard | No |
| Vue.js | JavaScript | Medium | No |
| HTML/CSS | HTML, CSS, JS | Medium | No |
| Streamlit | Python | Easy | Yes! |

We chose Streamlit because:
1. It is written in Python — same language as our backend and ML code
2. No need to learn JavaScript, HTML, or CSS
3. It connects to our API with simple Python code
4. It is specifically designed for data and ML applications
5. It deploys for free on Streamlit Cloud

**How the frontend connects to the backend:**

Every action on the website makes an API call:

```python
# When user clicks "Get Recommendations"
import requests

response = requests.get(
    "http://localhost:8000/api/v1/recommendations/",
    headers={"Authorization": f"Bearer {user_token}"}
)

movies = response.json()  # Get the list of movies
# Display them on screen
```

The frontend never touches the database directly. It always goes through the backend. This is the correct way to build web applications.

**Problems we faced:**

**Problem 1 — Slow page loading**
Every time the user clicked anything, the entire page reloaded and fetched data from the API again. This made the site feel slow.

**Fix:** We used `@st.cache_data` — a Streamlit feature that remembers the result of a function for a set time:
```python
@st.cache_data(ttl=600)  # Remember for 600 seconds (10 minutes)
def get_popular_movies():
    return requests.get("http://backend/api/v1/recommendations/popular").json()
```

Now popular movies are fetched once and remembered for 10 minutes. Tab switching became instant.

**Problem 2 — Duplicate widget error**
We showed the same movie in multiple genre rows (Action row and Thriller row both had Dark Knight). Each movie had a button with a key based on movie ID. Same movie = same key = error:
```
DuplicateWidgetID: There are multiple widgets with the same key='gr_Top_789'
```

**Fix:** We made the key unique by including the row name and position:
```python
key=f"gr_{row_label}_{position}_{movie_id}"
```

**Problem 3 — Red color on button click**
Streamlit's default theme uses red for active/focused buttons. Our design used blue. The red kept appearing on click.

**Fix:** We created a `config.toml` file in the `.streamlit` folder:
```toml
[theme]
primaryColor = "#2563eb"  # Blue instead of red
```

This tells Streamlit to use blue as the primary color everywhere.

---

## Chapter 15 — Deployment (Making It Live on the Internet)

Local development means the website only works on our computer. For the world to access it, we needed to put it on the internet.

We used three free cloud services:

---

### Part 1 — Railway (Database Hosting)

Railway is a cloud platform that hosts databases.

**Steps:**
1. Created account on railway.app
2. Created a new MySQL database
3. Got the connection URL:
   `mysql+pymysql://root:password@shuttle.proxy.rlwy.net:58035/railway`
4. Ran our migration script pointing to this URL
5. All 4803 movies loaded into Railway's MySQL

**Problem:** Migration was very slow because we were also fetching TMDB posters for each movie (0.05 second delay × 4803 movies = 4 minutes).

**Fix:** We ran migration without poster fetching first (fast), then ran a separate poster update script for just the top 60 popular movies.

---

### Part 2 — Render (Backend Hosting)

Render is a cloud platform that hosts web applications.

**Steps:**
1. Connected our GitHub repository to Render
2. Configured settings:
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
3. Added environment variables (DATABASE_URL, SECRET_KEY, TMDB_API_KEY)
4. Render built and deployed our FastAPI app

**Every time we push code to GitHub, Render automatically rebuilds and redeploys.** This is called **CI/CD — Continuous Integration / Continuous Deployment**.

**Problem:** Free tier on Render sleeps after 15 minutes of no activity. First request after sleep takes 60 seconds to wake up.

**Fix:** Before a demo or interview, open the `/health` URL first to wake it up. Then show the demo.

---

### Part 3 — Streamlit Cloud (Frontend Hosting)

Streamlit Cloud is a free hosting service specifically for Streamlit apps.

**Steps:**
1. Connected GitHub repository
2. Set main file as `frontend/app.py`
3. Added secret: `API_BASE_URL = "https://cineai-backend.onrender.com"`
4. Deployed

**Problem 1:** Streamlit Cloud used Python 3.14 by default. The Pillow library (used for images) does not support Python 3.14 yet. Build failed with:
```
Failed to build wheel for pillow
RequiredDependencyException: zlib
```

**Fix:** We created a `.python-version` file in the frontend folder with content `3.11`. This forces Streamlit Cloud to use Python 3.11 where everything works.

**Problem 2:** We also upgraded Streamlit from version 1.32.0 to 1.40.0 because the newer version has better Python 3.11 compatibility.

---

## Chapter 16 — Docker (For Easy Setup)

After all the deployment work, we also created Docker files so that anyone can run the entire project on their computer with just one command.

**What is Docker?**
Docker packages your application with everything it needs — Python, libraries, settings — into a container. A container is like a box that contains everything needed to run the app.

**The problem Docker solves:**
Without Docker, a new team member needs to:
1. Install Python (correct version)
2. Install MySQL
3. Install all Python libraries
4. Configure environment variables
5. Start everything in the right order

This takes 30-60 minutes and often has errors.

With Docker:
```bash
docker-compose up --build
```

One command. Everything starts automatically. Takes 5 minutes.

**We created:**
- `backend/Dockerfile` — instructions to build the backend container
- `frontend/Dockerfile` — instructions to build the frontend container
- `docker-compose.yml` — instructions to run all three (MySQL + backend + frontend) together

---

## Chapter 17 — The Complete Flow (How Everything Works Together)

Here is the complete journey when a user uses CineAI:

```
Step 1: User opens the website URL
→ Browser loads Streamlit frontend

Step 2: User registers
→ Frontend sends: POST /api/v1/auth/register
  with: {username, email, password}
→ Backend hashes password with bcrypt
→ Backend saves user to MySQL
→ Returns: {id, username, email}

Step 3: User logs in
→ Frontend sends: POST /api/v1/auth/login
  with: {email, password}
→ Backend checks password against hash
→ Backend creates JWT token
→ Returns: {access_token}
→ Frontend stores token

Step 4: User browses Home page
→ Frontend sends: GET /api/v1/recommendations/popular
→ Backend queries MySQL: top movies by popularity × rating
→ Returns: list of 20 movies with poster_path
→ Frontend builds poster URL: image.tmdb.org/t/p/w185/{poster_path}
→ Browser fetches images from TMDB's servers
→ Movie cards displayed

Step 5: User rates Inception as 9/10
→ Frontend sends: POST /api/v1/ratings/
  with: {movie_id: 19, rating: 9.0}
  header: Authorization: Bearer {token}
→ Backend validates token → gets user_id
→ Backend saves rating to MySQL

Step 6: User asks for recommendations
→ Frontend sends: GET /api/v1/recommendations/
  header: Authorization: Bearer {token}
→ Backend validates token → gets user_id
→ Backend checks: how many ratings does this user have?
→ If 5+: runs SVD + Content-Based hybrid
→ Applies genre preference boosts
→ Returns top 20 personalised movies

Step 7: User clicks "Why?" on a movie
→ Frontend sends: GET /api/v1/recommendations/explain/19
→ Backend checks: why was Inception recommended?
→ Returns: "Because you liked Interstellar" / "Matches your Sci-Fi preference"
→ Frontend shows explanation
```

---

## Summary — Lessons Learned

| What We Learned | How We Learned It |
|----------------|------------------|
| Always handle errors in code | JSON parsing crashed without try/except |
| Never hardcode API keys | Accidentally pushed key to GitHub |
| Database design is critical | Had to redesign tables twice |
| Test with small data first | Migration took hours with full dataset |
| Environment variables for secrets | Security best practice |
| Cache API calls | Site was slow without caching |
| Pin Python version in deployment | Python 3.14 broke Pillow |
| One command deployment saves time | Docker made setup easy for everyone |

---

## Final Summary — What We Built

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Movie Data | TMDB CSV + Kaggle | 4803 movies with all details |
| Poster Images | TMDB API | Movie poster images |
| Database | MySQL + SQLAlchemy | Store all data permanently |
| ML Engine | Scikit-learn (TF-IDF, SVD) | Recommendation algorithms |
| Backend | FastAPI + Python | API, business logic, security |
| Frontend | Streamlit | User interface |
| Security | JWT + bcrypt | Login and password protection |
| Deployment | Render + Railway + Streamlit Cloud | Live on internet |
| Containerisation | Docker | Easy setup for developers |
| Version Control | GitHub | Code storage and auto-deploy |

---

*CineAI — Built by Pavan (Team Leader), Yousuf, Arif, Dhanush*
*B.Tech Final Year Project — 2025*
