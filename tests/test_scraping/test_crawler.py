from unittest.mock import Mock, patch

import requests

from src.valuelens.scraping.crawler import fetch_html


def test_http_error():
    """Simulate HTTP 404 error."""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

    with patch("requests.get", return_value=mock_response):
        result = fetch_html("http://fake-url.com")

    assert result is None


def test_connection_error():
    """Simulate a network failure."""
    with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
        result = fetch_html("http://fake-url.com")

    assert result is None
