import unittest, os
from pyGeni import profile, set_token
from tests.FIXTURES import PHILIPIVid, PHILIPIVg, PHILIPIVget
from datetime import date


class testpyGeni(unittest.TestCase):
    def setUp(self):
        set_token(os.environ['GENI_KEY'])
        profile.s.update_geni_address("https://www.geni.com")
        profile.s.VERIFY_INPUT = "standard"
        self.philip = profile.profile(PHILIPIVg)

    def testGettingCorrectName(self):
        '''
        This test checks that the name of philip the IV of Spain is properly detected
        '''
        assert( "Felipe" in self.philip.nameLifespan())
        assert( "1605" in self.philip.nameLifespan())
        assert( "1665" in self.philip.nameLifespan())
        assert(self.philip.gen_data["birth"].get_date() == date(1605,4,8))
        assert(self.philip.gen_data["baptism"].year == 1605)
        assert(self.philip.gen_data["baptism"].month == 5)
        assert(self.philip.gen_data["death"].get_date() == date(1665,9,17))
        assert(self.philip.gen_data["burial"].get_date() == date(1665,9,20))
        
        assert(self.philip.gen_data["birth"].location["city"] == 'Valladolid')
        assert(self.philip.gen_data["baptism"].location["place_name"] == 'Iglesia Conventual San Pablo')
        assert(self.philip.gen_data["death"].location["city"] == 'El Escorial' )
        assert(self.philip.gen_data["burial"].location["place_name"] == 'San Lorenzo de El Escorial')
        
    def testUsingIdProfile(self):
        '''
        This test checks that using a different input id the id obtained is the same.
        '''
        philip_bis = profile.profile(PHILIPIVget, "")
        assert( philip_bis.get_id() == self.philip.get_id())
   
    def testgetrightid(self):
        '''
        Confirms that the id output is correct
        '''
        assert(self.philip.get_id() == PHILIPIVid)


if __name__ == '__main__':
    unittest.main()