import trafilatura


def extract_text(url: str) -> str | None:
    """Fetch and extract main text content from a given URL.

    Args:
        url: The URL of the website to scrape.

    Returns:
        Extracted text as a string, or None if extraction fails.
    """
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        return trafilatura.extract(downloaded)
    return None
