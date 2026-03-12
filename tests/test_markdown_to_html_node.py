import unittest

from src.markdown_blocks import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        # Verify that paragraphs render with inline formatting converted to HTML.
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        # Verify that fenced code blocks preserve their text and skip inline parsing.
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>    This is text that _should_ remain\n    the **same** even with inline stuff\n</code></pre></div>",
        )

    def test_codeblock_preserves_indentation(self):
        # Verify that indentation inside fenced code is preserved exactly.
        md = "```\n    def hello():\n        return 1\n```"

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>    def hello():\n        return 1\n</code></pre></div>",
        )

    def test_quote_block_without_space_after_marker(self):
        # Verify that quote lines without a space after ">" still render correctly.
        md = ">quote line 1\n>quote line 2"

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><blockquote>quote line 1\nquote line 2</blockquote></div>",
        )

    def test_html_output_is_escaped(self):
        # Verify that raw HTML-like text is escaped in the rendered output.
        md = "# <Title>\n\nParagraph with <b>raw</b> HTML & text."

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h1>&lt;Title&gt;</h1><p>Paragraph with &lt;b&gt;raw&lt;/b&gt; HTML &amp; text.</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
