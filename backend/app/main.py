from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, Base
from .routers import auth, movies, ratings, watchlist, recommendations
from .services.recommendation_engine import recommendation_engine
from .core.database import SessionLocal
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Recommendation API",
    description="Full-stack movie recommendation system with hybrid ML algorithms",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(ratings.router)
app.include_router(watchlist.router)
app.include_router(recommendations.router)


@app.on_event("startup")
async def startup_event():
    """Initialize recommendation engine on startup"""
    logger.info("Initializing recommendation engine...")
    db = SessionLocal()
    try:
        recommendation_engine.build_content_based_model(db)
        logger.info("Recommendation engine initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing recommendation engine: {e}")
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "movie-recommendation-api"}


@app.get("/")
def root():
    return {
        "message": "Movie Recommendation API",
        "version": "1.0.0",
        "docs": "/docs"
    }
