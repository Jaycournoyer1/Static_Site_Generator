import os
from extract_markdown import extract_title
from markdown_blocks import markdown_to_html_node

"""
# markdown  → raw markdown text
# template  → template.html contents
# html_node → HTMLNode tree
# html      → final HTML string
# title     → page title

1. print what page is being generated
2. read markdown file
3. read template file
4. convert markdown → HTML
5. extract title
6. replace {{ Title }}
7. replace {{ Content }}
8. ensure destination directory exists
9. write final HTML file

"""


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    directory = os.path.dirname(dest_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(dest_path, "w") as f:
        f.write(template)
