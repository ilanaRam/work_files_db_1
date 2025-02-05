import os
from typing import Union, List, Dict
    

class FilesToDict:
    """
    class reads files from a dcitionary 
    hh(should be  a part of the project in Git) and arranges in the dict + adds to dict
    """

    def __init__(self):
        self.working_path: str = None
        self.files_dict: Dict = {}

    def set_working_path(self, working_path: str):
        self.working_path = working_path
        print(f"\n\nWorking folder defined as: {working_path}")

    def validate_tests_folder(self) -> bool:
        print(f"\n\nChecking if the given path exists: {self.working_path} .....\n\n")

        # this method check if path exists in file system - path can be to a file or a folder
        if os.path.exists(self.working_path):
            print(f"Path exists!")
            return True
        else:
            print(f"Path does not exist #####")
            return False

    def get_files_from_path_into_list(self) -> Union[bool, List[str]]:
        print(f"Creating a list of files ...")
        files_list = []

        for root, dirs, files in os.walk(self.working_path):
            print(f"The root folder path: {root}")
            if not os.listdir(root):
                print(f"The folder {root}, is empty @@@")
                files_list.append(root)
                continue

            for file_name in files:
                print(f"The file name (only): {file_name}")

                full_file_path = os.path.join(root, file_name)
                print(f"Full file path: {full_file_path} - added into a list")
                files_list.append(full_file_path)

                # this function returns the 'directory portion of the path', removing the file name
                # if a file already a folder path without a file name - then will return same path
                path_file_only = os.path.dirname(full_file_path)
                print(f"Only the path of the file: {path_file_only}\n\n")
                # for exp: C:\Users\PRIVATE_ILANA\PHYTHON_HOW_TO\from_interviews\Files_Travers\files_folder\protectedCacheH

        if not files_list:
            print(f"The list is empty")
            return False

        print("\nThe list is: ")
        [print(file) for file in files_list]
        return (files_list)

    def get_files_from_list_into_dict(self, files_list: List[str]) -> bool:
        if not files_list:
            print(f"The list of files is empty - no file to create a dict")
            return False

        print(f"Creating a dict from a list of files ...")
        for item in files_list:
            # check if this is full path to a file
            if not os.path.isdir(item):
                dir_to_file = os.path.dirname(item)
                print(f"Path to a file: {dir_to_file}")

                folder_one_level_up = os.path.basename(dir_to_file)
                print(f"folder one level up: {folder_one_level_up}")

                file_name_only = os.path.basename(item)
                print(f"file name only: {file_name_only}\n")

                self.files_dict.setdefault(folder_one_level_up, []).append(file_name_only)

        if len(self.files_dict) == 0:
            print(f"The list of files is empty - no file to create a dict")
            return False
        return True

    def print_dict(self):
        print(f"The len of the dict is: {len(self.files_dict)}")
        print("\nThe dict is: ")
        for folder, file_name in self.files_dict.items():
            print(f"{folder} : {file_name}")