import datetime
import sqlite3
from data_base import DataBase
import pytest
from model import my_file_model



class TestDataBase:
    
    @pytest.fixture
    def db_member(self):
        """
        fixture that will be called per test twice.
        first time to create and yield client of the DB (based on SQLite3). second time to close the client
        Use in-memory SQLite for testing: that stores data in RAM and not on the disk for: speed access, for tests as dat not changing the environment - this is called clean testing
        """ 
        db_member = DataBase(":files_store:")
        yield db_member # it is like return 
        db_member.close()

    @pytest.fixture
    def file_member(self):
        return {
            "source": "test.html",            
            "date": datetime.now().isoformat()
        }

    def test_data_base_init(self, db_member):
        # Check if the connection and cursor are initialized
        assert db_member.conn is not None
        assert db_member.cursor is not None

    # def test_create_table(self, db_member):
    #     # create empty table
    #     # db_member.create_table() ??? the teable is created in __init()__ method so why I need this here?
    #     # read back the conversion table (it should be empty table), check if the table 'conversions' exists indeed
    #     db_member.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{data_base.MY_FILES_TABLE}'")
        
    #     # db_member.cursor holds the table - that we got after query
    #     # read all available rows from a table (it should be None as we didt insert anything yet)
    #     table = db_member.cursor.fetchone()
    #     assert len(table) > 0

    # def test_insert_file_into_table(self, db_member, file_member):
    #     # create empty table
    #     #db_member.create_table()
    #     # insert record (file), this operation returns id of the newly created record in the table
    #     id = db_member.insert(file_member["source"],                                                    
    #                             file_member["date"])
    #     assert id > 0
        
    #     # way 2 to request directly the record by SQL query without using class method
    #     db_member.cursor.execute(f'SELECT * FROM {data_base.MY_FILES_TABLE} WHERE id = ?', (id,))
    #     row = db_member.cursor.fetchone() # I know that was inserted single row hence I request for a table with single row
    #     assert row is not None
    #     assert row[1] == file_member["source"]       
    #     assert row[3] == file_member["date"]

    # def test_get_file_from_table_by_invalid_id(self, db_member):
    #     # create empty table
    #     #db_member.create_table()
    #     file = db_member.get_file_by_id(999)
    #     assert file is None

    # def test_get_file_from_table_by_existing_id(self, db_member, file_member):
    #     # create empty table
    #     #db_member.create_table()
    #     # Insert file
    #     id = db_member.insert(file_member["source"],                                        
    #                             file_member["date"])
    #     # Get file by ID
    #     file = db_member.get_file_by_id(id)
    #     # check retrieved data
    #     assert file is not None
    #     assert file.id == id
    #     assert file.source == file_member["source"]        
    #     assert file.date == file_member["date"]

    # def test_get_all_file_from_table(self, db_member, file_member):
    #     # create empty table
    #     #db_member.create_table()
    #     files = []
    #     # Insert few files
    #     for i in range(3):
    #         db_member.insert(f"{file_member['source']}{i}",                                     
    #                             file_member["date"])
    #     # Get all conversions
    #     files = db_member.get_all_files()
    #     assert len(files) == 3
    #     # all will return True only if all iterations will be resulted with True, assert will be issued if all will not return True
    #     assert all(isinstance(file, my_file_model)
    #                 for file in files)

    # def test_insert_file_invalide_format(self, db_member):
    #     # test how DBClient handles database errors (inserting invalid data or making operations on closed connection)
    #     # db_member.create_table()
    #     # Simulate invalid data (e.g., missing fields)
    #     invalide_file_id = db_member.insert(None, None)
    #     assert invalide_file_id == -1

    # def test_close_connection(self, db_member):
    #     """
    #     negative test - test shouldfail- we will catch the fail within 'context manager'
    #     """
    #     #db_member.create_table() # create empty table
    #     db_member.close() # close connection to a table
    #     # pytest way for negative tests - by doing this we expect test to fail, we catch failure in with context manager
    #     # we say what error we expect. test passes if this type of error will be caught by with else test fails.
    #     with pytest.raises(expected_exception=sqlite3.ProgrammingError):
    #         db_member.cursor.execute(f"SELECT * FROM {data_base.MY_FILES_TABLE}")  # this operation should fail after close connection

    # def test_empty_database(self, db_member):
    #     # create empty table
    #     #db_member.create_table()
    #     files = db_member.get_all_files()
    #     assert len(files) == 0