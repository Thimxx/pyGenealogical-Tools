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
        assert(profile.setCheckedGender("U"))
        assert(profile.gen_data["name_to_show"] == ACTUAL_NAME + " " + FATHER_SURNAME)
        self.assertFalse(profile.setCheckedGender("J"))
    
    def test_merge_profile(self):
        '''
        Test merge of profiles
        '''
        profile = gen_profile("Juana", "Bargas")
        profile2 = gen_profile("Juana", "de Bargas Gómez")
        profile.setCheckedDate("birth", 2016,4,23, "EXACT")
        date1 = date(2016,1,1)
        date2 = date(2018,8,25)
        date3 = date(2018,8,27)
        profile2.setCheckedDateWithDates("birth", date1, accuracy = "ABOUT")
        profile.setCheckedDate("death", 2018,1,1, "ABOUT")
        profile2.setCheckedDate("death", 2018,8,24, "EXACT")
        profile2.setCheckedDate("baptism", 2017,1,1, "ABOUT")
        profile2.setCheckedDateWithDates("burial", date2, accuracy = "BETWEEN", date2 = date3)
        profile.setComments("comment1")
        profile2.setComments("comment2")
        profile.setWebReference("THIS")
        profile2.setWebReference("OTHER")
        profile.gen_data["birth_place"] = {}
        profile.gen_data["birth_place"]["raw"] = "a"
        profile2.setPlaces("birth", GENERIC_PLACE_WITH_PLACE)
        
        result = profile.merge_profile(profile2, language="es", convention="spanish_surname")
        
        assert(result)
        assert(profile.gen_data["name"] == "Juana")
        assert(profile.gen_data["surname"] == "de Bargas Gómez")
        assert(profile.gen_data["birth"].get_date() == date(2016,4,23))
        assert(profile.gen_data["birth"].get_accuracy() == "EXACT")
        assert(profile.gen_data["comments"] == "comment1\ncomment2")
        assert("THIS" in profile.gen_data["web_ref"] )
        assert("OTHER" in profile.gen_data["web_ref"] )
        assert(profile2.gen_data["death"].get_date() ==  date(2018,8,24))
        assert(profile2.gen_data["death"].get_accuracy() == "EXACT")
        assert(profile2.gen_data["burial"].get_accuracy() == "BETWEEN")
        assert(profile2.gen_data["burial"].get_year_end() == 2018)
        assert(profile2.gen_data["baptism"].get_date() ==  date(2017,1,1))
        assert(profile2.gen_data["baptism"].get_accuracy() == "ABOUT")
        assert(profile2.gen_data["birth"].get_location()["city"] == "La Parrilla")
    
        profile3 = gen_profile("Juana", "Bargas")
        profile4 = gen_profile("Facundo", "Smith")
        result2 = profile3.merge_profile(profile4, language="es", convention="spanish_surname")
        self.assertFalse(result2)
    
    def test_introducing_birth_date(self):
        '''
        Testing right introduction of birth date in common_profile
        '''
        profile = gen_profile("Name", "Surname")
        assert(profile.setCheckedDate("birth", 2016, 10, 20, "EXACT"))
        assert(profile.setCheckedDate("birth", 2016, 10, 20, "BEFORE"))
        assert(profile.setCheckedDate("birth", 2016, 10, 20, "AFTER"))
        assert(profile.setCheckedDate("birth", 2016, 10, 20, "ABOUT"))
        assert(not profile.setCheckedDate("birth", 2016, 10, 20, "OTHER"))
        
        assert(profile.setCheckedDate("death", 2016, 12, 31))
        assert(not profile.setCheckedDate("birth", 2017,12,31))
        
    def test_introducing_death_date(self):
        '''
        Testing introduction of several death dates and the logic
        '''
        profile = gen_profile("Name", "Surname")
        
        
        assert(profile.setCheckedDate("death", 2017, 12, 31, "EXACT"))
        assert(profile.setCheckedDate("death", 2017, 12, 31, "BEFORE"))
        assert(profile.setCheckedDate("death", 2017, 12, 31, "AFTER"))
        assert(profile.setCheckedDate("death", 2017, 12, 31, "ABOUT"))
        assert(not profile.setCheckedDate("death", 2017, 12, 31, "OTHER"))
        
        assert(profile.setCheckedDate("birth", 2016, 10, 20))
        assert(not profile.setCheckedDate("death", 2015, 12 ,31))
    def test_introduce_baptism_date(self):
        '''
        Testing introduction of baptism date
        '''
        profile = gen_profile("Name", "Surname")
        assert(profile.setCheckedDate("birth", 2016,10, 20))
        assert(profile.setCheckedDate("death", 2019,12, 31))
        assert(profile.setCheckedDate("baptism", 2016,12, 31))
        #Checking the function earliest date.
        assert(profile.get_earliest_event() == date(2016,10, 20))
        
        assert(not profile.setCheckedDate("baptism", 2015,12, 31))
        assert(not profile.setCheckedDate("baptism", 2020,12, 31))
        assert(not profile.setCheckedDate("baptism", 2016,12, 31,"OTHER"))
    
    def test_introduce_burial_date(self):
        '''
        Testing introduction of baptism date
        '''
        profile = gen_profile("Name", "Surname")
        assert(profile.setCheckedDate("birth", 2016,10, 20))
        assert(profile.setCheckedDate("death", 2019,12, 29))
        assert(profile.setCheckedDate("burial", 2019,12, 31))
        
        assert(not profile.setCheckedDate("burial", 2015,12, 31))
        #Notice that will be ok to introudce a very late burial date
        assert(profile.setCheckedDate("burial", 2020,12, 31))
        assert(not profile.setCheckedDate("burial", 2019,12, 31,"OTHER"))
     
    def test_introduce_residence_date(self):
        '''
        Testing introduction of residence date
        '''
        profile = gen_profile("Name", "Surname")
        assert(profile.setCheckedDate("birth", 2016,10, 20))
        assert(profile.setCheckedDate("death",2019,12, 31))
        assert(profile.setCheckedDate("residence",2016,12, 31))
        
        assert(not profile.setCheckedDate("residence",2015,12, 31))
        assert(not profile.setCheckedDate("residence",2020,12, 31))
        assert(not profile.setCheckedDate("burial",2016,12, 31,"OTHER"))
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
        assert(profile.setCheckedDate("birth", 2016,10, 20))
        assert(profile.setCheckedDate("residence", 2016, accuracy="ABOUT"))
        profile2 = gen_profile("Name", "Surname")
        assert(profile2.setCheckedDate("birth", 2016,10, 20))
        assert(profile2.setCheckedDate("death", 2016,12, 31))
        assert(profile2.setCheckedDate("residence", 2016, accuracy="ABOUT"))
  
    def test_burial_date_earlier_than_death_date(self):
        '''
        Test burial date before death date is wrong
        '''
        profile = gen_profile("Name", "Surname")
        assert(profile.setCheckedDate("death", 2016,10, 20))
        self.assertFalse(profile.setCheckedDate("burial", 2016,10, 19))
    
    def test_event_places(self):
        '''
        Test introduction of places
        '''
        profile = gen_profile("Name", "Surname")
        
        self.assertFalse(profile.setPlaces("notvalid", GENERIC_PLACE_STRING))
        assert(profile.setPlaces("birth", GENERIC_PLACE_STRING))
        self.assertFalse("death" in profile.gen_data.keys())
        assert("birth" in profile.gen_data.keys())
        
        #Test wrong introduction of a place to be used in google places.
        assert(profile.setPlaces("marriage", ""))
           
        
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