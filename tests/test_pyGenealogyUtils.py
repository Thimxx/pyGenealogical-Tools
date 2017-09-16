'''
Created on 26 ago. 2017

@author: Val
'''
import unittest
from datetime import date
from pyGenealogy.gen_utils import is_year, get_children_surname, get_name_from_fullname, checkDateConsistency, getBestDate, get_partner_gender
from pyGenealogy.gen_utils import get_formatted_location, get_name_surname_from_complete_name, get_splitted_name_from_complete_name
from tests.FIXTURES import RIGHT_YEAR, RIGHT_YEAR_IN_A_TEXT, WRONG_YEAR, JUST_TEXT, RIGHT_YEAR_IN_A_DATE
from tests.FIXTURES import FATHER_SURNAME, MOTHER_SURNAME, SPANISH_CHILD_SURNAME
from tests.FIXTURES import FULL_NAME, FULL_NAME_SPANISH, ACTUAL_NAME, GENERIC_PLACE_STRING, GENERIC_PLACE_WITH_PLACE

class Test(unittest.TestCase):
    '''
    This module tests all functions inside pyGenealogy, but excluding the main
    class common_profile
    '''


    def test_correct_year_detection(self):
        '''
        Tests correct year detection
        '''
        assert(is_year(RIGHT_YEAR))
        self.assertFalse(is_year(RIGHT_YEAR_IN_A_DATE))
        self.assertFalse(is_year(RIGHT_YEAR_IN_A_TEXT))
        self.assertFalse(is_year(WRONG_YEAR))
        self.assertFalse(is_year(JUST_TEXT))
    
    def test_children_surname(self):
        '''
        Test output of children surname
        '''
        assert(get_children_surname(FATHER_SURNAME, MOTHER_SURNAME, "father_surname") == FATHER_SURNAME)
        assert(get_children_surname(FATHER_SURNAME, MOTHER_SURNAME, "spanish_surname") == SPANISH_CHILD_SURNAME)
        assert(get_children_surname(FATHER_SURNAME, MOTHER_SURNAME, "wrong_input") == "")
    
    def test_get_name(self):
        '''
        Test getting name out of complete name
        '''
        #Surnames
        list_father = [FATHER_SURNAME]
        list_mother = [MOTHER_SURNAME]
        assert(get_name_from_fullname(FULL_NAME, list_father, list_mother) == ACTUAL_NAME)
        assert(get_name_from_fullname(FULL_NAME_SPANISH, list_father, list_mother) == ACTUAL_NAME)
    
    def test_date_check(self):
        '''
        Test of the function for date check
        '''
        date1 = date(2017,1,1)
        date2 = date(2016,1,1)
        date3 = date(2015,1,1)
        date2b = date(2014,2,1)
        date4 = date(2014,1,1)
        assert(checkDateConsistency(None,date2b, None,None,None,None))
        assert(checkDateConsistency(date4,None, None,None,None,None))
        assert(checkDateConsistency(date4,None, None,None,None,date1))
        assert(checkDateConsistency(date4,None, date3,date2,date1,None))
        
        assert(not checkDateConsistency(date1,None, None,None,date4,None))
        assert(not checkDateConsistency(None,None, date1,None,date4,None))
        assert(not checkDateConsistency(date1,None, date4,None,None,None))
        #Checking that about dates are ok although the date2b is later than date4
        assert(checkDateConsistency(date2b, None, None, None, date4, date4, accuracy_death = "ABOUT", accuracy_burial = "ABOUT"))
    
    def test_getting_a_date(self):
        '''
        Test the module for merging dates
        '''
        date1 = date(2018,1,1)
        date2 = date(2016,1,1)
        date3, accuracy3 = getBestDate(date1, "EXACT", date2, "EXACT")
        assert(date3 == date1)
        assert(accuracy3 == "EXACT")
        
        date4, accuracy4 = getBestDate(date1, "AFTER", date2, "EXACT")
        assert(date4 == date2)
        assert(accuracy4 == "EXACT")
        
        date5, accuracy5 = getBestDate(date1, "AFTER", date2, "BEFORE")
        assert(date5 == date1)
        assert(accuracy5 == "AFTER")
        
        date6, accuracy6 = getBestDate(date1, "ABOUT", date2, "BEFORE")
        assert(date6 == date2)
        assert(accuracy6 == "BEFORE")
        
        date7, accuracy7 = getBestDate(date1, "ABOUT", date2, "ABOUT")
        assert(date7 == date(2017,1,1))
        assert(accuracy7 == "ABOUT")
        
        date8, accuracy8 = getBestDate(date1, "LALALA", date2, "ABOUT")
        assert(date8 == None)
        assert(accuracy8 == None)
    
    def test_get_location_data(self):
        '''
        Test the translation of location data using google API
        '''
        
        output = get_formatted_location(GENERIC_PLACE_STRING, language="en")
        assert(output["latitude"] > 41.4781556 )
        assert(output["longitude"] < -4.5863 )
        assert(output["city"] == "Portillo")
        assert(output["county"] == "Valladolid")
        assert(output["state"] == "Castilla y León")
        assert(output["country"] == "Spain")
        self.assertFalse("place_name" in output.keys())
        output2 = get_formatted_location(GENERIC_PLACE_WITH_PLACE, language="es")
        assert(output2["latitude"] > 41.535338 )
        assert(output2["longitude"] < -4.53061)
        assert(output2["city"] == "La Parrilla")
        assert(output2["county"] == "Valladolid")
        assert(output2["state"] == "Castilla y León")
        assert(output2["country"] == "España")
        assert(output2["place_name"] == "Nuestra Señora de los Remedios")
    
    def test_return_sex(self):
        '''
        Test function returning sex of partner
        '''
        assert(get_partner_gender("M") == "F")
        assert(get_partner_gender("F") == "M")
        assert(get_partner_gender("G") == None)
    
    def test_wrong_google_maps_message(self):
        '''
        Test wrong google maps message
        '''
        assert(get_formatted_location("") == None)
    
    def test_wrong_inputs(self):
        '''
        Test metaphone differences
        '''
        assert("Petra Regalada" == get_name_from_fullname("Petra Regalada Molpezérez Gómez", ['Molpecérez', 'Molpezerez'], ['Gómez', 'Gomez']))
        assert("Segunda" == get_name_from_fullname("Segunda Molpécerez Gómez", ['Molpecérez', 'Molpezerez'], ['Gómez', 'Gomez']))
        
        #Secure the updated version of metaphone takes into account b/v
        assert("Francisco" == get_name_from_fullname("Francisco Vaca Gomez", ['Baca'], ['Gómez', 'Gomez'], language="es"))
        
    def test_get_name_from_complete_name(self):
        '''
        Test get name from complete name
        '''
        name1 = "José Martínez  Pérez "
        name, surname = get_name_surname_from_complete_name(name1, convention="spanish_surname")
        assert(name == "José")
        assert(surname == "Martínez Pérez")
        
        name2 = "John Smith"
        name, surname = get_name_surname_from_complete_name(name2)
        assert(name == "John")
        assert(surname == "Smith")
        
        name, surname = get_name_surname_from_complete_name(name2, convention="wrong_convention")
        assert(name == None)
        assert(surname == None)
        
        #This one makes sure that having a spanish naming convention with only one surname will work.
        name3 = "Benito Molpecérez"
        name, surname = get_name_surname_from_complete_name(name3, convention = "spanish_surname")
        assert(name == "Benito")
        assert(surname == "Molpecérez")
    def test_name_splitted(self):
        '''
        Test the split of names function
        '''
        c_name1 = "Juan  Martínez "
        s_name = get_splitted_name_from_complete_name(c_name1)
        assert(s_name[0] == "Juan")
        assert(s_name[1] == "Martínez")
        
        c_name2 = "Juan   DE la MANcha del luGAR "
        s_name = get_splitted_name_from_complete_name(c_name2, language="es")
        assert(s_name[0] == "Juan")
        assert(s_name[1] == "de la Mancha")
        assert(s_name[2] == "del Lugar")
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()