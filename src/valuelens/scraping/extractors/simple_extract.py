import trafilatura


def extract_text(html: str) -> list[str]:
    extracted_text = trafilatura.extract(html)
    if extracted_text is None:
        return []
    return extracted_text.split("\n")
