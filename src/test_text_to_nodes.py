import unittest

from textnode import TextNode, TextType
from text_to_nodes import text_to_textnodes


class TestTextToNodes(unittest.TestCase):
    def test_plain_text(self):
        result = text_to_textnodes("just text")
        expected = [TextNode("just text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_empty_string_returns_empty_list(self):
        result = text_to_textnodes("")
        self.assertEqual(result, [])

    def test_mixed_all_supported_types(self):
        result = text_to_textnodes(
            "This is **bold** and _italic_ with `code`, a [link](https://a.com), and ![img](https://a.com/img.png)."
        )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://a.com"),
            TextNode(", and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://a.com/img.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_back_to_back_inline_elements(self):
        result = text_to_textnodes(
            "**b**_i_`c`![img](https://a.com/i.png)[lnk](https://a.com)"
        )
        expected = [
            TextNode("b", TextType.BOLD),
            TextNode("i", TextType.ITALIC),
            TextNode("c", TextType.CODE),
            TextNode("img", TextType.IMAGE, "https://a.com/i.png"),
            TextNode("lnk", TextType.LINK, "https://a.com"),
        ]
        self.assertEqual(result, expected)

    def test_invalid_unmatched_bold_delimiter_raises(self):
        with self.assertRaises(Exception):
            text_to_textnodes("this is **broken")

    def test_invalid_unmatched_italic_delimiter_raises(self):
        with self.assertRaises(Exception):
            text_to_textnodes("this is _broken")

    def test_invalid_unmatched_code_delimiter_raises(self):
        with self.assertRaises(Exception):
            text_to_textnodes("this is `broken")

    def test_markdown_inside_non_text_node_is_not_reparsed(self):
        result = text_to_textnodes(
            "**bold [x](https://a.com) ![i](https://a.com/i.png) `c` _y_**"
        )
        expected = [
            TextNode(
                "bold [x](https://a.com) ![i](https://a.com/i.png) `c` _y_",
                TextType.BOLD,
            )
        ]
        self.assertEqual(result, expected)

    def test_image_and_link_parsed_from_text_node_after_delimiters(self):
        result = text_to_textnodes(
            "prefix _mid_ [x](https://a.com) ![i](https://a.com/i.png) suffix"
        )
        expected = [
            TextNode("prefix ", TextType.TEXT),
            TextNode("mid", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("x", TextType.LINK, "https://a.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("i", TextType.IMAGE, "https://a.com/i.png"),
            TextNode(" suffix", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
