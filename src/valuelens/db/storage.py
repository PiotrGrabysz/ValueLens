from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.valuelens.schemas import Paragraph as ParagraphSchema

from .database import engine
from .models import Base, CompanyAnalysis, Paragraph


def init_db() -> None:
    """Create tables if they don’t exist."""
    Base.metadata.create_all(engine)


def save_analysis(
    session: Session,
    root_url: str,
    summary: str | None,
    extractor: str,
    paragraphs: Iterable[ParagraphSchema],
) -> CompanyAnalysis:
    analysis = CompanyAnalysis(
        root_url=root_url,
        summary=summary,
        extractor=extractor,
        paragraphs=[Paragraph(text=p.text, source_url=p.source) for p in paragraphs],
    )
    session.add(analysis)
    session.commit()
    return analysis


def load_history(session: Session, limit: int = 20) -> list[CompanyAnalysis]:
    stmt = select(CompanyAnalysis).order_by(CompanyAnalysis.created_at.desc()).limit(limit)
    return list(session.scalars(stmt).unique())


def delete_company(session: Session, company_id: int) -> None:
    """Delete company (and cascade paragraphs)."""
    company = session.get(CompanyAnalysis, company_id)
    if company:
        session.delete(company)
        session.commit()
