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
        assert(profile.setCheckedBirthDate(birth_date, "EXACT"))
        assert(profile.setCheckedBirthDate(birth_date, "BEFORE"))
        assert(profile.setCheckedBirthDate(birth_date, "AFTER"))
        assert(profile.setCheckedBirthDate(birth_date, "ABOUT"))
        assert(not profile.setCheckedBirthDate(birth_date, "OTHER"))
        
        assert(profile.setCheckedDeathDate(batpsim_date_before_birth))
        assert(not profile.setCheckedBirthDate(birth_date_late))
        
    def test_introducing_death_date(self):
        '''
        Testing introduction of several death dates and the logic
        '''
        birth_date = date(2016,10, 20)
        death_date = date(2017,12, 31)
        death_date_before = date(2015,12, 31)
        profile = gen_profile("Name", "Surname")
        assert(profile.setCheckedDeathDate(death_date, "EXACT"))
        assert(profile.setCheckedDeathDate(death_date, "BEFORE"))
        assert(profile.setCheckedDeathDate(death_date, "AFTER"))
        assert(profile.setCheckedDeathDate(death_date, "ABOUT"))
        assert(not profile.setCheckedDeathDate(death_date, "OTHER"))
        
        assert(profile.setCheckedBirthDate(birth_date))
        assert(not profile.setCheckedDeathDate(death_date_before))
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
        assert(profile.setCheckedBirthDate(birth_date))
        assert(profile.setCheckedDeathDate(death_date))
        assert(profile.setCheckedBaptismDate(baptism_date))
        
        assert(not profile.setCheckedBaptismDate(earliest_date))
        assert(not profile.setCheckedBaptismDate(latest_date))
        assert(not profile.setCheckedBaptismDate(baptism_date,"OTHER"))
    
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
        assert(profile.setCheckedBirthDate(birth_date))
        assert(profile.setCheckedDeathDate(death_date))
        assert(profile.setCheckedBurialDate(burial_date))
        
        assert(not profile.setCheckedBurialDate(earliest_date))
        #Notice that will be ok to introudce a very late burial date
        assert(profile.setCheckedBurialDate(latest_date))
        assert(not profile.setCheckedBurialDate(burial_date,"OTHER"))
     
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
        assert(profile.setCheckedBirthDate(birth_date))
        assert(profile.setCheckedDeathDate(death_date))
        assert(profile.setCheckedResidenceDate(residence_date))
        
        assert(not profile.setCheckedResidenceDate(earliest_date))
        assert(not profile.setCheckedResidenceDate(latest_date))
        assert(not profile.setCheckedBurialDate(residence_date,"OTHER"))
    def test_accuracy_in_dates(self):
        '''
        Testing the accuracy as introduced in dates
        '''
        profile = gen_profile("Name", "Surname")
        test_date = date(2016,10, 20)
        residence_date = date(2016,1, 1)
        death_date = date(2016,12, 31)
        late_residence_date = date(2016,1,1)
        assert(profile.setCheckedBirthDate(test_date))
        assert(profile.setCheckedResidenceDate(residence_date, "ABOUT"))
        profile2 = gen_profile("Name", "Surname")
        assert(profile2.setCheckedBirthDate(test_date))
        assert(profile2.setCheckedDeathDate(death_date))
        assert(profile2.setCheckedResidenceDate(late_residence_date, "ABOUT"))
  
    def test_burial_date_earlier_than_death_date(self):
        '''
        Test burial date before death date is wrong
        '''
        profile = gen_profile("Name", "Surname")
        death_date = date(2016,10, 20)
        burial_date = date(2016,10, 19)
        assert(profile.setCheckedDeathDate(death_date))
        self.assertFalse(profile.setCheckedBurialDate(burial_date))
    
    def test_event_places(self):
        '''
        Test introduction of places
        '''
        profile = gen_profile("Name", "Surname")
        
        self.assertFalse(profile.setPlaces("notvalid", GENERIC_PLACE_STRING))
        assert(profile.setPlaces("birth_place", GENERIC_PLACE_STRING))
        self.assertFalse("death_place" in profile.gen_data.keys())
        assert("birth_place" in profile.gen_data.keys())
           
        
    def test_other_functions(self):
        '''
        Testing of other functions in common profile
        '''
        profile = gen_profile("Name", "Surname")
        profile.returnFullName()
        profile.setComments("TEST COMMENT")
        profile.setWebReference("Myaddress")
        #Wrong declaration in the past created issues
        assert(len(profile.gen_data["web_ref"]) == 1)
        
      
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_introducing_gender']
    unittest.main()