'''
Created on 1 abr. 2018

@author: Val
'''
import unittest
from pyGenealogy.common_profile import gen_profile
from datetime import date
from pyRegisters.pyvocento import vocento_reader


class Test(unittest.TestCase):


    def test_using_vocento_reader(self):
        '''
        Test checking all Vocento Parses parser
        '''
        profile = gen_profile("José Luis", "García Martín")
        profile.setCheckedDateWithDates("birth", date(1931,4,2), "EXACT")
        reader = vocento_reader()
        records = reader.profile_is_matched(profile)
        assert(len(records) > 0)
        
        profile2 = gen_profile("Carmen", "Martín")
        profile2.setCheckedDateWithDates("birth", date(1935,4,2), "EXACT")
        reader = vocento_reader(reader = "ELCORREO")
        records = reader.profile_is_matched(profile2)
        assert(len(records) > 1)
        
        profile3 = gen_profile("José", "García Pérez")
        reader = vocento_reader(reader = "ELDIARIOMONTAÑES")
        records = reader.profile_is_matched(profile3)
        assert(len(records) >2)
        
        
        profile4 = gen_profile("María", "Martín")
        profile4.setCheckedDateWithDates("birth", date(1942,4,2), "EXACT")
        reader = vocento_reader(reader = "IDEAL")
        records = reader.profile_is_matched(profile4)
        assert(len(records) >6)
        
        
        profile5 = gen_profile("José", "Martínez García")
        profile5.setCheckedDateWithDates("birth", date(1933,4,2), "EXACT")
        reader = vocento_reader(reader = "LARIOJA")
        records = reader.profile_is_matched(profile5)
        assert(len(records) >1)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_using_elnortedecastilla']
    unittest.main()