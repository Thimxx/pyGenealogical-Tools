'''
Created on 27 ago. 2017

@author: Val
'''
import unittest
from pyGeni import profile
import os, time


class Test_sandbox_certificate(unittest.TestCase):

    def setUp(self):
        time.sleep(120)
        #We used the sandbox here
        self.stoken = os.environ['SANDBOX_KEY']
        profile.s.update_geni_address("https://www.sandbox.geni.com")


    def test_exception_on_standard_verify(self):
        '''
        Test that sandbox geni is not fixed
        '''
        try:
            profile.profile("1149101", self.stoken)
            assert(False)
        except:
            assert(True)
    
   
         
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()