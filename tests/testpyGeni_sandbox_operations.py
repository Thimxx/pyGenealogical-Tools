'''
Created on 29 ago. 2017

@author: Val
'''
import unittest
from pyGeni import profile
from pyGenealogy.common_profile import gen_profile
from tests.FIXTURES import ACTUAL_NAME, FATHER_SURNAME, MAIN_SANDBOX_PROFILE, OLD_DELETED_SON
import os

class Test(unittest.TestCase):


    def setUp(self):
        #We used the sandbox here
        self.stoken = os.environ['SANDBOX_KEY']
        profile.s.update_geni_address("https://www.sandbox.geni.com")
        profile.s.VERIFY_INPUT = False

    def test_reading_sandbox_profile(self):
        '''
        Test reading a profile in sandbox
        '''
        prof = profile.profile(MAIN_SANDBOX_PROFILE, self.stoken, type_geni="")
        assert( "Testing" in prof.nameLifespan())
        assert(prof.properly_executed)
    def test_wrong_execution(self):
        '''
        Test error OAuth in Geni
        '''
        prof2 = profile.profile(MAIN_SANDBOX_PROFILE, "a")
        self.assertFalse(prof2.properly_executed)
    
    def test_creating_a_child(self):
        '''
        Test creation of a child profile
        '''
        child_profile = gen_profile(ACTUAL_NAME, FATHER_SURNAME)
        profile.profile.create_as_a_child(child_profile, self.stoken, MAIN_SANDBOX_PROFILE )
        
        data_id = child_profile.geni_specific_data['guid']
        
        assert(child_profile.properly_executed)
        assert(child_profile.existing_in_geni)
        #We delete to avoid creation of data
        assert(child_profile.delete_profile())
        self.assertFalse(child_profile.existing_in_geni)
        
        #We check is deleted
        existing = profile.profile(data_id, self.stoken)
        
        assert(existing.geni_specific_data['deleted'])
    
    def test_delete_not_existing_profile(self):
        '''
        Test deleting a not existing profile
        '''
        prof3 = profile.profile(OLD_DELETED_SON, self.stoken, type_geni="")
        assert(prof3.geni_specific_data['deleted'])
        
        assert(prof3.delete_profile())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()