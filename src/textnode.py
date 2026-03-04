from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    """Enumerates the supported semantic types for inline text content."""

    TEXT = "text"  # Unformatted plain text.
    BOLD = "bold"  # Bold emphasis text.
    ITALIC = "italic"  # Italic emphasis text.
    CODE = "code"  # Inline code text.
    LINK = "link"  # Clickable hyperlink text.
    IMAGE = "image"  # Image reference (uses text as alt text).


class TextNode:
    """Container for parsed inline text plus its semantic type and optional URL."""

    def __init__(self, text, text_type, url=None):
        self.text = text  # Visible text content or alt text.
        self.text_type = text_type  # Value from TextType defining semantic meaning.
        self.url = url  # Optional URL used by LINK and IMAGE nodes.

    def __eq__(self, other):
        """Support value-based equality checks for testing and comparisons."""
        if not isinstance(other, TextNode):  # Different object types are never equal.
            return False

        return self.text == other.text and self.text_type == other.text_type and self.url == other.url  # Compare fields.

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"  # Developer-friendly debug string.


def text_node_to_html_node(text_node):
    """Map a `TextNode` into its corresponding `LeafNode` HTML representation."""
    if text_node.text_type == TextType.TEXT:  # Plain text maps to untagged leaf content.
        return LeafNode(None, text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)  # Bold text maps to <b>.

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)  # Italic text maps to <i>.

    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)  # Code text maps to <code>.

    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})  # Link text maps to <a href="...">.

    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})  # Image maps to <img src alt>.

    else:
        raise ValueError(f"invalid text type: {text_node.text_type}")  # Guard against unknown types.
