'''
Created on 14 oct. 2017

@author: Val

This function tests the new profile that includes the GedCom from Common profile
'''
import unittest, os

from pyGedcom.gedcom_profile import gedcom_profile
from pyGedcom.gedcom_profile import get_gedcom_formatted_date
from pyGenealogy.common_profile import gen_profile
from pyGenealogy.common_event import event_profile
from pyGedcom.gedcom_database import db_gedcom
from pyGedcom import get_date_info_from_ged
from datetime import date

class Test(unittest.TestCase):
    '''
    Function testing functionalities of gedcom file
    '''
    def setUp(self):
        "Creation of the different parameters needs for execution, including location of database"
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2
    def test_creating_gedcom_from_common(self):
        '''
        Test creating a GedCom from a common_profile
        '''
        profile = gen_profile("Juana", "Bargas")
        profile.setCheckedGender("F")
        profile.add_nickname("Nick1")
        profile.add_nickname("Nick2")
        profile.setCheckedDate("birth", 2014,3,2, accuracy="EXACT")
        profile.setCheckedDate("baptism", 2014,3,3, accuracy="AFTER")
        profile.setCheckedDate("death", 2016,3,2, accuracy="ABOUT")
        profile.setCheckedDate("burial", 2016,3,5, accuracy="BEFORE")
        profile.setPlaces("birth", "Portillo,Valladolid,Spain")
        #We transform to the gedcom class
        gedcom_profile.convert_gedcom(profile)
        assert(profile.getGender() == "F")
        assert(profile.getName() == "Juana")
        assert(profile.getSurname() == "Bargas")
        assert(profile.get_specific_event("birth").get_date() == date(2014,3,2))
        assert(profile.get_specific_event("death").get_date()== date(2016,3,2))
        assert(profile.get_specific_event("baptism").get_date()== date(2014,3,3))
        assert(profile.get_specific_event("burial").get_date()== date(2016,3,5))
        assert(profile.get_specific_event("birth").get_accuracy() ==  "EXACT")
        assert(profile.get_specific_event("death").get_accuracy() == "ABOUT")
        assert(profile.get_specific_event("baptism").get_accuracy() == "AFTER")
        assert(profile.get_specific_event("burial").get_accuracy() == "BEFORE")
        assert(profile.get_location_event("birth")["country"] == "Spain")
        assert(profile.get_location_event("birth")["place_name"] == "Portillo")
    def test_gedcom_as_database(self):
        '''
        Test using Gedcom database
        '''
        #Test using a previous non UTF-8 file
        input_file = os.path.join(self.filelocation, "gedcom_test.gedcom")
        new_ged = db_gedcom(input_file)
        prof = new_ged.get_profile_by_ID("@I1@")
        assert(prof.returnFullName() == "Francisco Sanz Sanz")
        assert(prof.getGender() == "U")
        assert(prof.get_specific_event("birth").get_year() == 1960)
        assert(prof.get_location_event("birth")["city"] == "Gallegos")
        assert(prof.get_accuracy_event("baptism") == "EXACT")
        assert(prof.get_specific_event("burial") == None)
        assert(len(prof.getEvents()) == 3)
        #Test of a big gedcom example.
        input_file = os.path.join(self.filelocation, "gedcom_example.ged")
        new_ged2 = db_gedcom(input_file)
        assert(new_ged2.get_family_by_ID("@FAMILY2@").getFather() == "@PERSON1@")
        assert(len(new_ged2.get_family_by_ID("@PARENTS@").getChildren()) == 2)
        assert("@PERSON1@" in new_ged2.get_family_by_ID("@PARENTS@").getChildren())
        assert("@PERSON4@" in new_ged2.get_family_by_ID("@PARENTS@").getChildren())
        prof2 = new_ged2.get_profile_by_ID("@PERSON1@") 
        assert(prof2.returnFullName() == "another name  surname")
        assert(prof2.getGender() == "M")
        assert(len(prof.getEvents()) == 3 )
    def test_generic_functions(self):
        '''
        Test of generic function methods in the module
        '''
        assert(get_date_info_from_ged("BEF 12 OCT 1999") == (1999, 10, 12, 'BEFORE', None, None, None) )
        assert(get_date_info_from_ged("BET 15 FEB 2001 AND MAR 2001") ==   (2001, 2, 15, 'BETWEEN', 2001, 3, None))
        assert(get_date_info_from_ged("AFT NOV 1700") == (1700, 11, None, 'AFTER', None, None, None))
        assert(get_date_info_from_ged("ABT 1710") == (1710, None, None, 'ABOUT', None, None, None))
        assert(get_date_info_from_ged("15 SEP 2001") == (2001, 9, 15, 'EXACT', None, None, None))
    def test_adding_and_saving_database(self):
        '''
        Test of addition to the gedcom file of new persons, families and saving it
        '''
        input_file = os.path.join(self.filelocation, "gedcom_test.gedcom")
        initial_gedcom = db_gedcom(input_file)
        no_gedcom = db_gedcom()
        #Profile to add an play :)
        profile1 = gedcom_profile(name ="Juana", surname = "Bargas")
        profile2 = gedcom_profile(name ="José", surname = "Sánchez")
        profile3 = gedcom_profile(name ="José", surname = "Bargas Sánchez")
        profile4 = gedcom_profile(name ="Juana", surname = "Bargas Sánchez")
        #Adding to initial gedcom
        assert(not "@I2@" in initial_gedcom.gedcom.keys())
        initial_gedcom.add_profile(profile1)
        assert("@I2@" in initial_gedcom.gedcom.keys())
        initial_gedcom.save_gedcom_file("delete_me_if_found.ged")
        assert(os.path.exists("delete_me_if_found.ged"))
        #Testing that I can read my own output
        initial_gedcom_again = db_gedcom("delete_me_if_found.ged")
        assert("@I2@" in initial_gedcom_again.gedcom.keys())
        os.remove("delete_me_if_found.ged")
        #Adding to the not existing database and also gedcom
        id1 = no_gedcom.add_profile(profile1)
        id2 = no_gedcom.add_profile(profile2)
        id3 = no_gedcom.add_profile(profile3)
        assert(profile4.get_id() == None)
        id4 = no_gedcom.add_profile(profile4)
        assert(profile4.get_id() == "@I4@")
        assert("@I4@" in no_gedcom.gedcom.keys())
        fm1 = no_gedcom.add_family(father = id1, mother = id2, children = [id3, id4])
        assert(fm1 == "@F1@")
        assert(no_gedcom.gedcom["@F1@"]["HUSB"]["VALUE"] == "@I1@")
        assert(len(no_gedcom.gedcom["@F1@"]["CHIL"]["VALUE"]) == 2)
        profs = no_gedcom.get_all_profiles()
        assert(len(profs) == 4)
    def test_wrong_event(self):
        '''
        Test introducing a wrong event
        '''
        event = event_profile("birth")
        assert( get_gedcom_formatted_date(event) == None)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()