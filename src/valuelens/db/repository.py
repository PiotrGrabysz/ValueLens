from collections.abc import Callable, Generator, Iterable
from contextlib import contextmanager

from sqlalchemy.orm import Session

from src.valuelens.schemas import HistoryRecord, Paragraph

from . import storage
from .database import SessionLocal
from .debug_db import SessionLocalDebug
from .models import CompanyAnalysis

type SessionFactory = Callable[[], Session]


class Repository:
    """Repository for all persistence operations."""

    def __init__(
        self, session_factory: SessionFactory | None = None, in_memory: bool = False
    ) -> None:
        if session_factory:
            self.session_factory = session_factory
        elif in_memory:
            self.session_factory = SessionLocalDebug
        else:
            self.session_factory = SessionLocal

        self.in_memory = in_memory

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """Provide a transactional scope for a series of operations."""
        session: Session = self.session_factory()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def save_analysis(
        self,
        root_url: str,
        summary: str | None,
        extractor: str,
        paragraphs: Iterable[Paragraph] | None,
    ) -> CompanyAnalysis:
        if paragraphs is None:
            paragraphs = []
        with self.session_scope() as session:
            return storage.save_analysis(session, root_url, summary, extractor, paragraphs)

    def load_history(self, limit: int = 20) -> list[HistoryRecord]:
        with self.session_scope() as session:
            return storage.load_history(session, limit=limit)

    def delete_company(self, company_id: int) -> None:
        with self.session_scope() as session:
            storage.delete_company(session, company_id)
