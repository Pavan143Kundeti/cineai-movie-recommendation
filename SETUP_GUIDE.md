# Quick Setup Guide

## Step-by-Step Setup

### 1. Install MySQL
Download and install MySQL from: https://dev.mysql.com/downloads/mysql/

### 2. Create Database
```bash
mysql -u root -p
CREATE DATABASE movie_recommender;
EXIT;
```

### 3. Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
# OR
cp .env.example .env    # Linux/Mac

# Edit .env file with your settings:
# - DATABASE_URL: Update with your MySQL password
# - TMDB_API_KEY: Get from https://www.themoviedb.org/settings/api
# - OMDB_API_KEY: Get from http://www.omdbapi.com/apikey.aspx
# - SECRET_KEY: Generate a random 32+ character string
```

### 4. Migrate Data
```bash
# Make sure you're in the backend directory
python migrate_data.py
```

### 5. Start Backend
```bash
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000
API Docs: http://localhost:8000/docs

### 6. Start Frontend (New Terminal)
```bash
cd frontend
streamlit run app.py
```

Frontend runs at: http://localhost:8501

## Getting API Keys

### TMDB API Key
1. Go to https://www.themoviedb.org/
2. Create an account
3. Go to Settings → API
4. Request an API key (choose "Developer")
5. Copy the API Key (v3 auth)

### OMDB API Key
1. Go to http://www.omdbapi.com/apikey.aspx
2. Select FREE tier
3. Enter your email
4. Check your email for the API key

## Troubleshooting

### Database Connection Error
- Make sure MySQL is running
- Check DATABASE_URL in .env file
- Verify MySQL username and password

### Module Not Found Error
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### API Connection Error
- Make sure backend is running on port 8000
- Check if firewall is blocking the connection

### Migration Fails
- Make sure CSV files exist in the parent directory
- Check if database is created
- Verify database permissions

## Testing the System

1. Register a new user account
2. Browse popular movies
3. Rate some movies (at least 5 for best recommendations)
4. Check personalized recommendations
5. Add movies to watchlist
6. Search for specific movies

## Project Structure

```
streamlit-project/
├── backend/
│   ├── app/
│   │   ├── core/          # Config, database, security
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── routers/       # API endpoints
│   │   ├── services/      # Business logic & ML
│   │   └── utils/         # Helper functions
│   ├── requirements.txt
│   ├── .env.example
│   └── migrate_data.py
├── frontend/
│   ├── app.py            # Streamlit application
│   └── requirements.txt
└── README_NEW.md
```
