import unittest

from extract_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images_single_match(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple_matches(self):
        text = (
            "Start ![first](https://a.com/1.png) middle "
            "![second](https://a.com/2.png) end"
        )
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("first", "https://a.com/1.png"), ("second", "https://a.com/2.png")],
            matches,
        )

    def test_extract_markdown_images_empty_alt_and_url(self):
        matches = extract_markdown_images("An empty image ![]() here")
        self.assertListEqual([("", "")], matches)

    def test_extract_markdown_images_no_match_for_plain_link(self):
        matches = extract_markdown_images("[link](https://example.com)")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_no_match_for_malformed_markdown(self):
        text = "Broken ![image](https://a.com and ![another](https://b.com"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_no_match_with_nested_brackets_or_parens(self):
        text = (
            "![with [brackets]](https://a.com/x.png) "
            "![ok](https://a.com/image(test).png)"
        )
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_multiline(self):
        text = "Before\n![multi line alt](https://a.com/img.png)\nAfter"
        matches = extract_markdown_images(text)
        self.assertListEqual([("multi line alt", "https://a.com/img.png")], matches)

    def test_extract_markdown_links_single_match(self):
        matches = extract_markdown_links("A [link](https://example.com) in text")
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_multiple_matches(self):
        text = "Read [first](https://a.com) then [second](https://b.com/path) now."
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("first", "https://a.com"), ("second", "https://b.com/path")], matches
        )

    def test_extract_markdown_links_empty_text_and_url(self):
        matches = extract_markdown_links("Edge case []()")
        self.assertListEqual([("", "")], matches)

    def test_extract_markdown_links_ignores_images(self):
        text = "![img](https://a.com/img.png) and [site](https://a.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("site", "https://a.com")], matches)

    def test_extract_markdown_links_no_match_for_malformed_markdown(self):
        text = "Broken [text](https://a.com and [other](https://b.com"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_no_match_with_nested_brackets_or_parens(self):
        text = "[with [brackets]](https://a.com) [ok](https://a.com/path(test))"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_ignores_double_exclamation_prefix(self):
        text = "!![not-a-link](https://a.com) but [real](https://b.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("real", "https://b.com")], matches)

    def test_extract_markdown_links_multiline(self):
        text = "Before\n[multi line link](https://a.com/path)\nAfter"
        matches = extract_markdown_links(text)
        self.assertListEqual([("multi line link", "https://a.com/path")], matches)

    def test_extract_title_basic_valid_h1(self):
        markdown = "# Hello World"
        title = extract_title(markdown)
        self.assertEqual("Hello World", title)

    def test_extract_title_h1_with_extra_whitespace(self):
        markdown = "#   Hello World   "
        title = extract_title(markdown)
        self.assertEqual("Hello World", title)

    def test_extract_title_h1_not_on_first_line(self):
        markdown = "Intro paragraph\n# Document Title\nMore text"
        title = extract_title(markdown)
        self.assertEqual("Document Title", title)

    def test_extract_title_returns_first_h1_when_multiple_exist(self):
        markdown = "# First Title\n## Subtitle\n# Second Title"
        title = extract_title(markdown)
        self.assertEqual("First Title", title)

    def test_extract_title_ignores_non_h1_headings(self):
        markdown = "## Section Title\n### Smaller Heading\n# Actual Title"
        title = extract_title(markdown)
        self.assertEqual("Actual Title", title)

    def test_extract_title_allows_empty_h1_title(self):
        markdown = "#   "
        title = extract_title(markdown)
        self.assertEqual("", title)

    def test_extract_title_raises_exception_when_no_h1_present(self):
        markdown = "Paragraph text\n## Section Title\n- List item"
        with self.assertRaisesRegex(Exception, "no h1 header"):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
