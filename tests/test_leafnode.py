import unittest

from src.htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        # Verify that a normal leaf node renders an opening and closing tag.
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        # Verify that leaf nodes include serialized props in the opening tag.
        node = LeafNode(
            "a",
            "Boot.dev",
            {"href": "https://www.boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.boot.dev" target="_blank">Boot.dev</a>',
        )

    def test_leaf_to_html_no_tag_returns_text(self):
        # Verify that untagged leaf nodes render as plain escaped text.
        node = LeafNode(None, "plain text")
        self.assertEqual(node.to_html(), "plain text")

    def test_leaf_to_html_escapes_text_content(self):
        # Verify that tagged leaf text is escaped before rendering.
        node = LeafNode("p", '5 < 7 & "quoted"')
        self.assertEqual(node.to_html(), "<p>5 &lt; 7 &amp; &quot;quoted&quot;</p>")

    def test_leaf_to_html_escapes_plain_text_nodes(self):
        # Verify that plain text leaf nodes are escaped before rendering.
        node = LeafNode(None, "safe < unsafe")
        self.assertEqual(node.to_html(), "safe &lt; unsafe")

    def test_leaf_to_html_renders_void_elements_without_closing_tag(self):
        # Verify that void elements such as img are rendered without a closing tag.
        node = LeafNode("img", "", {"src": "https://example.com/x.png", "alt": 'A "cat"'})
        self.assertEqual(
            node.to_html(),
            '<img src="https://example.com/x.png" alt="A &quot;cat&quot;">',
        )

    def test_leaf_to_html_no_value_raises_error(self):
        # Verify that leaf nodes require a value before rendering.
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        # Verify that the repr includes the leaf node fields for debugging.
        node = LeafNode("span", "Label", {"class": "badge"})
        self.assertEqual(
            node.__repr__(),
            "LeafNode(tag='span', value='Label', props={'class': 'badge'})",
        )


if __name__ == "__main__":
    unittest.main()
