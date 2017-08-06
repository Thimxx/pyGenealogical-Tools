import unittest
from pyGeni import profile
from tests.FIXTURES import *

class testpyGeni(unittest.TestCase):
    def setUp(self):
        self.philip = profile.profile(PHILIPIVg)
        self.philip.relations()

    def testGettingCorrectName(self):
        '''
        This test checks that the name of philip the IV of Spain is properly detected
        '''
        assert( "Felipe" in self.philip.nameLifespan())
        assert( "1605" in self.philip.nameLifespan())
        assert( "1665" in self.philip.nameLifespan())

    def testUnionDataCorrect(self):
        '''
        This test will check that unions are correct
        '''
        spouses, children, parent_marriage = self.philip.parse_union(PHILIPIV_PARENT_UNIONg )
        assert(len(spouses) == 2)
        assert(parent_marriage)
        assert(len(children) == 8)

    def testRelationsInfo(self):
        '''
        This test checks that all relationships of the profile are correct
        '''
        assert (len(self.philip.parents) == 2)
        assert(len(self.philip.sibligns) == 8)
        assert(len(self.philip.partner) == 3)
        assert(len(self.philip.children) == 16)




if __name__ == '__main__':
    unittest.main()