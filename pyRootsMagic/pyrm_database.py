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