'''
Created on 27 jul. 2019

@author: Val
'''
from pyGenealogy.common_database import gen_database
from pyGeni.profile import profile
from pyGeni.union import union

class geni_database_interface(gen_database):
    '''
    This class is intended to act as an interface with geni database.
    '''
    def __init__(self):
        '''
        Simple constructor of the database
        '''
        gen_database.__init__(self)
#===============================================================================
#         GET methods: replacing base models
#===============================================================================
    def get_profile_by_ID(self, id_profile):
        '''
        Returns the profile by the input ID
        '''
        if not id_profile in self.profiles.keys():
            prof = profile(id_profile)
            self.profiles[id_profile] = prof
        return self.profiles[id_profile]
    def get_family_by_ID(self, id_family):
        '''
        Returns the profile by the input ID
        '''
        if not id_family in self.families.keys():
            fam = union(id_family)
            self.families[id_family] = fam
        return self.families[id_family]