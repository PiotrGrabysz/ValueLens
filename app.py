import os

import streamlit as st

from src.valuelens.filtering import filter_relevant
from src.valuelens.logger import get_logger
from src.valuelens.scraping import extract_text
from src.valuelens.summarizer import MockSummarizer, OpenAISummarizer

logger = get_logger("ValueLens")
debug_mode = os.getenv("VALUELENS_DEBUG", "0") == "1"
if debug_mode:
    logger.info("Running in a debug mode")


def get_summarizer(debug: bool = False):
    """Factory to return the right summarizer."""
    if debug:
        return MockSummarizer()
    return OpenAISummarizer()


summarizer = get_summarizer(debug_mode)


st.title("🔍 ValueLens - Company Mission & Values Extractor")

url = st.text_input("Paste company website URL:")

if st.button("Analyze Website"):
    logger.info(f"Analysing content of {url=}")
    with st.spinner("Scraping website..."):
        text = extract_text(url)
        if not text:
            st.error("❌ Could not extract text from this website.")
            logger.error("Could not extract text from this website.")

        else:
            logger.info(f"Extracted text: {text[:1000]}")
            relevant = filter_relevant(text)
            if not relevant:
                st.warning("⚠️ No mission/values-related text found.")
                logger.warning("No mission/values-related text found.")
            else:
                summary = summarizer.summarize(" ".join(relevant))

                st.subheader("📌 Summary")
                st.write(summary)

                st.subheader("📄 Relevant Paragraphs")
                for p in relevant:
                    with st.expander("Show paragraph"):
                        st.write(p)
