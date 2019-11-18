'''
Created on 28 jul. 2019

@author: Val
'''
import logging
from messages.pygenanalyzer_messages import PROCESS_MATCH_NUMBER_OF_IMPACTS_BEGIN, PROCESS_MATCH_NUMBER_OF_IMPACTS_END
from messages.pygenanalyzer_messages import PROCESS_ADD_PROFILE_BEGIN, PROCESS_ADD_PROFILE_END
from analyzefamily.matcher_geni_profile import match_single_profile

class process_a_db(object):
    '''
    This class will take a database and will process it analyzing with the different databases
    already available in the code
    '''
    def __init__(self, db_input, db_check, data_language="en", name_convention="father_surname"):
        '''
        Constructor
        
        db_input = the database that will be matched 
        db_check = the database that will be the source of match and reference in db_input
        
        '''
        self.db_input = db_input
        self.db_check = db_check
        self.data_language = data_language
        self.name_convention = name_convention
    def process(self, profiles_2_analyze = "all"):
        '''
        Determines the full database and detects potential matches
        
        profiles_2_analyze = an array of profiles for the first database which shall be analyzed, in case of no
        input it will analyze all profiles.
        '''
        kind_match = self.db_check.get_db_kind()
        matcher_profiles = match_single_profile(self.db_input, self.db_check, data_language= self.data_language, name_convention= self.name_convention)
        linked_profies = {}
        for prof in self.db_input.get_all_profiles():
            webs = prof.get_all_webs()
            for web in webs:
                if web["name"] == kind_match:
                    linked_profies[prof.get_id()] = prof
        print_out(PROCESS_MATCH_NUMBER_OF_IMPACTS_BEGIN + str(kind_match) + PROCESS_MATCH_NUMBER_OF_IMPACTS_END + str(len(linked_profies)))
        for prof_id in linked_profies:
            #We will only analyze only the profiles which have been introduced
            if (profiles_2_analyze == "all") or (prof_id in profiles_2_analyze):
                non_matched_profiles_input, non_matched_profiles_check, conflict_profiles, matched_profiles = matcher_profiles.match(prof_id)
                if( ("father" in non_matched_profiles_check.values()) and ("mother" in non_matched_profiles_check.values())):
                    father_id = list(non_matched_profiles_check.keys())[list(non_matched_profiles_check.values()).index("father")]
                    mother_id = list(non_matched_profiles_check.keys())[list(non_matched_profiles_check.values()).index("mother")]
                    print_out("Adding both " + father_id + "and " + mother_id)
                    #We remove the profiles, as will be added
                    del non_matched_profiles_check[father_id]
                    del non_matched_profiles_check[mother_id]
                for prof_id in non_matched_profiles_check.keys():
                    print_out(PROCESS_ADD_PROFILE_BEGIN + self.db_check.get_profile_by_ID(prof_id).nameLifespan()
                              + PROCESS_ADD_PROFILE_END + non_matched_profiles_check[prof_id] )
            
def print_out(message):
    '''
    Function to be used for printing the obtained results
    '''
    logging.info(message)
        