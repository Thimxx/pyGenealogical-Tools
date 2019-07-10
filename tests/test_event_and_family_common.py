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
        
        family1 = family_profile(child = child1)
        assert(len(family1.children) == 1)

        family2 = family_profile(child = [child1, child2])
        assert(len(family2.children) == 2)
        
        family3 = family_profile(child = [child1, child2], father = father, mother = mother, marriage = event1)
        assert(family3.father and family3.mother and family3.children and family3.marriage)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()