import time
import os
import sqlite3
import sys
import pytest
import src.data_base as db
from src.model import my_file_model

class TestDataBase:

    @pytest.fixture
    def db_member(self):
        """
        fixture that will be called per test twice.
        first time to create and yield client of the DB (based on SQLite3). second time to close the client
        Use in-memory SQLite for testing: that stores data in RAM and not on the disk for: speed access, for tests as dat not changing the environment - this is called clean testing
        """ 
        print("\n++++++++ START TEST +++++++++++++++++++++++")
        db_member = db.DataBase(":memory:")
        yield db_member # it is like return 
        db_member.close()
        print("\n+++++++ END TEST ++++++++++++++++++++++++\n")


    @pytest.fixture
    def file_record(self):
        return {
                "source_file": "test.html",
                "date": time.strftime("%Y-%m-%d %H:%M:%S")}
               

    def test_data_base_init(self, db_member):
        """
        Test performs initialisation checks, it checks the connection and cursor after the table was created 
        in-memory SQLite for testing: this stores data in RAM and not on the disk for: speed access
        for tests as it doesnt changing the environment 
        so called -> clean testing 
        """
        assert db_member.conn is not None
        assert db_member.cursor is not None
        db_member.close()

    def test_get_empty_table_single_file(self, db_member):
        """
        Test requests content from empty table    
        read back the table content (it should be empty table)
        """    
        print("Test to get empty table content .... Started")
        db_member.cursor.execute(f"SELECT * FROM {db.MY_FILES_TABLE}")
        
        # db_member.cursor holds the table - that we got after query, if is no content the table the method: fetchone() returns None
        # read all available rows from a table (it should be None as we didt insert anything yet)
        table = db_member.cursor.fetchone()
        print(f"Table content is: {table}")
        assert table is None
    
    def test_empty_table_all_rows(self, db_member):        
        files = db_member.get_all_files()
        assert len(files) == 0

    def test_insert_first_file_into_table(self, db_member, file_record):
        """    
        Test inserts first record (file) into existing but empty table
        this operation returns id of the newly created record in the table
        """
        print(f"The file record is: {file_record}")
        print("Insert file record into the existing empty table")
        id = db_member.insert(source_file=file_record["source_file"],
                              date=file_record["date"])
        print(f"The id of the transaction is: {id}")
        assert id > 0
        print(f"Way1: check that file record was added succfully into the table")
        print(f"The operation 'insert' resulted weith id: {id}")
        
        # way 2 to request directly the record by SQL query without using class method
        print(f"Way2: check that file record was added succfully into the table")
        print(f"Use SQL query to read file record from a table by id")
        
        sql_query = f'SELECT * FROM {db.MY_FILES_TABLE} WHERE id = {id}'
        print(f"SQL query: {sql_query}")
        db_member.cursor.execute(f'SELECT * FROM {db.MY_FILES_TABLE} WHERE id = {id}')
        
        print(f"Use cursor to fetch results of the query")
        row = db_member.cursor.fetchone() # I know that was inserted single row so I can use fetchone
        print(f"The fetched row is: {row}")
        assert row is not None
        assert row[1] == file_record["source_file"]       
        assert row[2] == file_record["date"]

    def test_get_file_from_table_by_invalid_id(self, db_member):
        # create empty table       
        file = db_member.get_file_by_id(999)
        assert file is None

    def test_get_file_from_table_by_existing_id(self, db_member, file_record):       
        # Insert file
        id = db_member.insert(file_record["source_file"],                                        
                              file_record["date"])
        # Get file by ID
        file = db_member.get_file_by_id(id)
        print(f"Retrieved file is: {file}")
        # check retrieved data
        assert file is not None
        assert file.id == id
        assert file.source_file == file_record["source_file"]        
        assert file.date == file_record["date"]

    def test_get_all_files_from_table(self, db_member, file_record):        
        files = []
        # Insert few files
        print("Inserting 3 files into a table ...")
        for i in range(1,4):
            print(f"File: {i}{file_record['source_file']}, date: {file_record['date']}")
            db_member.insert(f"{i}{file_record['source_file']}",                                     
                                file_record["date"])
        # Get all files from a table - we get already modeled items
        files = db_member.get_all_files()
        assert len(files) == 3
        
        for file in files:
            # way1: files already modeled - so we can print them directly
            print(f"File: {file.source_file}, date: {file.date}")

            # way2: this way we convert model into struct and can get to each field of the stract. Here model is a dict. Each memver has 2 fileds:
            # source_file and date             
            file_obj = my_file_model(**file.model_dump())
            print(f"File: {file_obj.source_file}, date: {file_obj.date}")           
                

        # all will return True only if all iterations will be resulted with True, assert will be issued if all will not return True
        assert all(isinstance(file, my_file_model)
                    for file in files)

    def test_insert_file_invalide_format(self, db_member):
        # test how DBClient handles database errors (inserting invalid data or making operations on closed connection)
        # Simulate invalid data (e.g., missing fields)
        invalide_file_id = db_member.insert(None, None)
        print(f"Returned result is: {invalide_file_id}")
        assert invalide_file_id == -1

    def test_close_connection(self, db_member):
        """
        negative test - test shouldfail- we will catch the fail within 'context manager'
        """       
        db_member.close() # close connection to a table
        # pytest way for negative tests - by doing this we expect test to fail, we catch failure in with context manager
        # we say what error we expect. test passes if this type of error will be caught by with else test fails.
        print("Test trying retrieve files from a closed table ...")
        with pytest.raises(expected_exception=sqlite3.ProgrammingError):
            db_member.cursor.execute(f"SELECT * FROM {db.MY_FILES_TABLE}")  # this operation should fail after close connection  