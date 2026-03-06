# Full-Stack Movie Recommendation System

Professional movie recommendation platform with Streamlit frontend, FastAPI backend, MySQL database, and hybrid ML algorithms.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Git

### 1. Create MySQL Database
```bash
mysql -u root -p
CREATE DATABASE movie_recommender;
EXIT;
```

### 2. Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
```

### 3. Configure Environment Variables
Edit `backend/.env` file:
```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/movie_recommender
TMDB_API_KEY=your_tmdb_api_key_here
OMDB_API_KEY=your_omdb_api_key_here
SECRET_KEY=your-secret-key-min-32-characters-long
```

**Get Free API Keys:**
- TMDB: https://www.themoviedb.org/settings/api
- OMDB: http://www.omdbapi.com/apikey.aspx

### 4. Migrate Data to Database
```bash
# From backend directory
python migrate_data.py
```

### 5. Start Backend Server
```bash
# From backend directory
uvicorn app.main:app --reload
```
✅ Backend: http://localhost:8000
✅ API Docs: http://localhost:8000/docs

### 6. Start Frontend (New Terminal)
```bash
cd frontend
streamlit run app.py
```
✅ Frontend: http://localhost:8501

## 📁 Project Structure

```
streamlit-project/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── core/              # Config, database, security
│   │   ├── models/            # SQLAlchemy models
│   │   ├── routers/           # API endpoints
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # ML recommendation engine
│   │   ├── utils/             # Helper functions
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   ├── .env.example
│   └── migrate_data.py
├── frontend/                   # Streamlit Frontend
│   ├── app.py
│   └── requirements.txt
├── tmdb_5000_movies.csv       # Movie dataset
├── tmdb_5000_credits.csv      # Credits dataset
└── README.md
```

## ✨ Features

### User Features
- 🔐 User registration & login (JWT authentication)
- 🎯 Personalized movie recommendations
- ⭐ Rate movies (1-10 scale) & write reviews
- 📝 Watchlist management
- 🔍 Advanced search (title, genre, rating)
- 🎬 Similar movie recommendations
- 👤 User preferences (favorite/disliked genres)

### Technical Features
- 🤖 Hybrid ML algorithm (content-based + collaborative filtering)
- ❄️ Cold start problem handling
- 🗄️ MySQL database with proper schema
- 🔒 Secure authentication (bcrypt + JWT)
- 📊 RESTful API with 15+ endpoints
- 🚀 Performance optimized (precomputed matrices, indexes)

## 🧠 Machine Learning Algorithms

### 1. Content-Based Filtering
- TF-IDF vectorization on movie features
- Cosine similarity computation
- Features: genres, overview, cast, director

### 2. Collaborative Filtering
- User-based collaborative filtering
- Pearson correlation for user similarity
- Predicts ratings based on similar users

### 3. Hybrid Recommender
- Adaptive weights based on user history
- New users: 80% content, 20% collaborative
- Experienced users: 40% content, 60% collaborative
- Genre preference boosting

### 4. Cold Start Handling
- Popularity-based recommendations for new users
- Progressive transition to personalized recommendations

## 🛠️ Technology Stack

**Frontend:** Streamlit, Requests
**Backend:** FastAPI, SQLAlchemy, Pydantic, PyMySQL
**Database:** MySQL
**ML:** Scikit-learn, Pandas, NumPy
**Security:** Python-JOSE (JWT), Passlib (bcrypt)

## 📊 Database Schema

- **users**: User accounts and authentication
- **movies**: Movie metadata (5000+ movies)
- **ratings**: User ratings and reviews
- **watchlist**: User saved movies
- **user_preferences**: Genre preferences

## 🔧 Troubleshooting

### "Can't connect to database"
- Verify MySQL is running
- Check DATABASE_URL in .env
- Ensure database `movie_recommender` exists

### "Module not found"
- Activate virtual environment
- Run `pip install -r requirements.txt`

### "API key error"
- Get free API keys from TMDB and OMDB
- Add them to backend/.env file

### "Migration fails"
- Ensure CSV files exist in project root
- Check database permissions
- Verify MySQL connection

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Movies
- `GET /api/v1/movies/` - List movies
- `GET /api/v1/movies/{id}` - Get movie details
- `GET /api/v1/movies/search/` - Search movies

### Recommendations
- `GET /api/v1/recommendations/` - Personalized recommendations
- `GET /api/v1/recommendations/popular` - Popular movies

### Ratings
- `POST /api/v1/ratings/` - Rate a movie
- `GET /api/v1/ratings/my-ratings` - Get user's ratings

### Watchlist
- `POST /api/v1/watchlist/{movie_id}` - Add to watchlist
- `DELETE /api/v1/watchlist/{movie_id}` - Remove from watchlist
- `GET /api/v1/watchlist/` - Get user's watchlist

## 🎓 For BTech Students

This project demonstrates:
- Full-stack development skills
- RESTful API design
- Database design & optimization
- Machine learning implementation
- Authentication & security
- Problem-solving (cold start problem)

Perfect for final year projects and job interviews!

## 📝 License

MIT License - Free to use for educational and personal projects

## 🙏 Credits

- TMDB API for movie data
- OMDB API for additional metadata
- FastAPI and Streamlit communities
