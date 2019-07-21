'''
Created on 21 jul. 2019

@author: Val
'''

from pyGenealogy.common_family import family_profile

class rootsmagic_family(family_profile):
    '''
    Profile linking family search linking to RootsMagic families
    '''
    def __init__(self, family_id, database):
        '''
        Constructor, this contructor assumes the family is already existing in RootsMagic
        '''
        self.family_id = family_id
        self.database = database
        family_profile.__init__(self, father = None, mother = None, child = None, marriage = None)
#===============================================================================
#         RETURN methods: generic data used by the different functions in this class
#===============================================================================
    def returnFamilyRootsMagic(self):
        '''
        Return a vector in from FamilyTable to be used by other methods
        '''
        input_family = "SELECT * FROM FamilyTable WHERE FamilyId=?"
        events = self.database.execute(input_family, (str(self.family_id),) )
        return events.fetchone()
#===============================================================================
#         GET methods: to be overwritten from common_family
#===============================================================================
    def getFather(self):
        '''
        It will return the ID of the father
        '''
        father = self.returnFamilyRootsMagic()[1]
        if father == 0: return None
        else: return father
    def getMother(self):
        '''
        It will return the ID of the mother
        '''
        mother = self.returnFamilyRootsMagic()[2]
        if mother == 0: return None
        else: return mother
    def getChildren(self):
        '''
        It will a list with the IDs of the children
        '''
        input_children = "SELECT * FROM ChildTable WHERE FamilyId=?"
        children = self.database.execute(input_children, (str(self.family_id),) )
        all_children = []
        loop_fetch = True
        while loop_fetch:
            this_child = children.fetchone()
            if this_child:
                all_children.append(this_child[1])
            else:
                loop_fetch = False
                return all_children