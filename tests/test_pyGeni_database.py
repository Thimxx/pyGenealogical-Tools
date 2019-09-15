'''
Created on 27 jul. 2019

@author: Val
'''
import unittest, os
from pyGeni.interface_geni_database import geni_database_interface
from pyGeni import set_token
from pyGeni import profile

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
        assert("profile-403" in db_geni.profiles)
        assert(db_geni.get_profile_by_ID("profile-405"))
        assert(prof.get_specific_event("baptism").get_accuracy() == "BETWEEN")
        assert(prof.get_specific_event("baptism").year_end == 1901)
        
        fam = db_geni.get_family_by_ID("union-155")
        assert(len(fam.union_data["partners"]) == 2)
        assert(not "union-1349" in db_geni.families)
        #Testing getting the child
        assert(db_geni.get_family_from_child("profile-403"))
        assert("union-1349" in db_geni.families)
        #Testing getting the children
        children = db_geni.get_all_children("profile-403")
        assert(len(children) == 4)
        assert("profile-405" in children)
        #Checking the families where is parent the profile
        families = db_geni.get_all_family_ids_is_parent("profile-403")
        assert("union-155" in families)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()