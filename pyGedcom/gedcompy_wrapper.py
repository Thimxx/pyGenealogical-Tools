'''
Created on 15 oct. 2017

@author: Val

This class wraps the use of the library Gedcompy located here:
https://github.com/rory/gedcompy

It is currently not updated since 2 years and it is missing several key functions

'''
import gedcom

class gedcom_file(gedcom.GedcomFile):
    '''
    This wrapping is only creating
    '''


    def __init__(self):
        '''
        Constructor
        '''
        gedcom.GedcomFile.__init__(self)
    
    def create_family(self, husband, wife, children):
        '''
        Creates a family inside the gedcomfile, it only creates the family, all
        individuals should have been already included 
        
        Inputs shall be gedcom_profiles format, children shall be a list
        '''
        ged_family = self.family()
        #Let's create the different elements for our Family
        ged_husband = gedcom.Element(tag="HUSB", value=husband.return_id())
        ged_family.add_child_element(ged_husband)
        ged_wife = gedcom.Element(tag="WIFE", value=wife.return_id())
        ged_family.add_child_element(ged_wife)
        for child in children:
            ged_child = gedcom.Element(tag="CHIL", value=child.return_id())
            ged_family.add_child_element(ged_child)
        
        include_marr, ged_marr = husband.get_event_element("marriage")
        if include_marr: ged_family.add_child_element(ged_marr)
            
        