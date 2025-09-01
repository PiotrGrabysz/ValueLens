from unittest.mock import Mock, patch

import pytest
import requests

from src.valuelens.scraping.extractors.extract_with_headers import (
    ContentSection,
    extract_sections_from_text,
    extract_text,
    fetch_html,
    parse_content_section_to_markdown,
    should_skip_header,
)

SAMPLE_HTML = """
<html>
  <body>
    <h1>Who we are?</h1>
    <p>We are a dynamic team...</p>
    <h2>Our values</h2>
    <p>Innovation, sustainable growth...</p>
    <h3>Our approach</h3>
    <p>We focus on the client...</p>
    <h2>Contact</h2>
    <p>This is a useless nav section.</p>
  </body>
</html>
"""


class TestExtractSectionsFromText:
    @staticmethod
    def test_extracts_all_sections():
        sections = extract_sections_from_text(SAMPLE_HTML)
        expected_number_of_sections = 3

        assert len(sections) == expected_number_of_sections

    @staticmethod
    def test_contains_correct_headers_and_keywords():
        sections = extract_sections_from_text(SAMPLE_HTML)

        assert sections[0].header == "Who we are?"
        assert "dynamic team" in sections[0].content

        assert sections[1].header == "Our values"
        assert "Innovation" in sections[1].content

        assert sections[2].header == "Our approach"
        assert "client" in sections[2].content

    @staticmethod
    @pytest.mark.parametrize(
        "header, should_contain",
        [(1, True), (2, True), (3, True), (4, False), (5, False), (6, False)],
    )
    def test_works_with_specified_headers(header: int, should_contain: bool):
        sample_html = f"<h{header}>Who we are?</h{header}><p>We are a dynamic team...</p>"
        sections = extract_sections_from_text(sample_html, smallest_header_to_find=3)

        assert bool(sections) == should_contain

    def test_nav_sections_are_excluded(self):
        sections = extract_sections_from_text(SAMPLE_HTML)

        assert all("contact" != section.header.lower() for section in sections)


class TestFetchURL:
    @staticmethod
    def test_http_error():
        """Simulate HTTP 404 error."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        with patch("requests.get", return_value=mock_response):
            result = fetch_html("http://fake-url.com")

        assert result is None

    @staticmethod
    def test_connection_error():
        """Simulate a network failure."""
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            result = fetch_html("http://fake-url.com")

        assert result is None


def test_parse_content_section_to_markdown():
    section = ContentSection(header="Who we are?", content="We are a dynamic team...")
    expected_text = "### Who we are?\nWe are a dynamic team..."

    text = parse_content_section_to_markdown(section)

    assert text == expected_text


class TestExtractText:
    @staticmethod
    @pytest.fixture(scope="class")
    def mock_requests_get():
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = SAMPLE_HTML
            mock_get.return_value = mock_response
            yield mock_get

    @staticmethod
    def test_extracted_text_contains_sections(mock_requests_get):
        paragraphs = extract_text("http://fake-url.com")
        text = "\n".join(paragraphs)

        assert "### Who we are?" in text
        assert "dynamic team" in text


class TestShouldSkipHeader:
    def test_if_skips_too_short(self):
        assert should_skip_header("Word") is True

    def test_if_skips_not_alpha_numeric(self):
        assert should_skip_header("###") is True

    def test_if_skips_sll_caps(self):
        assert should_skip_header("ALL CAPS HEADER") is True
