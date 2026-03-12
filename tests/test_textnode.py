import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # Verify that text nodes with the same values compare equal.
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        # Verify that different text values make nodes unequal.
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node!", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        # Verify that different text types make nodes unequal.
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        # Verify that matching URLs are included in equality checks.
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        # Verify that different URLs make nodes unequal.
        node = TextNode("This is a text node", TextType.LINK, "https://a.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://b.com")
        self.assertNotEqual(node, node2)

    def test_default_url_equals_none(self):
        # Verify that an omitted URL compares the same as an explicit None.
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT, url=None)
        self.assertEqual(node, node2)

    def test_repr(self):
        # Verify that repr includes the URL when one is present.
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual("TextNode(This is a text node, text, https://www.boot.dev)", repr(node))

    def test_repr_no_url(self):
        # Verify that repr shows None when no URL is present.
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual("TextNode(This is a text node, text, None)", repr(node))


if __name__ == "__main__":
    unittest.main()
