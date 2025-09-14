from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.valuelens.schemas import HistoryRecord, Paragraph

from . import models
from .database import engine


def init_db() -> None:
    """Create tables if they don’t exist."""
    models.Base.metadata.create_all(engine)


def save_analysis(
    session: Session,
    root_url: str,
    summary: str | None,
    extractor: str,
    paragraphs: Iterable[Paragraph],
) -> models.CompanyAnalysis:
    analysis = models.CompanyAnalysis(
        root_url=root_url,
        summary=summary,
        extractor=extractor,
        paragraphs=[models.Paragraph(text=p.text, source_url=p.source) for p in paragraphs],
    )
    session.add(analysis)
    session.commit()
    return analysis


def load_history(session: Session, limit: int = 20) -> list[HistoryRecord]:
    stmt = (
        select(models.CompanyAnalysis)
        .options(selectinload(models.CompanyAnalysis.paragraphs))
        .order_by(models.CompanyAnalysis.created_at.desc())
        .limit(limit)
    )
    results = session.scalars(stmt).unique().all()

    # Convert ORM models → Pydantic DTOs
    return [
        HistoryRecord(
            root_url=r.root_url,
            summary=r.summary,
            extractor=r.extractor,
            created_at=r.created_at,
            paragraphs=[Paragraph(text=p.text, source=p.source_url) for p in r.paragraphs],
        )
        for r in results
    ]


def delete_company(session: Session, company_id: int) -> None:
    """Delete company (and cascade paragraphs)."""
    company = session.get(models.CompanyAnalysis, company_id)
    if company:
        session.delete(company)
        session.commit()
