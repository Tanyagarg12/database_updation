import os
import glob

def delete_temp_files():
    """Remove temporary/generated files except important scripts."""
    files_to_keep = {"__init__.py", "run_all.py", "data_fetcher.py", "file_reader.py", "data_updater.py", "setup.py","requirements.txt","README.md"}
    all_files = glob.glob("*")

    for file in all_files:
        if file not in files_to_keep and os.path.isfile(file):
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")

