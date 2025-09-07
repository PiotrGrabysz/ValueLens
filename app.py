import os

import streamlit as st

from src.valuelens.app_logic import AppConfig, process_url
from src.valuelens.logger import get_logger
from src.valuelens.scraping.extractors.factory import extractor_factory
from src.valuelens.summarizer import get_summarizer

logger = get_logger("ValueLens")
debug_mode = os.getenv("VALUELENS_DEBUG", "0") == "1"
if debug_mode:
    logger.info("Running in a debug mode")

summarizer = get_summarizer(debug_mode)


st.title("🔍 ValueLens - Company Mission & Values Extractor")

col1, col2 = st.columns([3, 1])
url = col1.text_input("Paste company website URL:")

scraper_option = col2.radio("Choose extraction method:", ["Trafilatura", "BeautifulSoup"])
scraper = extractor_factory(scraper_option)

config = AppConfig(extractor=scraper, summarizer=summarizer)

if st.button("Analyze Website"):
    logger.info(f"Analysing content of {url=}")
    with st.spinner("Scraping website..."):
        result = process_url(url, config)

    if result.summary:
        st.subheader("📌 Summary")
        st.write(result.summary)

        st.subheader("📄 Relevant Paragraphs")
        for p in result.relevant_paragraphs:
            with st.expander("Show paragraph"):
                st.write(f"{p.text}\n\nsource: {p.source}")

    elif not result.all_paragraphs:
        st.error("❌ Could not extract text from this website.")
        logger.error("Could not extract text from this website.")

    elif not result.relevant_paragraphs:
        st.warning("⚠️ No mission/values-related text found.")
        logger.warning("No mission/values-related text found.")
