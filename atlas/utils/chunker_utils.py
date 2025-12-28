import re


def slugify(text: str) -> str:
    """
    Converts a string to a slug by:
    - Lowercasing the text
    - Replacing spaces and non-word characters with underscores
    - Stripping leading and trailing underscores

    Eg: "Section 1: Introduction!" -> "section_1_introduction"

    Args:
        text (str): The input text to slugify.

    Returns:
        str: The slugified text.
    """
    return re.sub(r"[^\w]+", "_", text.lower()).strip("_")
