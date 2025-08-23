import streamlit as st

from src.valuelens.filtering import filter_relevant
from src.valuelens.scraping import extract_text
from src.valuelens.summarizer import summarize

st.title("🔍 ValueLens - Company Mission & Values Extractor")

url = st.text_input("Paste company website URL:")

if st.button("Analyze Website"):
    with st.spinner("Scraping website..."):
        text = extract_text(url)
        if not text:
            st.error("❌ Could not extract text from this website.")

        else:
            relevant = filter_relevant(text)
            if not relevant:
                st.warning("⚠️ No mission/values-related text found.")
            else:
                st.text_area("Extracted Text", text[:2000])  # preview only first 2000 chars
                summary = summarize(" ".join(relevant))

                st.subheader("📌 Summary")
                st.write(summary)

                st.subheader("📄 Relevant Paragraphs")
                for p in relevant:
                    with st.expander("Show paragraph"):
                        st.write(p)
