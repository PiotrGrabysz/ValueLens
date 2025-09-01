import requests


def fetch_html(url: str) -> str | None:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return None

    return response.text
