import unittest

from src.textnode import TextNode, TextType
from src.splitnodesdelimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_delimited_section_in_text_node(self):
        # Verify that one delimited section is split into text-code-text nodes.
        nodes = [TextNode("This is `code` text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimited_sections_in_one_node(self):
        # Verify that multiple delimited sections are split in order.
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
        # Verify that non-text nodes are passed through unchanged.
        bold = TextNode("already bold", TextType.BOLD)
        nodes = [bold]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [bold])

    def test_mixed_text_and_non_text_nodes(self):
        # Verify that only plain text nodes are split when the list mixes node types.
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
        # Verify that text without delimiters is returned unchanged.
        nodes = [TextNode("plain text only", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [TextNode("plain text only", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_unmatched_delimiter_raises_exception(self):
        # Verify that unmatched delimiters raise an exception.
        nodes = [TextNode("This is `broken", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "`", TextType.CODE)

    def test_adjacent_delimited_sections(self):
        # Verify that adjacent delimited sections produce adjacent formatted nodes.
        nodes = [TextNode("`a``b`", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("a", TextType.CODE),
            TextNode("b", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_delimiter_at_start_and_end(self):
        # Verify that delimiters at the string boundaries still produce one formatted node.
        nodes = [TextNode("`only`", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [TextNode("only", TextType.CODE)]
        self.assertEqual(result, expected)

    def test_empty_input_returns_empty_output(self):
        # Verify that an empty node list returns an empty result.
        result = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(result, [])

    def test_empty_text_node_results_in_no_nodes(self):
        # Verify that an empty text node contributes no output nodes.
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
