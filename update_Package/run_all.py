import os
from update_Package import data_fetcher, file_reader, data_updater, cleaner_manager

def execute_scripts():
    """Run scripts sequentially."""
    print("Running scripts...")
    data_fetcher
    file_reader
    data_updater

def cleanup():
    """Delete unnecessary files after execution."""
    cleaner_manager.delete_temp_files()

# ✅ Ensure this is correct to prevent double execution
if __name__ == "__main__":  
    execute_scripts()
    cleanup()
    print("All scripts executed and cleanup done.")
