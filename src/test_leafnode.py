import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_with_props(self):
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
        node = LeafNode(None, "plain text")
        self.assertEqual(node.to_html(), "plain text")
        
    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
            
    def test_leaf_repr(self):
        node = LeafNode("span", "Label", {"class": "badge"})
        self.assertEqual(
            node.__repr__(),
            "LeafNode(tag='span', value='Label', props={'class': 'badge'})",
        )

if __name__ == "__main__":
    unittest.main()
