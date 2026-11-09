
import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "normalize",
    ROOT / "03_normalize.py"
)

normalize = importlib.util.module_from_spec(spec)
spec.loader.exec_module(normalize)


def test_parse_ml_title():
    title, year = normalize.parse_ml_title("Toy Story (1995)")

    assert title == "Toy Story"
    assert year == 1995.0


def test_parse_title_without_year():
    title, year = normalize.parse_ml_title("Toy Story")

    assert title == "Toy Story"
    assert year != year  # NaN


def test_normalize_language():
    assert normalize.normalize_lang("EN") == "en"
    assert normalize.normalize_lang("FR") == "fr"
    assert normalize.normalize_lang("cn") == "zh"
    assert normalize.normalize_lang("xx") is None


def test_movie_genres_mapping():
    genres = normalize.ml_genres_to_canonical(
        "Action|Adventure|Comedy"
    )

    assert genres == ["Action", "Adventure", "Comedy"]


def test_invalid_genres_are_removed():
    genres = normalize.ml_genres_to_canonical(
        "Film-Noir|IMAX"
    )

    assert genres == []


def test_duplicate_genres_are_removed():
    genres = normalize.ml_genres_to_canonical(
        "Action|Action|Comedy"
    )

    assert genres == ["Action", "Comedy"]
