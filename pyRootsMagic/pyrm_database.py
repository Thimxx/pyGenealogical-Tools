'''
Created on 6 jul. 2019

@author: Val
'''
import sqlite3
from pyRootsMagic.rootsmagic_profile import rootsmagic_profile
from pyRootsMagic.rootsmagic_family import rootsmagic_family
from pyGenealogy.common_database import gen_database

class database_rm(gen_database):
    '''
    This class is used for reading a database RootsMagic and allowing to access
    to the different profiles.
    '''
    def __init__(self, db_file):
        '''
        Construction, taking as initial parameter the location of the database
        '''
        gen_database.__init__(self)
        self.database = None
        self.right_read = False
        #Open database and get it as part of the class
        self.database = sqlite3.connect(db_file)
    def close_db(self):
        '''
        Closes the database
        '''
        self.database.close()
#===============================================================================
#         GET methods: all methods compatible with common_database
#===============================================================================
    def get_profile_by_ID(self, id_profile):
        '''
        Returns the profile by the input ID
        '''
        profile_id = "SELECT * FROM PersonTable WHERE PersonID=?"
        profile_cursor = self.database.execute(profile_id, (str(id_profile),) )
        #Now let's fetch the first value
        is_profile_in = profile_cursor.fetchone()
        if is_profile_in:
            return rootsmagic_profile(id_profile, self.database)
        else:
            return None
    def get_family_by_ID(self, id_family):
        '''
        Returns the profile by the input ID
        '''
        family_id = "SELECT * FROM FamilyTable WHERE FamilyID=?"
        family_cursor = self.database.execute(family_id, (str(id_family),) )
        #Now let's fetch the first value
        is_family_in = family_cursor.fetchone()
        if is_family_in:
            return rootsmagic_family(id_family, self.database)
        else:
            return None
    def get_all_profiles(self):
        '''
        Returns all profiles in the database
        '''
        res_names = self.database.execute("SELECT * FROM PersonTable")
        #We obtain now all profiles
        profiles = {}
        for name in res_names:
            prof = rootsmagic_profile(name[0], self.database)
            profiles[name[0]] = prof
        return profiles.values()
    def get_family_from_child(self, profile_id):
        '''
        It will return the family of a profile where is the child
        Returns the id of the family and the family object
        '''
        family_id = "SELECT * FROM ChildTable WHERE ChildID=?"
        family_cursor = self.database.execute(family_id, (str(profile_id),) )
        #Now let's fetch the first value, we are not expecting several fathers
        is_family_in = family_cursor.fetchone()
        if is_family_in:
            return int(is_family_in[2]), self.get_family_by_ID(is_family_in[2])
        else:
            return None, None
    def get_all_family_ids_is_parent(self, profile_id):
        '''
        It will provide all the families where the profile is one of the parents
        '''
        families = []
        family_id = "SELECT * FROM FamilyTable WHERE FatherID=? OR MotherID=?"
        family_cursor = self.database.execute(family_id, (str(profile_id),str(profile_id),) )
        #There can be several families
        for family in family_cursor:
            families.append(int(family[0]))
        return families
    def get_all_children(self, profile_id):
        '''
        This function will provide all the children associated to a profile
        '''
        children = []
        #First, we get all families
        families = self.get_all_family_ids_is_parent(profile_id)
        for family_id in families:
            child_db = "SELECT * FROM ChildTable WHERE FamilyID=?"
            child_cursor = self.database.execute(child_db, (str(family_id),) )
            for child in child_cursor:
                children.append(child[1])
        return children