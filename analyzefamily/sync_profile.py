'''
Created on 1 jun. 2020

@author: Val
'''

MATCH = "_MATCH"

class sync_profiles(object):
    '''
    This class is a synchronizer of the data of 2 profiles, it makes sure the profiles
    have the same values, copying the missing data from one to the other
    '''
    def __init__(self, database_primary, database_secondary, data_language="en", name_convention="father_surname"):
        '''
        It gets as inputs:
        - database_primary: is derived function of common_database which will store the recording of the comparison
        - database_seconday: is derived function of common_database which is an external source for data
        - data_language: is the expected data languages as standards
        - name_convention: is the convention of inheriting surnames between families
        '''
        self.dbp = database_primary
        self.dbs = database_secondary
        self.data_language = data_language
        self.name_convention = name_convention
    def execute_sync(self):
        '''
        This is the core function, it will execute the global sync of profiles Between
        primary and secondary database
        '''
        kind_match = self.dbs.get_db_kind()
        match_str = str(kind_match) + MATCH
        #This execution will tell us the number of profiles that can be mathces
        linked_profiles = {}
        for prof in self.dbp.get_all_profiles():
            if prof.get_specific_web(kind_match): linked_profiles[prof.get_id()] = prof
        print(linked_profiles)
        