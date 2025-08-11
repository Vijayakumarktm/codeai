def clean_code_blocks(text):
    """
    Safely remove triple backtick code fences from LLM output.
    Handles ```js, ```jsx, or ``` alone at the start.
    """
    lines = text.strip().splitlines()

    # Remove the first line if it's a code fence
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]

    # Remove the last line if it's a closing fence
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    return "\n".join(lines).strip()
