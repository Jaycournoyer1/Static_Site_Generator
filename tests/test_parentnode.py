import unittest

from src.htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        # Verify that a parent node renders its direct child inside the parent tag.
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        # Verify that nested parent-child structures render recursively.
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        # Verify that multiple children render in the original order.
        child_1 = LeafNode("span", "first")
        child_2 = LeafNode("b", "second")
        child_3 = LeafNode(None, "raw-text")
        parent_node = ParentNode("div", [child_1, child_2, child_3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>first</span><b>second</b>raw-text</div>",
        )

    def test_to_html_with_nested_parentnode_siblings(self):
        # Verify that sibling parent branches are rendered one after another.
        left_branch = ParentNode("section", [LeafNode("p", "left")])
        right_branch = ParentNode("section", [LeafNode("p", "right")])
        root = ParentNode("main", [left_branch, right_branch])
        self.assertEqual(
            root.to_html(),
            "<main><section><p>left</p></section><section><p>right</p></section></main>",
        )

    def test_to_html_with_deep_nesting(self):
        # Verify that deeply nested parent nodes still render correctly.
        root = ParentNode(
            "div",
            [
                ParentNode(
                    "article",
                    [
                        ParentNode(
                            "section",
                            [
                                LeafNode("span", "deep"),
                            ],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(
            root.to_html(),
            "<div><article><section><span>deep</span></section></article></div>",
        )

    def test_to_html_with_parent_props(self):
        # Verify that parent node props are serialized on the wrapper element.
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], {"class": "wrapper", "id": "container"})
        self.assertEqual(
            parent.to_html(),
            '<div class="wrapper" id="container"><span>child</span></div>',
        )

    def test_to_html_with_no_children_list_raises(self):
        # Verify that parent nodes require a children list before rendering.
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_tag_raises(self):
        # Verify that parent nodes require a tag before rendering.
        parent_node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_empty_children_list(self):
        # Verify that an empty children list renders as an empty element.
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_empty_tag_string(self):
        # Verify that an empty tag string is rendered literally.
        parent_node = ParentNode("", [LeafNode("span", "child")])
        self.assertEqual(parent_node.to_html(), "<><span>child</span></>")


if __name__ == "__main__":
    unittest.main()
