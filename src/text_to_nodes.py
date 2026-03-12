from .splitnodesdelimiter import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from .textnode import TextNode, TextType


def text_to_textnodes(text):
    """Convert raw markdown-like text into an ordered list of typed `TextNode` objects."""
    nodes = [TextNode(text, TextType.TEXT)]  # Start with one plain-text node containing the full input.

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)  # Convert **bold** segments.
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)  # Convert _italic_ segments.
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)  # Convert `code` segments.

    nodes = split_nodes_image(nodes)  # Convert ![alt](url) segments into IMAGE nodes.
    nodes = split_nodes_link(nodes)  # Convert [text](url) segments into LINK nodes.

    return nodes  # Return the fully tokenized node list.
