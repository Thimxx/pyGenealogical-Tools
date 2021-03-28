'''
Created on 27 jul. 2019

@author: Val
'''
import unittest, os
from pyGeni.interface_geni_database import geni_database_interface
from pyGeni import set_token
from pyGeni import profile
from tests.FIXTURES import UNCLE_ID, UNCLE_PROF_ID, FATHER_MOTHER_UNION_ID, MARRIAGE_ID, SON_PROF_ID, FATHER_PROF_ID
from tests.FIXTURES import MAIN_SANDBOX_PROFILE_ID, WIFE_PROF_ID

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
        prof = db_geni.get_profile_by_ID(UNCLE_ID)
        assert(UNCLE_PROF_ID in db_geni.profiles)
        assert(db_geni.get_profile_by_ID(UNCLE_PROF_ID))
        assert(prof.get_specific_event("baptism").get_accuracy() == "BETWEEN")
        assert(prof.get_specific_event("baptism").year_end == 1901)
        
        fam = db_geni.get_family_by_ID(FATHER_MOTHER_UNION_ID)
        assert(len(fam.union_data["partners"]) == 2)
        assert(not MARRIAGE_ID in db_geni.families)
        #Testing getting the child
        assert(db_geni.get_family_from_child(SON_PROF_ID))
        assert(MARRIAGE_ID in db_geni.families)
        #Testing getting the children
        children = db_geni.get_all_children(FATHER_PROF_ID)
        assert(len(children) == 3)
        assert(MAIN_SANDBOX_PROFILE_ID in children)
        #Checking the families where is parent the profile
        families = db_geni.get_all_family_ids_is_parent(MAIN_SANDBOX_PROFILE_ID)
        assert(MARRIAGE_ID in families)
        
        assert(WIFE_PROF_ID in db_geni.get_partners_from_profile(MAIN_SANDBOX_PROFILE_ID))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()