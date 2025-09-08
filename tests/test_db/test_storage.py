import time

from src.valuelens.db import models, storage
from src.valuelens.schemas import Paragraph


def test_create_company_with_paragraphs(session):
    company = storage.save_analysis(
        session=session,
        root_url="https://example.com",
        summary="Sample summary",
        extractor="Trafilatura",
        paragraphs=[
            Paragraph(text="About us", source="https://example.com/about"),
            Paragraph(text="Contact", source="https://example.com/contact"),
        ],
    )

    assert company.id is not None
    assert len(company.paragraphs) == 2
    assert company.paragraphs[0].source_url == "https://example.com/about"
    assert company.paragraphs[0].text == "About us"


def test_cascade_delete_company(session):
    company = storage.save_analysis(
        session=session,
        root_url="https://delete-me.com",
        summary="Sample summary",
        extractor="Trafilatura",
        paragraphs=[Paragraph(text="Tmp", source="/about")],
    )
    company_id = company.id
    para_id = company.paragraphs[0].id

    storage.delete_company(session, company_id)

    # Both company and paragraph should be gone
    assert session.get(models.CompanyAnalysis, company_id) is None
    assert session.get(models.Paragraph, para_id) is None


def test_load_history_orders_and_limits(session):
    urls = ["https://a.com", "https://b.com", "https://c.com"]
    for url in urls:
        storage.save_analysis(
            session=session,
            root_url=url,
            summary="Sample summary",
            extractor="Trafilatura",
            paragraphs=[Paragraph(text="Sample paragraph", source="/sub_page")],
        )
        time.sleep(0.01)  # ensure timestamp difference

    results = storage.load_history(session, limit=2)

    # Should return 2 most recent
    assert len(results) == 2
    returned_urls = [c.root_url for c in results]
    # Most recent is c.com, then b.com
    assert returned_urls == ["https://c.com", "https://b.com"]
