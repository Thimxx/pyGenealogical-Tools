'''
Created on 6 jul. 2019

@author: Val
'''
import unittest, os
from pyRootsMagic.pyrm_database import database_rm
from datetime import date


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
        
        #This profile has a date "ABOUT"
        prof2 = db.get_profile_by_ID(3)
        event_birth2 = prof2.get_specific_event("birth")
        assert(event_birth2.get_year() == 1910)
        assert(event_birth2.get_accuracy() == "ABOUT")
        event_death2 = prof2.get_specific_event("death")
        assert(not event_death2)
        
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
        
        #This profile has a date BETWEEN
        prof5 = db.get_profile_by_ID(1)
        event_birth3 = prof5.get_specific_event("birth")
        assert(event_birth3.get_location()["county"] == "Segovia")
        assert(event_birth3.get_location()["latitude"] < 41.07)
        
        #Now we check that None is provided if there is no profile in
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
        
        db.close_db()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()