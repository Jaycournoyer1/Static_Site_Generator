import unittest

from blocktype import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph_single_line(self):
        block = "Just a normal paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_multi_line_plain_text(self):
        block = "Line one\nLine two\nLine three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_level_1(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_level_6(self):
        block = "###### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_missing_required_space_is_paragraph(self):
        block = "###Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_more_than_six_hashes_is_paragraph(self):
        block = "####### Too many"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_with_no_text_is_still_heading(self):
        block = "### "
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_empty_body(self):
        block = "```\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_must_have_newline_after_open_fence(self):
        block = "```print('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_missing_closing_fence_is_paragraph(self):
        block = "```\nprint('hi')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = "> quote line 1\n>quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_allows_bare_gt_lines(self):
        block = ">\n>"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_mixed_lines_is_paragraph(self):
        block = "> quoted\nnot quoted"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- a\n- b\n- c"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_allows_empty_items(self):
        block = "- \n- "
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_wrong_marker_is_paragraph(self):
        block = "- a\n* b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_requires_space_after_dash(self):
        block = "-a\n-b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. a\n2. b\n3. c"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_single_item(self):
        block = "1. only"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_must_start_at_one(self):
        block = "2. a\n3. b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_must_increment_by_one(self):
        block = "1. a\n3. b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_requires_space_after_period(self):
        block = "1.a\n2.b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_marker_can_be_overridden_by_heading_precedence(self):
        block = "# 1. Not an ordered list"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_precedence_over_other_block_types(self):
        block = "```\n# heading\n> quote\n- item\n1. item\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_heading_precedence_over_quote(self):
        block = "# > not quote"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_quote_precedence_over_unordered_list(self):
        block = "> - item\n> - item two"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_precedence_over_ordered_list(self):
        block = "- 1. one\n- 2. two"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)


if __name__ == "__main__":
    unittest.main()
