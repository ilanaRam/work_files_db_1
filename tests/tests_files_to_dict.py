import datetime
import pytest
from src.travers_path_get_files import FilesToDict


class TestFilesToDict:    

    @pytest.fixture
    def files_obj(self):
        print("\n\n############### test - Started ###########")
        yield FilesToDict()
        print("\n############### test - Ended #############\n\n")
        

    #Parametrized fixture
    @pytest.mark.parametrize("files_path", # <---- this is a name of the fixture, each time the fixture will hold 1 path to test by a test
                            [
                                (r"\resources\Files_Travers\files_folder"),
                                (r"\resources\Files_Travers\files_folder_single_file")
                            ])
    def test_travers_path_get_all_files_existing_path_with_files(self, 
                                                                 files_obj, 
                                                                 files_path):
        print(f"The test param (path) is: {files_path}")
        assert files_obj.validate_tests_folder(files_path) is True, "Test failed, the validation of the test folder path"
        files_obj.set_working_path(files_path)   

        files_list = files_obj.get_files_from_path_into_list()
        assert len(files_list) > 0, "Test did not foind any test files"

        assert files_obj.get_files_from_list_into_dict(files_list) is True, "Test failed to create dict of tests files"
        files_obj.print_dict()

    # Parametrized fixture
    @pytest.mark.parametrize("files_path", # <---- this is a name of the fixture, each time the fixture will hold 1 path to test by a test
                            [
                                (r"\resources\Files_Travers\empty_files_folder"),
                                (r"\resources\Files_Travers\files_folder_with_empty_folder"),
                                (r"\resources\Files_Travers\not_existing_file.txt"),
                                (r"\resources\Files_Travers\not_existing_files_folder")                                
                            ])
    def test_travers_path_negative_cases(self, 
                                         files_obj, 
                                         files_path):
        
        print(f"The test param (path) is: {files_path}")        

        # AssertionError will occur if the dict will be empty (len = 0) - we will catch it as we expect for it to happen
        with pytest.raises(AssertionError):
            assert files_obj.validate_tests_folder(files_path) is True, "Test failed the validation of the test folder"
            files_obj.set_working_path(files_path)

            files_list = files_obj.get_files_from_path_into_list()
            assert len(files_list) > 0, "Test did not foind any test files"

            assert files_obj.get_files_from_list_into_dict(files_list) is True, "Test failed to create dict of tests files"
            files_obj.print_dict()