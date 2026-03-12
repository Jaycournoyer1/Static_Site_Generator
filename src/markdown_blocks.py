from text_to_nodes import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import ParentNode, LeafNode
from blocktype import BlockType, block_to_block_type


def markdown_to_blocks(markdown):
    """Split markdown text into non-empty blocks separated by blank lines."""

    blocks = []  # Final list of cleaned, non-empty block strings.
    pieces = markdown.split("\n\n")  # Split only on double newlines (blank-line boundaries).

    for piece in pieces:
        block = (piece.strip())  # Remove outer whitespace/newlines from each candidate block.
        if block != "":
            blocks.append(block)  # Keep only meaningful blocks.
    return blocks  # Return blocks in original order.


def markdown_to_html_node(markdown):
    """Convert full markdown text into a root HTML div node."""
    blocks = markdown_to_blocks(markdown)  # Break document into logical block chunks.
    block_nodes = []  # Collect one HTML node per markdown block.
    for block in blocks:  # Convert each block by detected markdown block type.
        block_type = block_to_block_type(block)  # Classify block (heading, list, etc.).

        if block_type == BlockType.HEADING:
            node = heading_block_to_html_node(block)  # Map heading block to <h1>-<h6>.

        elif block_type == BlockType.PARAGRAPH:
            node = paragraph_block_to_html_node(block)  # Map paragraph block to <p>.

        elif block_type == BlockType.QUOTE:
            node = quote_block_to_html_node(block)  # Map quote block to <blockquote>.

        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_to_html_node(block)  # Map unordered list block to <ul>.

        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_to_html_node(block)  # Map ordered list block to <ol>.

        elif block_type == BlockType.CODE:
            node = code_block_to_html_node(block)  # Map fenced code block to <pre><code>.

        block_nodes.append(node)  # Keep converted block in document order.

    return ParentNode("div", block_nodes)  # Wrap all block nodes under a single root.


""" Helper functions for markdown_to_html_node() """

def text_to_children(text):
    """Convert inline markdown text into a list of HTML child nodes."""
    text_nodes = text_to_textnodes(text)  # Parse inline markdown into text node objects.
    children = []  # Store HTML nodes converted from each text node.
    for node in text_nodes:  # Convert every parsed text node into an HTML node.
        children.append(text_node_to_html_node(node))  # Preserve original inline ordering.
    return children  # Return the HTML-ready children for a parent node.


def heading_block_to_html_node(block):
    """Convert a markdown heading block into an HTML heading node."""
    heading_marks, heading_text = block.split(" ", 1)  # Separate hashes from heading text.
    level = len(heading_marks)  # Heading level equals number of # characters.
    children = text_to_children(heading_text)  # Parse heading inline markdown content.
    return ParentNode(f"h{level}", children)  # Build matching <h1>-<h6> parent node.


def paragraph_block_to_html_node(block):
    """Convert a markdown paragraph block into an HTML paragraph node."""
    normalized = " ".join(line.strip() for line in block.split("\n"))  # Fold lines into one.
    children = text_to_children(normalized)  # Parse inline formatting inside paragraph text.
    return ParentNode("p", children)  # Wrap parsed text in a <p> node.


def quote_block_to_html_node(block):
    """Convert a markdown quote block into an HTML blockquote node."""
    lines = block.split("\n")  # Split quote block into individual source lines.
    cleaned_lines = []  # Store quote lines with the markdown marker removed.
    for line in lines:  # Remove leading "> " from each quote line.
        cleaned_lines.append(line[2:])  # Keep only the quote text content.
    text = "\n".join(cleaned_lines)  # Reassemble quote text with line breaks preserved.
    children = text_to_children(text)  # Parse inline markdown inside the quote content.
    return ParentNode("blockquote", children)  # Wrap parsed quote text in <blockquote>.


def unordered_list_to_html_node(block):
    """Convert a markdown unordered list block into an HTML ul node."""
    lines = block.split("\n")  # Split the list block into one line per item.
    list_items = []  # Collect generated <li> nodes for the list.
    for line in lines:  # Convert each markdown bullet line into one list item.
        item_text = line[2:]  # Remove leading "- " bullet marker.
        children = text_to_children(item_text)  # Parse inline markdown inside item text.
        list_items.append(ParentNode("li", children))  # Add completed <li> node.
    return ParentNode("ul", list_items)  # Wrap all items in a <ul> node.


def ordered_list_to_html_node(block):
    """Convert a markdown ordered list block into an HTML ol node."""
    lines = block.split("\n")  # Split ordered list into one line per numbered item.
    list_items = []  # Collect generated <li> nodes.
    for line in lines:  # Process each numbered line in order.
        list_number, list_text = line.split(" ", 1)  # Split "1." token from item content.
        children = text_to_children(list_text)  # Parse inline markdown in item text.
        list_items.append(ParentNode("li", children))  # Store item as an <li> node.
    return ParentNode("ol", list_items)  # Wrap items in an <ol> node.


def code_block_to_html_node(block):
    """Convert a fenced markdown code block into <pre><code> HTML nodes."""
    lines = block.split("\n")  # Split entire fenced code block into lines.
    code_lines = lines[1:-1]  # Remove opening/closing triple-backtick fence lines.

    non_empty = [line for line in code_lines if line.strip() != ""]  # Ignore blank lines.
    common_indent = 0  # Default to no dedent if block has no non-empty lines.
    if non_empty:  # Find smallest leading-space indentation across content lines.
        common_indent = min(len(line) - len(line.lstrip(" ")) for line in non_empty)

    dedented = []  # Store code lines after removing shared leading indentation.
    for line in code_lines:  # Dedent every line by the common indent amount.
        if len(line) >= common_indent:  # Only slice when line length can support dedent.
            dedented.append(line[common_indent:])  # Remove shared leading spaces.
        else:
            dedented.append(line)  # Keep very short lines unchanged for safety.

    text = "\n".join(dedented) + "\n"  # Rebuild code text with a trailing newline.
    code_node = LeafNode("code", text)  # Create leaf <code> element containing raw text.
    return ParentNode("pre", [code_node])  # Wrap <code> inside <pre> for code blocks.
