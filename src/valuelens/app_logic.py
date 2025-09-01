from dataclasses import dataclass

from src.valuelens.filtering import filter_relevant
from src.valuelens.scraping.crawler import fetch_html
from src.valuelens.scraping.extractors.factory import Extractor
from src.valuelens.summarizer import Summarizer


@dataclass
class AppConfig:
    scraper: Extractor
    summarizer: Summarizer


@dataclass
class SummaryResult:
    summary: str | None
    relevant_paragraphs: list[str]
    all_paragraphs: list[str] | None


def process_url(url: str, config: AppConfig) -> SummaryResult:
    """Core app logic: scrape a URL and summarize it."""
    html = fetch_html(url)
    paragraphs = config.scraper(html)
    if not paragraphs:
        return SummaryResult(summary=None, relevant_paragraphs=[], all_paragraphs=None)

    relevant_paragraphs = filter_relevant(paragraphs)
    if not relevant_paragraphs:
        return SummaryResult(summary=None, relevant_paragraphs=[], all_paragraphs=paragraphs)

    text_to_summarize = "\n\n".join(relevant_paragraphs)
    summary = config.summarizer.summarize(text_to_summarize)
    return SummaryResult(
        summary=summary, relevant_paragraphs=relevant_paragraphs, all_paragraphs=paragraphs
    )
