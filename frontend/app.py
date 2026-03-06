import streamlit as st
import requests
from typing import List, Dict, Optional
import os

# Page configuration - MUST BE FIRST
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Custom CSS
st.markdown("""
<style>
    .movie-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None


def api_request(endpoint: str, method: str = "GET", data: dict = None, auth: bool = False):
    """Make API request with optional authentication"""
    url = f"{API_BASE_URL}{endpoint}"
    headers = {}
    
    if auth and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        if response.status_code in [200, 201]:
            return response.json() if response.text else None
        elif response.status_code == 204:
            return None
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None


def display_movie_card(movie: Dict):
    """Display a movie card with poster and details"""
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Use TMDB poster if available, otherwise placeholder
            if movie.get('poster_path'):
                poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
            else:
                # Use TMDB ID to construct poster URL as fallback
                tmdb_id = movie.get('tmdb_id', movie.get('id'))
                poster_url = f"https://via.placeholder.com/300x450/1a1a1a/ffffff?text={movie['title'][:15]}"
            
            st.image(poster_url, use_column_width=True)
        
        with col2:
            st.subheader(movie['title'])
            
            if movie.get('genres'):
                genres_str = ', '.join(movie['genres']) if isinstance(movie['genres'], list) else movie['genres']
                st.write(f"**Genres:** {genres_str}")
            
            if movie.get('vote_average'):
                rating = movie['vote_average']
                stars = "⭐" * int(rating / 2)
                st.write(f"{stars} **{rating}/10**")
            
            if movie.get('release_date'):
                st.write(f"📅 **Release:** {movie['release_date']}")
            
            if movie.get('director'):
                st.write(f"🎬 **Director:** {movie['director']}")
            
            if movie.get('cast') and len(movie['cast']) > 0:
                cast_str = ', '.join(movie['cast'][:3])
                st.write(f"👥 **Cast:** {cast_str}")
            
            if movie.get('overview'):
                overview = movie['overview'][:200] + "..." if len(movie['overview']) > 200 else movie['overview']
                st.write(f"**Overview:** {overview}")
            
            # Action buttons
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("➕ Watchlist", key=f"watch_{movie['id']}"):
                    result = api_request(f"/api/v1/watchlist/{movie['id']}", method="POST", auth=True)
                    if result:
                        st.success("Added!")
                        st.rerun()
            
            with col_b:
                if st.button("⭐ Rate", key=f"rate_{movie['id']}"):
                    st.session_state.rating_movie = movie
                    st.rerun()
            
            with col_c:
                if st.button("🎯 Similar", key=f"similar_{movie['id']}"):
                    st.session_state.similar_movie_id = movie['id']
                    st.session_state.page = "Recommendations"
                    st.rerun()
        
        st.divider()


def show_rating_dialog():
    """Show rating dialog for selected movie"""
    if 'rating_movie' in st.session_state and st.session_state.rating_movie:
        movie = st.session_state.rating_movie
        
        with st.form(key=f"rating_form_{movie['id']}"):
            st.subheader(f"Rate: {movie['title']}")
            rating = st.slider("Rating", 1.0, 10.0, 5.0, 0.5)
            review = st.text_area("Review (optional)", max_chars=1000)
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Submit Rating")
            with col2:
                cancel = st.form_submit_button("Cancel")
            
            if submit:
                data = {
                    "movie_id": movie['id'],
                    "rating": rating,
                    "review_text": review if review else None
                }
                result = api_request("/api/v1/ratings/", method="POST", data=data, auth=True)
                if result:
                    st.success("Rating submitted!")
                    st.session_state.rating_movie = None
                    st.rerun()
            
            if cancel:
                st.session_state.rating_movie = None
                st.rerun()


def login_page():
    """Login/Register page"""
    st.title("🎬 Movie Recommendation System")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to your account")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            data = {"email": email, "password": password}
            result = api_request("/api/v1/auth/login", method="POST", data=data)
            
            if result:
                st.session_state.token = result['access_token']
                st.success("Login successful!")
                st.rerun()
    
    with tab2:
        st.subheader("Create new account")
        username = st.text_input("Username", key="reg_username")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        
        if st.button("Register"):
            data = {"username": username, "email": email, "password": password}
            result = api_request("/api/v1/auth/register", method="POST", data=data)
            
            if result:
                st.success("Registration successful! Please login.")


def main_app():
    """Main application after login"""
    
    # Initialize page in session state
    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🎬 Movie Recommender")
        st.session_state.page = st.radio("Navigation", 
            ["Home", "Recommendations", "Watchlist", "Search"],
            index=["Home", "Recommendations", "Watchlist", "Search"].index(st.session_state.page)
        )
        
        st.divider()
        
        if st.button("🚪 Logout"):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.page = "Home"
            st.rerun()
    
    page = st.session_state.page
    
    # Show rating dialog if movie selected
    if 'rating_movie' in st.session_state and st.session_state.rating_movie:
        show_rating_dialog()
        return
    
    # Home Page
    if page == "Home":
        st.title("🏠 Popular Movies")
        st.write("Discover trending and highly-rated movies")
        
        movies = api_request("/api/v1/recommendations/popular")
        
        if movies:
            for movie in movies[:10]:  # Show top 10
                display_movie_card(movie)
        else:
            st.warning("Unable to load movies. Make sure the backend is running.")
    
    # Recommendations Page
    elif page == "Recommendations":
        st.title("🎯 Personalized Recommendations")
        
        similar_movie_id = st.session_state.get('similar_movie_id')
        
        if similar_movie_id:
            st.write("Movies similar to your selection")
            if st.button("← Back to All Recommendations"):
                st.session_state.similar_movie_id = None
                st.rerun()
            movies = api_request(f"/api/v1/recommendations?movie_id={similar_movie_id}", auth=True)
        else:
            st.write("Recommendations based on your ratings and preferences")
            movies = api_request("/api/v1/recommendations", auth=True)
        
        if movies:
            for movie in movies:
                display_movie_card(movie)
        else:
            st.info("💡 Rate at least 5 movies to get personalized recommendations!")
            st.write("Go to Home or Search to find movies to rate.")
    
    # Watchlist Page
    elif page == "Watchlist":
        st.title("📝 My Watchlist")
        
        movies = api_request("/api/v1/watchlist/", auth=True)
        
        if movies:
            st.write(f"You have {len(movies)} movies in your watchlist")
            for movie in movies:
                col1, col2 = st.columns([4, 1])
                with col1:
                    display_movie_card(movie)
                with col2:
                    if st.button("🗑️ Remove", key=f"remove_{movie['id']}"):
                        result = api_request(f"/api/v1/watchlist/{movie['id']}", method="DELETE", auth=True)
                        if result is not None:
                            st.success("Removed!")
                            st.rerun()
        else:
            st.info("📭 Your watchlist is empty. Add some movies from Home or Search!")
    
    # Search Page
    elif page == "Search":
        st.title("🔍 Search Movies")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            query = st.text_input("Search for movies...", placeholder="Enter movie title")
        with col2:
            genre = st.selectbox("Genre", ["All", "Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller"])
        
        if query:
            genre_param = "" if genre == "All" else f"&genre={genre}"
            movies = api_request(f"/api/v1/movies/search/?q={query}{genre_param}")
            
            if movies:
                st.write(f"Found {len(movies)} movies")
                for movie in movies:
                    display_movie_card(movie)
            else:
                st.info("No movies found. Try a different search term.")
        else:
            st.info("👆 Enter a movie title to search")


# Main app logic
if st.session_state.token:
    main_app()
else:
    login_page()
