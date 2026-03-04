from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Split plain-text nodes by a delimiter and label delimited segments with `text_type`."""
    new_nodes = []  # Collect transformed nodes while preserving original order.

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:  # Leave pre-typed nodes untouched.
            new_nodes.append(node)  # Carry non-text nodes forward as-is.
        else:
            parts = node.text.split(delimiter)  # Break text around delimiter markers.

            if len(parts) % 2 == 0:  # Even section count means an unmatched opening/closing delimiter.
                raise Exception("that's invalid Markdown syntax")

            for i, part in enumerate(parts):
                if part == "":  # Ignore empty pieces created by adjacent delimiters.
                    continue

                if i % 2 == 0:  # Even positions are outside delimiters (normal text).
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))  # Odd positions are inside delimiters.

    return new_nodes  # Return the fully split list.


def split_nodes_image(old_nodes):
    """Split plain-text nodes into text and image nodes based on Markdown image syntax."""
    new_nodes = []  # Collect output nodes after image extraction.

    for node in old_nodes:
        if node.text_type != TextType.TEXT:  # Skip nodes that are already typed.
            new_nodes.append(node)
            continue  # Move to the next node.

        images = extract_markdown_images(node.text)  # Find all Markdown images in the text.
        if len(images) == 0:  # No image syntax found; keep original node unchanged.
            new_nodes.append(node)
            continue

        remainging_text = node.text  # Track the unprocessed tail as each image is consumed.
        for alt, url in images:
            image_markdown = f"![{alt}]({url})"  # Rebuild exact Markdown substring to split on.
            sections = remainging_text.split(image_markdown, 1)  # Split into text-before and text-after.

            if len(sections) != 2:  # Must produce exactly [before, after] for valid parsing.
                raise ValueError("invalid markdown, image section not closed")

            if sections[0] != "":  # Keep any leading plain text before this image.
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))  # Convert image Markdown into IMAGE node.
            remainging_text = sections[1]  # Continue parsing from the remaining suffix.

        if remainging_text != "":  # Append leftover plain text after the final image.
            new_nodes.append(TextNode(remainging_text, TextType.TEXT))

    return new_nodes  # Return mixed TEXT/IMAGE nodes.


def split_nodes_link(old_nodes):
    """Split plain-text nodes into text and link nodes based on Markdown link syntax."""
    new_nodes = []  # Collect output nodes after link extraction.

    for node in old_nodes:
        if node.text_type != TextType.TEXT:  # Skip nodes that are already typed.
            new_nodes.append(node)
            continue  # Move to the next node.

        links = extract_markdown_links(node.text)  # Find all Markdown links in the text.
        if len(links) == 0:  # No link syntax found; keep original node unchanged.
            new_nodes.append(node)
            continue

        remaining_text = node.text  # Track the unprocessed tail as each link is consumed.
        for text, url in links:
            link_markdown = f"[{text}]({url})"  # Rebuild exact Markdown substring to split on.
            sections = remaining_text.split(link_markdown, 1)  # Split into text-before and text-after.

            if len(sections) != 2:  # Must produce exactly [before, after] for valid parsing.
                raise ValueError("invalid markdown, image section not closed")

            if sections[0] != "":  # Keep any leading plain text before this link.
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(text, TextType.LINK, url))  # Convert link Markdown into LINK node.
            remaining_text = sections[1]  # Continue parsing from the remaining suffix.

        if remaining_text != "":  # Append leftover plain text after the final link.
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes  # Return mixed TEXT/LINK nodes.
