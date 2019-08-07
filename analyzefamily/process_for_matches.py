'''
Created on 28 jul. 2019

@author: Val
'''

class process_a_db(object):
    '''
    This class will take a database and will process it analyzing with the different databases
    already available in the code
    '''
    def __init__(self, db):
        '''
        Constructor
        '''
        self.db = db
    def process(self):
        '''
        Determines the full database and detects potential matches
        '''
        for prof in self.db.profiles.keys():
            name = self.db.get_profile_by_ID(prof).nameLifespan()
        