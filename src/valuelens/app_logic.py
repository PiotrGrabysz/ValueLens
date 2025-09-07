from dataclasses import dataclass

from src.valuelens.filtering import Paragraph, filter_relevant
from src.valuelens.scraping.crawler import crawl_site
from src.valuelens.scraping.extractors.factory import Extractor
from src.valuelens.summarizer import Summarizer


@dataclass
class AppConfig:
    extractor: Extractor
    summarizer: Summarizer


@dataclass
class SummaryResult:
    summary: str | None
    relevant_paragraphs: list[Paragraph]
    all_paragraphs: list[Paragraph] | None


def process_url(url: str, config: AppConfig) -> SummaryResult:
    """Core app logic: scrape a URL and summarize it."""
    page_results = crawl_site(root_url=url, extractor=config.extractor)
    paragraphs = []
    for page_result in page_results:
        for paragraph in page_result.paragraphs:
            paragraphs.append(Paragraph(text=paragraph, source=page_result.url))

    if not page_results:
        return SummaryResult(summary=None, relevant_paragraphs=[], all_paragraphs=None)

    relevant_results = filter_relevant(paragraphs)

    if not relevant_results:
        return SummaryResult(
            summary=None, relevant_paragraphs=relevant_results, all_paragraphs=paragraphs
        )

    text_to_summarize = "\n\n".join(p.text for p in paragraphs)
    summary = config.summarizer.summarize(text_to_summarize)
    return SummaryResult(
        summary=summary, relevant_paragraphs=relevant_results, all_paragraphs=paragraphs
    )
