'''
Created on 6 ago. 2019

@author: Val
'''
import unittest
from pyGenealogy.common_database import gen_database
from pyGenealogy.common_profile import gen_profile


class Test_common_database(unittest.TestCase):


    def testName(self):
        '''
        Testing basic introduction of new profiles and families.
        '''
        db = gen_database()
        person1 = gen_profile("Name", "Surname")
        person2 = gen_profile("Name2", "Surname2")
        person3 = gen_profile("Chid", "Surname2")
        assert(db.add_profile(person1) == "I1")
        assert(db.add_profile(person2) == "I2")
        assert(db.add_profile(person3) == "I3")
        assert(db.add_family(father = "I1", mother = "I2", children=["I3"]) == "F1")
        assert(db.get_profile_by_ID("I1").getName() == "Name")
        assert(db.get_family_by_ID("F1").getFather() == "I1")
        assert(db.get_family_by_ID("F1").get_id() == "F1")
        assert(db.get_family_by_ID("xxx1") == None)
        assert(db.get_profile_by_ID("xxx1") == None)
        
        id_fam, fam = db.get_family_from_child("I3")
        assert(id_fam == "F1")
        assert(fam.getMother() == "I2")
        
        id_fam2, fam2 = db.get_family_from_child("I1")
        assert( id_fam2 == None)
        #Get father of profile
        assert(db.get_father_from_child("I3")[0] == "I1")
        #Get mother of profile
        assert(db.get_mother_from_child("I3")[0] == "I2")
        #Get Children function
        assert("I3" in db.get_all_children("I1"))
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()