import unittest

from src.textnode import TextNode, TextType
from src.splitnodesdelimiter import split_nodes_image


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images_multiple(self):
        # Verify that multiple images are split out of one text node in order.
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_none(self):
        # Verify that text without images is returned unchanged.
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_non_text_passthrough(self):
        # Verify that non-text nodes are passed through untouched.
        node = TextNode("bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_at_start(self):
        # Verify that an image at the start becomes an image node followed by text.
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_at_end(self):
        # Verify that an image at the end becomes trailing image output.
        node = TextNode(
            "before ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_back_to_back(self):
        # Verify that adjacent images are both extracted without extra empty text nodes.
        node = TextNode(
            "x ![a](https://a.com/a.png)![b](https://a.com/b.png) y",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("x ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "https://a.com/a.png"),
                TextNode("b", TextType.IMAGE, "https://a.com/b.png"),
                TextNode(" y", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
