'''
Created on 26 ago. 2017

@author: Val
'''
import unittest
from datetime import date
from pyGenealogy.gen_utils import is_year, get_children_surname, get_name_from_fullname, checkDateConsistency, getBestDate, get_partner_gender
from pyGenealogy.gen_utils import get_formatted_location, get_name_surname_from_complete_name, get_splitted_name_from_complete_name
from pyGenealogy.gen_utils import get_score_compare_names, get_score_compare_dates, get_compared_data_file, adapted_doublemetaphone
from pyGenealogy.gen_utils import get_location_standard
from tests.FIXTURES import RIGHT_YEAR, RIGHT_YEAR_IN_A_TEXT, WRONG_YEAR, JUST_TEXT, RIGHT_YEAR_IN_A_DATE
from tests.FIXTURES import FATHER_SURNAME, MOTHER_SURNAME, SPANISH_CHILD_SURNAME, GENERIC_PLACE_CAPITALS
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
        
        assert(get_name_from_fullname("Eusebio Masa Y Viloria", ['Masa'], ['Viloria'], language="es") == "Eusebio")
        #This one checks the bug of "de Bargas" issue
        assert(get_name_from_fullname("Geronima De Bargas Albarez", ['Vargas'], ['Álvarez'], language="es") == "Gerónima")
        #The bug with the "de" particle
        assert(get_name_from_fullname("Florentina Montemayor Leon", ['Montemayor'], ['de Leon'], language="es") == "Florentina")
        #Checking the bug of "Maria de la Cruz" captured as just Maria, due to similarity phonetically of Cruz and Grazia
        assert(get_name_from_fullname("Maria De La Cruz Garcia", ['García', 'Grazia'], ['Díez', 'Díaz'], language="es") == "María de la Cruz" )
        
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
        
        #Test bug of burial and death
        assert(checkDateConsistency(None,None, None, None,date4,date2b, accuracy_death = "ABOUT", accuracy_burial = "BEFORE"))
    
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
        assert(output["longitude"] < -4.0 )
        assert(output["city"] == "Portillo")
        assert(output["county"] == "Valladolid")
        assert(output["state"] == "Castile and León")
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
        
        assert(get_location_standard(output2) == "La Parrilla, Valladolid, Castilla y León, España" )
        
        output3 = get_formatted_location("La Asunción, Herrera De Duero, Valladolid, Spain", language="es")
        
        assert("city" in output3)
        
        
        output4 = get_formatted_location("")
        assert("raw" in output4)
        self.assertFalse("country" in output4)
        
        #Suggestino from https://stackoverflow.com/questions/47063366/google-maps-geocoding-api-zero-results-example/47092855
        output5 = get_formatted_location("postal_code%3A12345%7Ccountry%3ASE,,,", language="es")
        assert("raw" in output5)
        self.assertFalse("country" in output5)
    
    def test_return_sex(self):
        '''
        Test function returning sex of partner
        '''
        assert(get_partner_gender("M") == "F")
        assert(get_partner_gender("F") == "M")
        assert(get_partner_gender("G") == None)
    
    
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
        name, surname, _ = get_name_surname_from_complete_name(name1, convention="spanish_surname")
        assert(name == "José")
        assert(surname == "Martínez Pérez")
        
        name2 = "John Smith"
        name, surname, _ = get_name_surname_from_complete_name(name2)
        assert(name == "John")
        assert(surname == "Smith")
        
        name, surname, _ = get_name_surname_from_complete_name(name2, convention="wrong_convention")
        assert(name == None)
        assert(surname == None)
        
        #This one makes sure that having a spanish naming convention with only one surname will work.
        name3 = "Benito Molpecérez"
        name, surname, _ = get_name_surname_from_complete_name(name3, convention = "spanish_surname")
        assert(name == "Benito")
        assert(surname == "Molpecérez")
        
        name4 = "Valentín Lupicino"
        name, surname, _ = get_name_surname_from_complete_name(name4, convention = "spanish_surname", language="es")
        assert(name == name4)
        assert(surname == "")
        
        name5 = "Valentin Lupicino Martin"
        name, surname, _ = get_name_surname_from_complete_name(name5, convention = "spanish_surname", language="es")
        assert(name == "Valentín Lupicino")
        assert(surname == "Martín")
        
        name6 = "Pedro"
        name, surname, _ = get_name_surname_from_complete_name(name6, convention = "spanish_surname", language="es")
        assert(name == "Pedro")
        assert(surname == "")
        
        name7 = "Hijinia"
        name, surname, _ = get_name_surname_from_complete_name(name7, convention = "spanish_surname", language="es")
        assert(name == "Higinia")
        assert(surname == "")
        #Bug with particle San in Spanish
        name8 = "Michaela San Miguel"
        name, surname, _ = get_name_surname_from_complete_name(name8, convention = "spanish_surname", language="es")
        assert(name == "Micaela")
        assert(surname == "San Miguel")
    def test_name_splitted(self):
        '''
        Test the split of names function
        '''
        c_name1 = "Juan  Martínez "
        s_name = get_splitted_name_from_complete_name(c_name1)
        assert(s_name[0][0] == "Juan")
        assert(s_name[0][1] == "Martínez")
        
        c_name2 = "Juan   DE la MANcha del chaCON "
        s_name = get_splitted_name_from_complete_name(c_name2, language="es")
        assert(s_name[0][0] == "Juan")
        assert(s_name[0][1] == "de la Mancha")
        assert(s_name[0][2] == "del Chacón")
        
    def test_compare_names(self):
        '''
        Test comparison and score of names
        '''
        score, factor = get_score_compare_names("Juan", "Fernandez", "Macias", "García")
        assert(score + factor == 0.0)
        score, factor = get_score_compare_names("Juan", "Gomez", "Juan", "Gómez")
        assert(score == 4.0)
        assert(factor == 1.0)
        score, factor = get_score_compare_names("Juan Antonio", "Gomez Perez", "Juan", "Gómez")
        assert(score > 3.0)
        assert(factor > 0.8)
        score, factor = get_score_compare_names("Juan José Fernando", "Gomez Perez", "Agustín Juan", "Gómez")
        assert(score > 2.0)
        assert(factor > 0.1)
        score, factor = get_score_compare_names("Juan", "de la Fuente", "Juan", "Fuente", language="es")
        assert(score == 4.0)
        assert(factor == 1.0)
    
    def test_compare_date(self):
        '''
        Test comparison of dates with scoring
        '''
        date1 = date(2018,1,1)
        date2 = date(2018,2,6)
        
        score, factor = get_score_compare_dates(date1, "EXACT", date1, "EXACT")
        assert(score == 2.0)
        assert(factor == 1.0)
        score, factor = get_score_compare_dates(date1, "EXACT", date(2018,1,2), "EXACT")
        assert(score >1.8)
        assert(factor > 0.9)
        score, factor = get_score_compare_dates(date1, "EXACT", date(2018,1,8), "EXACT")
        assert(score >1.4)
        assert(factor > 0.7)
        score, factor = get_score_compare_dates(date1, "EXACT", date(2018,2,6), "EXACT")
        assert(score >0.8)
        assert(factor > 0.4)
        score, factor = get_score_compare_dates(date1, "EXACT", date(2019,1,1), "EXACT")
        assert(score >0.08)
        assert(factor > 0.04)
        #About parameters
        score, factor = get_score_compare_dates(date2, "EXACT", date(2017,1,1), "ABOUT")
        assert(score == 1.0)
        assert(factor == 1.0)
        score, factor = get_score_compare_dates(date2, "EXACT", date(2016,1,1), "ABOUT")
        assert(score >0.95)
        assert(factor == 1.0)
        score, factor = get_score_compare_dates(date2, "ABOUT", date(2013,1,1), "EXACT")
        assert(score >0.2)
        assert(factor > 0.4)
        score, factor = get_score_compare_dates(date2, "EXACT", date(2010,1,1), "ABOUT")
        assert(score < 0.1)
        assert(factor > 0.1)
        #Let's check the dates
        score, factor = get_score_compare_dates(date(2010,1,1), "ABOUT", date(2010,1,1), "ABOUT")
        assert(score == 1.0)
        assert(factor == 1.0)
        score, factor = get_score_compare_dates(date(2014,1,1), "ABOUT", date(2010,1,1), "ABOUT")
        assert(score > 0.499)
        assert(factor > 0.799)
        score, factor = get_score_compare_dates(date(2017,1,1), "ABOUT", date(2010,1,1), "ABOUT")
        assert(score > 0.37999)
        assert(factor > 0.41999)
        score, factor = get_score_compare_dates(date(2030,1,1), "ABOUT", date(2010,1,1), "ABOUT")
        assert(score > 0.04999)
        assert(factor > 0.074999)
    def test_bug_capital_letters(self):
        '''
        Test Capital Letters are fixed
        '''
        output = get_formatted_location(GENERIC_PLACE_CAPITALS, language="es")
        assert(output["place_name"] == "San Juan Evangelista del Arrabal")
        assert(output["country"] == "España")
    
    def test_compare_with_files(self):
        '''
        Test comparing surnames and names with files
        '''
        assert("data" == get_compared_data_file("data", language="jp")[0])
        result, value = get_compared_data_file("Garcia", language="es", data_kind="surname")
        assert(result == "García")
        assert(value == 1.0)
        result2, value2 = get_compared_data_file("Martin", language="es", data_kind="surname")
        assert(result2 == "Martín")
        assert(value2 == 1.0)
        result3 = get_compared_data_file("Martines", language="es", data_kind="surname")
        assert(result3[0] == "Martínez")
        result4 = get_compared_data_file("albares", language="es", data_kind="surname")
        assert(result4[0] == "Álvarez")
        
        
        result5 = get_compared_data_file("jesus", language="es", data_kind="name")
        assert(result5[0] == "Jesús")
        result6 =  get_compared_data_file("jesuz", language="es", data_kind="name")
        assert(result6[0] == "Jesús")
        result7 =  get_compared_data_file("balentin", language="es", data_kind="name")
        assert(result7[0] == "Valentín")
    
    def test_adapted_metaphone(self):
        '''
        Test adapted metaphone
        '''
        assert(adapted_doublemetaphone("Mathea", language="es") == adapted_doublemetaphone("Matea", language="es"))
        assert(adapted_doublemetaphone("Catalina", language="es") == adapted_doublemetaphone("Cathalina", language="es"))
        assert(adapted_doublemetaphone("Phelipe", language="es") == adapted_doublemetaphone("Felipe", language="es"))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()