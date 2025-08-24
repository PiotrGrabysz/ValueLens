from typing import Protocol


class Summarizer(Protocol):
    def summarize(self, text: str) -> str | None: ...


class OpenAISummarizer:
    def __init__(self):
        from openai import OpenAI

        self.client = OpenAI()

    def summarize(self, text: str) -> str | None:
        """Summarize the given text using OpenAI's GPT model.

        Args:
            text: The input text to summarize.

        Returns:
            A short summary string, or None if summarization fails.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that summarizes company missions and values in 2–3 sentences.",
                    },
                    {
                        "role": "user",
                        "content": f"Summarize the following company values and mission:\n\n{text}",
                    },
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Summarization failed: {e}")
            return None


class MockSummarizer:
    @staticmethod
    def summarize(text: str) -> str:
        snippet = text[:200].replace("\n", " ")
        return f"[MOCK SUMMARY] Example values summary based on text: {snippet}..."


def get_summarizer(debug: bool = False):
    """Factory to return the right summarizer."""
    if debug:
        return MockSummarizer()
    return OpenAISummarizer()
