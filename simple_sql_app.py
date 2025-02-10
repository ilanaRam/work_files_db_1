import os
import time
import src.data_base as db
from src.model import my_file_model
import pytest
from src.travers_path_get_files import FilesToDict

WORKING_DIR = r"/resources/Files_Travers/files_folder"



def main():
    # Initialize the database
    db_name = "files_store.db"
    database = db.DataBase(db_name)# after this step, the connection to sqlite will be created + cursorto execute queries to db will be ready
    
    # Use FilesToDict to find file paths    
    files_to_dict_obj = FilesToDict()
    
    print("\n\n-- Preparing the files: ---------\n\n")
    if not files_to_dict_obj.validate_tests_folder(WORKING_DIR):
        print(f"The working directory: {WORKING_DIR}, does not exist ###")
        raise FileNotFoundError(f"The working directory: {WORKING_DIR}, does not exist ###")    
    files_to_dict_obj.set_working_path(WORKING_DIR)   

    files_list = files_to_dict_obj.get_files_from_path_into_list()    
    if not files_to_dict_obj.get_files_from_list_into_dict(files_list):
        print(f"Failed to create a dict from test files ###")
        raise Exception(f"Failed to create a dict from test files ###")        
    files_to_dict_obj.print_dict()    
    files_dict = files_to_dict_obj.get_files_dict()
   
    # Insert file paths into the database
    print("\n\n-- Inserting files into SSQLite data base: ---------\n\n")
    for folder, file_list in files_dict.items():
        print(f"\nFolder is: {folder}")
        for file in file_list:
            print(f"File is: {file}")
            date = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Date is: {date}")
            database.insert(source_file=file, date=date)   
        
    print("\n\n-- Retrieving (and printing) the files from SQLite database: ---------\n\n")
    # Optionally, retrieve and print all files from the database
    all_files = database.get_all_files()
    for file in all_files:
        print(f"File: {file.source_file}, Date: {file.date}")
    
    print("\n\n-- Preparing SQLite file database: ---------\n\n")
    database.write_sql_file()    
    
    # Close the database connection
    database.close()


if __name__ == '__main__':
    # pytest.main()  # <---- this way main will run after all tests will be executed
    main()