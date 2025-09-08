from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class CompanyAnalysis(Base):
    __tablename__ = "company_analysis"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    root_url: Mapped[str] = mapped_column(String(500))
    summary: Mapped[str | None] = mapped_column(Text)
    extractor: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    # Relationship: one company has many paragraphs
    paragraphs: Mapped[list["Paragraph"]] = relationship(
        back_populates="company_analysis", cascade="all, delete-orphan", lazy="joined"
    )


class Paragraph(Base):
    __tablename__ = "paragraphs"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    source_url: Mapped[str] = mapped_column(String(500))

    company_id: Mapped[int] = mapped_column(ForeignKey("company_analysis.id"))
    company_analysis: Mapped["CompanyAnalysis"] = relationship(back_populates="paragraphs")
