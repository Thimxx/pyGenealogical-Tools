'''
Created on 8 ago. 2017

@author: Val
'''
import unittest, os
from pyGeni.data_models import geni_union
from pyGeni.immediate_family import immediate_family
from pyGeni import  geniapi_common
from tests import FIXTURES 


class testpyGeniNoProfile(unittest.TestCase):
 
    def setUp(self):
        self.token = os.environ['GENI_KEY']
        geniapi_common.s.update_geni_address("https://www.geni.com")
        geniapi_common.s.VERIFY_INPUT = "standard"
        

    def testgenerateunion(self):
        '''
        This test checks that a union is properly registered in the data model
        when introduced as input from geni
        '''
        union_test = geni_union(FIXTURES.UNION_EXAMPLE, FIXTURES.UNION_EXAMPLE_ID)
        assert(union_test.union_id == FIXTURES.UNION_EXAMPLE_ID)
        #Check of the parent
        assert(union_test.is_profile_parent(FIXTURES.UNION_EXAMPLE_PARENT))
        self.assertFalse(union_test.is_profile_child(FIXTURES.UNION_EXAMPLE_PARENT))
        
        #Check the children
        self.assertFalse(union_test.is_profile_parent(FIXTURES.UNION_EXAMPLE_CHILD))
        assert(union_test.is_profile_child(FIXTURES.UNION_EXAMPLE_CHILD))
        
        #Check random profile
        self.assertFalse(union_test.is_profile_parent(FIXTURES.UNION_EXAMPLE_NOT_INCLUDED))
        self.assertFalse(union_test.is_profile_child(FIXTURES.UNION_EXAMPLE_NOT_INCLUDED))
        
        #Check the number of children
        assert(len(union_test.children) == FIXTURES.UNION_EXAMPLE_NUMBER_CHILDREN)
        
    def testimmediatefamily(self):
        '''
        This test confirms that the immediate family gets the right values
        '''
        philip_family = immediate_family(self.token, FIXTURES.PHILIPIVid)
        assert (len(philip_family.parents) == 3)
        assert(len(philip_family.sibligns) == 7)
        assert(len(philip_family.partner) == 4)
        assert(len(philip_family.children) == 17)
        assert(philip_family.union_extracted)
        
    def test_immediatefamily_not_operational(self):
        '''
        I do not know why, but this profile is failing when providing
        the immediate family
        '''
        failing_family = immediate_family(self.token, FIXTURES.PROFILE_NOT_WORKING)
        
        assert (len(failing_family.parents) == 0)
        assert(len(failing_family.sibligns) == 0)
        assert(len(failing_family.partner) == 0)
        assert(len(failing_family.children) == 0)
        self.assertFalse(failing_family.union_extracted)
        
    def test_valid_token(self):
        '''
        Secure that we are using a valid token
        '''
        base_geni = geniapi_common.geni_calls(self.token)
        assert(base_geni.check_valid_genikey())
    
    def test_no_valid_token(self):
        '''
        Secure no valid token is found
        '''
        base_geni2 = geniapi_common.geni_calls("")
        self.assertFalse(base_geni2.check_valid_genikey())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()