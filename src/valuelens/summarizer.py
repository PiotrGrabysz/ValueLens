from openai import OpenAI

client = OpenAI()


def summarize(text: str) -> str | None:
    """Summarize the given text using OpenAI's GPT model.

    Args:
        text: The input text to summarize.

    Returns:
        A short summary string, or None if summarization fails.
    """
    try:
        response = client.chat.completions.create(
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
