'''
Created on 13 ago. 2017

@author: Val
'''
import unittest
from datetime import date
from pyGenealogy.common_profile import gen_profile


class Test(unittest.TestCase):


    def test_introducing_gender(self):
        '''
        Testing right introduction of gender in common_profile
        '''
        profile = gen_profile("Name", "Surname")
        assert(profile.setCheckedGender("F"))
        assert(profile.setCheckedGender("M"))
        self.assertFalse(profile.setCheckedGender("J"))
    def test_introducing_birth_date(self):
        '''
        Testing right introduction of birth date in common_profile
        '''
        birth_date = date(2016,10, 20)
        profile = gen_profile("Name", "Surname")
        assert(profile.setCheckedBirthDate(birth_date, "EXACT"))
        assert(profile.setCheckedBirthDate(birth_date, "BEFORE"))
        assert(profile.setCheckedBirthDate(birth_date, "AFTER"))
        assert(profile.setCheckedBirthDate(birth_date, "ABOUT"))
        assert(not profile.setCheckedBirthDate(birth_date, "OTHER"))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_introducing_gender']
    unittest.main()