'''
Created on 28 mar. 2018

@author: Val
'''
import unittest
from pyRegisters.pygenanalyzer import gen_analyzer
from pyGenealogy.common_profile import gen_profile
from datetime import date
from pyGedcom.gedcom_profile import gedcom_profile
from pyGedcom.gedcompy_wrapper import gedcom_file


class Test(unittest.TestCase):
    '''
    This test will execute a test for using the different websites implemented
    '''


    def test_output_from_gedcom(self):
        '''
        It will take a gedcom dataclass and perform all executions available
        '''
        profile = gen_profile("Julián", "Gómez Gómez")
        profile.setCheckedDate("baptism", 1970, 4 ,2)
        profile.setCheckedDate("birth", 1960, 4, 2)
        profile.setCheckedDate("death", 2017, 2, 12)
        gedcom_profile.convert_gedcom(profile)
        
        
        new_gedcom = gedcom_file()
        new_gedcom.add_element(profile.individual)
        
        
        analysis = gen_analyzer(new_gedcom)
        analysis.execute()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()