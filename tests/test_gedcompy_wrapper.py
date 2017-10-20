'''
Created on 15 oct. 2017

@author: Val

This is a testing file of the wrapper created for gedcompy
'''
import unittest
from pyGedcom.gedcompy_wrapper import gedcom_file
from datetime import date

from pyGedcom.gedcom_profile import gedcom_profile
from pyGenealogy.common_profile import gen_profile

class Test(unittest.TestCase):


    def test_gedcompy_usage(self):
        '''
        Test gedcompy wrapper use
        '''
        date_marr = date(2015,1,1)
        husband = gen_profile("Mario", "Vargas")
        husband.setCheckedDate("marriage_date", date_marr, "EXACT")
        wife = gen_profile("María", "Sanz")
        wife.setCheckedDate("marriage_date", date_marr, "EXACT")
        child1 = gen_profile("Francisco", "Vargas Sanz")
        child2 = gen_profile("Roberto", "Vargas Sanz")
        
        
        gedcom_profile.convert_gedcom(husband)
        gedcom_profile.convert_gedcom(wife)
        gedcom_profile.convert_gedcom(child1)
        gedcom_profile.convert_gedcom(child2)
        
        new_gedcom = gedcom_file()
        new_gedcom.add_element(husband.individual)
        new_gedcom.add_element(wife.individual)
        new_gedcom.add_element(child1.individual)
        new_gedcom.add_element(child2.individual)
        
        assert(husband.return_id() == "@I1@")
        assert(wife.return_id() == "@I2@")
        assert(child1.return_id() == "@I3@")
        assert(child2.return_id() == "@I4@")
        
        new_gedcom.create_family(husband, wife, [child1, child2])
        
        for ele in new_gedcom.__dict__["root_elements"]:
            if ele.tag == "FAM":
                for member in ele.__dict__['child_elements']:
                    if (member.tag == "HUSB"): assert (member.value == '@I1@')
                    if (member.tag == "WIFE"): assert (member.value == '@I2@')
                    if (member.tag == "CHILD"): assert (member.value in ['@I3@','@I4@'])
                    if (member.tag == "MARR"):
                        marr=member.__dict__['child_elements'][0]
                        assert(marr.value == "01 JAN 2015")
    
    def test_list_profile(self):
        '''
        Test converting a list of profiles into gedcom
        '''    
        child1 = gen_profile("Francisco", "Vargas Sanz")
        child2 = gen_profile("Roberto", "Vargas Sanz")
        array = [child1, child2]
        gedcom_profile.convert_gedcom(array)
        for prof in array:
            assert(hasattr(prof, 'individual'))
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()