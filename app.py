import os
from typing import Literal

import streamlit as st

from src.valuelens.app_logic import AppConfig, process_url
from src.valuelens.db.repository import Repository
from src.valuelens.db.storage import init_db
from src.valuelens.logger import get_logger
from src.valuelens.scraping.extractors.factory import extractor_factory
from src.valuelens.summarizer import get_summarizer

logger = get_logger("ValueLens")
debug_mode = os.getenv("VALUELENS_DEBUG", "0") == "1"
if debug_mode:
    logger.info("Running in a debug mode")
    repo = Repository(in_memory=True)
else:
    init_db()
    repo = Repository()


def analyze_website_page() -> None:
    col1, col2 = st.columns([3, 1])
    url = col1.text_input("Paste company website URL:")

    extraction_option: Literal["Trafilatura", "BeautifulSoup"] = col2.radio(
        "Choose extraction method:", ["Trafilatura", "BeautifulSoup"]
    )
    crawler_max_pages = col2.slider("Number of pages to crawl", min_value=1, max_value=10)

    summarizer = get_summarizer(debug_mode)
    extractor = extractor_factory(extraction_option)

    config = AppConfig(extractor=extractor, summarizer=summarizer)

    if st.button("Analyze Website"):
        logger.info(f"Analysing content of {url=}")
        analyze_website(url, config, extraction_option, crawler_max_pages)


def analyze_website(url: str, config: AppConfig, extraction_option: str, max_pages: int) -> None:
    with st.spinner("Scraping website..."):
        result = process_url(url, config, max_pages)

    repo.save_analysis(
        root_url=url,
        summary=result.summary,
        extractor=extraction_option,
        paragraphs=result.relevant_paragraphs,
    )

    if result.summary:
        st.subheader("📌 Summary")
        st.write(result.summary)

        st.subheader("📄 Relevant Paragraphs")
        for p in result.relevant_paragraphs:  # type: ignore
            with st.expander("Show paragraph"):
                st.write(f"{p.text}\n\nsource: {p.source}")

    elif not result.all_paragraphs:
        st.error("❌ Could not extract text from this website.")
        logger.error("Could not extract text from this website.")

    elif not result.relevant_paragraphs:
        st.warning("⚠️ No mission/values-related text found.")
        logger.warning("No mission/values-related text found.")


def show_history(limit: int = 20) -> None:
    history = repo.load_history(limit=limit)
    for item in history:
        st.write(f"**{item.root_url}** ({item.created_at:%Y-%m-%d %H:%M:%S})")
        st.write(f"Extracted with `{item.extractor}`")
        st.write(f"Summary:\n\n{item.summary}")
        st.divider()


if __name__ == "__main__":
    st.title("🔍 ValueLens - Company Mission & Values Extractor")

    tab1, tab2 = st.tabs(["Analyze", "History"])

    with tab1:
        analyze_website_page()

    with tab2:
        show_history()
