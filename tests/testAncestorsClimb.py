'''
Created on 8 ago. 2017

@author: Val
'''
import unittest
import os
from pyGeni import set_token
from pyGeni.profile import profile
from tests.FIXTURES import PHILIPIVg, FLAVIAg, COUSIN_PROFILE
from analyzefamily.ancerstors_climb import climb


class testAncestorsClimb(unittest.TestCase):

    def setUp(self):
        set_token(os.environ['GENI_KEY'])
 
    def testCountingOfAncestors(self):
        '''
        Testing the right calculation of ancestors. We know Philip IV was
        having duplicated ancestors, so the number will be lower than the 
        generation count.
        '''
        philip = profile(PHILIPIVg)
        
        climber = climb(philip)
        ancestors, profiles = climber.get_ancestors(4)
        i = 0
        for generation in ancestors:
            i = i + len(generation.values())
        assert(i == 23)
        assert(len(profiles) == 23)
    def testStopWithNoAncestors(self):
        '''
        If there are no longer ancestors, the ancestor climb should stop.
        Checking if that works! This profile has only one generation available
        '''
        flavia = profile(FLAVIAg)
        
        climber = climb(flavia)
        ancestors = climber.get_ancestors(6)
        
        assert(len(ancestors) == 2)
    
    def testCousinsExecution(self):
        '''
        We will test the cousins execution in different way. Will be tested by
        number, not by person
        '''
        philip = profile(COUSIN_PROFILE)
        generations = 2
        
        climber = climb(philip)
        ancestors, anc_count, profiles = climber.get_cousins(generations)
        
        total_center = 0
        total_outside = 0
        for i in range(0, generations+1):
            total_center = total_center + anc_count[i][i]
            for j in range(i+1, generations + 1):
                total_outside = total_outside + anc_count[i][j]
        assert(total_center == 7) 
        assert(total_outside == 0) 
        
        total_final = 0
        for i in range(0, generations+1):
            for j in range(0, generations + 1):
                total_final = total_final + anc_count[i][j]
        assert(total_final == 36)
        assert(len(profiles) == 36)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()