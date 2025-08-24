from dataclasses import dataclass

from src.valuelens.filtering import filter_relevant
from src.valuelens.scraping import extract_text
from src.valuelens.summarizer import Summarizer


@dataclass
class SummaryResult:
    summary: str | None
    relevant_paragraphs: list[str]
    raw_text: str | None


def process_url(url: str, summarizer: Summarizer) -> SummaryResult:
    """Core app logic: scrape a URL and summarize it."""
    text = extract_text(url)
    if not text:
        return SummaryResult(summary=None, relevant_paragraphs=[], raw_text=None)

    relevant_paragraphs = filter_relevant(text)
    if not relevant_paragraphs:
        return SummaryResult(summary=None, relevant_paragraphs=[], raw_text=text)

    summary = summarizer.summarize(text)
    return SummaryResult(summary=summary, relevant_paragraphs=relevant_paragraphs, raw_text=text)
