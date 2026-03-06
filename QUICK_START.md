# Quick Start Guide - 5 Minutes

## Prerequisites Check
- [ ] Python 3.8+ installed
- [ ] MySQL installed and running
- [ ] Git installed

## Step 1: Database Setup (2 minutes)
```bash
# Open MySQL
mysql -u root -p

# Create database
CREATE DATABASE movie_recommender;
EXIT;
```

## Step 2: Backend Setup (2 minutes)
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env file - REQUIRED:
# - DATABASE_URL: mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/movie_recommender
# - TMDB_API_KEY: Get from https://www.themoviedb.org/settings/api
# - OMDB_API_KEY: Get from http://www.omdbapi.com/apikey.aspx
# - SECRET_KEY: Any random 32+ character string
```

## Step 3: Migrate Data (1 minute)
```bash
# Still in backend directory
python migrate_data.py
```

## Step 4: Start Backend (30 seconds)
```bash
# Still in backend directory
uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000
✅ API Docs at: http://localhost:8000/docs

## Step 5: Start Frontend (30 seconds)
```bash
# Open NEW terminal
cd frontend

# Run Streamlit
streamlit run app.py
```

✅ Frontend running at: http://localhost:8501

## Test It! (2 minutes)
1. Open http://localhost:8501
2. Click "Register" tab
3. Create account (username, email, password)
4. Login with your credentials
5. Browse popular movies
6. Rate some movies (at least 5)
7. Go to "Recommendations" page
8. See personalized recommendations!

## Common Issues

### "Module not found"
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### "Can't connect to database"
```bash
# Check MySQL is running
# Verify DATABASE_URL in .env
# Check username and password
```

### "API key error"
```bash
# Make sure you got API keys from:
# TMDB: https://www.themoviedb.org/settings/api
# OMDB: http://www.omdbapi.com/apikey.aspx
# Add them to .env file
```

### "Migration fails"
```bash
# Make sure CSV files exist in parent directory
# Check database is created
# Verify database permissions
```

## Project Structure Quick Reference

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── core/                # Config, database, security
│   ├── models/              # Database models
│   ├── routers/             # API endpoints
│   ├── schemas/             # Request/response schemas
│   └── services/            # ML engine
├── requirements.txt
├── .env                     # Your config (create this!)
└── migrate_data.py          # Data migration

frontend/
├── app.py                   # Streamlit app
└── requirements.txt
```

## API Endpoints Quick Reference

### Auth
- POST `/api/v1/auth/register` - Register
- POST `/api/v1/auth/login` - Login

### Movies
- GET `/api/v1/movies/` - List movies
- GET `/api/v1/movies/search/?q=avatar` - Search

### Recommendations
- GET `/api/v1/recommendations/` - Personalized
- GET `/api/v1/recommendations/popular` - Popular

### Ratings
- POST `/api/v1/ratings/` - Rate movie

### Watchlist
- POST `/api/v1/watchlist/{movie_id}` - Add
- GET `/api/v1/watchlist/` - View

## Commands Cheat Sheet

### Start Backend
```bash
cd backend
venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

### Start Frontend
```bash
cd frontend
streamlit run app.py
```

### Check API
```bash
# Open browser
http://localhost:8000/docs
```

### Reset Database
```bash
mysql -u root -p
DROP DATABASE movie_recommender;
CREATE DATABASE movie_recommender;
EXIT;
python migrate_data.py
```

## Getting API Keys (Free)

### TMDB API Key
1. Go to https://www.themoviedb.org/
2. Sign up (free)
3. Go to Settings → API
4. Request API Key (Developer)
5. Copy "API Key (v3 auth)"
6. Paste in .env as TMDB_API_KEY

### OMDB API Key
1. Go to http://www.omdbapi.com/apikey.aspx
2. Select FREE (1,000 requests/day)
3. Enter email
4. Check email for API key
5. Paste in .env as OMDB_API_KEY

## Environment Variables Template

```env
# .env file
DATABASE_URL=mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost:3306/movie_recommender
TMDB_API_KEY=your_tmdb_key_here
OMDB_API_KEY=your_omdb_key_here
SECRET_KEY=any-random-32-character-string-for-jwt-tokens
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## Success Checklist

After setup, verify:
- [ ] Backend running on port 8000
- [ ] Frontend running on port 8501
- [ ] Can register new user
- [ ] Can login
- [ ] Can see popular movies
- [ ] Can rate movies
- [ ] Can add to watchlist
- [ ] Can see recommendations
- [ ] API docs accessible at /docs

## Next Steps

1. ✅ Get it running (follow this guide)
2. 📖 Read PROJECT_SUMMARY.md (understand what was built)
3. 🏗️ Read ARCHITECTURE.md (understand how it works)
4. 💼 Read INTERVIEW_GUIDE.md (prepare for interviews)
5. 🎨 Customize and add features
6. 🚀 Deploy to cloud (optional)

## Need Help?

- Setup issues → SETUP_GUIDE.md
- Architecture questions → ARCHITECTURE.md
- Interview prep → INTERVIEW_GUIDE.md
- Project overview → PROJECT_SUMMARY.md

## Time Estimate

- Setup: 5-10 minutes
- Testing: 5 minutes
- Understanding: 30 minutes
- Customization: 1-2 hours
- Interview prep: 1 hour

**Total: 2-4 hours to be fully ready!**
