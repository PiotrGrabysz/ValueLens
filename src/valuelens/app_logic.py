from dataclasses import dataclass

from src.valuelens.filtering import filter_relevant
from src.valuelens.schemas import Paragraph, SummaryResult
from src.valuelens.scraping.crawler import PageResult, crawl_site
from src.valuelens.scraping.extractors.factory import Extractor
from src.valuelens.summarizer import Summarizer


@dataclass
class AppConfig:
    extractor: Extractor
    summarizer: Summarizer


def process_url(url: str, config: AppConfig, max_pages: int) -> SummaryResult:
    """Core app logic: scrape a URL and summarize it."""
    page_results = crawl_site(root_url=url, extractor=config.extractor, max_pages=max_pages)
    paragraphs = _extract_results_into_paragraphs(page_results)

    if not page_results:
        return SummaryResult(summary=None, relevant_paragraphs=None, all_paragraphs=None)

    relevant_results = filter_relevant(paragraphs)

    if not relevant_results:
        return SummaryResult(
            summary=None,
            relevant_paragraphs=None,
            all_paragraphs=paragraphs,
        )

    text_to_summarize = "\n\n".join(p.text for p in paragraphs)
    summary = config.summarizer.summarize(text_to_summarize)
    return SummaryResult(
        summary=summary,
        relevant_paragraphs=relevant_results,
        all_paragraphs=paragraphs,
    )


def _extract_results_into_paragraphs(page_results: list[PageResult]) -> list[Paragraph]:
    paragraphs = [
        Paragraph(text=paragraph, source=page_result.url)
        for page_result in page_results
        for paragraph in page_result.paragraphs
    ]

    return paragraphs
