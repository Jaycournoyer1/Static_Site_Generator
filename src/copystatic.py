import os
import shutil


def copy_static(src_dir, dest_dir):
    """Recursively copy all files and folders from the static directory."""
    if not os.path.exists(dest_dir):  # Create the destination folder if it does not exist yet.
        os.mkdir(dest_dir)  # Make the destination directory for copied files.

    for item in os.listdir(src_dir):  # Loop through every file and folder in the source directory.
        source_path = os.path.join(src_dir, item)  # Build the full path to the current source item.
        dest_path = os.path.join(dest_dir, item)  # Build the full path where the item should be copied.

        if os.path.isfile(source_path):  # Copy the item directly if it is a file.
            print(f"Copying {source_path} -> {dest_path}")  # Show which file is being copied.
            shutil.copy(source_path, dest_path)  # Copy the file into the destination directory.
        else:  # Recurse if the item is another directory.
            copy_static(source_path, dest_path)  # Copy the contents of the nested directory.
