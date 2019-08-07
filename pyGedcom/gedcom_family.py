'''
Created on 5 ago. 2019

@author: Val
'''
from pyGenealogy.common_family import family_profile

class family_gedcom(family_profile):
    '''
    Family profile which is based on common_family. Will be used as input the gedcom file.
    '''
    def __init__(self, gedcom_input = None, father = None, mother = None, child = None, marriage = None):
        '''
        Constructor, it will use as input a dictionary with Gedcom input
        '''
        #We set the values internally
        family_profile.__init__(self)
        if gedcom_input:
            self.family = gedcom_input
            #We set-up the family entering one-by-one all different inputs
            if "HUSB" in gedcom_input: self.setFather(gedcom_input["HUSB"].get("VALUE", None))
            if "WIFE" in gedcom_input: self.setMother(gedcom_input["WIFE"].get("VALUE", None))
            if "CHIL" in gedcom_input: self.setChild(gedcom_input["CHIL"].get("VALUE", None))
        else:
            self.family = {"VALUE" : "FAM"}
            if father:
                self.setFather(father)
                self.family["HUSB"] = {"VALUE" : father}
            if mother:
                self.setMother(mother)
                self.family["WIFE"] = {"VALUE" : mother}
            if child:
                self.setChild(child)
                self.family["CHIL"] = {"VALUE" : child}