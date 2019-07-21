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
#         GET methods: to be overwritten from common_family
#===============================================================================


        