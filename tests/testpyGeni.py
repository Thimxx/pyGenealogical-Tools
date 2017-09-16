import unittest
import os
from pyGeni import profile
from tests.FIXTURES import PHILIPIVid, PHILIPIVg, PHILIPIVget


class testpyGeni(unittest.TestCase):
    def setUp(self):
        token = os.environ['GENI_KEY']
        profile.s.update_geni_address("https://www.geni.com")
        profile.s.VERIFY_INPUT = "standard"
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
   
    def testgetrightid(self):
        '''
        Confirms that the id output is correct
        '''
        assert(self.philip.get_id() == PHILIPIVid)

    
        

if __name__ == '__main__':
    unittest.main()