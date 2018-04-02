'''
Created on 1 abr. 2018

@author: Val
'''
import unittest
from pyGenealogy.common_profile import gen_profile
from datetime import date
from pyRegisters.pyelnortedecastilla import elnortedecastilla_reader


class Test(unittest.TestCase):


    def test_using_elnortedecastilla(self):
        '''
        Test checking el Norte de Castilla parser
        '''
        profile = gen_profile("José Luis", "García Martín")
        profile.setCheckedDate("birth_date", date(1931,4,2), "EXACT")
        reader = elnortedecastilla_reader()
        records = reader.profile_is_matched(profile)
        assert(len(records) > 0)
        
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_using_elnortedecastilla']
    unittest.main()