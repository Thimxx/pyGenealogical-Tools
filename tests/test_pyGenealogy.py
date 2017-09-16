'''
Created on 13 ago. 2017

@author: Val
'''
import unittest
from datetime import date
from pyGenealogy.common_profile import gen_profile
from tests.FIXTURES import ACTUAL_NAME, FATHER_SURNAME, GENERIC_PLACE_STRING


class Test(unittest.TestCase):


    def test_introducing_gender(self):
        '''
        Testing right introduction of gender in common_profile
        '''
        profile = gen_profile(ACTUAL_NAME, FATHER_SURNAME)
        assert(profile.setCheckedGender("F"))
        assert(profile.setCheckedGender("M"))
        assert(profile.gen_data["name_to_show"] == ACTUAL_NAME + " " + FATHER_SURNAME)
        self.assertFalse(profile.setCheckedGender("J"))
    def test_introducing_birth_date(self):
        '''
        Testing right introduction of birth date in common_profile
        '''
        birth_date = date(2016,10, 20)
        birth_date_late = date(2017,12, 31)
        batpsim_date_before_birth = date(2016,12, 31)
        profile = gen_profile("Name", "Surname")
        assert(profile.setCheckedDate("birth_date", birth_date, "EXACT"))
        assert(profile.setCheckedDate("birth_date", birth_date, "BEFORE"))
        assert(profile.setCheckedDate("birth_date", birth_date, "AFTER"))
        assert(profile.setCheckedDate("birth_date", birth_date, "ABOUT"))
        assert(not profile.setCheckedDate("birth_date", birth_date, "OTHER"))
        
        assert(profile.setCheckedDate("death_date", batpsim_date_before_birth))
        assert(not profile.setCheckedDate("birth_date", birth_date_late))
        
    def test_introducing_death_date(self):
        '''
        Testing introduction of several death dates and the logic
        '''
        birth_date = date(2016,10, 20)
        death_date = date(2017,12, 31)
        death_date_before = date(2015,12, 31)
        profile = gen_profile("Name", "Surname")
        assert(profile.setCheckedDate("death_date", death_date, "EXACT"))
        assert(profile.setCheckedDate("death_date", death_date, "BEFORE"))
        assert(profile.setCheckedDate("death_date", death_date, "AFTER"))
        assert(profile.setCheckedDate("death_date", death_date, "ABOUT"))
        assert(not profile.setCheckedDate("death_date", death_date, "OTHER"))
        
        assert(profile.setCheckedDate("birth_date", birth_date))
        assert(not profile.setCheckedDate("death_date", death_date_before))
    def test_introduce_baptism_date(self):
        '''
        Testing introduction of baptism date
        '''
        birth_date = date(2016,10, 20)
        baptism_date = date(2016,12, 31)
        death_date = date(2019,12, 31)
        earliest_date = date(2015,12, 31)
        latest_date = date(2020,12, 31)
        profile = gen_profile("Name", "Surname")
        assert(profile.setCheckedDate("birth_date", birth_date))
        assert(profile.setCheckedDate("death_date", death_date))
        assert(profile.setCheckedDate("baptism_date", baptism_date))
        
        assert(not profile.setCheckedDate("baptism_date", earliest_date))
        assert(not profile.setCheckedDate("baptism_date", latest_date))
        assert(not profile.setCheckedDate("baptism_date", baptism_date,"OTHER"))
    
    def test_introduce_burial_date(self):
        '''
        Testing introduction of baptism date
        '''
        birth_date = date(2016,10, 20)
        death_date = date(2019,12, 29)
        burial_date = date(2019,12, 31)
        earliest_date = date(2015,12, 31)
        latest_date = date(2020,12, 31)
        profile = gen_profile("Name", "Surname")
        assert(profile.setCheckedDate("birth_date", birth_date))
        assert(profile.setCheckedDate("death_date", death_date))
        assert(profile.setCheckedDate("burial_date", burial_date))
        
        assert(not profile.setCheckedDate("burial_date", earliest_date))
        #Notice that will be ok to introudce a very late burial date
        assert(profile.setCheckedDate("burial_date", latest_date))
        assert(not profile.setCheckedDate("burial_date", burial_date,"OTHER"))
     
    def test_introduce_residence_date(self):
        '''
        Testing introduction of residence date
        '''
        birth_date = date(2016,10, 20)
        residence_date = date(2016,12, 31)
        death_date = date(2019,12, 31)
        earliest_date = date(2015,12, 31)
        latest_date = date(2020,12, 31)
        profile = gen_profile("Name", "Surname")
        assert(profile.setCheckedDate("birth_date", birth_date))
        assert(profile.setCheckedDate("death_date",death_date))
        assert(profile.setCheckedDate("residence_date",residence_date))
        
        assert(not profile.setCheckedDate("residence_date",earliest_date))
        assert(not profile.setCheckedDate("residence_date",latest_date))
        assert(not profile.setCheckedDate("burial_date",residence_date,"OTHER"))
    def test_wrong_input(self):
        '''
        Test wrong input date class
        '''
        birth_date = date(2016,10, 20)
        profile = gen_profile("Name", "Surname")
        assert(not profile.setCheckedDate("no_valid_date",birth_date))
        
    def test_accuracy_in_dates(self):
        '''
        Testing the accuracy as introduced in dates
        '''
        profile = gen_profile("Name", "Surname")
        test_date = date(2016,10, 20)
        residence_date = date(2016,1, 1)
        death_date = date(2016,12, 31)
        late_residence_date = date(2016,1,1)
        assert(profile.setCheckedDate("birth_date", test_date))
        assert(profile.setCheckedDate("residence_date", residence_date, "ABOUT"))
        profile2 = gen_profile("Name", "Surname")
        assert(profile2.setCheckedDate("birth_date", test_date))
        assert(profile2.setCheckedDate("death_date", death_date))
        assert(profile2.setCheckedDate("residence_date", late_residence_date, "ABOUT"))
  
    def test_burial_date_earlier_than_death_date(self):
        '''
        Test burial date before death date is wrong
        '''
        profile = gen_profile("Name", "Surname")
        death_date = date(2016,10, 20)
        burial_date = date(2016,10, 19)
        assert(profile.setCheckedDate("death_date", death_date))
        self.assertFalse(profile.setCheckedDate("burial_date", burial_date))
    
    def test_event_places(self):
        '''
        Test introduction of places
        '''
        profile = gen_profile("Name", "Surname")
        
        self.assertFalse(profile.setPlaces("notvalid", GENERIC_PLACE_STRING))
        assert(profile.setPlaces("birth_place", GENERIC_PLACE_STRING))
        self.assertFalse("death_place" in profile.gen_data.keys())
        assert("birth_place" in profile.gen_data.keys())
        
        #Test wrong introduction of a place to be used in google places.
        self.assertFalse(profile.setPlaces("marriage_place", ""))
           
        
    def test_other_functions(self):
        '''
        Testing of other functions in common profile
        '''
        profile = gen_profile("Name", "Surname")
        profile.returnFullName()
        profile.setComments("TEST COMMENT")
        profile.set_surname("TEST SURNAME")
        assert(profile.gen_data["name_to_show"] == profile.nameLifespan())
    
    def test_web_reference_adding(self):
        '''
        Testing adding web reference
        '''
        profile = gen_profile("Name", "Surname")
        profile.setWebReference("Myaddress")
        #Wrong declaration in the past created issues
        assert(len(profile.gen_data["web_ref"]) == 1)
        profile.setWebReference(["Myaddress"])
        #This will check the data types is working
        assert(len(profile.gen_data["web_ref"]) == 2)
            
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_introducing_gender']
    unittest.main()