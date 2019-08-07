'''
Created on 28 jul. 2019

@author: Val
'''
import unittest, os
from pyRootsMagic.pyrm_database import database_rm
from analyzefamily.process_for_matches import process_a_db


class Test_processor_for_db(unittest.TestCase):
    '''
    This testing will test the system for looking for matches in the database
    '''
    def setUp(self):
        "Creation of the different parameters needs for execution, including location of database"
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2
    def test_simple_process(self):
        '''
        Testing basic execution of the checker
        '''
        input_file = os.path.join(self.filelocation, "Rootstest.rmgc")
        db = database_rm(input_file)
        processor = process_a_db(db)
        processor.process()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()