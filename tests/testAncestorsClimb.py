'''
Created on 8 ago. 2017

@author: Val
'''
import unittest
import os
from pyGeni.profile import profile
from tests.FIXTURES import PHILIPIVg
from analyzefamily.ancerstors_climb import climb


class testAncestorsClimb(unittest.TestCase):


    def testCountingOfAncestors(self):
        '''
        Testing the right calculation of ancestors. We know Philip IV was
        having duplicated ancestors, so the number will be lower than the 
        generation count.
        '''
        token = os.environ['GENI_KEY']
        philip = profile(PHILIPIVg, token)
        
        climber = climb(philip)
        ancestors = climber.get_ancestors(4)
        i = 0
        for generation in ancestors:
            i = i + len(generation.values())
        assert(i == 23)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()