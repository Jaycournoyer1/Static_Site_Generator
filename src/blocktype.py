import re
from enum import Enum


class BlockType(Enum):
    """Enumerate the supported Markdown block-level node types."""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    """Classify a markdown block by checking the supported syntax patterns in order."""

    if block.startswith("```") and block.endswith("```"):
        # must start with ```\n (per spec)
        if block.startswith("```\n"):
            return BlockType.CODE

    # HEADING (1-6 # followed by space)
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    lines = block.split("\n")  # Split once so the remaining multi-line checks can reuse the same lines.

    # QUOTE: every line starts with >
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # UNORDERED LIST: every line starts with "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # ORDERED LIST: every line starts with "1. ", "2. ", ...
    is_ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH  # Treat anything unmatched as a normal paragraph block.
