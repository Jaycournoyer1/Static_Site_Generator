import unittest

from textnode import TextNode, TextType
from splitnodesdelimiter import split_nodes_link


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links_multiple(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and another [second link](https://blog.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://blog.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_non_text_passthrough(self):
        node = TextNode("bold", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_at_start(self):
        node = TextNode("[link](https://boot.dev) after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_end(self):
        node = TextNode("before [link](https://boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_back_to_back(self):
        node = TextNode("x [a](https://a.com)[b](https://b.com) y", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("x ", TextType.TEXT),
                TextNode("a", TextType.LINK, "https://a.com"),
                TextNode("b", TextType.LINK, "https://b.com"),
                TextNode(" y", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
