'''
Created on 22 jul. 2019

@author: Val
'''
from pyGenealogy.common_family import family_profile
CHAR_PROF = "I"
CHAR_FAM = "F"

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
        self.count_prof = 0
        self.count_fam = 0
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
    def get_all_profiles(self):
        '''
        Returns all profiles in the database
        '''
        return self.profiles.values()
#===============================================================================
#         ADD methods: Add methods used to include a new profile and new family
#===============================================================================
    def add_profile(self, profile):
        '''
        It will add a new profile in the database
        '''
        self.count_prof += 1
        id_prof = CHAR_PROF + str(self.count_prof)
        self.profiles[id_prof] = profile
        return id_prof
    def add_family(self, father = None, mother = None, children = None, marriage = None):
        '''
        It will create and add a new family to the database
        it is better that each database will create their own families
        '''
        self.count_fam += 1
        id_fam = CHAR_FAM + str(self.count_fam)
        fam = family_profile(father = father, mother = mother, child = children, marriage = marriage)
        self.families[id_fam] = fam
        return id_fam