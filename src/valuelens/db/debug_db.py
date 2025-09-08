from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .models import Base

# Single in-memory engine (lives for entire app session)
engine = create_engine(
    "sqlite:///:memory:",
    echo=False,
    future=True,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
Base.metadata.create_all(engine)

# Session factory for in-memory DB
SessionLocalDebug = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
