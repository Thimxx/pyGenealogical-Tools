'''
Created on 18 abr. 2020

@author: Val
'''
import unittest, os
from tests.FIXTURES import FILE2DELETE_QUALITY
from pyRootsMagic.pyrm_database import database_rm
from shutil import copyfile
from analyzefamily.quality_check import qcheck


class Test(unittest.TestCase):
    def setUp(self):
        "Creation of the different parameters needs for execution, including location of database"
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2
    def test_qualify_of_db(self):
        '''
        Test quality parameters
        '''
        #Just in case the file was created before
        if os.path.exists(FILE2DELETE_QUALITY): os.remove(FILE2DELETE_QUALITY)
        
        #input_file = os.path.join(self.filelocation, "RootsMagic_analyzer.rmgc")
        input_file = os.path.join(self.filelocation, "Rootstest.rmgc")
        copyfile(input_file , FILE2DELETE_QUALITY)
        dbroots = database_rm(FILE2DELETE_QUALITY)
        
        qdata = qcheck(dbroots)
        issue, issue_dict = qdata.execute()
        
        assert(issue == 7)
        assert(6 in issue_dict["gender"])
        assert(9 in issue_dict["existing_date"])
        
        dbroots.close_db()
        
        if os.path.exists(FILE2DELETE_QUALITY): os.remove(FILE2DELETE_QUALITY)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_qualify_of_db']
    unittest.main()