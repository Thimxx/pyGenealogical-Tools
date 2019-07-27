'''
Created on 27 jul. 2019

@author: Val
'''
import unittest, os
from pyGeni.interface_geni_database import geni_database_interface
from pyGeni import set_token
from pyGeni import profile
from tests.FIXTURES import MAIN_SANDBOX_PROFILE


class Test(unittest.TestCase):
    '''
    This test will check that the class dealing with Geni as a database works
    '''

    def setUp(self):
        #We used the sandbox here
        set_token(os.environ['SANDBOX_KEY'])
        profile.s.update_geni_address("https://sandbox.geni.com")
    def test_basic_db_function_Geni(self):
        '''
        Testing basic database functionality
        '''
        db_geni = geni_database_interface()
        prof = db_geni.get_profile_by_ID("1149810")
        assert(prof.get_specific_event("baptism").get_accuracy() == "BETWEEN")
        assert(prof.get_specific_event("baptism").year_end == 1901)
        
        fam = db_geni.get_family_by_ID("union-155")
        assert(len(fam.union_data["partners"]) == 2)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()