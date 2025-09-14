from dataclasses import dataclass
from datetime import datetime


@dataclass
class Paragraph:
    text: str
    source: str


@dataclass
class SummaryResult:
    summary: str | None
    relevant_paragraphs: list[Paragraph] | None
    all_paragraphs: list[Paragraph] | None


@dataclass
class HistoryRecord:
    root_url: str
    summary: str | None
    extractor: str
    created_at: datetime

    # Relationship: one company has many paragraphs
    paragraphs: list[Paragraph]
