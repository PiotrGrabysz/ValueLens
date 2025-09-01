from collections.abc import Callable
from typing import Literal

from src.valuelens.scraping.extractors import extract_with_headers, simple_extract

type Extractor = Callable[[str], list[str] | None]


def extractor_factory(method: Literal["Trafilatura", "BeautifulSoup"]) -> Extractor:
    if method == "Trafilatura":
        return simple_extract.extract_text

    elif method == "BeautifulSoup":
        return extract_with_headers.extract_text

    raise ValueError("Only possible values are 'Trafilatura' and 'BeautifulSoup'!")
