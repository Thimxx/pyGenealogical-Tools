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
    def get_family_from_child(self, profile_id):
        '''
        It will return the family of a profile where is the child
        Returns the id of the family and the family object
        '''
        for family_id in self.families.keys():
            if self.families[family_id].is_child_in_family(profile_id): return family_id, self.families[family_id]
        return None, None
    def get_father_from_child(self, profile_id):
        '''
        It will return the father of the profile
        Returns the id of the profile and the profile object
        '''
        family = self.get_family_from_child(profile_id)[1]
        #We may get an empty family...
        if family: return family.getFather(), self.get_profile_by_ID(family.getFather())
        else: return None, None
    def get_mother_from_child(self, profile_id):
        '''
        It will return the mother of the profile
        Returns the id of the profile and the profile object
        '''
        family = self.get_family_from_child(profile_id)[1]
        if family: return family.getMother(), self.get_profile_by_ID(family.getMother())
        else: return None, None
    def get_all_family_ids_is_parent(self, profile_id):
        '''
        It will provide all the families where the profile is one of the parents
        '''
        families = []
        for family_id in self.families.keys():
            if profile_id in self.get_family_by_ID(family_id).get_parents(): families.append(family_id)
        return families
    def get_all_children(self, profile_id):
        '''
        This function will provide all the children associated to a profile
        '''
        children = []
        for family_id in self.get_all_family_ids_is_parent(profile_id):
            children += self.get_family_by_ID(family_id).getChildren()
        return children
    def get_parents_from_child(self, profile_id):
        '''
        It returns the ids and profiles of the parents for the given profile
        '''
        f_id, f_profile = self.get_father_from_child(profile_id)
        m_id, m_profile = self.get_mother_from_child(profile_id)
        return [f_id, m_id], [f_profile, m_profile]
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
        fam.set_id(id_fam)
        self.families[id_fam] = fam
        return id_fam