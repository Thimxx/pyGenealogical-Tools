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
        birth_date, accuracy = prof.getDate("birth_date")
        assert(birth_date == date(1860,7,15))
        assert(accuracy == "EXACT")
        death_date, accuracy2 = prof.getDate("death_date")
        assert(death_date == date(1950,1,1))
        assert(accuracy2 == "EXACT")
        assert(prof.getGender() == "F")
        
        #This profile has a date "ABOUT"
        prof2 = db.profiles[2]
        birth_date2, accuracy3 = prof2.getDate("birth_date")
        assert(birth_date2 == date(1910,1,1))
        assert(accuracy3 == "ABOUT")
        death_date2, accuracy4 = prof2.getDate("death_date")
        assert(not death_date2)
        assert(not accuracy4)
        
        #This profile has a date "BEFORE"
        prof3 = db.profiles[3]
        death_date3, accuracy5 = prof3.getDate("death_date")
        assert(death_date3 == date(1970,1,1))
        assert(accuracy5 == "BEFORE")
        assert(prof3.getGender() == "M")
        
        
        #This profile includes a wrong sex, it will check the file works properly
        prof4 = db.profiles[5]
        assert(prof4.getGender() == "U")
        
        db.close_db()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()