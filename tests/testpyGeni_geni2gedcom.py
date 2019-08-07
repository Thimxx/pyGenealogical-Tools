'''
Created on 26 mar. 2018

@author: Val
'''
import unittest, os
from pyGeni import profile, set_token, geni2gedcom
from tests.FIXTURES import GRANDFATHER_SANDBOX


class Test(unittest.TestCase):

    def setUp(self):
        #We used the sandbox here
        set_token(os.environ['SANDBOX_KEY'])
        profile.s.update_geni_address("https://sandbox.geni.com")
        #We locate the folder here
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2

    def test_get_gedcom(self):
        '''
        Test to obtain a gedcom down a profile
        '''
        file_ged = os.path.join(self.filelocation, "output_test_geni2gedcom.ged")
        if os.path.exists(file_ged): os.remove(file_ged)
        prof = profile.profile(GRANDFATHER_SANDBOX)
        tester = geni2gedcom.geni2gedcom(prof)
        geddb = tester.get_gedcom(file_ged)
        
        #gedcomfile = gedcom.parse(file_ged)
        counts = 0
        for person in geddb.get_all_profiles():
            if "Avoid Duplicate in Gedcom" in person.getName2Show(): counts += 1
        assert(counts == 1)
        
        if os.path.exists(file_ged): os.remove(file_ged)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()