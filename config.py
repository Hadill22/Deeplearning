
"""Configuration centrale du projet Movie Recommendation."""

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

# Charger les variables secrètes depuis .env
load_dotenv()

# Racine du projet
ROOT = Path(__file__).resolve().parent

# Charger la configuration YAML
CONFIG_FILE = ROOT / "configs" / "params.yaml"

with CONFIG_FILE.open("r", encoding="utf-8") as file:
    CONFIG = yaml.safe_load(file) or {}


def get_path(key: str, default: str) -> Path:
    """Convertir un chemin YAML en chemin absolu."""
    value = CONFIG.get("paths", {}).get(key, default)
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


# --- Chemins des données -----------------------------------------------

RAW = get_path("data_raw", "data/raw")
PROCESSED = get_path("data_processed", "data/processed")

ML_DIR = get_path("movielens", "data/raw/movielens")
TMDB_DIR = get_path("tmdb", "data/raw/tmdb")
POSTER_DIR = get_path("posters", "data/raw/posters")
LOG_DIR = get_path("logs", "logs")

# Créer automatiquement les dossiers nécessaires
for directory in (ML_DIR, TMDB_DIR, POSTER_DIR, PROCESSED, LOG_DIR):
    directory.mkdir(parents=True, exist_ok=True)


# --- MovieLens ---------------------------------------------------------

ML_VERSION = os.getenv(
    "ML_VERSION",
    CONFIG.get("movielens", {}).get("version", "ml-latest-small")
)

ML_URL = (
    f"https://files.grouplens.org/datasets/movielens/"
    f"{ML_VERSION}.zip"
)


# --- TMDB --------------------------------------------------------------

TMDB_CONFIG = CONFIG.get("tmdb", {})

TMDB_API = TMDB_CONFIG.get(
    "api_url", "https://api.themoviedb.org/3"
)

TMDB_TOKEN = os.getenv("TMDB_READ_TOKEN", "")

POSTER_BASE = TMDB_CONFIG.get(
    "poster_base_url", "https://image.tmdb.org/t/p/w342"
)

LANGUAGE = TMDB_CONFIG.get("language", "en-US")

MAX_CONCURRENCY = int(
    os.getenv(
        "MAX_CONCURRENCY",
        str(TMDB_CONFIG.get("max_concurrency", 20))
    )
)


# --- Paramètres du pipeline --------------------------------------------

PIPELINE_CONFIG = CONFIG.get("pipeline", {})

RANDOM_SEED = int(PIPELINE_CONFIG.get("random_seed", 42))
TEST_LIMIT = int(PIPELINE_CONFIG.get("test_limit", 100))


# --- Référentiel unique des genres -------------------------------------

CANONICAL_GENRES = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
    "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western",
]

ML_TO_CANONICAL = {
    "Action": "Action",
    "Adventure": "Adventure",
    "Animation": "Animation",
    "Children": "Family",
    "Comedy": "Comedy",
    "Crime": "Crime",
    "Documentary": "Documentary",
    "Drama": "Drama",
    "Fantasy": "Fantasy",
    "Film-Noir": None,
    "Horror": "Horror",
    "IMAX": None,
    "Musical": "Music",
    "Mystery": "Mystery",
    "Romance": "Romance",
    "Sci-Fi": "Science Fiction",
    "Thriller": "Thriller",
    "War": "War",
    "Western": "Western",
    "(no genres listed)": None,
}
