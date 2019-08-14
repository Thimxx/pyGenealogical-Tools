'''
Created on 28 mar. 2018

@author: Val
'''
import unittest, os
from pyRegisters.pygenanalyzer import gen_analyzer
from pyGenealogy.common_profile import gen_profile
from pyGedcom.gedcom_profile import gedcom_profile
from pyGedcom.gedcom_database import db_gedcom
from pyGenealogy.common_database import gen_database
from pyRootsMagic.pyrm_database import database_rm


class Test(unittest.TestCase):
    '''
    This test will execute a test for using the different websites implemented
    '''
    def setUp(self):
        "Creation of the different parameters needs for execution, including location of database"
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2
    def test_output_from_gedcom(self):
        '''
        It will take a gedcom dataclass and perform all executions available
        '''
        profile = gen_profile("Julián", "Gómez Gómez")
        profile.setCheckedDate("baptism", 1970, 4 ,2)
        profile.setCheckedDate("birth", 1960, 4, 2)
        profile.setCheckedDate("death", 2017, 2, 12)
        gedcom_profile.convert_gedcom(profile)
        
        dbgenea = gen_database()
        dbgenea.add_profile(profile)
        
        
        profile2 = gedcom_profile(name = "Julián", surname = "Gómez Gómez")
        profile2.setCheckedDate("baptism", 1970, 4 ,2)
        profile2.setCheckedDate("birth", 1960, 4, 2)
        profile2.setCheckedDate("death", 2017, 2, 12)
        assert("BIRT" in profile2.individual)
        dbged = db_gedcom()
        dbged.add_profile(profile2)
        
        #Test that works with RootsMagic
        input_file = os.path.join(self.filelocation, "Rootstest.rmgc")
        dbroots = database_rm(input_file)
        
        analysis = gen_analyzer()
        analysis.execute(dbgenea)
        analysis.execute(dbged)
        analysis.execute(dbroots)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()