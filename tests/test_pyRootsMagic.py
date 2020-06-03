'''
Created on 6 jul. 2019

@author: Val
'''
import unittest, os
from pyRootsMagic.pyrm_database import database_rm
from pyRootsMagic import return_date_from_event
from pyGenealogy.common_profile import gen_profile
from pyGenealogy.common_event import event_profile
from datetime import date
from shutil import copyfile
from tests.FIXTURES import TEST_FACEBOOK, TEST_GOOGLE, TEST_WIKIPEDIA
from pyGenealogy.common_event import event_profile


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
        assert(db.get_db_kind() == "ROOTSMAGIC")
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
        assert(len(prof.getEvents()) == 4)
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
        event_marriage = prof3.get_specific_event("marriage")
        assert(event_marriage[0].get_year() == 1880)
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
        eventsof1= prof5.getEvents()
        no_marriage = True
        assert("Mariano Profile" in prof5.get_nicknames())
        for event in eventsof1:
            if event.get_event_type() == "marriage": no_marriage = False
        assert(no_marriage)
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
        
        assert(10 in db.get_partners_from_profile(11))
        assert(13 in db.get_partners_from_profile(11))
    
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
        webs = prof.get_all_webs()
        google_found = False
        for web in webs:
            if web["url"] == "http://www.google.com":
                if web["name"] == "": google_found = True
        assert(google_found)
        assert(prof.update_web_ref(TEST_GOOGLE, "Google", "A note"))
        google_found = False
        webs = prof.get_all_webs()
        for web in webs:
            if web["name"] == "Google": google_found = True
        assert(google_found)
        assert(TEST_GOOGLE in prof.get_all_urls())
        assert(TEST_WIKIPEDIA in prof.get_all_urls())
        assert(prof.get_specific_web("Google"))
        assert(not prof.get_specific_web("Not existing"))
        
        prof.del_web_ref(TEST_WIKIPEDIA)
        assert(not (TEST_WIKIPEDIA in prof.get_all_urls()))
        #It does not essent
        assert(prof.update_web_ref("DOES NOT EXISTS", "Googles", "A note") is None)
        
        prof.set_task("TEST", details="HAHA")
        
        #Introduce a research log
        row_id = prof.set_task("TEST_OF_LOG", task_type=2)
        assert(prof.get_specific_research_log("TEST_OF_LOG"))
        assert(prof.get_specific_research_log("TEST_NOT_EXISTING") == None)
        
        
        prof.set_research_item(row_id, repository = "www.google.com", source = "GOOGLE", result = "GOOD")
        prof.update_research_item(row_id, "www.google.com", source = "GOOGLE2", result = "BAD")
        #Error when 2 research logs of the same name in the same profile.
        profb = db.get_profile_by_ID(6)
        with self.assertLogs("rootsmagic", level="WARNING") as cm:
            profb.get_specific_research_log("TWICE")
            assert("TWICE" in cm.output[0])
        
        prof2 = db.get_profile_by_ID(1)
        
        assert(len(prof2.get_all_research_item()) == 2)
        
        
        prof3 = db.get_profile_by_ID(3)
        
        assert(len(prof3.get_all_research_item()) == 0)
        
        #Setting up the sources
        assert(prof2.get_source_id_ref("TESTING") == None)
        prof2.set_source_id("TESTING")
        prof2.setWebReference("http//here.com", "NEW_URL")
        assert(prof2.get_source_id_ref("TESTING") == 1)
        assert(prof2.get_citation_with_comments("http://test.com") == None)
        prof2.set_citation(1, details="http://test.com")
        assert(prof2.get_citation_with_comments("http://test.com") == 1)
        
        #Testing the insert of the profiles
        insert_profile = gen_profile("RootsMagic", "Adding")
        insert_profile.setCheckedGender("M")
        insert_profile.setCheckedDate("birth", 1820,accuracy="ABOUT")
        
        
        event_both = event_profile("birth")
        event_both.setLocationAlreadyProcessed({"formatted_location": "Gallegos, Segovia"})
        event_both.setDate(1820,accuracy="ABOUT")
        event_date = event_profile("death")
        event_date.setDate(1902, month = 2, day = 1, accuracy = "EXACT")
        event_location = event_profile("burial")
        event_location.setLocation("Aldealaguna, Segovia, Spain")
        
        insert_profile.setNewEvent(event_both)
        insert_profile.setNewEvent(event_date)
        insert_profile.setNewEvent(event_location)
        
        prof_id = db.add_profile(insert_profile)
        #Check the results
        prof_entered = db.get_profile_by_ID(prof_id)
        assert(prof_entered.getName() == "RootsMagic")
        assert(prof_entered.get_specific_event("birth").get_year() == 1820)
        assert(prof_entered.get_specific_event("birth").get_accuracy() == "ABOUT")
        assert(prof_entered.get_specific_event("birth").get_location()["raw"] == "Gallegos, Segovia")
        assert(prof_entered.get_specific_event("death").get_year() == 1902)
        assert(prof_entered.get_specific_event("death").get_accuracy() == "EXACT" )
        assert(prof_entered.get_specific_event("death").get_location() == None)
        assert(prof_entered.get_specific_event("burial").get_year() == None)
        assert(prof_entered.get_specific_event("burial").get_location()["raw"] == 'Aldealaguna, Segovia, Spain')
        
        #Now, let's also create a family for this profile
        insert_wife = gen_profile("RootsMagic", "Wife")
        insert_wife.setCheckedGender("F")
        wife_id = db.add_profile(insert_wife)
        prof_wife = db.get_profile_by_ID(wife_id)
        event_marriage = event_profile("marriage")
        event_marriage.setDate(1815, accuracy = "ABOUT")
        assert(prof_wife.get_specific_event("marriage") == [])
        fam_id = db.add_family(father = prof_id, mother = wife_id, children = [6], marriage = event_marriage)
        assert(prof_wife.get_specific_event("marriage")[0].get_year() == 1815)
        assert(db.get_family_from_child(6)[0] == fam_id)
        
        #Methods for updating the family of RootsMagic
        assert(not db.update_family(fam_id))
        new_husband = gen_profile("New", "Husband")
        new_wife = gen_profile("New", "Wife")
        new_child = gen_profile("New", "Child")
        new_husband_id = db.add_profile(new_husband)
        new_wife_id = db.add_profile(new_wife)
        new_child_id = db.add_profile(new_child)
        marriage = event_profile("marriage")
        marriage.setDate(1900)
        fam3 = db.get_family_by_ID(3)
        assert(fam3.getMother() == None)
        db.update_family(3, mother_id = new_wife_id, children = [new_child_id], marriage = marriage)
        assert(fam3.getMother() == new_wife_id)
        
        fam4 = db.get_family_by_ID(4)
        assert(fam4.getFather() == None)
        db.update_family(4, father_id = new_husband_id,  marriage = marriage)
        assert(fam4.getFather() == new_husband_id)
        
        
        new_child2 = gen_profile("Newer", "Child")
        new_child3 = gen_profile("Older", "Child")
        previous_len = len(fam4.getChildren())
        db.add_child(4, [new_child2, new_child3] )
        assert(len(fam4.getChildren()) - previous_len == 2)
        
        new_partner1 = gen_profile("New", "Partner")
        new_marriage = event_profile("birth")
        new_marriage.set_year("2019")
        previous_partners = len(db.get_partners_from_profile(4))
        db.add_partner(4, new_partner1, new_marriage)
        assert( len(db.get_partners_from_profile(4))  - previous_partners == 1 )
        
        db.close_db()
        if os.path.exists(working_file): os.remove(working_file)
    def test_common_init_functions(self):
        '''
        This test will be testing those functions included in init file
        '''
        my_event = event_profile("birth")
        
        assert(return_date_from_event(my_event) == None)
        
        my_event.setDate(2019, 5, 3, "EXACT")        
        #D.+20190503..+00000000..
        assert(return_date_from_event(my_event) == "D.+20190503..+00000000..")
        
        my_event.setDate(1970, accuracy="BEFORE")        
        #DB+19700000..+00000000..
        assert(return_date_from_event(my_event) == "DB+19700000..+00000000.." )
        
        my_event.setDate(1890, accuracy="AFTER")        
        #DA+18900000..+00000000..
        assert(return_date_from_event(my_event) == "DA+18900000..+00000000..")
        
        my_event.setDate(1820, accuracy="BETWEEN", year_end = 1821, month_end=3)        
        #DR+18200000..+18210300..
        assert(return_date_from_event(my_event) == "DR+18200000..+18210300..")
        
        my_event.setDate(1910, accuracy="ABOUT")        
        #D.+19100000.C+00000000..
        assert(return_date_from_event(my_event) == "D.+19100000.A+00000000..")
        
        
        #my_event.setDate(year, month, day, accuracy, year_end, month_end, day_end)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()