import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        # Verify that missing props serialize to an empty string.
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty(self):
        # Verify that an empty props dictionary serializes to an empty string.
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_multiple_props(self):
        # Verify that multiple props are serialized in attribute form.
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_escapes_attribute_values(self):
        # Verify that special characters in attribute values are HTML-escaped.
        node = HTMLNode(props={"title": '5 < 7 & "quoted"'})
        self.assertEqual(node.props_to_html(), ' title="5 &lt; 7 &amp; &quot;quoted&quot;"')

    def test_repr(self):
        # Verify that the repr includes the node fields for debugging.
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )


if __name__ == "__main__":
    unittest.main()
