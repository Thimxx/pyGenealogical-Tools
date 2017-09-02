'''
Created on 29 ago. 2017

@author: Val
'''
import unittest
from pyGeni import profile
from pyGenealogy.gen_utils import get_formatted_location
from datetime import date
from pyGenealogy.common_profile import gen_profile
from tests.FIXTURES import ACTUAL_NAME, FATHER_SURNAME, MAIN_SANDBOX_PROFILE, OLD_DELETED_SON, GENERIC_PLACE_IN_DICTIONARY, UNION_MAIN_PROFILE
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
        
        assert(prof.gen_data["gender"] == "M")
        assert(prof.gen_data["surname"] == "Profile")
        assert(prof.gen_data["name"] == "Testing")
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
        child_profile.setCheckedGender("M")
        child_profile.set_name_2_show(ACTUAL_NAME)
        child_profile.setCheckedBirthDate(date(2017,11,20), "ABOUT")
        child_profile.setCheckedDeathDate(date(2017,12,1), "EXACT")
        profile.profile.create_as_a_child(child_profile, self.stoken, UNION_MAIN_PROFILE )
        
        data_id = child_profile.geni_specific_data['guid']
        assert(child_profile.properly_executed)
        assert(child_profile.existing_in_geni)
        #Check input of data
        assert(child_profile.data["gender"] == "male")
        assert(child_profile.data["last_name"] == FATHER_SURNAME)
        #Checking dates
        assert(child_profile.data["birth"]["date"]["year"] == 2017)
        assert(child_profile.data["birth"]["date"]["circa"] == True)
        self.assertFalse("month" in child_profile.data["birth"]["date"].keys())
        assert(child_profile.data["death"]["date"]["year"] == 2017)
        assert(child_profile.data["death"]["date"]["month"] == 12)
        assert(child_profile.data["death"]["date"]["day"] == 1)
        
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
    
    def test_date_structure(self):
        '''
        Test creation of geni date structure
        '''
        test_date = date(2017,11,20)
        
        output = profile.getDateStructureGeni(test_date, "EXACT")
        assert(output["year"] == 2017)
        assert(output["month"] == 11)
        assert(output["day"] == 20)
        output2 = profile.getDateStructureGeni(test_date, "ABOUT")
        assert(output2["year"] == 2017)
        self.assertFalse("month" in output2.keys())
        self.assertFalse("day" in output2.keys())
        assert(output2["circa"] == True)
        output3 = profile.getDateStructureGeni(test_date, "BEFORE")
        assert(output3["range"] == "before")
        output4 = profile.getDateStructureGeni(test_date, "AFTER")
        assert(output4["range"] == "after")
        
        self.assertFalse( profile.getDateStructureGeni(None, None))
        
    def test_location_input(self):
        '''
        Test the location input to Geni
        '''
        data_location = profile.getLocationStructureGeni(GENERIC_PLACE_IN_DICTIONARY)
        
        assert(data_location["country"] == "Spain")
        assert(data_location["state"] == 'Castilla y León')
        assert(data_location["county"] == "Valladolid")
        assert(data_location["city"] == "Portillo")
        
        self.assertFalse(profile.getLocationStructureGeni(None))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()