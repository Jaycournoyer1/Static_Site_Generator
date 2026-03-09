import unittest

from textnode import TextNode, TextType
from splitnodesdelimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_delimited_section_in_text_node(self):
        nodes = [TextNode("This is `code` text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimited_sections_in_one_node(self):
        nodes = [TextNode("A `x` and `y` test", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("x", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("y", TextType.CODE),
            TextNode(" test", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_non_text_nodes_are_left_unchanged(self):
        bold = TextNode("already bold", TextType.BOLD)
        nodes = [bold]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [bold])

    def test_mixed_text_and_non_text_nodes(self):
        nodes = [
            TextNode("before", TextType.TEXT),
            TextNode("locked", TextType.BOLD),
            TextNode("`code` after", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("before", TextType.TEXT),
            TextNode("locked", TextType.BOLD),
            TextNode("code", TextType.CODE),
            TextNode(" after", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiter_returns_same_text_content(self):
        nodes = [TextNode("plain text only", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [TextNode("plain text only", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_unmatched_delimiter_raises_exception(self):
        nodes = [TextNode("This is `broken", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "`", TextType.CODE)

    def test_adjacent_delimited_sections(self):
        nodes = [TextNode("`a``b`", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("a", TextType.CODE),
            TextNode("b", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_delimiter_at_start_and_end(self):
        nodes = [TextNode("`only`", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [TextNode("only", TextType.CODE)]
        self.assertEqual(result, expected)

    def test_empty_input_returns_empty_output(self):
        result = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(result, [])

    def test_empty_text_node_results_in_no_nodes(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
