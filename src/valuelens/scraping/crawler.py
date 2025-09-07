from collections.abc import Callable
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from src.valuelens.logger import get_logger
from src.valuelens.scraping.extractors.extract_with_headers import extract_text
from src.valuelens.scraping.extractors.factory import Extractor

logger = get_logger("ValueLens")


@dataclass
class PageResult:
    url: str
    paragraphs: list[str]


def fetch_html(url: str, timeout: int = 10) -> str | None:
    """Fetch raw HTML from the given URL. Return None on error."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException:
        logger.error(f"Cannot fetch the site: {url}")
        return None
    else:
        return response.text


def crawl_site(
    root_url: str,
    extractor: Extractor = extract_text,
    fetcher: Callable[[str], str | None] = fetch_html,
    max_pages: int = 10,
    max_depth: int = 1,
) -> list[PageResult]:
    """
    Crawl a site starting from root_url, following links within same domain.
    """
    visited = set()
    results: list[PageResult] = []

    root_domain = get_domain(root_url)

    def _crawl(url: str, depth: int) -> None:
        if url in visited or len(results) >= max_pages or depth > max_depth:
            return
        visited.add(url)
        logger.debug(f"Scraping the url: {url}")

        html = fetcher(url)
        if not html:
            return

        text = extractor(html)
        if text:
            results.append(PageResult(url, text))

        for link in parse_links(html, url):
            if get_domain(link) == root_domain:
                _crawl(link, depth + 1)

    _crawl(root_url, depth=0)
    return results


def parse_links(html: str, base_url: str) -> list[str]:
    """Extract and normalize links from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(base_url, href)
        links.append(full_url)

    return links


def get_domain(url: str) -> str:
    return urlparse(url).netloc
