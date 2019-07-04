'''
Created on 3 abr. 2018

@author: Val
'''
import unittest
from datetime import date
from pyGenealogy.common_profile import gen_profile
from pyRegisters.pyabc import abc_reader


class Test(unittest.TestCase):


    def test_using_abc_records(self):
        '''
        Test use of abc records
        '''
        profile = gen_profile("José", "García Reyes")
        profile.setCheckedDate("birth_date", date(1931,4,2), "EXACT")
        reader = abc_reader()
        records = reader.profile_is_matched(profile)
        assert(len(records) >0 )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_using_abc_records']
    unittest.main()