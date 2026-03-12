import os
import sys
import shutil
from .copystatic import copy_static
from .generate_page import generate_pages_recursive

dir_path_static = "./static"  # Store the folder that contains images, CSS, and other static files.
dir_path_public = "./docs"  # Store the output folder where the generated site will be written.
dir_path_content = "./content"  # Store the folder that contains the Markdown source files.
template_path = "./template.html"  # Store the HTML template used for every generated page.


def main():
    """Rebuild the public site by copying assets and generating HTML pages."""

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"  # Use the first CLI argument as the site base path, or "/" by default.

    print("Deleting public directory")  # Announce that the old output folder is being removed.
    if os.path.exists(dir_path_public):  # Remove the old public folder if it already exists.
        shutil.rmtree(dir_path_public)  # Delete the public directory and everything inside it.

    print("Copying static files to public directory")  # Announce that static assets are being copied.
    copy_static(dir_path_static, dir_path_public)  # Copy images, CSS, and other static files into public.

    print("Page Generating")  # Announce that Markdown pages are being converted to HTML.
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)  # Build the full site from the content folder.


if __name__ == "__main__":
    main()  # Run only when this file is executed directly.
