'''
Created on 27 ago. 2017

@author: Val
'''
import unittest
from pyGeni import set_token
from pyGeni import profile, geni_request_get, geni_request_post
from tests.FIXTURES import GENI_WRONG_GET_METHOD
import os


class Test_sandbox_certificate(unittest.TestCase):

    def setUp(self):
        #We used the sandbox here
        set_token(os.environ['SANDBOX_KEY'])
        profile.s.update_geni_address("https://www.sandbox.geni.com")


    def test_exception_on_standard_verify(self):
        '''
        Test that sandbox geni is not fixed
        '''
        try:
            profile.profile("1149101")
            assert(False)
        except:
            assert(True)
            
    
    def test_error_get_post(self):
        '''
        Test error get and post
        '''
        data = geni_request_get(GENI_WRONG_GET_METHOD)
        assert("error" in data.json())
        data2 = geni_request_post(GENI_WRONG_GET_METHOD)
        assert("error" in data2.json())
    
   
         
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()