import pytest

from src.valuelens.scraping.extractors.extract_with_headers import (
    ContentSection,
    extract_sections_from_text,
    extract_text,
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


def test_parse_content_section_to_markdown():
    section = ContentSection(header="Who we are?", content="We are a dynamic team...")
    expected_text = "### Who we are?\nWe are a dynamic team..."

    text = parse_content_section_to_markdown(section)

    assert text == expected_text


class TestExtractText:
    @staticmethod
    def test_extracted_text_contains_sections():
        paragraphs = extract_text(SAMPLE_HTML)
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
