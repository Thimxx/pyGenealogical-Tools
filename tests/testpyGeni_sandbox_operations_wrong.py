'''
Created on 21 oct. 2017

@author: Val
'''
import unittest
from tests.FIXTURES import WRONG_TOKEN, MAIN_SANDBOX_PROFILE
from pyGeni import profile, set_token, geniapi_common


class Test(unittest.TestCase):


    def setUp(self):
        #We used the sandbox here
        set_token(WRONG_TOKEN)
        profile.s.update_geni_address("https://sandbox.geni.com")


    def test_wrong_execution(self):
        '''
        Test error OAuth in Geni
        '''
        prof2 = profile.profile(MAIN_SANDBOX_PROFILE)
        self.assertFalse(prof2.properly_executed)
    
    def test_no_valid_token(self):
        '''
        Secure no valid token is found
        '''
        base_geni2 = geniapi_common.geni_calls()
        self.assertFalse(base_geni2.check_valid_genikey())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()