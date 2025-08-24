from collections.abc import Callable
from typing import Literal

from src.valuelens.scraping import extract_with_headers, simple_extract

type Scraper = Callable[[str], list[str] | None]


def scraper_factory(method: Literal["Trafilatura", "BeautifulSoup"]) -> Scraper:
    if method == "Trafilatura":
        return simple_extract.extract_text

    elif method == "BeautifulSoup":
        return extract_with_headers.extract_text

    raise ValueError("Only possible values are 'Trafilatura' and 'BeautifulSoup'!")
