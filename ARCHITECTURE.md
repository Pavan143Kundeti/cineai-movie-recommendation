# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                      (Streamlit Frontend)                       │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────────┐  │
│  │   Home   │  Recs    │ Watchlist│  Search  │   Profile    │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST API
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Gateway                            │  │
│  │  ┌────────┬────────┬────────┬────────┬────────────────┐  │  │
│  │  │  Auth  │ Movies │ Ratings│Watchlist│Recommendations│  │  │
│  │  └────────┴────────┴────────┴────────┴────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│  ┌──────────────────────────┴────────────────────────────┐    │
│  │              Business Logic Layer                      │    │
│  │  ┌──────────┬──────────┬──────────┬──────────────┐    │    │
│  │  │   User   │  Movie   │  Rating  │  Watchlist   │    │    │
│  │  │ Service  │ Service  │ Service  │   Service    │    │    │
│  │  └──────────┴──────────┴──────────┴──────────────┘    │    │
│  └────────────────────────────────────────────────────────┘    │
│                             │                                   │
│  ┌──────────────────────────┴────────────────────────────┐    │
│  │           Machine Learning Engine                      │    │
│  │  ┌──────────────┬──────────────┬──────────────────┐   │    │
│  │  │  Content-    │ Collaborative│  Hybrid          │   │    │
│  │  │  Based       │  Filtering   │  Recommender     │   │    │
│  │  │  Filter      │              │                  │   │    │
│  │  └──────────────┴──────────────┴──────────────────┘   │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │ SQLAlchemy ORM
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MySQL DATABASE                             │
│  ┌────────┬────────┬────────┬──────────┬──────────────────┐    │
│  │ users  │ movies │ ratings│ watchlist│ user_preferences │    │
│  └────────┴────────┴────────┴──────────┴──────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Layer (Streamlit)
- **Purpose**: User interface and interaction
- **Technology**: Streamlit (Python web framework)
- **Responsibilities**:
  - Display movies with posters and details
  - Handle user authentication (login/register)
  - Manage user sessions
  - Make API calls to backend
  - Display recommendations and search results

### API Gateway (FastAPI)
- **Purpose**: RESTful API endpoints
- **Technology**: FastAPI with Pydantic validation
- **Responsibilities**:
  - Route HTTP requests to appropriate services
  - Validate request data
  - Handle authentication (JWT tokens)
  - Return JSON responses
  - CORS middleware for frontend communication

### Business Logic Layer
- **User Service**: User management, authentication, preferences
- **Movie Service**: Movie CRUD operations, search, filtering
- **Rating Service**: Handle user ratings and reviews
- **Watchlist Service**: Manage user watchlists
- **Recommendation Service**: Orchestrate ML algorithms

### Machine Learning Engine

#### Content-Based Filter
- **Algorithm**: TF-IDF + Cosine Similarity
- **Features**: Genres, overview, cast, director
- **Output**: Similar movies based on content
- **Use Case**: "Movies like this one"

#### Collaborative Filter
- **Algorithm**: User-based CF with Pearson correlation
- **Data**: User-item rating matrix
- **Output**: Predicted ratings for unwatched movies
- **Use Case**: "Users like you also liked"

#### Hybrid Recommender
- **Strategy**: Weighted combination of both filters
- **Weights**: Adaptive based on user history
- **Enhancements**: Genre preferences, diversity filter
- **Use Case**: Personalized recommendations

### Database Layer (MySQL)
- **Purpose**: Persistent data storage
- **Technology**: MySQL with SQLAlchemy ORM
- **Tables**:
  - `users`: User accounts and authentication
  - `movies`: Movie metadata and features
  - `ratings`: User ratings and reviews
  - `watchlist`: User saved movies
  - `user_preferences`: Genre preferences

## Data Flow

### User Registration Flow
```
User → Frontend → POST /api/v1/auth/register → User Service
                                              → Hash Password
                                              → Save to DB
                                              ← Return User Data
```

### Recommendation Flow
```
User → Frontend → GET /api/v1/recommendations → Recommendation Service
                                               → Check User History
                                               → ML Engine (Hybrid)
                                                 ├─ Content-Based Filter
                                                 └─ Collaborative Filter
                                               → Combine Results
                                               → Apply Preferences
                                               → Query Movie Details
                                               ← Return Recommendations
```

### Rating Flow
```
User → Frontend → POST /api/v1/ratings → Rating Service
                                        → Save Rating to DB
                                        → Trigger CF Update
                                        ← Return Confirmation
```

## Security Architecture

### Authentication Flow
```
1. User Login → Backend validates credentials
2. Backend generates JWT token (24h expiry)
3. Frontend stores token in session
4. All protected requests include token in header
5. Backend validates token on each request
6. Token decoded to get user_id
```

### Security Measures
- **Password Hashing**: bcrypt with 12 rounds
- **JWT Tokens**: HS256 algorithm with secret key
- **Environment Variables**: Sensitive data in .env
- **CORS**: Configured for specific origins
- **Input Validation**: Pydantic schemas
- **SQL Injection**: SQLAlchemy ORM prevents injection

## Scalability Considerations

### Current Optimizations
- Precomputed similarity matrices
- Database indexes on foreign keys
- Connection pooling (5-20 connections)
- Efficient queries with proper joins

### Future Scalability
- Redis caching for recommendations
- Celery for async tasks
- Load balancing with multiple backend instances
- Database replication for read scaling
- CDN for movie posters

## Technology Choices Rationale

### Why Streamlit?
- Rapid development for ML applications
- Python-native (same language as backend)
- Good for prototypes and demos
- Easy to showcase ML features

### Why FastAPI?
- Modern Python web framework
- Automatic API documentation (OpenAPI)
- Fast performance (async support)
- Built-in validation with Pydantic
- Easy to learn and use

### Why MySQL?
- Relational data (users, movies, ratings)
- ACID compliance for data integrity
- Wide industry adoption
- Good for structured data
- JSON column support for flexible fields

### Why Hybrid ML?
- Content-based: Works for new users
- Collaborative: Improves with more data
- Hybrid: Best of both worlds
- Adaptive weights: Optimizes for user history
