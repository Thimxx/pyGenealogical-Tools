'''
Created on 28 jul. 2019

@author: Val
'''
import unittest, os
from shutil import copyfile
from pyRootsMagic.pyrm_database import database_rm
from analyzefamily.process_for_matches import process_a_db
from pyGeni.interface_geni_database import geni_database_interface
from pyGeni import set_token
from pyGeni import profile

class Test_processor_for_db(unittest.TestCase):
    '''
    This testing will test the system for looking for matches in the database
    '''
    def setUp(self):
        "Creation of the different parameters needs for execution, including location of database"
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        set_token(os.environ['SANDBOX_KEY'])
        profile.s.update_geni_address("https://sandbox.geni.com")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2
    def test_simple_process(self):
        '''
        Testing basic execution of the checker
        '''
        input_file = os.path.join(self.filelocation, "Rootstest.rmgc")
        working_file = os.path.join(self.filelocation, "Rootstest_process.rmgc")
        
        if os.path.exists(working_file): os.remove(working_file)
        copyfile(input_file, working_file)
        
        db = database_rm(working_file)
        db_geni = geni_database_interface()
        processor = process_a_db(db, db_geni)
        processor.process()

        db.close_db()
        if os.path.exists(working_file): os.remove(working_file)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()