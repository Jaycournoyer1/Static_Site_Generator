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
    """Return the text from the first Markdown h1 heading."""
    lines = markdown.split("\n")  # Break the Markdown string into individual lines.
    
    for line in lines:  # Check each line until an h1 heading is found.
        if line.startswith("# "):  # Match only top-level headings that begin with "# ".
            return line[2:].strip()  # Remove the "# " prefix and surrounding whitespace.
    raise Exception("no h1 header")  # Fail if the Markdown file does not contain an h1 title.
