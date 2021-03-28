'''
Created on 19 sept. 2017

@author: Val
'''
import unittest, os
import pyGeni as geni
from pyGeni.union import union
from tests.FIXTURES import MARRIAGE_ID
from datetime import date

class Test(unittest.TestCase):

    def setUp(self):
        '''
        We introduce the data here
        '''
        #We used the sandbox here
        geni.update_geni_address("https://sandbox.geni.com")
        geni.set_token(os.environ['SANDBOX_KEY'])
    def test_union_geni_in_sandbox(self):
        '''
        Test union in sandbox
        '''
        un1 =union(MARRIAGE_ID)
        assert(un1.union_data["id"] == MARRIAGE_ID)
        assert(un1.union_data["url"] == "https://api.sandbox.geni.com/union-96")
        assert(un1.union_data["guid"] == "328817")
        assert(un1.union_data["marriage"].get_date() == date(1960,1,30))
        assert(un1.union_data["marriage"].get_location()["city"] == 'Madrid')
        assert(len(un1.union_data["partners"]) == 2)
        assert(len(un1.union_data["children"]) == 3)
        #Testing base function
        assert(len(un1.getChildren()) == 3)
        assert(un1.getFather() == "profile-452")
        assert(un1.getMother() == "profile-459")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_union_geni_in_sandbox']
    unittest.main()