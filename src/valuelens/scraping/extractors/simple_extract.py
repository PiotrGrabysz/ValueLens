"""
Scraping utilities for extracting text content from company websites.
"""

import trafilatura


def extract_text(url: str) -> list[str] | None:
    """Extract cleaned text content from a URL.

    Args:
        url (str): The website URL.

    Returns:
        str | None: The extracted text, or None if extraction fails.
    """
    html = fetch_html(url)
    if not html:
        return None

    extracted_text = trafilatura.extract(html)
    return extracted_text.split("\n")


def fetch_html(url: str) -> str | None:
    """Fetch raw HTML content from a URL."""
    return trafilatura.fetch_url(url)
