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