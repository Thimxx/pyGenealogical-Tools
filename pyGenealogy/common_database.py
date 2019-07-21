'''
Created on 22 jul. 2019

@author: Val
'''

class gen_database(object):
    '''
    Base database for containing overall profiles handled in the genealogy. 
    Will contain base functions for all database to be adapted per kind of database
    (Geni, GEDCOM, RootsMagic or internal)
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.profiles = {}
        self.families = {}
#===============================================================================
#         GET methods: to be used by all upper functions or be replace
#===============================================================================
    def get_profile_by_ID(self, id_profile):
        '''
        Returns the profile by the input ID
        '''
        if id_profile in self.profiles.keys():
            return self.profiles[id_profile]
        else:
            return None
    def get_family_by_ID(self, id_family):
        '''
        Returns the profile by the input ID
        '''
        if id_family in self.families.keys():
            return self.families[id_family]
        else:
            return None
        