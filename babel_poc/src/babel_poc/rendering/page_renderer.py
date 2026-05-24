import textwrap


def render_tokens(tokens: list[str], punctuation: set[str]) -> str:
    """
    Render tokens into readable text.
    - no space before punctuation
    - space after punctuation unless end of page
    - words separated by spaces
    """
    result: list[str] = []
    for token in tokens:
        if token in punctuation:
            if result:
                result[-1] = result[-1] + token
            else:
                result.append(token)
        else:
            result.append(token)
    return " ".join(result)


def wrap_text(text: str, width: int = 80) -> str:
    """Wrap text for terminal display."""
    return textwrap.fill(text, width=width)
