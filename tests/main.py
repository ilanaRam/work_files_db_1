import src.data_base as db
from src.model import my_file_model
import pytest
from src.travers_path_get_files import FilesToDict


def main():
    # Initialize the database
    db_name = "files_store.db"
    database = db.DataBase(db_name)
    
    # Use FilesToDict to find file paths
    directory_to_search = "/path/to/your/directory"  # Replace with the directory you want to search
    files_to_dict = FilesToDict(directory_to_search)
    files_dict = files_to_dict.get_files_dict()
    
    # Insert file paths into the database
    for file_path in files_dict.values():
        source_file = file_path
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        database.insert(source_file=source_file, date=date)
    
    # Optionally, retrieve and print all files from the database
    all_files = database.get_all_files()
    for file in all_files:
        print(f"File: {file.source_file}, Date: {file.date}")
    
    # Close the database connection
    database.close()


if __name__ == __main__:
    pytest.main()