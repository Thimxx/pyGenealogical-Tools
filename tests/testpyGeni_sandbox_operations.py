'''
Created on 29 ago. 2017

@author: Val
'''
import unittest
from pyGeni import profile, set_token
from pyGenealogy.common_profile import gen_profile
from pyGenealogy.common_event import event_profile
from tests.FIXTURES import ACTUAL_NAME, FATHER_SURNAME, MAIN_SANDBOX_PROFILE, OLD_DELETED_SON, GENERIC_PLACE_IN_DICTIONARY, UNION_MAIN_PROFILE
from tests.FIXTURES import SANDBOX_MAIN_ADDRESS, SANDBOX_MAIN_API_G, SANDBOX_MAIN_API_NOG, MAIN_SANDBOX_PROFILE_ID, ACTUAL_SECOND, ACTUAL_THIRD
from tests.FIXTURES import FATHER_PROFILE_SANDBOX, BROTHER_PROFILE_SANDBOX, GENERIC_PLACE_STRING, GENI_INPUT_THROUGH, GENI_INPUT_THROUGH_API
from tests.FIXTURES import GENI_TWO_MARRIAGES_PROFILE, GENI_TWO_MARRIAGES_PROFILE_LINK, MAIN_SANDBOX_PROFILE_API
import os

class Test(unittest.TestCase):


    def setUp(self):
        #We used the sandbox here
        set_token(os.environ['SANDBOX_KEY'])
        profile.s.update_geni_address("https://sandbox.geni.com")

    def test_reading_sandbox_profile(self):
        '''
        Test reading a profile in sandbox
        '''
        prof = profile.profile(MAIN_SANDBOX_PROFILE, type_geni="")
        assert( "Testing" in prof.nameLifespan())
        assert(prof.properly_executed)
        
        assert(prof.gen_data["gender"] == "M")
        assert(prof.gen_data["surname"] == "Profile")
        assert(prof.gen_data["name"] == "Testing")
        #Securing before is properly captured
        assert(prof.get_accuracy_event("baptism") == "BEFORE")
        
        prof = profile.profile(MAIN_SANDBOX_PROFILE_API)
        assert(prof.gen_data["name"] == "Testing")
        assert(prof.properly_executed)
        
    
    def test_creating_a_child(self):
        '''
        Test creation of a child profile
        '''
        child_profile = gen_profile(ACTUAL_NAME, FATHER_SURNAME)
        child_profile.setCheckedGender("M")
        child_profile.set_name_2_show(ACTUAL_NAME)
        child_profile.setCheckedDate("birth", 2017, month =  11, day = 20, accuracy = "ABOUT")
        child_profile.setCheckedDate("death", 2017, month =  12, day = 1)
        child_profile.setCheckedDate("burial", 2017, month =  12, day = 2, accuracy = "BETWEEN", year_end = 2017, month_end = 12, day_end = 3)
        child_profile.add_nickname("my_nickname")
        profile.profile.create_as_a_child(child_profile, union = UNION_MAIN_PROFILE )
        
        data_id = child_profile.geni_specific_data['guid']
        assert(child_profile.properly_executed)
        assert(child_profile.existing_in_geni)
        #Check input of data
        assert(child_profile.data["gender"] == "male")
        assert(child_profile.data["last_name"] == FATHER_SURNAME)
        #Checking dates
        assert(child_profile.data["birth"]["date"]["year"] == 2017)
        assert(child_profile.data["birth"]["date"]["circa"] == True)
        assert("month" in child_profile.data["birth"]["date"].keys())
        assert(child_profile.data["death"]["date"]["year"] == 2017)
        assert(child_profile.data["death"]["date"]["month"] == 12)
        assert(child_profile.data["death"]["date"]["day"] == 1)
        assert(child_profile.data["burial"]["date"]["year"] == 2017)
        assert(child_profile.data["burial"]["date"]["end_day"] == 3)
        assert(child_profile.data["public"] == False)
        assert("my_nickname" in child_profile.data["nicknames"] )
        prof_relations = profile.profile(MAIN_SANDBOX_PROFILE, type_geni="")
        
        assert(len(prof_relations.marriage_union) == 1)
        for dif_union in prof_relations.marriage_union:
            assert("union-156" in dif_union.union_id)
        for dif_union in prof_relations.parent_union:
            assert("union-155" in dif_union.union_id)
        
        #We introduce other 2 childs using different methods
        second_profile = gen_profile(ACTUAL_SECOND, FATHER_SURNAME)
        profile.profile.create_as_a_child(second_profile, profile = prof_relations )
        third_profile = gen_profile(ACTUAL_THIRD, FATHER_SURNAME)
        profile.profile.create_as_a_child(third_profile, geni_input = MAIN_SANDBOX_PROFILE, type_geni="" )
        assert(second_profile.properly_executed)
        assert(third_profile.properly_executed)
        
        #We delete to avoid creation of data
        assert(child_profile.delete_profile())
        assert(second_profile.delete_profile())
        assert(third_profile.delete_profile())
        self.assertFalse(child_profile.existing_in_geni)
        
        #We check is deleted
        existing = profile.profile(data_id)
        
        assert(existing.geni_specific_data['deleted'])
    
    def test_error_create_child(self):
        '''
        Test wrong inputs creating a child
        '''
        child_profile = gen_profile(ACTUAL_NAME, FATHER_SURNAME)
        child_profile.setCheckedGender("M")
        self.assertFalse(profile.profile.create_as_a_child(child_profile, geni_input = "https://sandbox.geni.com/people/Brother-Profile/1150205" ))
    
    def test_delete_not_existing_profile(self):
        '''
        Test deleting a not existing profile
        '''
        prof3 = profile.profile(OLD_DELETED_SON, type_geni="")
        assert(prof3.geni_specific_data['deleted'])
        
        assert(prof3.delete_profile())
    
    def test_date_structure(self):
        '''
        Test creation of geni date structure
        '''
        my_event = event_profile("birth")
        #my_event.setDate(year, month, day, accuracy, year_end, month_end, day_end)
        my_event.setDate(2017, 11, 20, "EXACT")
        
        output = profile.getDateStructureGeni(my_event)
        assert(output["year"] == 2017)
        assert(output["month"] == 11)
        assert(output["day"] == 20)
        #Testing about
        my_event.setDate(2017,accuracy = "ABOUT")
        output2 = profile.getDateStructureGeni(my_event)
        assert(output2["year"] == 2017)
        self.assertFalse("month" in output2.keys())
        self.assertFalse("day" in output2.keys())
        assert(output2["circa"] == True)
        my_event.setDate(2017,accuracy = "ABOUT")
        #Testing the data before
        my_event.setDate(2017,accuracy = "BEFORE")
        output3 = profile.getDateStructureGeni(my_event)
        assert(output3["range"] == "before")
        #Testing the data before
        my_event.setDate(2017,accuracy = "AFTER")
        output4 = profile.getDateStructureGeni(my_event)
        assert(output4["range"] == "after")
        
        my_other_event = event_profile("birth")
        self.assertFalse( profile.getDateStructureGeni(my_other_event))
        
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
    
    def test_different_geni_inptus(self):
        '''
        Test different Geni inputs to profile
        '''
        prof = profile.profile(SANDBOX_MAIN_ADDRESS)
        prof2 = profile.profile(SANDBOX_MAIN_API_G)
        prof3 = profile.profile(SANDBOX_MAIN_API_NOG)
        
        assert(prof.geni_specific_data["id"] == MAIN_SANDBOX_PROFILE_ID)
        assert(prof2.geni_specific_data["id"] == MAIN_SANDBOX_PROFILE_ID)
        assert(prof3.geni_specific_data["id"] == MAIN_SANDBOX_PROFILE_ID)
    
    def test_adding_a_partner(self):
        '''
        Testing adding a parent to a profile
        '''
        partner_profile = gen_profile(ACTUAL_NAME, FATHER_SURNAME)
        my_event = event_profile("marriage")
        my_event.setDate(2017, 11, 20)
        partner_profile.setCheckedDate("marriage", 2017, 10, 20)
        partner_profile.setPlaces("marriage_place",GENERIC_PLACE_STRING , language="es")
        profile.profile.create_as_a_partner(partner_profile, geni_input = BROTHER_PROFILE_SANDBOX)
        #TODO: add checking of marriage data once is included
        assert(partner_profile.properly_executed)
        assert(partner_profile.delete_profile())
        
    def test_adding_a_parent(self):
        '''
        Test adding a parent in Geni
        '''
        
        father_profile = gen_profile(ACTUAL_NAME, FATHER_SURNAME)
        father_profile.setCheckedGender("M")
        
        profile.profile.create_as_a_parent(father_profile, geni_input=FATHER_PROFILE_SANDBOX)
        
        prof3 = profile.profile(FATHER_PROFILE_SANDBOX)
        assert(father_profile.geni_specific_data["id"] in prof3.parents)
        assert(father_profile.delete_profile())
        
    def test_adding_with_through(self):
        '''
        Test including Geni link with through
        '''
        data = profile.process_geni_input(GENI_INPUT_THROUGH, "g") 
        assert(data == GENI_INPUT_THROUGH_API)
     
    def test_error_adding_marriage(self):
        '''
        Test no adding marriage data due to error
        '''
        prof = profile.profile(GENI_TWO_MARRIAGES_PROFILE, type_geni="")
        self.assertFalse(prof.add_marriage_in_geni())
        self.assertFalse(prof.delete_profile())
    
    def test_parser_profile_input(self):
        '''
        Tests that a profile inputs provide the right result
        '''
        prof = profile.profile(GENI_TWO_MARRIAGES_PROFILE, type_geni="")
        example = profile.process_profile_input(profile=prof)
        assert(example == GENI_TWO_MARRIAGES_PROFILE_LINK)
    
    def test_alternative_data_in_profile(self):
        '''
        Test other data in the profile
        '''
        prof = profile.profile(BROTHER_PROFILE_SANDBOX)
        assert(len(prof.gen_data["nicknames"]) == 2)
        assert("brother" in prof.gen_data["nicknames"])
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()