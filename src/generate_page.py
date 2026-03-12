import os
from pathlib import Path
from extract_markdown import extract_title
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path, basepath):
    """Build one HTML page from a Markdown file and an HTML template."""
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")  # Show which file is being converted.

    with open(from_path) as f:  # Open the source Markdown file for reading.
        markdown = f.read()  # Load the entire Markdown file into memory.

    with open(template_path) as f:  # Open the HTML template file for reading.
        template = f.read()  # Load the template contents into memory.

    html_node = markdown_to_html_node(markdown)  # Convert Markdown text into an HTML node tree.
    html = html_node.to_html()  # Render the HTML node tree into an HTML string.

    title = extract_title(markdown)  # Pull the page title from the Markdown h1 heading.

    template = template.replace("{{ Title }}", title)  # Fill the title placeholder in the template.
    template = template.replace("{{ Content }}", html)  # Fill the content placeholder with generated HTML.
    template = template.replace('href="/', f'href="{basepath}')  # Rewrite root-relative links to include the configured base path.
    template = template.replace('src="/', f'src="{basepath}')  # Rewrite root-relative asset paths to include the configured base path.

    directory = os.path.dirname(dest_path)  # Get the output folder for the final HTML file.
    if not os.path.exists(directory):  # Create the folder path if it does not already exist.
        os.makedirs(directory)  # Make any missing directories in the destination path.

    with open(dest_path, "w") as f:  # Open the destination HTML file for writing.
        f.write(template)  # Save the completed HTML page.

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    """Walk the content tree and generate HTML pages for every Markdown file."""
    for filename in os.listdir(dir_path_content):  # Loop through each item in the current content directory.
        from_path = os.path.join(dir_path_content, filename)  # Build the source path for this item.
        dest_path = os.path.join(dest_dir_path, filename)  # Build the matching destination path.

        if os.path.isdir(from_path):  # If the current item is a directory, recurse into it.
            if not os.path.exists(dest_path):  # Create the matching output directory when needed.
                os.mkdir(dest_path)  # Make the destination folder for nested content.
            generate_pages_recursive(from_path, template_path, dest_path, basepath)  # Process all files inside the subdirectory.

        elif filename.endswith(".md"):  # Convert only Markdown files into HTML pages.
            dest_path = Path(dest_path).with_suffix(".html")  # Swap the Markdown extension for .html in the output path.
            generate_page(from_path, template_path, dest_path, basepath)  # Generate the HTML file for this Markdown source.
