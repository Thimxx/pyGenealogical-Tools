'''
Created on 13 ago. 2017

@author: Val
'''
import unittest
from datetime import date
from pyGenealogy.common_profile import gen_profile
from tests.FIXTURES import ACTUAL_NAME, FATHER_SURNAME, GENERIC_PLACE_STRING, GENERIC_PLACE_WITH_PLACE


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
    
    def test_merge_profile(self):
        '''
        Test merge of profiles
        '''
        profile = gen_profile("Juana", "Bargas")
        profile2 = gen_profile("Juana", "de Bargas Gómez")
        profile.setCheckedDate("birth_date", date(2016,4,23), "EXACT")
        profile2.setCheckedDate("birth_date", date(2016,1,1), "ABOUT")
        profile.setCheckedDate("death_date", date(2018,1,1), "ABOUT")
        profile2.setCheckedDate("death_date", date(2018,8,24), "EXACT")
        profile2.setCheckedDate("baptism_date", date(2017,1,1), "ABOUT")
        profile.setComments("comment1")
        profile2.setComments("comment2")
        profile.setWebReference("THIS")
        profile2.setWebReference("OTHER")
        profile.gen_data["birth_place"] = {}
        profile.gen_data["birth_place"]["raw"] = "a"
        profile2.setPlaces("birth_place", GENERIC_PLACE_WITH_PLACE)
        
        result = profile.merge_profile(profile2, language="es", convention="spanish_surname")
        
        assert(result)
        assert(profile.gen_data["name"] == "Juana")
        assert(profile.gen_data["surname"] == "de Bargas Gómez")
        assert(profile.gen_data["birth_date"] == date(2016,4,23))
        assert(profile.gen_data["accuracy_birth_date"] == "EXACT")
        assert(profile.gen_data["comments"] == "comment1\ncomment2")
        assert("THIS" in profile.gen_data["web_ref"] )
        assert("OTHER" in profile.gen_data["web_ref"] )
        assert(profile.gen_data["death_date"] ==  date(2018,8,24))
        assert(profile.gen_data["accuracy_death_date"] == "EXACT")
        assert(profile.gen_data["baptism_date"] ==  date(2017,1,1))
        assert(profile.gen_data["accuracy_baptism_date"] == "ABOUT")
        assert(profile.gen_data["birth_place"]["city"] == "La Parrilla")
    
        profile3 = gen_profile("Juana", "Bargas")
        profile4 = gen_profile("Facundo", "Smith")
        result2 = profile3.merge_profile(profile4, language="es", convention="spanish_surname")
        self.assertFalse(result2)
    
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
        assert(profile.setPlaces("marriage_place", ""))
           
        
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
    
    def test_comparison_profile(self):
        '''
        Test some profile comparison 
        '''
        profile = gen_profile("Name", "Surname")
        profile2 = gen_profile("Name", "Surname")
        
        profile.setCheckedGender("M")
        profile2.setCheckedGender("M")
        
        score, factor = profile.comparison_score(profile2)
        assert(score == 4.5)
        assert(factor == 1.0)
        
        profile2.setCheckedGender("F")
        score, factor = profile.comparison_score(profile2)
        assert(score == 4.0)
        assert(factor == 0.5)
               
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_introducing_gender']
    unittest.main()