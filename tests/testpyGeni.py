import unittest
import os
from pyGeni import profile
from tests.FIXTURES import PHILIPIVid, PHILIPIVg, PHILIPIVget
from datetime import date


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
        assert(self.philip.gen_data["birth_date"] == date(1605,4,8))
        assert(self.philip.gen_data["baptism_date"] == date(1605,5,1))
        assert(self.philip.gen_data["death_date"] == date(1665,9,17))
        assert(self.philip.gen_data["burial_date"] == date(1665,9,20))
        assert(self.philip.gen_data["birth_place"]["city"] == 'Valladolid')
        assert(self.philip.gen_data["baptism_place"]["place_name"] == 'Iglesia Conventual San Pablo')
        assert(self.philip.gen_data["death_place"]["city"] == 'El Escorial' )
        assert(self.philip.gen_data["burial_place"]["place_name"] == 'San Lorenzo de El Escorial')
        
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