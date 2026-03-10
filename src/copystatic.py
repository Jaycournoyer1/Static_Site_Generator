import os
import shutil


def copy_static(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    for item in os.listdir(src_dir):
        source_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            print(f"Copying {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            copy_static(source_path, dest_path)
