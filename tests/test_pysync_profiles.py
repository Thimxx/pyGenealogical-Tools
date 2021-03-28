'''
Created on 1 jun. 2020

@author: Val
'''
import unittest, os, logging
from shutil import copyfile
from pyRootsMagic.pyrm_database import database_rm
from analyzefamily.sync_profile import sync_profiles
from pyGeni import set_token, update_geni_address
from pyGeni.interface_geni_database import geni_database_interface
from datetime import datetime


class Test(unittest.TestCase):
    def setUp(self):
        "Creation of the different parameters needs for execution, including location of database"
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2
        #We used the sandbox here
        set_token(os.environ['SANDBOX_KEY'])
        update_geni_address("https://sandbox.geni.com")

    def test_single_match(self):
        '''
        Tests a single match in GENI
        '''
        #First we create the files for testing
        input_file = os.path.join(self.filelocation, "Rootstest.rmgc")
        working_file = os.path.join(self.filelocation, "Rootstest_sync.rmgc")
        
        if os.path.exists(working_file): os.remove(working_file)
        copyfile(input_file, working_file)
        ########
        #EXECUTION PART
        ########
        #Preparing the inputs
        db = database_rm(working_file)
        db_geni = geni_database_interface()

        sync_class = sync_profiles(db, db_geni, data_language="es", name_convention="spanish_surname")
        
        logging.basicConfig(level=logging.INFO)
        
        ########
        #PRE-CHECK PART
        ########
        #In RootsMagic there is not baptism
        assert("baptism" not in db.get_profile_by_ID(2).getEventsDict())
        #The update has been done several days ago
        assert((datetime.today()-db.get_profile_by_ID(2).get_update_datetime()).days > 0)
        
        sync_class.execute_sync()
        
        ########
        #CHECKING STEP
        ########
        #Baptism should have been copied from the profile in Geni, so now it should have been created
        assert("baptism" in db.get_profile_by_ID(2).getEventsDict())
        #The update has been done today
        assert((datetime.today()-db.get_profile_by_ID(2).get_update_datetime()).days == 0)
        
        
        #We delete the testing data
        db.close_db()
        if os.path.exists(working_file): os.remove(working_file)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()