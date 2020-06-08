import pytest
from app.utils import get_average_of_ratings


def test_get_average_of_ratings():
    test_rating_dict = {
        1: 1,
        2: 0,
        3: 0,
        4: 3,
        5: 0
    }
    assert get_average_of_ratings(test_rating_dict) == '3.25'


def test_get_average_of_ratings_error():
    test_rating_dict = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    }
    assert get_average_of_ratings(test_rating_dict) == 0.0