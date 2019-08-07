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
        res_names = self.database.execute("SELECT * FROM PersonTable")
        #We transfer all profiles to the database
        for name in res_names:
            prof = rootsmagic_profile(name[0], self.database)
            self.profiles[name[0]] = prof
        res_families = self.database.execute("SELECT * FROM FamilyTable")
        #We transfer as well all families to the database
        for family in res_families:
            fam = rootsmagic_family(family[0], self.database)
            self.families[family[0]] = fam
    def close_db(self):
        '''
        Closes the database
        '''
        self.database.close()
#===============================================================================
#         GET methods: all methods compatible with common_database
#===============================================================================