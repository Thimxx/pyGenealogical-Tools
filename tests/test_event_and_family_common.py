'''
Created on 8 jul. 2019

@author: Val
'''
import unittest
from pyGenealogy.common_event import event_profile
from pyGenealogy.common_family import family_profile
from pyGenealogy.common_profile import gen_profile

class Test(unittest.TestCase):


    def test_basic_event(self):
        '''
        Testing basic usage of common_event class
        '''
        event1 = event_profile("birth")
        assert(event1.setDate(2011, accuracy="EXACT"))
        assert(event1.setDate(2013,month = 2, accuracy="ABOUT"))
        assert(event1.setDate(2013,month = 2, accuracy="BEFORE"))
        assert(event1.setDate(2013,month = 2, accuracy="AFTER"))
        assert(event1.setDate(2013,month = 2, accuracy="BETWEEN", year_end = 2013))
        self.assertFalse( event1.setDate(2013,month = 2, accuracy="BETWEEN")  )
        self.assertFalse( event1.setDate(2013,month = 2, accuracy="LALA")  )
        self.assertFalse( event1.setDate(2013,month = 2, accuracy="ABOUT", month_end = 2)  )
        assert(event1)
        #Introducing wrong data
        self.assertRaises(ValueError, lambda:event_profile("wrong_data"))
        event1.setLocation("Madrid, Spain")
        assert(event1.location["place_name"] == "Madrid")
        #Let's check introducing a lower date in the end day
        assert(event1.setDate(2015,month = 2, day = 1, accuracy="BETWEEN", year_end = 2013, month_end = 2, day_end = 5))
        assert(event1.year == 2013)
    
    def test_family(self):
        '''
        This test will check the basic operation of family classes
        '''
        father = gen_profile("Father", "Profile")
        mother = gen_profile("Mother", "Profile")
        child1 = gen_profile("Child", "First")
        child2 = gen_profile("Child", "Second")
        
        event1 = event_profile("birth")
        assert(event1.setDate(2013,month = 2, accuracy="ABOUT"))
        
        family1 = family_profile(child = 3)
        assert(len(family1.getChildren()) == 1)

        family2 = family_profile(child = [1, 2])
        assert(len(family2.getChildren()) == 2)
        
        family3 = family_profile(child = [1, 2], father = 3, mother = 4, marriage = event1)
        assert(family3.father and family3.mother and family3.children and family3.marriage)
        assert(family3.getFather() == 3)
        assert(family3.getMother() == 4)
    
    def test_date_checker(self):
        '''
        It will check 2 dates to confirm which one is the smaller
        '''
        new_event = event_profile("birth")
        
        self.assertFalse(new_event.is_first_date_lower(2012, None, None, 2010, None, None))
        assert(new_event.is_first_date_lower(1910, None, None, 1912, None, None))
        assert(new_event.is_first_date_lower(2010, 1, None, 2010, None, None) == None)
        assert(new_event.is_first_date_lower(2010, 1, None, 2010, 2, None))
        self.assertFalse(new_event.is_first_date_lower(2012, 5, None, 2012, 1, None))
        assert(new_event.is_first_date_lower(2010, 1, None, 2010, 1, None) == None)
        assert(new_event.is_first_date_lower(2010, 2, 12, 2010, 2, 22))
        self.assertFalse(new_event.is_first_date_lower(2012, 5, 12, 2012, 5, 5))
        assert(new_event.is_first_date_lower(2010, 1, 2, 2010, 1, 2) == "Equal")
        
        #Testing that the event is smaller or not
        new_event1 = event_profile("birth")
        new_event1.setDate(2013,month = 2, accuracy = "AFTER")
        new_event2 = event_profile("death")
        new_event2.setDate(2012, day = 3, accuracy = "ABOUT")
        
        self.assertFalse(new_event1.is_this_event_earlier_or_simultaneous_to_this(new_event2))
        assert(new_event2.is_this_event_earlier_or_simultaneous_to_this(new_event1))

        assert(new_event1.is_this_event_later_or_simultaneous_to_this(new_event2) )
        self.assertFalse(new_event2.is_this_event_later_or_simultaneous_to_this(new_event1))
    def test_date_for_gedcom(self):
        '''
        Testing the output for gedcom
        '''
        new_event = event_profile("birth")
        new_event.setDate(2013,month = 2)
        assert(new_event.get_gedcom_date() == "FEB 2013")
        new_event.setDate(2013)
        assert(new_event.get_gedcom_date() == "2013")
        new_event.setDate(2013,6, 1)
        assert(new_event.get_gedcom_date() == "01 JUN 2013")
        new_event.setDate(2013,12, 18)
        assert(new_event.get_gedcom_date() == "18 DEC 2013")
    def test_date_differences(self):
        '''
        Will test the differences between 2 events
        '''
        event1 = event_profile("birth")
        event1.setDate(2013, 2, 13, "EXACT")
        event2 = event_profile("birth")
        event2.setDate(2013, 6, 26, "EXACT")
        assert(event1.get_difference_in_days(event2) == 133)
        event2.setDate(2013, accuracy="EXACT")
        assert(event1.get_difference_in_days(event2) == 43)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()