import re
import unicodedata

def clean_text(text: str) -> str:
    """
    Efficiently cleans text data by removing extra spaces,
    special characters, and other unwanted noise.

    Parameters:
        text (str): The raw input text.

    Returns:
        str: Cleaned and normalized text.
    """

    if not isinstance(text, str):
        text = str(text)

    # Step 1: Normalize Unicode (e.g., accented letters → plain form)
    text = unicodedata.normalize("NFKD", text)

    # Step 2: Remove HTML entities like &nbsp; or &amp;
    text = re.sub(r"&\w+;", " ", text)

    # Step 3: Remove all non-alphanumeric characters (except basic punctuation)
    text = re.sub(r"[^a-zA-Z0-9.,!?;:()\[\]\s]", " ", text)

    # Step 4: Remove multiple punctuation marks (like "!!!", "??", etc.)
    text = re.sub(r"([.,!?;:])\1+", r"\1", text)

    # Step 5: Replace multiple spaces/newlines/tabs with single space
    text = re.sub(r"\s+", " ", text)

    # Step 6: Trim spaces from ends
    text = text.strip()

    return text
