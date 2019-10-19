'''
Created on 15 oct. 2019

@author: Val
'''
import unittest
from pyGenealogy.common_profile import gen_profile
from pyRegisters.pyesquelas import esquelas_reader
from pyRegisters.pycementry_valencia import valencia_reader


class Test(unittest.TestCase):


    def test_esquelas(self):
        '''
        Test checking el Esquelas parser
        '''
        profile = gen_profile("José Luis", "García Martín")
        reader = esquelas_reader()
        records = reader.profile_is_matched(profile)
        assert(len(records) > 2)
        
    def test_valencia(self):
        '''
        Tests the database of valencia cementry
        '''
        profile = gen_profile("José", "García López")
        profile.setCheckedDate("death", 1993, accuracy="ABOUT")
        reader = valencia_reader()
        records = reader.profile_is_matched(profile)
        assert(len(records)>6)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()