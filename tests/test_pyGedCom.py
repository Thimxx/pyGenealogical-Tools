'''
Created on 14 oct. 2017

@author: Val

This function tests the new profile that includes the GedCom from Common profile
'''
import unittest, gedcom

from pyGedcom.gedcom_profile import gedcom_profile
from pyGenealogy.common_profile import gen_profile
from datetime import date


class Test(unittest.TestCase):


    def test_creating_gedcom_profile(self):
        '''
        Test Creating a GedCom Profile
        '''
        name_data = "MyName"
        surname = "MySurname"
        total_name = name_data +"/" + surname +"/"
        
        individual = gedcom.Individual()
        name = gedcom.Element(tag="NAME", value=total_name)
        name_given = gedcom.Element(tag="GIVN", value=name_data)
        name_surname = gedcom.Element(tag="SURN", value=surname)
        name.add_child_element(name_given)
        name.add_child_element(name_surname)
        individual.add_child_element(name)
        
        profile = gedcom_profile(individual)
        
        assert(profile.gen_data["name"] == name_data)
        assert(profile.gen_data["surname"] == surname)
    def test_creating_gedcom_from_common(self):
        '''
        Test creating a GedCom from a common_profile
        '''
        profile = gen_profile("Juana", "Bargas")
        profile.setCheckedGender("F")
        profile.add_nickname("Nick1")
        profile.add_nickname("Nick2")
        profile.setCheckedDate("birth_date", date(2014,3,2), accuracy="EXACT")
        profile.setCheckedDate("baptism_date", date(2014,3,3), accuracy="AFTER")
        profile.setCheckedDate("death_date", date(2016,3,2), accuracy="ABOUT")
        profile.setCheckedDate("burial_date", date(2016,3,5), accuracy="BEFORE")
        profile.setPlaces("birth_place", "Portillo,Valladolid,Castile and Leon,Spain", language="es")
        #We transform to the gedcom class
        gedcom_profile.convert_gedcom(profile)
        
        gedcom_transform = profile.individual
        for ele in gedcom_transform.__dict__["child_elements"]:
            if ele.tag == "NAME":
                for sub_ele in ele.__dict__["child_elements"]:
                    if sub_ele.tag == "GIVN" : assert(sub_ele.value == "Juana")
                    if sub_ele.tag == "SURN" : assert(sub_ele.value == "Bargas")
                    if sub_ele.tag == "NICK" : assert(sub_ele.value == "Nick1,Nick2")
            elif ele.tag == "SEX":
                assert(ele.value == "F")
            elif ele.tag == "BIRT":
                for sub_ele in ele.__dict__["child_elements"]:
                    if sub_ele.tag == "DATE" : assert(sub_ele.value == "02 MAR 2014")
                    if sub_ele.tag == "ADDR" :
                        for sub_ele2 in sub_ele.__dict__["child_elements"]:
                            if sub_ele2.tag == "CITY" : assert(sub_ele2.value == "Portillo")
                            if sub_ele2.tag == "STAE" : assert(sub_ele2.value == "Castilla y León")
                            if sub_ele2.tag == "CTRY" : assert(sub_ele2.value == "España")
            elif ele.tag == "DEAT":
                for sub_ele in ele.__dict__["child_elements"]:
                    if sub_ele.tag == "DATE" : assert(sub_ele.value == "ABT 2016")
            elif ele.tag == "BAPM":
                for sub_ele in ele.__dict__["child_elements"]:
                    if sub_ele.tag == "DATE" : assert(sub_ele.value == "AFT 03 MAR 2014")
            elif ele.tag == "BURI":
                for sub_ele in ele.__dict__["child_elements"]:
                    if sub_ele.tag == "DATE" : assert(sub_ele.value == "BEF 05 MAR 2016")
                
        gedcomfile = gedcom.GedcomFile()     
        gedcomfile.add_element(profile.individual)            
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()