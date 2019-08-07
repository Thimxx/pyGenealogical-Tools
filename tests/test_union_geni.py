'''
Created on 19 sept. 2017

@author: Val
'''
import unittest, os
import pyGeni as geni
from pyGeni.union import union
from tests.FIXTURES import UNION_SANDBOX
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
        un1 =union(UNION_SANDBOX)
        assert(un1.union_data["id"] == "union-155")
        assert(un1.union_data["url"] == "https://api.sandbox.geni.com/union-155")
        assert(un1.union_data["guid"] == "1149813")
        assert(un1.union_data["marriage"].get_date() == date(1923,4,3))
        assert(un1.union_data["marriage"].get_location()["county"] == 'Madrid')
        assert(len(un1.union_data["partners"]) == 2)
        assert(len(un1.union_data["children"]) == 4)
        #Testing base function
        assert(len(un1.getChildren()) == 4)
        assert(un1.getFather() == "profile-403")
        assert(un1.getMother() == "profile-404")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_union_geni_in_sandbox']
    unittest.main()