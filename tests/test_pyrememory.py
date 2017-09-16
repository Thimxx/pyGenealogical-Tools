'''
Created on 16 sept. 2017

@author: Val
'''
import unittest
from datetime import date
from pyRegisters.pyrememori import rememori_reader
from pyGenealogy.common_profile import gen_profile

class Test(unittest.TestCase):


    def test_reading_an_input(self):
        profile = gen_profile("José", "García Martín")
        reader = rememori_reader()
        records = reader.profile_is_matched(profile)
        date1 = date(2016,4,2)
        date2 = date(2014,12,28)
        date1_found = False
        date2_found = False
        for profile in records:
            if (profile.gen_data["death_date"] == date1): date1_found = True
            if (profile.gen_data["death_date"] == date2): date2_found = True
        assert(date1_found)
        assert(date2_found)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_reading_an_input']
    unittest.main()