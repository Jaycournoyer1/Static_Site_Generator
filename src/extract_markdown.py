import re


def extract_markdown_images(text):
    """Extract all Markdown images as `(alt_text, url)` tuples from a string."""
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"  # Match ![alt](url) image syntax.
    matches = re.findall(pattern, text)  # Return every (alt, url) pair found in order.
    return matches  # Example: [("logo", "https://site/logo.png")].


def extract_markdown_links(text):
    """Extract all Markdown links as `(link_text, url)` tuples from a string."""
    pattern = (
        r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"  # Match [text](url), but not images.
    )
    matches = re.findall(pattern, text)  # Return every (text, url) pair found in order.
    return matches  # Example: [("Boot.dev", "https://boot.dev")].


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no h1 header")
