'''
Created on 27 mar. 2018

@author: Val
'''
import unittest, os
from pyGeni import profile, set_token
from tests.FIXTURES import MAIN_SANDBOX_PROFILE
from pyGedcom.gedcom_profile import gedcom_profile
from gedcom import Element
class TestMixedModules(unittest.TestCase):
    '''
    This module will test mixed operations between the different existing modules
    '''
    def setUp(self):
        #We used the sandbox here
        set_token(os.environ['SANDBOX_KEY'])
        profile.s.update_geni_address("https://sandbox.geni.com")
    def test_geni_to_gedcom(self):
        '''
        Test a geni profile to Gedcom
        '''
        prof = profile.profile(MAIN_SANDBOX_PROFILE, type_geni="")
        assert( "Testing" in prof.nameLifespan())
        gedcom_profile.convert_gedcom(prof)
        data_event = prof.get_event_element("birth")
        element_top = data_event[1]
        element_sub = element_top.child_elements[1]
        #We crosscheck the value is properly included in the file
        assert(element_sub.tag == "PLAC")
        assert("Gallegos" in element_sub.value)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()