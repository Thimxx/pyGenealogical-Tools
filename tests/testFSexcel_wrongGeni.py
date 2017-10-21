'''
Created on 18 oct. 2017

@author: Val
'''
import unittest
from pyFS.pyfs_open_xlsx import getFSfamily
import os
from pyGeni import profile, set_token
from tests.FIXTURES import SANDBOX_MAIN_ADDRESS, WRONG_TOKEN


class Test(unittest.TestCase):
    
    def setUp(self):
        '''
        Let's make it simple... is just a test not a good code. If it is not located in one place will
        be in another!
        '''
        #We used the sandbox here, this token is wrong...
        set_token(WRONG_TOKEN)
        profile.s.update_geni_address("https://sandbox.geni.com")
        #We locate the folder here
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2


    def test_wrong_geni_key_creation(self):
        '''
        Test pyfs breaks if wrong Geni input
        '''
        input_file = os.path.join(self.filelocation, "fs-MartinPerez.xlsx")
        fsclass = getFSfamily(input_file, naming_convention="spanish_surname", language = "es")
        
        
        execution = fsclass.create_profiles_in_Geni(SANDBOX_MAIN_ADDRESS)
        self.assertFalse(execution)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()