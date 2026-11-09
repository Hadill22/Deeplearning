
from config import (
    ROOT,
    ML_DIR,
    TMDB_DIR,
    POSTER_DIR,
    PROCESSED,
    ML_VERSION,
    MAX_CONCURRENCY,
    RANDOM_SEED,
    TEST_LIMIT,
    CANONICAL_GENRES,
)


def test_project_root_exists():
    assert ROOT.exists()


def test_data_paths_are_inside_project():
    for path in (ML_DIR, TMDB_DIR, POSTER_DIR, PROCESSED):
        assert path.is_relative_to(ROOT)


def test_configuration_values():
    assert ML_VERSION == "ml-latest-small"
    assert MAX_CONCURRENCY > 0
    assert RANDOM_SEED == 42
    assert TEST_LIMIT > 0


def test_canonical_genres_are_unique():
    assert len(CANONICAL_GENRES) == len(set(CANONICAL_GENRES))
