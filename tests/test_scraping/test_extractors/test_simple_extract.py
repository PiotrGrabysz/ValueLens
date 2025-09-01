from src.valuelens.scraping.extractors.simple_extract import extract_text


def test_extract_text_successful_response():
    text = extract_text("<html><body><p>Our mission is innovation.</p></body></html>")
    assert text == ["Our mission is innovation."]
