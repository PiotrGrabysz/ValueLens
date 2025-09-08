from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.valuelens.schemas import Paragraph

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


def load_history(session: Session, limit: int = 20) -> list[models.CompanyAnalysis]:
    stmt = (
        select(models.CompanyAnalysis)
        .order_by(models.CompanyAnalysis.created_at.desc())
        .limit(limit)
    )
    return list(session.scalars(stmt).unique())


def delete_company(session: Session, company_id: int) -> None:
    """Delete company (and cascade paragraphs)."""
    company = session.get(models.CompanyAnalysis, company_id)
    if company:
        session.delete(company)
        session.commit()
