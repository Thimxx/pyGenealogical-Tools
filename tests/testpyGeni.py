import unittest
import os
from pyGeni import profile
from tests.FIXTURES import *
from pyGeni.data_models import geni_union


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
        
    def testUsingIdProfile(self):
        '''
        This test checks that using a different input id the id obtained is the same.
        '''
        token = os.environ['GENI_KEY']
        philip_bis = profile.profile(PHILIPIVget, token , "")
        assert( philip_bis.get_id() == self.philip.get_id())

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

    def testgenerateunion(self):
        '''
        This test checks that a union is properly registered in the data model
        when introduced as input from geni
        '''
        union_test = geni_union(UNION_EXAMPLE, UNION_EXAMPLE_ID)
        assert(union_test.union_id == UNION_EXAMPLE_ID)
        #Check of the parent
        assert(union_test.is_profile_parent(UNION_EXAMPLE_PARENT))
        self.assertFalse(union_test.is_profile_child(UNION_EXAMPLE_PARENT))
        
        #Check the children
        self.assertFalse(union_test.is_profile_parent(UNION_EXAMPLE_CHILD))
        assert(union_test.is_profile_child(UNION_EXAMPLE_CHILD))
        
        #Check random profile
        self.assertFalse(union_test.is_profile_parent(UNION_EXAMPLE_NOT_INCLUDED))
        self.assertFalse(union_test.is_profile_child(UNION_EXAMPLE_NOT_INCLUDED))
        
        #Check the number of children
        assert(len(union_test.children) == UNION_EXAMPLE_NUMBER_CHILDREN)
        
        

if __name__ == '__main__':
    unittest.main()