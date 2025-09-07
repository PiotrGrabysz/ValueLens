from src.valuelens.scraping.crawler import crawl_site, parse_links
from src.valuelens.scraping.extractors.simple_extract import extract_text


def test_parse_links_relative_link():
    html = """
    <html>
      <body>
        <a href="/about">About</a>
        <a href="https://example.com/contact">Contact</a>
      </body>
    </html>
    """
    links = parse_links(html, base_url="https://example.com")
    assert "https://example.com/about" in links


def test_parse_links_absolute_link():
    html = """
    <html>
      <body>
        <a href="https://example.com/contact">Contact</a>
      </body>
    </html>
    """
    links = parse_links(html, base_url="https://example.com")
    assert "https://example.com/contact" in links


def test_crawl_site():
    pages = {
        "https://example.com": """
            <html>
              <body>
                <a href="https://example.com/page2">Next</a>
                <p>Home Page Page</p>
              </body>
            </html>
        """,
        "https://example.com/page2": """
            <html>
              <body><p>Page 2 content</p></body>
            </html>
        """,
    }

    def fake_fetch(url: str) -> str | None:
        return pages.get(url)

    results = crawl_site(
        "https://example.com", max_depth=1, fetcher=fake_fetch, extractor=extract_text
    )

    assert len(results) == 2

    assert results[0].url == "https://example.com"
    assert results[1].url == "https://example.com/page2"


def test_page_cannot_be_searched_twice():
    page_with_link_to_itself = {
        "https://example.com": """
            <html>
              <body>
                <a href="https://example.com">Example</a>
                <p>Home Page Page</p>
              </body>
            </html>
        """
    }

    def fake_fetch(url: str) -> str | None:
        return page_with_link_to_itself.get(url)

    results = crawl_site(
        "https://example.com", max_depth=1, fetcher=fake_fetch, extractor=extract_text
    )

    assert len(results) == 1
