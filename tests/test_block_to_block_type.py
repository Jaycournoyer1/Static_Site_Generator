import unittest

from src.blocktype import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph_single_line(self):
        # Verify that a plain one-line block is classified as a paragraph.
        block = "Just a normal paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_empty_block(self):
        # Verify that an empty block falls back to paragraph classification.
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_multi_line_plain_text(self):
        # Verify that multi-line plain text still counts as a paragraph block.
        block = "Line one\nLine two\nLine three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_level_1(self):
        # Verify that a single hash heading is detected as a heading block.
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_level_6(self):
        # Verify that a level-six heading is still treated as a heading block.
        block = "###### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_missing_required_space_is_paragraph(self):
        # Verify that headings without a space after the hashes are rejected.
        block = "###Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_more_than_six_hashes_is_paragraph(self):
        # Verify that headings deeper than six hashes are not accepted.
        block = "####### Too many"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_with_no_text_is_still_heading(self):
        # Verify that a heading marker with empty text is still a heading block.
        block = "### "
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        # Verify that fenced code blocks are classified as code.
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_empty_body(self):
        # Verify that an empty fenced code block is still classified as code.
        block = "```\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_must_have_newline_after_open_fence(self):
        # Verify that the opening fence must be followed by a newline.
        block = "```print('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_missing_closing_fence_is_paragraph(self):
        # Verify that an unterminated fence does not count as a code block.
        block = "```\nprint('hi')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block(self):
        # Verify that blocks whose lines all start with ">" are classified as quotes.
        block = "> quote line 1\n>quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_allows_bare_gt_lines(self):
        # Verify that quote lines containing only ">" still count as a quote block.
        block = ">\n>"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_mixed_lines_is_paragraph(self):
        # Verify that mixed quoted and unquoted lines fall back to paragraph.
        block = "> quoted\nnot quoted"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        # Verify that dash-prefixed lines are classified as an unordered list.
        block = "- a\n- b\n- c"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_allows_empty_items(self):
        # Verify that empty unordered list items are still accepted.
        block = "- \n- "
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_wrong_marker_is_paragraph(self):
        # Verify that inconsistent list markers break unordered-list detection.
        block = "- a\n* b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_requires_space_after_dash(self):
        # Verify that a dash must be followed by a space to count as a list item.
        block = "-a\n-b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        # Verify that sequential numeric markers create an ordered list block.
        block = "1. a\n2. b\n3. c"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_single_item(self):
        # Verify that a one-item ordered list is still recognized.
        block = "1. only"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_must_start_at_one(self):
        # Verify that ordered lists must start numbering at one.
        block = "2. a\n3. b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_must_increment_by_one(self):
        # Verify that ordered list numbers must increase sequentially.
        block = "1. a\n3. b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_requires_space_after_period(self):
        # Verify that ordered list markers require a space after the period.
        block = "1.a\n2.b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_marker_can_be_overridden_by_heading_precedence(self):
        # Verify that heading syntax takes precedence over ordered-list syntax.
        block = "# 1. Not an ordered list"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_precedence_over_other_block_types(self):
        # Verify that fenced code takes precedence over other embedded block markers.
        block = "```\n# heading\n> quote\n- item\n1. item\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_heading_precedence_over_quote(self):
        # Verify that heading syntax is chosen before quote parsing.
        block = "# > not quote"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_quote_precedence_over_unordered_list(self):
        # Verify that quote syntax wins over unordered-list syntax inside quoted lines.
        block = "> - item\n> - item two"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_precedence_over_ordered_list(self):
        # Verify that unordered-list detection wins when lines start with "- ".
        block = "- 1. one\n- 2. two"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)


if __name__ == "__main__":
    unittest.main()
