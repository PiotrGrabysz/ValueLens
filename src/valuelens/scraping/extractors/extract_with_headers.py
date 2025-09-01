from dataclasses import dataclass

from bs4 import BeautifulSoup

from src.valuelens.logger import get_logger

SMALLEST_HEADER_TO_FIND = 6

logger = get_logger("ValueLens")


@dataclass
class ContentSection:
    header: str
    content: str


def extract_text(html: str) -> list[str]:
    sections = extract_sections_from_text(html)
    parsed_sections = [parse_content_section_to_markdown(section) for section in sections]
    return parsed_sections


def extract_sections_from_text(
    text: str, smallest_header_to_find: int = SMALLEST_HEADER_TO_FIND
) -> list[ContentSection] | None:
    headers_to_find = _get_applicable_headers(smallest_header_to_find)

    soup = BeautifulSoup(text, "html.parser")
    sections: list[ContentSection] = []

    for header in soup.find_all(headers_to_find):
        logger.debug(header)
        header_text = header.get_text(strip=True)
        if should_skip_header(header_text):
            logger.debug("Skipping the header because it's suspected to be a navigation header.")
            continue

        content_parts: list[str] = []

        # Collect paragraphs until next header
        for sibling in header.find_next_siblings():
            logger.debug(f"{sibling=}")
            if sibling.name in headers_to_find:
                break
            if sibling.name == "p":
                content_parts.append(sibling.get_text(strip=True))

        if header_text and content_parts:
            sections.append(ContentSection(header=header_text, content=" ".join(content_parts)))

    return sections


def _get_applicable_headers(smallest_header_to_find: int) -> list[str]:
    _raise_if_incorrect_header(smallest_header_to_find)
    return [f"h{num}" for num in range(1, smallest_header_to_find + 1)]


def _raise_if_incorrect_header(smallest_header_to_find: int) -> None:
    if smallest_header_to_find < 1:
        raise ValueError("Header can't be smaller than bigger than <h1>!")
    if smallest_header_to_find > 6:
        raise ValueError("Header can't be smaller than smaller than <h6>!")


def should_skip_header(text: str) -> bool:
    """Heuristic filter for meaningful headers."""
    if not text:
        return True

    stripped = text.strip()
    words = stripped.split()

    # Too short
    if len(words) < 2:
        return True

    # Check for alphabetic content
    if not any(word.isalpha() for word in words):
        return True

    # Drop ALL CAPS headers (navigation bars often are like this)
    if stripped.isupper():
        return True

    return False


def parse_content_section_to_markdown(section: ContentSection) -> str:
    return f"### {section.header}\n{section.content}"
