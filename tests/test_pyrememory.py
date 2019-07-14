'''
Created on 16 sept. 2017

@author: Val
'''
import unittest, requests
from datetime import date
from pyRegisters.pyrememori import rememori_reader, RememoryPersonParser
from pyGenealogy.common_profile import gen_profile

class Test(unittest.TestCase):


    def test_reading_an_input(self):
        profile = gen_profile("José", "García Martín")
        reader = rememori_reader()
        records = reader.profile_is_matched(profile)
        date1 = date(2016,4,2)
        date2 = date(2014,12,28)
        date1_found = False
        date2_found = False
        for profile in records:
            if (profile.gen_data["death"].get_date() == date1): date1_found = True
            if (profile.gen_data["death"].get_date() == date2): date2_found = True
        assert(date1_found)
        assert(date2_found)
    
    def test_simplifying_list(self):
        '''
        Test confirming list will be simplified
        '''
        profile = gen_profile("Julián", "Gómez Gómez")
        profile.setCheckedDate("baptism", 1970,4,2, "EXACT")
        reader = rememori_reader()
        records = reader.profile_is_matched(profile)
        date_found = False
        for deceased in records:
            if (deceased.gen_data["death"].get_date() == date(2017,2,13)): date_found = True
        assert(date_found)
    
    def test_avoiding_analysis(self):
        '''
        Test confirming no analysis if antique record
        '''
        profile = gen_profile("Julián", "Gómez Gómez")
        profile.setCheckedDate("baptism", 1870,4,2, "EXACT")
        reader = rememori_reader()
        records = reader.profile_is_matched(profile)
        assert(len(records) == 0)
        
    def test_person_parser(self):
        '''
        Test isolated the person parser
        '''
        url_check = "https://www.rememori.com/874091:julian_gomez_izquierdo"
        data = requests.get(url_check)
        person_parser = RememoryPersonParser()
        person_parser.feed(data.text)
        assert(person_parser.age == 75)
        assert(person_parser.location == "Bilbao")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_reading_an_input']
    unittest.main()