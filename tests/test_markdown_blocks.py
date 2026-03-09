import unittest

from markdown_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string_returns_no_blocks(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_whitespace_only_returns_no_blocks(self):
        md = "   \n\n\t\n\n  "
        self.assertEqual(markdown_to_blocks(md), [])

    def test_leading_and_trailing_blank_lines_are_ignored(self):
        md = "\n\n  First block  \n\nSecond block\n\n"
        self.assertEqual(markdown_to_blocks(md), ["First block", "Second block"])

    def test_multiple_blank_lines_between_blocks(self):
        md = "First\n\n\n\nSecond"
        self.assertEqual(markdown_to_blocks(md), ["First", "Second"])

    def test_single_newlines_do_not_split_blocks(self):
        md = "line one\nline two\nline three"
        self.assertEqual(markdown_to_blocks(md), ["line one\nline two\nline three"])

    def test_preserves_internal_spacing_within_block(self):
        md = "First line\n  indented line\n\tTabbed line"
        self.assertEqual(markdown_to_blocks(md), ["First line\n  indented line\n\tTabbed line"])

    def test_trims_whitespace_around_each_block(self):
        md = "   block one   \n\n\t block two\t"
        self.assertEqual(markdown_to_blocks(md), ["block one", "block two"])

    def test_crlf_double_newlines_do_not_split(self):
        md = "first\r\n\r\nsecond"
        self.assertEqual(markdown_to_blocks(md), ["first\r\n\r\nsecond"])
