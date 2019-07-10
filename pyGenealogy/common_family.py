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
        else: self.children.append(child)
    def setMarriage(self, marriage):
        '''
        Assigning the event of the marriage
        '''
        if marriage: self.marriage = marriage
        
        