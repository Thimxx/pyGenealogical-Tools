'''
Created on 6 jul. 2019

@author: Val
'''
import sqlite3
from pyRootsMagic.rootsmagic_profile import rootsmagic_profile

class database_rm(object):
    '''
    This class is used for reading a database RootsMagic and allowing to access
    to the different profiles.
    '''
    def __init__(self, db_file):
        '''
        Construction, taking as initial parameter the location of the database
        '''
        self.database = None
        self.right_read = False
        #Open database and get it as part of the class
        self.database = sqlite3.connect(db_file)
        res_names = self.database.execute("SELECT * FROM NameTable")
        self.profiles = []
        for name in res_names:
            prof = rootsmagic_profile(name[3], name[2], name[0], name[1], self.database)
            self.profiles.append(prof)
    def close_db(self):
        '''
        Closes the database
        '''
        self.database.close()