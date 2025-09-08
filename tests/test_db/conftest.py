from collections.abc import Generator

import pytest
from sqlalchemy.orm import Session

from src.valuelens.db.debug_db import SessionLocalDebug


@pytest.fixture
def session() -> Generator[Session, None, None]:
    """Provide a clean in-memory DB session for each test."""
    with SessionLocalDebug() as session:
        yield session
        session.rollback()
