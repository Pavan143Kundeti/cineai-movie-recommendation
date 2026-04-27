import streamlit as st
import requests
import os

st.set_page_config(
    page_title="CineAI – Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

ALL_GENRES = [
    "Action","Adventure","Animation","Comedy","Crime",
    "Documentary","Drama","Family","Fantasy","History",
    "Horror","Music","Mystery","Romance","Science Fiction",
    "Thriller","War","Western",
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, .stApp, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #f8f9fa !important;
    color: #1a1a2e !important;
}
.stApp { background-color: #f8f9fa !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.2rem 2rem 2rem !important; max-width: 1200px !important; }

/* ── Sidebar wider ── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 2px solid #e2e8f0 !important;
    min-width: 230px !important;
}
[data-testid="stSidebar"] > div { min-width: 230px !important; }
[data-testid="stSidebar"] * { color: #1e293b !important; }
[data-testid="stSidebar"] .stMarkdown p { color: #475569 !important; }

/* NUKE all red from sidebar buttons in every state */
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] .stButton > button:focus,
[data-testid="stSidebar"] .stButton > button:active,
[data-testid="stSidebar"] .stButton > button:focus-visible,
[data-testid="stSidebar"] .stButton > button:focus-within {
    outline: none !important;
    box-shadow: none !important;
    border-color: #e2e8f0 !important;
}

/* Sidebar nav buttons */
[data-testid="stSidebar"] .stButton > button {
    background: #f1f5f9 !important;
    color: #1e293b !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 0.6rem 1rem !important;
    text-align: left !important;
    transition: all 0.15s !important;
    width: 100% !important;
    margin-bottom: 4px !important;
    white-space: nowrap !important;
    overflow: visible !important;
    min-height: 42px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #2563eb !important;
    color: #ffffff !important;
    border-color: #2563eb !important;
    cursor: pointer !important;
}

/* ── Main action buttons ── */
section[data-testid="stMain"] .stButton > button {
    background: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    padding: 0.4rem 0.5rem !important;
    transition: background 0.15s !important;
    width: 100% !important;
}
section[data-testid="stMain"] .stButton > button:hover {
    background: #1d4ed8 !important;
}

/* ── Form submit ── */
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.7rem 1rem !important;
    width: 100% !important;
    transition: all 0.15s !important;
    box-shadow: 0 4px 15px rgba(37,99,235,0.3) !important;
}
.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.4) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input {
    background: #ffffff !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #1a1a2e !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 0.9rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
    outline: none !important;
}
.stTextInput label { color: #64748b !important; font-size: 0.85rem !important; font-weight: 600 !important; }

.stTextArea textarea {
    background: #ffffff !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #1a1a2e !important;
}
.stTextArea textarea:focus { border-color: #2563eb !important; }
.stTextArea label { color: #64748b !important; font-size: 0.85rem !important; font-weight: 600 !important; }

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #ffffff !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #1a1a2e !important;
}
.stSelectbox label { color: #64748b !important; font-size: 0.85rem !important; }

/* ── Number input ── */
.stNumberInput input {
    background: #ffffff !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #1a1a2e !important;
}

/* ── Multiselect ── */
.stMultiSelect > div > div {
    background: #ffffff !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #1a1a2e !important;
}
.stMultiSelect label { color: #64748b !important; font-size: 0.85rem !important; font-weight: 600 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff !important;
    border-radius: 12px !important;
    padding: 5px !important;
    gap: 4px !important;
    border: 2px solid #e2e8f0 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #94a3b8 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 2rem !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #1a1a2e !important; background: #f1f5f9 !important; }
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: #fff !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.3) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #ffffff !important;
    border-radius: 0 0 12px 12px !important;
    padding: 1.8rem !important;
    border: 2px solid #e2e8f0 !important;
    border-top: none !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
}

/* ── Slider ── */
.stSlider label { color: #64748b !important; font-weight: 600 !important; }

/* ── Movie card ── */
.movie-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    margin-bottom: 0.9rem;
    overflow: hidden;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.movie-card:hover {
    border-color: #2563eb;
    box-shadow: 0 8px 25px rgba(37,99,235,0.12);
    transform: translateY(-2px);
}
.mc-inner { display: flex; }
.mc-poster {
    flex: 0 0 110px;
    background: #f1f5f9;
    border-radius: 14px 0 0 14px;
    overflow: hidden;
}
.mc-poster img { width: 110px; height: 165px; object-fit: cover; display: block; }
.mc-placeholder {
    width: 110px; height: 165px;
    background: linear-gradient(135deg, #1a1a2e, #0f3460);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center; gap: 4px;
}
.mc-placeholder-icon { font-size: 2rem; }
.mc-placeholder-text { font-size: 0.6rem; color: #94a3b8; text-align: center; padding: 0 6px; }
.mc-body { flex: 1; padding: 0.85rem 1.1rem; }
.mc-title { font-size: 1rem; font-weight: 700; color: #1a1a2e; margin: 0 0 0.4rem; line-height: 1.3; }
.mc-meta { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-bottom: 0.4rem; align-items: center; }
.badge { background: #f1f5f9; border-radius: 5px; padding: 2px 8px; font-size: 0.7rem; color: #64748b; font-weight: 500; }
.badge-star { background: #fef3c7; color: #d97706 !important; font-weight: 700; border: 1px solid #fde68a; }
.badge-genre { background: #eff6ff; color: #3b82f6 !important; border: 1px solid #bfdbfe; }
.mc-sub { font-size: 0.75rem; color: #94a3b8; margin-top: 0.2rem; }
.mc-overview { font-size: 0.78rem; color: #64748b; line-height: 1.5; margin-top: 0.3rem;
    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 18px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 8px 30px rgba(26,26,46,0.2);
}
.hero h1 { font-size: 2.8rem; font-weight: 800; color: #fff; margin: 0; letter-spacing: -1px; }
.hero h1 span { color: #2563eb; }
.hero p { color: #94a3b8; font-size: 1rem; margin-top: 0.5rem; }

/* ── Section header ── */
.sec-hdr {
    font-size: 1.25rem; font-weight: 700; color: #1a1a2e;
    margin: 0 0 1rem; padding-left: 0.8rem;
    border-left: 4px solid #2563eb;
}
/* ── Stat card ── */
.stat-card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 1.1rem; text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    transition: transform 0.2s;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.1); }
.stat-num { font-size: 1.5rem; font-weight: 800; color: #2563eb; }
.stat-lbl { font-size: 0.72rem; color: #94a3b8; margin-top: 0.2rem; font-weight: 500; }

/* ── Info / warn ── */
.info-box {
    background: #f0fdf4; border: 1px solid #bbf7d0;
    border-radius: 10px; padding: 0.8rem 1rem; color: #166534; font-size: 0.85rem;
}
.warn-box {
    background: #fff7ed; border: 1px solid #fed7aa;
    border-radius: 10px; padding: 0.8rem 1rem; color: #9a3412; font-size: 0.85rem;
}

/* ── Divider ── */
hr { border-color: #e2e8f0 !important; margin: 0.4rem 0 !important; }

/* ── Movie of the Day banner ── */
.motd {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f3460 100%);
    border-radius: 18px; padding: 0; margin-bottom: 1.5rem;
    overflow: hidden; position: relative;
    box-shadow: 0 10px 40px rgba(15,23,42,0.3);
    display: flex; min-height: 220px;
}
.motd-poster { flex: 0 0 150px; }
.motd-poster img { width: 150px; height: 220px; object-fit: cover; display: block; }
.motd-body { flex: 1; padding: 1.5rem 1.8rem; display: flex; flex-direction: column; justify-content: center; }
.motd-label { font-size: 0.7rem; font-weight: 700; color: #f59e0b; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0.4rem; }
.motd-title { font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 0 0 0.5rem; line-height: 1.2; }
.motd-meta { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.7rem; }
.motd-overview { font-size: 0.85rem; color: #94a3b8; line-height: 1.5;
    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

/* ── Mood buttons ── */
.mood-grid { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-bottom: 1.2rem; }
.mood-btn {
    background: #ffffff; border: 2px solid #e2e8f0; border-radius: 50px;
    padding: 0.5rem 1.2rem; font-size: 0.88rem; font-weight: 600;
    color: #1e293b; cursor: pointer; transition: all 0.15s;
    display: inline-flex; align-items: center; gap: 0.4rem;
}
.mood-btn:hover, .mood-btn.active {
    background: #2563eb; border-color: #2563eb; color: #fff;
}

/* ── Dashboard stats ── */
.dash-card {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    border-radius: 14px; padding: 1.2rem; text-align: center; color: white;
    box-shadow: 0 4px 15px rgba(37,99,235,0.3);
}
.dash-num { font-size: 2rem; font-weight: 800; color: #fff; }
.dash-lbl { font-size: 0.75rem; color: rgba(255,255,255,0.75); margin-top: 0.2rem; }

/* ── Detail page ── */
.detail-hero {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border-radius: 16px; padding: 2rem; margin-bottom: 1.5rem;
    display: flex; gap: 2rem;
}
.detail-poster img { width: 180px; height: 270px; object-fit: cover; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.4); }
.detail-info { flex: 1; }
.detail-title { font-size: 2rem; font-weight: 800; color: #fff; margin: 0 0 0.5rem; }
.detail-tagline { font-size: 0.9rem; color: #94a3b8; font-style: italic; margin-bottom: 0.8rem; }
.detail-overview { font-size: 0.9rem; color: #cbd5e1; line-height: 1.6; }

/* ── Netflix-style genre row ── */
.genre-row { margin-bottom: 2rem; }
.genre-row-title {
    font-size: 1.1rem; font-weight: 700; color: #1e293b;
    margin-bottom: 0.7rem; padding-left: 0.5rem;
    border-left: 3px solid #2563eb;
    display: flex; align-items: center; gap: 0.4rem;
}
.poster-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.7rem;
}
.poster-card {
    background: #fff; border: 1px solid #e2e8f0;
    border-radius: 10px; overflow: hidden;
    transition: all 0.2s ease;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    cursor: pointer;
}
.poster-card:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 10px 25px rgba(37,99,235,0.18);
    border-color: #2563eb;
}
.poster-card img {
    width: 100%; aspect-ratio: 2/3;
    object-fit: cover; display: block;
}
.poster-card-placeholder {
    width: 100%; aspect-ratio: 2/3;
    background: linear-gradient(135deg, #1e293b, #0f3460);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center; gap: 4px;
}
.poster-card-body {
    padding: 0.5rem 0.6rem 0.4rem;
}
.poster-card-title {
    font-size: 0.75rem; font-weight: 700; color: #1e293b;
    line-height: 1.3; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis;
}
.poster-card-meta {
    font-size: 0.65rem; color: #94a3b8; margin-top: 2px;
}

/* ── Autocomplete ── */
.autocomplete-item {
    padding: 0.5rem 0.8rem; cursor: pointer; border-bottom: 1px solid #f1f5f9;
    font-size: 0.88rem; color: #1e293b; background: #fff;
}
.autocomplete-item:hover { background: #eff6ff; color: #2563eb; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2563eb; }

/* Nuclear option — kill ALL red/pink borders and outlines site-wide */
* {
    --primary-color: #2563eb !important;
}
button:focus, button:active, button:focus-visible,
button:focus-within, button:focus-within * {
    outline: none !important;
    box-shadow: none !important;
    border-color: #e2e8f0 !important;
}
/* Streamlit injects a red border via inline style on active buttons — override */
[data-testid="stSidebar"] button[kind="secondary"],
[data-testid="stSidebar"] button[kind="secondary"]:focus,
[data-testid="stSidebar"] button[kind="secondary"]:active,
[data-testid="stSidebar"] button[kind="secondary"]:focus-visible {
    border: 1px solid #e2e8f0 !important;
    outline: none !important;
    box-shadow: none !important;
}
/* Override Streamlit's red primary color variable */
:root {
    --primary-color: #2563eb !important;
    --secondary-background-color: #f8f9fa !important;
}
/* Any element that gets a red border on click */
[data-testid="stSidebar"] .stButton > button:focus,
[data-testid="stSidebar"] .stButton > button:active {
    border: 1px solid #e2e8f0 !important;
    box-shadow: none !important;
    outline: none !important;
    background: #f1f5f9 !important;
    color: #1e293b !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
for k, v in [("token",None),("user",None),("page","Home"),
              ("rating_movie",None),("similar_movie_id",None),("explain_movie",None),
              ("selected_movie",None),("mood",None),("home_page",0),("home_genre","All Genres"),
              ("search_page",0)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── API ────────────────────────────────────────────────────────────────────────
def api(endpoint, method="GET", data=None, auth=False, silent=False):
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {st.session_state.token}"} if (auth and st.session_state.token) else {}
    try:
        if   method == "GET":    r = requests.get(url, headers=headers, timeout=8)
        elif method == "POST":   r = requests.post(url, json=data, headers=headers, timeout=8)
        elif method == "DELETE": r = requests.delete(url, headers=headers, timeout=8)
        else: return None
        if r.status_code in (200,201): return r.json() if r.text else {}
        if r.status_code == 204: return {}
        if not silent:
            try: st.error(r.json().get("detail", f"Error {r.status_code}"))
            except: st.error(f"Error {r.status_code}")
        return None
    except requests.exceptions.ConnectionError:
        if not silent: st.error("⚠️ Cannot connect to backend on port 8000.")
        return None
    except Exception as e:
        if not silent: st.error(f"Request failed: {e}")
        return None

# ── Cached data fetchers (speed fix) ──────────────────────────────────────────
@st.cache_data(ttl=600, show_spinner=False)
def cached_popular(genre="", skip=0, limit=20):
    params = f"?skip={skip}&limit={limit}"
    if genre: params += f"&genre={genre}"
    try:
        r = requests.get(f"{API_BASE_URL}/api/v1/recommendations/popular{params}", timeout=8)
        return r.json() if r.status_code == 200 else []
    except: return []

@st.cache_data(ttl=600, show_spinner=False)
def cached_popular_count(genre=""):
    # Fetch a large batch to get total — backend returns up to 4800
    params = "?skip=0&limit=1&count_only=true"
    if genre: params += f"&genre={genre}"
    try:
        # Use a high limit to estimate total pages
        r = requests.get(f"{API_BASE_URL}/api/v1/recommendations/popular?skip=0&limit=4800{'&genre='+genre if genre else ''}", timeout=15)
        return len(r.json()) if r.status_code == 200 else 0
    except: return 0

@st.cache_data(ttl=300, show_spinner=False)
def cached_search(q, genre, min_r, skip=0, limit=20):
    params = [f"skip={skip}", f"limit={limit}"]
    if q: params.append(f"q={q}")
    if genre: params.append(f"genre={genre}")
    if min_r > 0: params.append(f"min_rating={min_r}")
    try:
        r = requests.get(f"{API_BASE_URL}/api/v1/movies/search/?{'&'.join(params)}", timeout=8)
        return r.json() if r.status_code == 200 else []
    except: return []

@st.cache_data(ttl=120, show_spinner=False)
def cached_movie(movie_id):
    r = requests.get(f"{API_BASE_URL}/api/v1/movies/{movie_id}", timeout=8)
    return r.json() if r.status_code == 200 else None

@st.cache_data(ttl=300, show_spinner=False)
def cached_trending():
    try:
        r = requests.get(f"{API_BASE_URL}/api/v1/recommendations/trending", timeout=8)
        return r.json() if r.status_code == 200 else []
    except: return []

@st.cache_data(ttl=60, show_spinner=False)
def cached_mood(mood, token=""):
    try:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        r = requests.get(f"{API_BASE_URL}/api/v1/recommendations/mood/{mood}",
                         headers=headers, timeout=8)
        return r.json() if r.status_code == 200 else []
    except: return []

@st.cache_data(ttl=600, show_spinner=False)
def cached_genre_row(genre, limit=10):
    import json
    try:
        r = requests.get(
            f"{API_BASE_URL}/api/v1/recommendations/popular?limit={limit}&genre={genre}",
            timeout=8)
        return r.json() if r.status_code == 200 else []
    except: return []

@st.cache_data(ttl=60, show_spinner=False)
def cached_autocomplete(q):
    if len(q) < 2: return []
    try:
        r = requests.get(f"{API_BASE_URL}/api/v1/movies/search/?q={q}&limit=6", timeout=4)
        return r.json() if r.status_code == 200 else []
    except: return []

# ── Helpers ────────────────────────────────────────────────────────────────────
def get_poster_html(movie):
    path  = movie.get("poster_path","")
    title = movie.get("title","?")[:14]
    if path and path.startswith("/"):
        return f'<img src="https://image.tmdb.org/t/p/w185{path}" alt="{title}" loading="lazy"/>'
    initials = "".join(w[0].upper() for w in title.split()[:2])
    return f'<div class="mc-placeholder"><div class="mc-placeholder-icon">🎬</div><div style="color:#2563eb;font-weight:700;font-size:1rem;">{initials}</div><div class="mc-placeholder-text">{title}</div></div>'

def star_str(s):
    n = int(round(s/2)); return "★"*n + "☆"*(5-n)

# ── Movie card ─────────────────────────────────────────────────────────────────
def movie_card(movie, show_remove=False, show_explain=False):
    mid      = movie["id"]
    title    = movie.get("title","Unknown")
    genres   = movie.get("genres") or []
    if isinstance(genres, str): genres = [genres]
    rating   = movie.get("vote_average") or 0
    year     = (movie.get("release_date") or "")[:4]
    runtime  = movie.get("runtime")
    director = movie.get("director","")
    cast     = movie.get("cast") or []
    overview = movie.get("overview","")

    genre_html = "".join(f'<span class="badge badge-genre">{g}</span>' for g in genres[:3])
    star_html  = f'<span class="badge badge-star">⭐ {rating:.1f}</span>' if rating else ""
    year_html  = f'<span class="badge">{year}</span>' if year else ""
    rt_html    = f'<span class="badge">{runtime}m</span>' if runtime else ""
    cast_str   = ", ".join(cast[:3]) if cast else ""

    st.markdown(f"""
    <div class="movie-card">
      <div class="mc-inner">
        <div class="mc-poster">{get_poster_html(movie)}</div>
        <div class="mc-body">
          <div class="mc-title">{title}</div>
          <div class="mc-meta">{star_html}{year_html}{rt_html}{genre_html}</div>
          {"<div class='mc-sub'>🎬 " + director + "</div>" if director else ""}
          {"<div class='mc-sub'>👥 " + cast_str + "</div>" if cast_str else ""}
          <div class="mc-overview">{overview}</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    ncols = sum([1, 1, 1, 1, show_explain, show_remove])  # added Details
    cols  = st.columns(ncols)
    idx   = 0
    with cols[idx]:
        if st.button("📄 Details", key=f"det_{mid}"):
            st.session_state.selected_movie = movie
            st.session_state.page = "Detail"
            st.rerun()
    idx+=1
    with cols[idx]: 
        if st.button("➕ Watchlist", key=f"wl_{mid}"):
            if not st.session_state.token: st.warning("Login first")
            else:
                res = api(f"/api/v1/watchlist/{mid}", "POST", auth=True, silent=True)
                if res is not None: st.success("Added!"); st.rerun()
    idx+=1
    with cols[idx]:
        if st.button("⭐ Rate", key=f"rt_{mid}"):
            if not st.session_state.token: st.warning("Login first")
            else: st.session_state.rating_movie = movie; st.rerun()
    idx+=1
    with cols[idx]:
        if st.button("🎯 Similar", key=f"sim_{mid}"):
            st.session_state.similar_movie_id = mid
            st.session_state.page = "Recommendations"
            st.rerun()
    idx+=1
    if show_explain:
        with cols[idx]:
            if st.button("💡 Why?", key=f"exp_{mid}"):
                st.session_state.explain_movie = mid; st.rerun()
        idx+=1
    if show_remove:
        with cols[idx]:
            if st.button("🗑 Remove", key=f"rm_{mid}"):
                res = api(f"/api/v1/watchlist/{mid}", "DELETE", auth=True)
                if res is not None: st.success("Removed!"); st.rerun()
    st.markdown("<hr/>", unsafe_allow_html=True)

# ── Rating dialog ──────────────────────────────────────────────────────────────
def rating_dialog():
    movie = st.session_state.rating_movie
    if not movie: return
    st.markdown(f"<div class='sec-hdr'>⭐ Rate: {movie['title']}</div>", unsafe_allow_html=True)
    with st.form("rating_form"):
        rating = st.slider("Your Rating (1–10)", 1.0, 10.0, 7.0, 0.5)
        st.markdown(f"**{star_str(rating)}  {rating}/10**")
        review = st.text_area("Review (optional)", max_chars=500, height=80)
        c1,c2  = st.columns(2)
        with c1: submit = st.form_submit_button("✅ Submit", use_container_width=True)
        with c2: cancel = st.form_submit_button("✖ Cancel", use_container_width=True)
    if submit:
        res = api("/api/v1/ratings/", "POST", auth=True,
                  data={"movie_id": movie["id"], "rating": rating, "review_text": review or None})
        if res: st.success("Rating saved!"); st.session_state.rating_movie = None; st.rerun()
    if cancel: st.session_state.rating_movie = None; st.rerun()

# ── Explain dialog ─────────────────────────────────────────────────────────────
def explain_dialog():
    mid  = st.session_state.explain_movie
    data = api(f"/api/v1/recommendations/explain/{mid}", auth=True)
    if data:
        st.markdown(f"<div class='sec-hdr'>💡 Why: {data.get('movie_title','')}</div>", unsafe_allow_html=True)
        st.info(f"Algorithm: {data.get('algorithm','')}")
        for r in data.get("reasons",[]): st.markdown(f"- {r}")
    if st.button("← Back"): st.session_state.explain_movie = None; st.rerun()

# ── Auth page ──────────────────────────────────────────────────────────────────
def auth_page():
    st.markdown("""
    <div class="hero">
      <h1>🎬 <span>CineAI</span></h1>
      <p>Personalised movie recommendations powered by advanced machine learning</p>
    </div>""", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        tab1, tab2 = st.tabs(["  🔑  Login  ", "  📝  Register  "])
        with tab1:
            st.markdown("<br/>", unsafe_allow_html=True)
            with st.form("login_form"):
                email    = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="Your password")
                st.markdown("<br/>", unsafe_allow_html=True)
                submit   = st.form_submit_button("Login →", use_container_width=True)
            if submit:
                if not email or not password: st.error("Fill in all fields.")
                else:
                    res = api("/api/v1/auth/login", "POST", data={"email": email, "password": password})
                    if res:
                        st.session_state.token = res["access_token"]
                        me = api("/api/v1/users/me", auth=True)
                        if me: st.session_state.user = me
                        st.rerun()

        with tab2:
            st.markdown("<br/>", unsafe_allow_html=True)
            with st.form("register_form"):
                username = st.text_input("Username", placeholder="e.g. pavanfan99")
                email    = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="Min 6 characters")
                st.markdown("<br/>", unsafe_allow_html=True)
                submit   = st.form_submit_button("Create Account →", use_container_width=True)
            if submit:
                if not username or not email or not password: st.error("Fill in all fields.")
                else:
                    res = api("/api/v1/auth/register", "POST",
                              data={"username": username, "email": email, "password": password})
                    if res: st.success("✅ Account created! Go to Login tab.")

    st.markdown("<br/>", unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    for col,(icon,num,lbl) in zip([c1,c2,c3,c4],[
        ("🤖","SVD","Matrix Factorization"),
        ("📊","TF-IDF","Content-Based Filtering"),
        ("👥","Pearson","Collaborative Filtering"),
        ("🎬","4800+","Movies in Database"),
    ]):
        with col:
            st.markdown(f"""<div class="stat-card">
              <div style="font-size:1.6rem;margin-bottom:4px">{icon}</div>
              <div class="stat-num">{num}</div>
              <div class="stat-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    # Team credits on login page
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; padding: 1.2rem; background:#ffffff;
                border:1px solid #e2e8f0; border-radius:14px;
                box-shadow:0 2px 8px rgba(0,0,0,0.05);">
      <div style="font-size:0.72rem; color:#94a3b8; letter-spacing:1.5px;
                  text-transform:uppercase; font-weight:600; margin-bottom:0.6rem;">
        Final Year Project — Team
      </div>
      <div style="display:flex; justify-content:center; gap:1.5rem; flex-wrap:wrap;">
        <span style="background:#eff6ff; color:#2563eb; border:1px solid #bfdbfe;
                     border-radius:20px; padding:0.3rem 0.9rem; font-size:0.82rem; font-weight:600;">
          👨‍💻 Pavan
        </span>
        <span style="background:#eff6ff; color:#2563eb; border:1px solid #bfdbfe;
                     border-radius:20px; padding:0.3rem 0.9rem; font-size:0.82rem; font-weight:600;">
          👨‍💻 Yousuf
        </span>
        <span style="background:#eff6ff; color:#2563eb; border:1px solid #bfdbfe;
                     border-radius:20px; padding:0.3rem 0.9rem; font-size:0.82rem; font-weight:600;">
          👨‍💻 Arif
        </span>
        <span style="background:#eff6ff; color:#2563eb; border:1px solid #bfdbfe;
                     border-radius:20px; padding:0.3rem 0.9rem; font-size:0.82rem; font-weight:600;">
          👨‍💻 Dhanush
        </span>
      </div>
      <div style="font-size:0.7rem; color:#cbd5e1; margin-top:0.6rem;">
        B.Tech Final Year Project · 2025
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:1.5rem 0 0.8rem;text-align:center;">
          <div style="font-size:2.2rem;">🎬</div>
          <div style="font-size:1.4rem;font-weight:800;color:#1e293b;letter-spacing:-0.5px;">CineAI</div>
          <div style="font-size:0.7rem;color:#94a3b8;margin-top:3px;">ML-Powered Recommendations</div>
        </div>""", unsafe_allow_html=True)

        if st.session_state.user:
            uname = st.session_state.user.get("username","User")
            st.markdown(f"""
            <div style="background:#f8fafc;border:1px solid #e2e8f0;
                        border-radius:10px;padding:0.6rem 0.9rem;margin:0.3rem 0 0.8rem;">
              <div style="font-size:0.68rem;color:#94a3b8;">Logged in as</div>
              <div style="font-weight:700;color:#2563eb;font-size:0.9rem;">👤 {uname}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        pages = [("🏠","Home"),("📈","Trending"),("�","Mood"),("�🎯","Recommendations"),
                 ("🔍","Search"),("📋","Watchlist"),("⭐","My Ratings"),
                 ("📊","Dashboard"),("⚙️","Preferences")]
        for icon,page in pages:
            label = f"{'▶  ' if st.session_state.page==page else '    '}{icon}  {page}"
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                st.session_state.page = page
                st.session_state.rating_movie  = None
                st.session_state.explain_movie = None
                st.rerun()

        st.markdown("---")
        if st.button("🚪  Logout", use_container_width=True):
            for k in ["token","user","rating_movie","similar_movie_id","explain_movie"]:
                st.session_state[k] = None
            st.session_state.page = "Home"
            st.rerun()

        st.markdown("""
        <div style="margin-top:1.5rem;font-size:0.65rem;color:#94a3b8;text-align:center;line-height:1.7;">
          SVD · TF-IDF · Pearson CF<br/>FastAPI · MySQL · Streamlit
        </div>
        <div style="margin-top:0.8rem;text-align:center;">
          <div style="font-size:0.6rem;color:#cbd5e1;margin-bottom:0.4rem;letter-spacing:1px;text-transform:uppercase;">Team</div>
          <div style="font-size:0.72rem;color:#475569;font-weight:600;line-height:1.9;">
            👨‍💻 Pavan &nbsp;·&nbsp; 👨‍💻 Yousuf<br/>
            👨‍💻 Arif &nbsp;·&nbsp; 👨‍💻 Dhanush
          </div>
          <div style="font-size:0.6rem;color:#cbd5e1;margin-top:0.3rem;">B.Tech Final Year · 2025</div>
        </div>""", unsafe_allow_html=True)

# ── Pages ──────────────────────────────────────────────────────────────────────
def render_genre_row(label, icon, movies):
    """Render a Netflix-style horizontal poster row"""
    if not movies: return
    # Make a safe key prefix from the label
    key_prefix = label.replace(" ", "_").replace("/", "_")
    st.markdown(f"<div class='genre-row-title'>{icon} {label}</div>", unsafe_allow_html=True)
    cols = st.columns(5)
    for i, m in enumerate(movies[:5]):
        with cols[i]:
            path   = m.get("poster_path","")
            title  = m.get("title","")
            rating = m.get("vote_average",0)
            year   = (m.get("release_date",""))[:4]
            src    = f"https://image.tmdb.org/t/p/w185{path}" if path else ""
            initials = "".join(w[0].upper() for w in title.split()[:2])

            img_html = (f'<img src="{src}" alt="{title}"/>'
                        if src else
                        f'<div class="poster-card-placeholder">'
                        f'<div style="font-size:2rem;">🎬</div>'
                        f'<div style="color:#2563eb;font-weight:700;">{initials}</div>'
                        f'</div>')

            st.markdown(f"""
            <div class="poster-card">
              {img_html}
              <div class="poster-card-body">
                <div class="poster-card-title">{title[:22]}</div>
                <div class="poster-card-meta">⭐ {rating:.1f} · {year}</div>
              </div>
            </div>""", unsafe_allow_html=True)

            if st.button("Details", key=f"gr_{key_prefix}_{i}_{m['id']}", use_container_width=True):
                st.session_state.selected_movie = m
                st.session_state.page = "Detail"; st.rerun()
    st.markdown("<br/>", unsafe_allow_html=True)


def page_home():
    # ── Movie of the Day ──
    section_motd()

    # ── Stats row ──
    c1,c2,c3,c4 = st.columns(4)
    for col,(num,lbl) in zip([c1,c2,c3,c4],[
        ("4800+","Movies"),("3","ML Algorithms"),("15+","API Endpoints"),("Hybrid","Engine")
    ]):
        with col:
            st.markdown(f'<div class="stat-card"><div class="stat-num">{num}</div><div class="stat-lbl">{lbl}</div></div>',
                        unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Trending row ──
    trending = cached_trending()
    render_genre_row("Trending This Week", "🔥", trending)

    # ── Genre rows (Netflix style) ──
    genre_rows = [
        ("Top Action",        "💥", "Action"),
        ("Top Comedy",        "😂", "Comedy"),
        ("Top Drama",         "🎭", "Drama"),
        ("Top Sci-Fi",        "🚀", "Science Fiction"),
        ("Top Thriller",      "😱", "Thriller"),
        ("Top Animation",     "🎨", "Animation"),
        ("Top Romance",       "❤️", "Romance"),
        ("Top Horror",        "👻", "Horror"),
    ]
    for label, icon, genre in genre_rows:
        movies = cached_genre_row(genre, 10)
        render_genre_row(label, icon, movies)

    # ── Browse All (paginated) ──
    st.markdown("<div class='sec-hdr'>🎬 Browse All Movies</div>", unsafe_allow_html=True)
    cg, cl = st.columns([3,1])
    with cg:
        genre_filter = st.selectbox("Genre", ["All Genres"]+ALL_GENRES, label_visibility="collapsed")
    with cl:
        page_size = st.selectbox("Show", [10,20,30], index=0, label_visibility="collapsed")

    if genre_filter != st.session_state.home_genre:
        st.session_state.home_page  = 0
        st.session_state.home_genre = genre_filter

    g    = "" if genre_filter == "All Genres" else genre_filter
    skip = st.session_state.home_page * page_size
    movies = cached_popular(g, skip, page_size)
    total  = cached_popular_count(g)

    if movies:
        total_pages = max(1, (total + page_size - 1) // page_size)
        st.markdown(f"<div style='color:#64748b;font-size:0.82rem;margin-bottom:0.8rem;'>Showing {skip+1}–{min(skip+page_size,total)} of {total} movies</div>",
                    unsafe_allow_html=True)
        for m in movies: movie_card(m)
        cp, ci, cn = st.columns([1,2,1])
        with cp:
            if st.session_state.home_page > 0:
                if st.button("← Previous", use_container_width=True):
                    st.session_state.home_page -= 1; st.rerun()
        with ci:
            st.markdown(f"<div style='text-align:center;color:#64748b;padding-top:0.5rem;font-size:0.85rem;font-weight:600;'>Page {st.session_state.home_page+1} of {total_pages}</div>",
                        unsafe_allow_html=True)
        with cn:
            if skip + page_size < total:
                if st.button("Next →", use_container_width=True):
                    st.session_state.home_page += 1; st.rerun()
    else:
        st.markdown("<div class='warn-box'>⚠️ Could not load movies.</div>", unsafe_allow_html=True)


def page_recommendations():
    if st.session_state.explain_movie:
        explain_dialog(); return

    similar_id = st.session_state.get("similar_movie_id")
    if similar_id:
        st.markdown("<div class='sec-hdr'>🎯 Similar Movies</div>", unsafe_allow_html=True)
        if st.button("← Back to Recommendations"):
            st.session_state.similar_movie_id = None; st.rerun()
        with st.spinner("Finding similar movies..."):
            movies = api(f"/api/v1/recommendations/?movie_id={similar_id}", auth=True) or []
    else:
        st.markdown("<div class='sec-hdr'>🎯 Personalised For You</div>", unsafe_allow_html=True)
        st.markdown("""<div class="info-box">
          💡 Powered by <strong>Hybrid ML</strong>: SVD Matrix Factorization + TF-IDF Content-Based Filtering.
          Rate more movies to improve accuracy.
        </div><br/>""", unsafe_allow_html=True)
        with st.spinner("Loading recommendations..."):
            movies = api("/api/v1/recommendations/", auth=True) or []

    if movies:
        for m in movies: movie_card(m, show_explain=True)
    else:
        st.markdown("""<div class="warn-box">
          🎬 Rate at least 5 movies to unlock personalised recommendations!
        </div>""", unsafe_allow_html=True)


def page_search():
    st.markdown("<div class='sec-hdr'>🔍 Search Movies</div>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([4,2,1])
    with c1: query = st.text_input("", placeholder="Search by title…", label_visibility="collapsed")
    with c2: genre = st.selectbox("", ["All Genres"]+ALL_GENRES, label_visibility="collapsed")
    with c3: min_r = st.number_input("Min ⭐", 0.0, 10.0, 0.0, 0.5, label_visibility="collapsed")

    # Feature 6: Autocomplete suggestions
    if query and len(query) >= 2:
        suggestions = cached_autocomplete(query)
        if suggestions:
            suggest_titles = [m["title"] for m in suggestions[:5]]
            st.markdown("<div style='font-size:0.78rem;color:#94a3b8;margin-bottom:0.3rem;'>Suggestions:</div>",
                        unsafe_allow_html=True)
            scols = st.columns(len(suggest_titles))
            for sc, title in zip(scols, suggest_titles):
                with sc:
                    if st.button(title[:20], key=f"sug_{title}", use_container_width=True):
                        query = title

    g = "" if genre=="All Genres" else genre
    if query or g:
        if "search_page" not in st.session_state: st.session_state.search_page = 0
        page_size = 10
        skip = st.session_state.search_page * page_size
        with st.spinner("Searching..."):
            movies = cached_search(query, g, min_r, skip, page_size)
        if movies:
            st.markdown(f"<div style='color:#64748b;font-size:0.82rem;margin-bottom:0.8rem;'>{len(movies)} results on this page</div>",
                        unsafe_allow_html=True)
            for m in movies: movie_card(m)
            cp, ci, cn = st.columns([1,2,1])
            with cp:
                if st.session_state.search_page > 0:
                    if st.button("← Prev", use_container_width=True):
                        st.session_state.search_page -= 1; st.rerun()
            with ci:
                st.markdown(f"<div style='text-align:center;color:#64748b;padding-top:0.5rem;font-size:0.85rem;font-weight:600;'>Page {st.session_state.search_page+1}</div>",
                            unsafe_allow_html=True)
            with cn:
                if len(movies) == page_size:
                    if st.button("Next →", use_container_width=True):
                        st.session_state.search_page += 1; st.rerun()
        else:
            st.session_state.search_page = 0
            st.markdown("<div class='warn-box'>No movies found. Try a different search.</div>", unsafe_allow_html=True)
    else:
        if "search_page" in st.session_state: st.session_state.search_page = 0
        st.markdown("<div class='info-box'>👆 Type a title or pick a genre to search.</div>", unsafe_allow_html=True)


def page_watchlist():
    st.markdown("<div class='sec-hdr'>📋 My Watchlist</div>", unsafe_allow_html=True)
    with st.spinner("Loading watchlist..."):
        movies = api("/api/v1/watchlist/", auth=True) or []
    if movies:
        st.markdown(f"<div style='color:#94a3b8;font-size:0.82rem;margin-bottom:0.8rem;'>{len(movies)} saved</div>",
                    unsafe_allow_html=True)
        for m in movies: movie_card(m, show_remove=True)
    else:
        st.markdown("<div class='info-box'>📭 Watchlist empty. Add movies from Home or Search.</div>",
                    unsafe_allow_html=True)


def page_my_ratings():
    st.markdown("<div class='sec-hdr'>⭐ My Ratings</div>", unsafe_allow_html=True)
    with st.spinner("Loading ratings..."):
        ratings = api("/api/v1/ratings/my-ratings", auth=True) or []
    if ratings:
        st.markdown(f"<div style='color:#94a3b8;font-size:0.82rem;margin-bottom:0.8rem;'>Rated {len(ratings)} movies</div>",
                    unsafe_allow_html=True)
        for r in ratings:
            movie = cached_movie(r['movie_id'])
            if movie:
                c1,c2 = st.columns([5,1])
                with c1: movie_card(movie)
                with c2:
                    st.markdown(f"""<div class="stat-card" style="margin-top:0.5rem;">
                      <div class="stat-num" style="font-size:1.4rem;">{r['rating']}</div>
                      <div class="stat-lbl">{star_str(r['rating'])}</div>
                    </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='info-box'>🎬 No ratings yet. Rate movies to get personalised recommendations!</div>",
                    unsafe_allow_html=True)


def page_preferences():
    st.markdown("<div class='sec-hdr'>⚙️ Genre Preferences</div>", unsafe_allow_html=True)
    st.markdown("""<div class="info-box">
      Preferred genres get a <strong>+15% boost</strong>, disliked genres get a <strong>-30% penalty</strong> in your recommendations.
    </div><br/>""", unsafe_allow_html=True)
    current  = api("/api/v1/users/preferences", auth=True) or {}
    cur_pref = current.get("preferred_genres") or []
    cur_dis  = current.get("disliked_genres") or []
    with st.form("prefs_form"):
        preferred = st.multiselect("✅ Genres I love", ALL_GENRES, default=[g for g in cur_pref if g in ALL_GENRES])
        disliked  = st.multiselect("❌ Genres I dislike", ALL_GENRES, default=[g for g in cur_dis if g in ALL_GENRES])
        save = st.form_submit_button("💾 Save Preferences", use_container_width=True)
    if save:
        res = api("/api/v1/users/preferences", "POST", auth=True,
                  data={"preferred_genres": preferred, "disliked_genres": disliked})
        if res: st.success("✅ Preferences saved! Recommendations updated.")


# ── Feature 1: Movie Detail Page ──────────────────────────────────────────────
def page_detail():
    movie = st.session_state.selected_movie
    if not movie:
        st.session_state.page = "Home"; st.rerun(); return

    if st.button("← Back"):
        st.session_state.selected_movie = None
        st.session_state.page = "Home"; st.rerun()

    title    = movie.get("title","")
    overview = movie.get("overview","")
    genres   = movie.get("genres") or []
    rating   = movie.get("vote_average") or 0
    year     = (movie.get("release_date") or "")[:4]
    runtime  = movie.get("runtime","")
    director = movie.get("director","")
    cast     = movie.get("cast") or []
    path     = movie.get("poster_path","")

    poster_src = f"https://image.tmdb.org/t/p/w342{path}" if path else ""
    genre_html = "".join(f'<span class="badge badge-genre">{g}</span>' for g in genres)
    cast_html  = ", ".join(cast[:6]) if cast else "N/A"

    st.markdown(f"""
    <div class="detail-hero">
      <div class="detail-poster">
        {"<img src='" + poster_src + "' />" if poster_src else "<div style='width:180px;height:270px;background:#1e293b;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:3rem;'>🎬</div>"}
      </div>
      <div class="detail-info">
        <div class="detail-title">{title}</div>
        <div class="mc-meta" style="margin-bottom:0.8rem;">
          <span class="badge badge-star">⭐ {rating:.1f}/10</span>
          <span class="badge">{year}</span>
          {"<span class='badge'>" + str(runtime) + " min</span>" if runtime else ""}
          {genre_html}
        </div>
        {"<div style='color:#94a3b8;font-size:0.82rem;margin-bottom:0.5rem;'>🎬 Directed by <strong style=color:#e2e8f0>" + director + "</strong></div>" if director else ""}
        {"<div style='color:#94a3b8;font-size:0.82rem;margin-bottom:0.8rem;'>👥 " + cast_html + "</div>"}
        <div class="detail-overview">{overview}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # YouTube trailer embed
    st.markdown("<div class='sec-hdr'>🎬 Trailer</div>", unsafe_allow_html=True)
    trailer_query = f"{title} {year} official trailer"
    yt_search = f"https://www.youtube.com/results?search_query={trailer_query.replace(' ', '+')}"
    st.markdown(f"""
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.2rem;text-align:center;">
      <div style="font-size:1rem;color:#64748b;margin-bottom:0.8rem;">
        Click below to watch the official trailer on YouTube
      </div>
      <a href="{yt_search}" target="_blank" style="
        background:#ff0000;color:white;padding:0.6rem 1.5rem;
        border-radius:8px;text-decoration:none;font-weight:700;font-size:0.95rem;
        display:inline-flex;align-items:center;gap:0.5rem;">
        ▶ Watch Trailer on YouTube
      </a>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("➕ Add to Watchlist", use_container_width=True):
            if not st.session_state.token: st.warning("Login first")
            else:
                res = api(f"/api/v1/watchlist/{movie['id']}", "POST", auth=True, silent=True)
                if res is not None: st.success("Added to watchlist!")
    with c2:
        if st.button("⭐ Rate This Movie", use_container_width=True):
            st.session_state.rating_movie = movie; st.rerun()
    with c3:
        if st.button("🎯 Find Similar", use_container_width=True):
            st.session_state.similar_movie_id = movie["id"]
            st.session_state.page = "Recommendations"; st.rerun()


# ── Feature 2: Trending This Week ─────────────────────────────────────────────
def section_trending():
    st.markdown("<div class='sec-hdr'>📈 Trending This Week</div>", unsafe_allow_html=True)
    with st.spinner(""):
        movies = cached_trending()
    if movies:
        cols = st.columns(5)
        for i, m in enumerate(movies[:10]):
            with cols[i % 5]:
                path  = m.get("poster_path","")
                title = m.get("title","")[:20]
                rating= m.get("vote_average",0)
                src   = f"https://image.tmdb.org/t/p/w185{path}" if path else ""
                st.markdown(f"""
                <div class="movie-card" style="cursor:pointer;" onclick="">
                  {"<img src='" + src + "' style='width:100%;border-radius:10px 10px 0 0;height:160px;object-fit:cover;display:block;'/>" if src else "<div style='height:160px;background:#1e293b;border-radius:10px 10px 0 0;display:flex;align-items:center;justify-content:center;font-size:2rem;'>🎬</div>"}
                  <div style="padding:0.5rem 0.6rem;">
                    <div style="font-size:0.78rem;font-weight:700;color:#1e293b;line-height:1.3;">{title}</div>
                    <span class="badge badge-star" style="font-size:0.65rem;">⭐ {rating:.1f}</span>
                    <span class="badge badge-trend" style="font-size:0.6rem;">🔥 #{i+1}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
                if st.button("Details", key=f"tr_{m['id']}", use_container_width=True):
                    st.session_state.selected_movie = m
                    st.session_state.page = "Detail"; st.rerun()


# ── Feature 3: Mood-Based Recommendations ─────────────────────────────────────
def section_mood():
    st.markdown("<div class='sec-hdr'>🎭 I'm in the Mood for...</div>", unsafe_allow_html=True)
    moods = [
        ("💥","Action","action"),("😂","Comedy","comedy"),
        ("❤️","Feel-Good","feelgood"),("🧠","Mind-Bending","mindbending"),
        ("👻","Horror","horror"),("🏛️","Classic","classic"),
    ]
    cols = st.columns(len(moods))
    for col, (icon, label, key) in zip(cols, moods):
        with col:
            active = st.session_state.mood == key
            btn_style = "background:#2563eb!important;color:white!important;" if active else ""
            if st.button(f"{icon} {label}", key=f"mood_{key}", use_container_width=True):
                st.session_state.mood = None if active else key
                st.rerun()

    if st.session_state.mood:
        mood_label = next((l for _, l, k in moods if k == st.session_state.mood), "")
        st.markdown(f"<div style='color:#64748b;font-size:0.82rem;margin:0.5rem 0 0.8rem;'>Showing {mood_label} movies</div>",
                    unsafe_allow_html=True)
        with st.spinner(""):
            movies = cached_mood(st.session_state.mood, st.session_state.token or "")
        if movies:
            for m in movies[:6]: movie_card(m)


# ── Feature 4: User Dashboard ─────────────────────────────────────────────────
def section_dashboard():
    stats = api("/api/v1/users/stats", auth=True, silent=True)
    if not stats or stats.get("total_ratings", 0) == 0:
        st.markdown("""<div class="info-box">
          🎬 Rate some movies to see your personal dashboard!
        </div>""", unsafe_allow_html=True)
        return

    c1,c2,c3,c4 = st.columns(4)
    cards = [
        (str(stats["total_ratings"]), "Movies Rated"),
        (str(stats["avg_rating"]), "Avg Rating"),
        (stats["fav_genre"], "Fav Genre"),
        ("🏆", stats.get("top_movie","")[:15] + "…" if stats.get("top_movie") else "N/A"),
    ]
    for col,(num,lbl) in zip([c1,c2,c3,c4], cards):
        with col:
            st.markdown(f"""<div class="dash-card">
              <div class="dash-num">{num}</div>
              <div class="dash-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)


# ── Feature 5: Movie of the Day ───────────────────────────────────────────────
@st.cache_data(ttl=86400, show_spinner=False)
def get_movie_of_day():
    import datetime
    try:
        r = requests.get(f"{API_BASE_URL}/api/v1/recommendations/popular?skip=0&limit=100", timeout=8)
        movies = r.json() if r.status_code == 200 else []
        if not movies: return None
        idx = datetime.date.today().toordinal() % len(movies)
        return movies[idx]
    except: return None

def section_motd():
    movie = get_movie_of_day()
    if not movie: return
    path     = movie.get("poster_path","")
    title    = movie.get("title","")
    overview = movie.get("overview","")[:150] + "…"
    rating   = movie.get("vote_average",0)
    year     = (movie.get("release_date",""))[:4]
    genres   = movie.get("genres") or []
    genre_html = "".join(f'<span class="badge badge-genre" style="font-size:0.68rem;">{g}</span>' for g in genres[:3])
    src = f"https://image.tmdb.org/t/p/w342{path}" if path else ""

    st.markdown(f"""
    <div class="motd">
      <div class="motd-poster">
        {"<img src='" + src + "' />" if src else "<div style='width:150px;height:220px;background:#1e293b;display:flex;align-items:center;justify-content:center;font-size:3rem;'>🎬</div>"}
      </div>
      <div class="motd-body">
        <div class="motd-label">🌟 Movie of the Day</div>
        <div class="motd-title">{title}</div>
        <div class="motd-meta">
          <span class="badge badge-star">⭐ {rating:.1f}</span>
          <span class="badge" style="background:rgba(255,255,255,0.1);color:#e2e8f0;">{year}</span>
          {genre_html}
        </div>
        <div class="motd-overview">{overview}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("📄 View Details", key="motd_detail", use_container_width=True):
            st.session_state.selected_movie = movie
            st.session_state.page = "Detail"; st.rerun()


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    if not st.session_state.token:
        auth_page(); return

    if not st.session_state.user:
        me = api("/api/v1/users/me", auth=True, silent=True)
        if me: st.session_state.user = me
        else: st.session_state.token = None; st.rerun()

    sidebar()

    if st.session_state.rating_movie:
        rating_dialog(); return

    page = st.session_state.page
    if   page == "Home":            page_home()
    elif page == "Mood":            section_mood()
    elif page == "Recommendations": page_recommendations()
    elif page == "Search":          page_search()
    elif page == "Watchlist":       page_watchlist()
    elif page == "My Ratings":      page_my_ratings()
    elif page == "Dashboard":       
        st.markdown("<div class='sec-hdr'>📊 My Dashboard</div>", unsafe_allow_html=True)
        section_dashboard()
    elif page == "Preferences":     page_preferences()
    elif page == "Detail":          page_detail()

main()

