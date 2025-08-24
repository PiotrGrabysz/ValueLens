import os

import streamlit as st

from src.valuelens.app_logic import process_url
from src.valuelens.logger import get_logger
from src.valuelens.summarizer import get_summarizer

logger = get_logger("ValueLens")
debug_mode = os.getenv("VALUELENS_DEBUG", "0") == "1"
if debug_mode:
    logger.info("Running in a debug mode")

summarizer = get_summarizer(debug_mode)


st.title("🔍 ValueLens - Company Mission & Values Extractor")

url = st.text_input("Paste company website URL:")

if st.button("Analyze Website"):
    logger.info(f"Analysing content of {url=}")
    with st.spinner("Scraping website..."):
        result = process_url(url, summarizer)
        logger.info(f"Extracted text: {result.raw_text[:1000]}")

    if result.summary:
        st.subheader("📌 Summary")
        st.write(result.summary)

        st.subheader("📄 Relevant Paragraphs")
        for p in result.relevant_paragraphs:
            with st.expander("Show paragraph"):
                st.write(p)

    elif not result.raw_text:
        st.error("❌ Could not extract text from this website.")
        logger.error("Could not extract text from this website.")

    elif not result.relevant_paragraphs:
        st.warning("⚠️ No mission/values-related text found.")
        logger.warning("No mission/values-related text found.")
