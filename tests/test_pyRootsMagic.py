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
        prof = db.profiles[4]
        assert(prof.getName() == "GrandMother")
        assert(prof.getSurname() == "Profile")
        event_birth = prof.get_specific_event("birth")
        assert(event_birth.get_date() == date(1860,7,15))
        assert(event_birth.get_accuracy() == "EXACT")
        event_death = prof.get_specific_event("death")
        assert(event_death.get_year() == 1950)
        assert(event_death.get_accuracy() == "EXACT")
        assert(prof.getGender() == "F")
        
        #This profile has a date "ABOUT"
        prof2 = db.profiles[2]
        event_birth2 = prof2.get_specific_event("birth")
        assert(event_birth2.get_year() == 1910)
        assert(event_birth2.get_accuracy() == "ABOUT")
        event_death2 = prof2.get_specific_event("death")
        assert(not event_death2)
        
        #This profile has a date "BEFORE"
        prof3 = db.profiles[3]
        event_death3 = prof3.get_specific_event("death")
        assert(event_death3.get_year() == 1970)
        assert(event_death3.get_accuracy() == "BEFORE")
        assert(prof3.getGender() == "M")
        
        
        #This profile includes a wrong sex, it will check the file works properly
        prof4 = db.profiles[5]
        assert(prof4.getGender() == "U")
        
        #This profile has a date BETWEEN
        prof3 = db.profiles[5]
        event_death4 = prof3.get_specific_event("birth")
        assert(event_death4.get_date() == None)
        assert(event_death4.get_year() == 1820)
        assert(event_death4.get_accuracy() == "BETWEEN")
        assert(event_death4.year_end == 1821)
        assert(event_death4.month_end == 3)
        self.assertFalse(event_death4.day_end)
        
        #This profile has a date BETWEEN
        prof5 = db.profiles[0]
        event_birth3 = prof5.get_specific_event("birth")
        assert(event_birth3.get_location()["county"] == "Segovia")
        assert(event_birth3.get_location()["latitude"] < 41.07)
        
        db.close_db()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()