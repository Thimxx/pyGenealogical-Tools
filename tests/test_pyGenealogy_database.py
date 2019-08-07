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
        assert(db.add_profile(person1) == "I1")
        assert(db.add_profile(person2) == "I2")
        assert(db.add_family(father = person1, mother = person2) == "F1")
        assert(db.get_family_by_ID("F1").getFather().getName() == "Name")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()