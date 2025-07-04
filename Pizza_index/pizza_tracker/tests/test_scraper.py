# pizza_tracker/tests/test_scraper.py

import pytest
from unittest.mock import patch
from src import scraper

@pytest.fixture
def mock_html():
    """Provides a sample HTML content for testing."""
    with open("tests/mock_data/sample_page.html", "r") as f:
        return f.read()

@patch("src.scraper.get_html")
def test_get_popular_times(mock_get_html, mock_html):
    """Tests the get_popular_times function."""
    mock_get_html.return_value = mock_html
    data = scraper.get_popular_times("some_url")
    assert len(data) > 0
    assert "day_of_week" in data[0]
    assert "hour_of_day" in data[0]
    assert "popularity_percent_normal" in data[0]
