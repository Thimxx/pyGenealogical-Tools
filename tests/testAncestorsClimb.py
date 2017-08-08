'''
Created on 8 ago. 2017

@author: Val
'''
import unittest
import os
from pyGeni.profile import profile
from tests.FIXTURES import PHILIPIVg, FLAVIAg
from analyzefamily.ancerstors_climb import climb


class testAncestorsClimb(unittest.TestCase):

    def setUp(self):
        self.token = os.environ['GENI_KEY']
 
    def testCountingOfAncestors(self):
        '''
        Testing the right calculation of ancestors. We know Philip IV was
        having duplicated ancestors, so the number will be lower than the 
        generation count.
        '''
        philip = profile(PHILIPIVg, self.token)
        
        climber = climb(philip)
        ancestors = climber.get_ancestors(4)
        i = 0
        for generation in ancestors:
            i = i + len(generation.values())
        assert(i == 23)
    def testStopWithNoAncestors(self):
        '''
        If there are no longer ancestors, the ancestor climb should stop.
        Checking if that works! This profile has only one generation available
        '''
        flavia = profile(FLAVIAg, self.token)
        
        climber = climb(flavia)
        ancestors = climber.get_ancestors(6)
        
        assert(len(ancestors) == 2)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()