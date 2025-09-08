from dataclasses import dataclass


@dataclass
class Paragraph:
    text: str
    source: str


@dataclass
class SummaryResult:
    summary: str | None
    relevant_paragraphs: list[Paragraph] | None
    all_paragraphs: list[Paragraph] | None
