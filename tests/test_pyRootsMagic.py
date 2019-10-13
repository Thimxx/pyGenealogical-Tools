'''
Created on 6 jul. 2019

@author: Val
'''
import unittest, os
from pyRootsMagic.pyrm_database import database_rm
from datetime import date
from shutil import copyfile
from tests.FIXTURES import TEST_FACEBOOK, TEST_GOOGLE, TEST_WIKIPEDIA

class Test_use_and_access_RootsMagic(unittest.TestCase):
    def setUp(self):
        "Creation of the different parameters needs for execution, including location of database"
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2
    def test_open_dabatase_and_read(self):
        '''
        Test accessing the RootsMagic database and basic information access
        '''
        input_file = os.path.join(self.filelocation, "Rootstest.rmgc")
        db = database_rm(input_file)
        
        #Let's take one profile and test is properly taken
        prof = db.get_profile_by_ID(5)
        assert(prof.getName() == "GrandMother")
        assert(prof.getSurname() == "Profile")
        event_birth = prof.get_specific_event("birth")
        assert(event_birth.get_date() == date(1860,7,15))
        assert(event_birth.get_accuracy() == "EXACT")
        assert(prof.get_accuracy_event("birth") == "EXACT")
        
        event_death = prof.get_specific_event("death")
        assert(event_death.get_year() == 1950)
        assert(event_death.get_accuracy() == "EXACT")
        assert(prof.getGender() == "F")
        assert(len(prof.getEvents()) == 3)
        assert(prof.getLiving() == False)
        
        #This profile has a date "ABOUT"
        prof2 = db.get_profile_by_ID(3)
        event_birth2 = prof2.get_specific_event("birth")
        assert(event_birth2.get_year() == 1910)
        assert(event_birth2.get_accuracy() == "ABOUT")
        event_death2 = prof2.get_specific_event("death")
        assert(not event_death2)
        #Also includes web_references
        iswebthere = False
        for web in prof2.get_all_urls().keys():
            if "familysearch.org/tree/person" in web: iswebthere = True
        assert(iswebthere)
        
        #This profile has a date "BEFORE"
        prof3 = db.get_profile_by_ID(4)
        event_death3 = prof3.get_specific_event("death")
        assert(event_death3.get_year() == 1970)
        assert(event_death3.get_accuracy() == "BEFORE")
        assert(prof3.getGender() == "M")
        
        
        #This profile includes a wrong sex, it will check the file works properly
        prof4 = db.get_profile_by_ID(6)
        assert(prof4.getGender() == "U")
        event_death4 = prof4.get_specific_event("birth")
        assert(event_death4.get_date() == None)
        assert(event_death4.get_year() == 1820)
        assert(event_death4.get_accuracy() == "BETWEEN")
        assert(event_death4.year_end == 1821)
        assert(event_death4.month_end == 3)
        self.assertFalse(event_death4.day_end)
        #Also includes web_references
        assert(len(prof4.get_all_webs()) == 2)
        
        #This profile has a date BETWEEN
        prof5 = db.get_profile_by_ID(1)
        event_birth3 = prof5.get_specific_event("birth")
        assert(event_birth3.get_location()["county"] == "Segovia")
        assert(event_birth3.get_location()["latitude"] < 41.08)
        assert(prof5.getLiving())
        
        #Now we check that None is provided if there is no profile in
        assert(db.get_profile_by_ID("dsdf") == None)
        assert(db.get_profile_by_ID(2325) == None)
        
        #Let's check all families
        assert(db.get_family_by_ID(2325) == None)
        
        #Let's check the proper data of a family
        assert(db.get_family_by_ID(1).getFather() == 2)
        assert(db.get_family_by_ID(1).getMother() == 3)
        assert(db.get_family_by_ID(3).getMother() == None)
        assert(db.get_family_by_ID(4).getFather() == None)
        assert(db.get_family_by_ID(1).getChildren() == [1, 7])
        assert(len(db.get_family_by_ID(5).getChildren()) == 0)
        #Check getting the family id from the child
        assert(db.get_family_from_child(7)[0] == 1)
        assert(db.get_father_from_child(7)[0] == 2)
        assert(db.get_mother_from_child(7)[0] == 3)
        
        #This will provide the children of a given profile
        assert(2 in db.get_all_family_ids_is_parent(5))
        children = db.get_all_children(2)
        assert(1 in children)
        assert(1 in children)
    
    def test_insert_methods(self):
        '''
        Testing insert methods inside RootsMagic
        '''
        initial_file = os.path.join(self.filelocation, "Rootstest.rmgc")
        working_file = os.path.join(self.filelocation, "Rootstest_insert.rmgc")
        
        if os.path.exists(working_file): os.remove(working_file)
        copyfile(initial_file, working_file)
        
        
        db = database_rm(working_file)
        
        
        prof = db.get_profile_by_ID(5)
        prof.setWebReference([TEST_GOOGLE, TEST_FACEBOOK])
        prof.setWebReference(TEST_WIKIPEDIA, name = "Wikipedia", notes="introduced")
        
        assert(prof.get_all_webs()[0]["name"] == "")
        assert(prof.update_web_ref(TEST_GOOGLE, "Google", "A note"))
        assert(prof.get_all_webs()[0]["name"] == "Google")
        assert(TEST_GOOGLE in prof.get_all_urls())
        assert(TEST_WIKIPEDIA in prof.get_all_urls())
        #It does not essent
        assert(prof.update_web_ref("DOES NOT EXISTS", "Google", "A note") == None)
        
        prof.set_task("TEST")
        
        db.close_db()
        if os.path.exists(working_file): os.remove(working_file)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()