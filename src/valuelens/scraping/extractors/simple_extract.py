import trafilatura


def extract_text(html: str) -> list[str]:
    extracted_text = trafilatura.extract(html)
    return extracted_text.split("\n")
