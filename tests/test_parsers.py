'''
Created on 15 oct. 2019

@author: Val
'''
import unittest
from pyGenealogy.common_profile import gen_profile
from pyRegisters.pyesquelas import esquelas_reader
from pyRegisters.pycementry_valencia import valencia_reader
from pyRegisters.pylavanguardia import vanguardia_reader
from pyRegisters import sp_age_location_colector

class Test(unittest.TestCase):


    def test_basic_colector(self):
        '''
        Test the operation of the colector
        '''
        assert(sp_age_location_colector("Falleció en Santander, el día 22 de febrero de 1567, a los 61 años de edad, habiendo") == ("Santander", 61))
        assert(sp_age_location_colector("Falleció en Asturias. Habiendo recibido") == ("Asturias", None))
        assert(sp_age_location_colector("Falleció el día 8 de marzo de 2013, a los 64 años de edad,")== (None, 64))
        assert(sp_age_location_colector("en Madrid") == ("Madrid", None))
        assert(sp_age_location_colector("en Barcelona a los 67 años")== ("Barcelona", 67))
        assert(sp_age_location_colector(" Ha fallecido cristianamente en Barcelona, a la edad de 93 años, el")== ("Barcelona", 93))
        #With detection
        assert(sp_age_location_colector(" Ha mort a Barcelona, a l'edat de 99 anys, el dia 24 de febrer", detect_lan = True)== ("Barcelona", 99))
             
          
    def test_esquelas(self):
        '''
        Test checking el Esquelas parser
        '''
        profile = gen_profile("José Luis", "García Martín")
        reader = esquelas_reader()
        records = reader.profile_is_matched(profile)
        assert(len(records) > 2)
        
    def test_valencia(self):
        '''
        Tests the database of valencia cementry
        '''
        profile = gen_profile("José", "García López")
        profile.setCheckedDate("death", 1993, accuracy="ABOUT")
        reader = valencia_reader()
        records = reader.profile_is_matched(profile)
        assert(len(records)>6)
    
    def test_lavanguardia(self):
        '''
        Test the obituary database of La Vanguardia
        '''
        profile = gen_profile("José", "García López")
        reader = vanguardia_reader()
        records = reader.profile_is_matched(profile)
        assert(len(records) > 0)
        year_birth = False
        year_death = False
        for profile in records:
            if profile.get_specific_event("birth").get_year() == 1916: year_birth = True
            if profile.get_specific_event("death").get_year() == 2015: year_death = True
        assert(year_birth)
        assert(year_death)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()