'''
Created on 15 oct. 2019

@author: Val
'''
import unittest
from pyGenealogy.common_profile import gen_profile
from datetime import date
from pyRegisters.pyesquelas import esquelas_reader


class Test(unittest.TestCase):


    def testName(self):
        '''
        Test checking el Esquelas parser
        '''
        profile = gen_profile("José Luis", "García Martín")
        profile.setCheckedDate("birth_date", date(1931,4,2), "EXACT")
        reader = esquelas_reader()
        records = reader.profile_is_matched(profile)
        assert(len(records) > 2)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()