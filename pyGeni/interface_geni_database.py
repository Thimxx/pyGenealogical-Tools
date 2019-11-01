'''
Created on 27 jul. 2019

@author: Val
'''
from pyGenealogy.common_database import gen_database
from pyGeni.profile import profile
from pyGeni.union import union
from pyGeni.immediate_family import immediate_family

class geni_database_interface(gen_database):
    '''
    This class is intended to act as an interface with geni database.
    '''
    def __init__(self):
        '''
        Simple constructor of the database
        '''
        gen_database.__init__(self)
        self.equivalence = {}
        self.inmediate = {}
#===============================================================================
#         GET methods: replacing base models
#===============================================================================
    def get_db_kind(self):
        '''
        Identified of the kind of database in use
        '''
        return "GENI"
    def get_profile_by_ID(self, id_profile):
        '''
        Returns the profile by the input ID
        '''
        if not ( (id_profile in self.profiles.keys()) or (id_profile in self.equivalence.keys()) ):
            prof = profile(id_profile)
            #We use an unique id wiht profile in front
            self.profiles[prof.get_id()] = prof
            if id_profile != prof.get_id():
                self.equivalence[id_profile] = prof.get_id()
        if id_profile in self.profiles.keys(): return self.profiles[id_profile]
        else: return self.profiles[self.equivalence[id_profile]]
    def get_family_by_ID(self, id_family):
        '''
        Returns the profile by the input ID
        '''
        if not id_family in self.families.keys():
            fam = union(id_family)
            self.families[id_family] = fam
        return self.families[id_family]
    def get_family_from_child(self, profile_id):
        '''
        It will return the family of a profile where is the child
        Returns the id of the family and the family object
        '''
        for family_id in self.families.keys():
            if self.families[family_id].is_child_in_family(profile_id): return family_id, self.families[family_id]
        #If we arrived here is because the family has not been found
        link_fam = self.get_families_from_profile(profile_id)
        if (len(link_fam.parent_union) > 0):
            union_id = link_fam.parent_union[0].get_id()
            return union_id, self.get_family_by_ID(union_id)
        else: return None, None
    def get_all_family_ids_is_parent(self, profile_id):
        '''
        It will provide all the families where the profile is one of the parents
        '''
        link_fam = self.get_families_from_profile(profile_id)
        families = []
        for union in link_fam.marriage_union:
            families.append(union.get_id())
        return families
    def get_all_children(self, profile_id):
        '''
        It will return all the families where the profile is a parent
        '''
        link_fam = self.get_families_from_profile(self.equivalence.get(profile_id,profile_id))
        return link_fam.children
    def get_father_from_child(self, profile_id):
        '''
        It will return the father of the profile
        In the specific case of GENI, the family is not allowing us to differentiate between Father and Mother
        '''
        family = self.get_family_from_child(profile_id)[1]
        #We may get an empty family...
        if family:
            for parent in family.get_parents():
                #We need to check each single partner to see if it is the Father or the Mother
                parent_prof = self.get_profile_by_ID(parent)
                if parent_prof.getGender() == "M":
                    return parent_prof.get_id(), parent_prof
        return None, None
    def get_mother_from_child(self, profile_id):
        '''
        It will return the mother of the profile
        In the specific case of GENI, the family is not allowing us to differentiate between Father and Mother
        '''
        family = self.get_family_from_child(profile_id)[1]
        #We may get an empty family...
        if family:
            for parent in family.get_parents():
                #We need to check each single partner to see if it is the Father or the Mother
                parent_prof = self.get_profile_by_ID(parent)
                if parent_prof.getGender() == "F":
                    return parent_prof.get_id(), parent_prof
        return None, None
    def get_partners_from_profile(self, profile_id):
        '''
        It will return all partners associated with the profile
        '''
        partners = []
        for family_id in self.get_all_family_ids_is_parent(profile_id):
            parents = self.get_family_by_ID(family_id).get_parents()
            addapted_parents = []
            #Due to bug issues in union, we will extract the actual ID.
            for parent in parents:
                prof_parent = self.get_profile_by_ID(parent)
                addapted_parents.append(prof_parent.get_id())
            addapted_parents.remove(profile_id)
            partners += addapted_parents
        return partners
#===============================================================================
#        INTERMEDIATE methods: methods avoiding duplications
#===============================================================================
    def get_families_from_profile(self, profile_id):
        '''
        Intermediate function providing families for a profile
        '''
        link_fam = self.inmediate.get(profile_id, immediate_family(profile_id))
        if not link_fam in self.inmediate.keys(): self.inmediate[profile_id] = link_fam
        return link_fam
        