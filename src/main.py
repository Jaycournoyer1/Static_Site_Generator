import os
import shutil
from copystatic import copy_static
from generate_page import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    """Rebuild the public site by copying assets and generating HTML pages."""
    print("Deleting public directory")  # Announce that the old output folder is being removed.
    if os.path.exists(dir_path_public):  # Remove the old public folder if it already exists.
        shutil.rmtree(dir_path_public)  # Delete the public directory and everything inside it.

    print("Copying static files to public directory")  # Announce that static assets are being copied.
    copy_static(dir_path_static, dir_path_public)  # Copy images, CSS, and other static files into public.

    print("Page Generating")  # Announce that Markdown pages are being converted to HTML.
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)  # Build the full site from the content folder.


if __name__ == "__main__":
    main()  # Run only when this file is executed directly.
