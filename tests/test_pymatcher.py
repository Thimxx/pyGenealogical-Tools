'''
Created on 22 oct. 2019

@author: Val
'''
import unittest, os
from shutil import copyfile
from pyRootsMagic.pyrm_database import database_rm
from analyzefamily.matcher_geni_profile import match_single_profile
from pyGeni import set_token, update_geni_address
from pyGeni.interface_geni_database import geni_database_interface

class Test(unittest.TestCase):
    def setUp(self):
        "Creation of the different parameters needs for execution, including location of database"
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2
        #We used the sandbox here
        set_token(os.environ['SANDBOX_KEY'])
        update_geni_address("https://sandbox.geni.com")
    def test_single_match(self):
        '''
        Tests a single match in GENI
        '''
        
        input_file = os.path.join(self.filelocation, "Rootstest.rmgc")
        working_file = os.path.join(self.filelocation, "Rootstest_match.rmgc")
        
        if os.path.exists(working_file): os.remove(working_file)
        copyfile(input_file, working_file)
        
        db = database_rm(working_file)
        db_geni = geni_database_interface()
        
        matcher = match_single_profile(db, db_geni, data_language="es", name_convention="spanish_surname")
        #Testing profile, no GENI
        assert(matcher.match(1) == False)
        non_matched_profiles_rm, non_matched_profiles_geni, conflict_profiles, matched_profiles = matcher.match(2)
        #=================================================
        #Now we check executions properly done
        #=================================================
        #Profile URL is matched
        matched_total = True
        for id_prof in [4, 5, 1]:
            prof_matched = db.get_profile_by_ID(id_prof)
            is_matched_by_geni = False
            for web_dict in prof_matched.get_all_webs():
                if (web_dict["name"] == "GENI") : is_matched_by_geni = True
            if (not is_matched_by_geni): matched_total = False
        assert(matched_total)
        #Matched is consistent
        assert(4 in matched_profiles.keys())
        assert(5 in matched_profiles.keys())
        assert(3 in matched_profiles.keys())
        assert(1 in matched_profiles.keys())
        #Secure detected conflicts
        assert(7 in conflict_profiles.keys())
        #Check not matched profiles
        assert('profile-406' in non_matched_profiles_geni.keys())
        assert('profile-930' in non_matched_profiles_geni.keys())
        #No missing match in RM part
        assert(len(non_matched_profiles_rm.keys()) == 0)
        
        geni_detected = False
        for task in db.get_profile_by_ID(7).get_all_tasks():
            if ("GENI" in task["task_details"]): geni_detected = True
        assert(geni_detected)
        
        #===============================================
        # New test with different parameter
        #===============================================
        non_matched_profiles_rm2, non_matched_profiles_geni2, conflict_profiles2, matched_profiles2 = matcher.match(11)
        
        assert(12 in non_matched_profiles_rm2.keys())
        #assert(13 in non_matched_profiles_rm2.keys())
        assert("profile-3798" in non_matched_profiles_geni2.keys())
        assert("profile-30062" in non_matched_profiles_geni2.keys())
        assert(not conflict_profiles2)
        assert(10 in matched_profiles2.keys())
        
        
        db.close_db()
        if os.path.exists(working_file): os.remove(working_file)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()