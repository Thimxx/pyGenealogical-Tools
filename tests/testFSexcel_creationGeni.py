'''
Created on 17 sept. 2017

@author: Val
'''
import unittest
from pyFS.pyfs_open_xlsx import getFSfamily
import os
from pyGeni import profile, set_token
import datetime
from tests.FIXTURES import SANDBOX_MAIN_ADDRESS

class Test(unittest.TestCase):
    def setUp(self):
        '''
        Let's make it simple... is just a test not a good code. If it is not located in one place will
        be in another!
        '''
        #We used the sandbox here
        set_token(os.environ['SANDBOX_KEY'])
        profile.s.update_geni_address("https://sandbox.geni.com")
        #We locate the folder here
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2


    def test_fs_with_a_marriage(self):
        '''
        Test a FS file with marriage
        '''
        input_file = os.path.join(self.filelocation, "fs-MartinPerez.xlsx")
        fsclass = getFSfamily(input_file, naming_convention="spanish_surname", language = "es")
        assert(fsclass.correct_execution)
        first_profile = fsclass.profiles[0]
        assert(first_profile.gen_data["name"] == "Tiburcio")
        second_profile = fsclass.profiles[1]
        assert(second_profile.gen_data["name"] == "Lucía")
        married_profile = fsclass.profiles[2]
        assert(married_profile.gen_data["name"] == "Nicasia")
        assert(married_profile.gen_data["marriage"].get_location()["place_name"] == "Tudela de Duero")
        testing_date = datetime.date(1841, 11, 30)
        assert(married_profile.gen_data["marriage"].get_date() == testing_date)
        
        fsclass.create_profiles_in_Geni(SANDBOX_MAIN_ADDRESS)
        
        #We check the partner
        fsclass.related_geni_profiles[0].get_relations()
        #TODO: add checking when marriage is available in relations
        for parent_profile in fsclass.parents_geni_profiles:
            assert(parent_profile.delete_profile())
        for partner_profile in fsclass.related_geni_profiles:
            assert(testing_date == partner_profile.gen_data["marriage"].get_date())
            assert(partner_profile.gen_data["surname"] == "González Ruiz")
            assert(partner_profile.delete_profile())
        for data_profile in fsclass.geni_profiles:
            assert(data_profile.delete_profile())
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_fs_reader']
    unittest.main()