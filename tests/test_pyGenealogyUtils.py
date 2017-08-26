'''
Created on 26 ago. 2017

@author: Val
'''
import unittest
from pyGenealogy.gen_utils import is_year, get_children_surname, get_name_from_fullname
from tests.FIXTURES import RIGHT_YEAR, RIGHT_YEAR_IN_A_TEXT, WRONG_YEAR, JUST_TEXT, RIGHT_YEAR_IN_A_DATE
from tests.FIXTURES import FATHER_SURNAME, MOTHER_SURNAME, SPANISH_CHILD_SURNAME
from tests.FIXTURES import FULL_NAME, FULL_NAME_SPANISH, ACTUAL_NAME

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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()