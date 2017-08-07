import unittest
import os
from pyGeni import profile
from tests.FIXTURES import *


class testpyGeni(unittest.TestCase):
    def setUp(self):
        token = os.environ['GENI_KEY']
        self.philip = profile.profile(PHILIPIVg, token)

    def testGettingCorrectName(self):
        '''
        This test checks that the name of philip the IV of Spain is properly detected
        '''
        assert( "Felipe" in self.philip.nameLifespan())
        assert( "1605" in self.philip.nameLifespan())
        assert( "1665" in self.philip.nameLifespan())

    def testRelationsInfo(self):
        '''
        This test checks that all relationships of the profile are correct
        '''
        assert (len(self.philip.parents) == 2)
        assert(len(self.philip.sibligns) == 8)
        assert(len(self.philip.partner) == 3)
        assert(len(self.philip.children) == 16)
    
    def testgetrightid(self):
        '''
        Confirms that the id output is correct
        '''
        assert(self.philip.get_id() == PHILIPIVid)


if __name__ == '__main__':
    unittest.main()