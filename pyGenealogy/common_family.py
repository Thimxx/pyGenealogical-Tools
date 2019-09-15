'''
Created on 8 jul. 2019

@author: Val
'''

class family_profile(object):
    '''
    Common profile used to handle families within pyGenealogy. It will relate parents with childs including marriage date
    '''
    def __init__(self, father = None, mother = None, child = None, marriage = None):
        '''
        Constructor
        '''
        self.father = None
        self.mother = None
        self.children = []
        self.marriage = None
        self.setFather(father)
        self.setMother(mother)
        self.setChild(child)
        self.setMarriage(marriage)
    def setFather(self, father):
        '''
        Just defining the father
        '''
        if father: self.father = father
    def setMother(self, mother):
        '''
        Just defining the mother
        '''
        if mother: self.mother = mother
    def setChild(self, child):
        '''
        Just defining the children of hte family
        '''
        if isinstance(child, list): self.children = child
        elif child: self.children.append(child)
    def setMarriage(self, marriage):
        '''
        Assigning the event of the marriage
        '''
        if marriage: self.marriage = marriage
    def set_id(self, id_fam):
        '''
        Determines the id of the family
        '''
        self.id = id_fam
#===============================================================================
#         GET methods: common get methods used for all families
#===============================================================================
    def getFather(self):
        '''
        It will return the ID of the father
        '''
        return self.father
    def getMother(self):
        '''
        It will return the ID of the mother
        '''
        return self.mother
    def getChildren(self):
        '''
        It will a list with the IDs of the children
        '''
        return self.children
    def get_id(self):
        '''
        Returns the id of the union
        '''
        return self.id
    def get_parents(self):
        '''
        Returns the parents of the union
        '''
        parents = []
        if self.getFather() : parents.append(self.getFather())
        if self.getMother() : parents.append(self.getMother())
        return parents
#===============================================================================
#         Other generic methods
#===============================================================================
    def is_child_in_family(self, child):
        '''
        Will confirm if the child is in the family
        '''
        return child in self.getChildren()