'''
Created on 22 oct. 2019

@author: Val
'''
import logging, datetime, logging
from messages.pygenanalyzer_messages import MATCH_PROFILE_ERROR, MATCH_GENI, MATCH_CONFLICT_TASK, MATCH_CONFLICT_INFO
from messages.pygenanalyzer_messages import MATCH_REVIEW_TASK_BEGIN, MATCH_REVIEW_TASK_END, MATCH_REVIEW_DETAILS
from analyzefamily import CHILD, FATHER, MOTHER, PARTNER

THRESHOLD_MATCH = 2.0

class match_single_profile(object):
    '''
    This class matches a single profile with a GENI database, it shall return
    matches with other profiles
    '''
    def __init__(self, database, database_geni, data_language="en", name_convention="father_surname",  threshold = THRESHOLD_MATCH):
        '''
        It gets as input the profile to be matched within GENI
        '''
        self.database = database
        self.database_geni = database_geni
        self.data_language = data_language
        self.name_convention = name_convention
        self.threshold = threshold
        #Initialization of the different matcher functions
        self._init_tracking_logs()
    def match(self, profile_ID):
        '''
        It executes the match, assumes contains a GENI link in the profile_ID
        It will:
        - Generate a web link to the matched profile
        - Return the following:
            - A list of non-matched profiles with the relationship according to standard namings requesting review.
            - A dictonary of conflicts linked to lists of profile in score with request to review
            - A dictionary of matched profiles.
        '''
        #Initialization of the different matcher functions
        self._init_tracking_logs()
        profile_rm = self.database.get_profile_by_ID(profile_ID)
        print_out(str(profile_ID) + " = "  + profile_rm.nameLifespan())
        url = None
        #We confirm is a valid profile, should contain a match
        confirmed = False
        for web_ref in profile_rm.get_all_webs():
            if web_ref["name"] == self.database_geni.get_db_kind():
                confirmed = True
                url = web_ref["url"]
        if not confirmed:
            logging.error(MATCH_PROFILE_ERROR)
            return False
        #This is the profile for analysis
        profile_geni = self.database_geni.get_profile_by_ID(url)
        #Starting checking of the parents
        #FATHER
        _, father_rm = self.database.get_father_from_child(profile_rm.get_id())
        _, father_geni = self.database_geni.get_father_from_child(profile_geni.get_id())
        #First case is a potential match between the profiles
        if (father_rm and father_geni):
            self._match_single_pair(father_rm, father_geni)
        #We can only have the father_rm
        elif father_rm:
            self.non_matched_profiles_rm[father_rm.get_id()] = FATHER
            print_out("-    NO MATCH in profile " + str(father_rm.nameLifespan()) + " Relation = " + FATHER)
        elif father_geni:
            self.non_matched_profiles_geni[father_geni.get_id()] = FATHER
            print_out("-    NO MATCH in profile " + str(father_geni.nameLifespan()) + " Relation = " + FATHER)
        #Notice that we do not consider teh case of no parents at all identified, no match needed.
        #MOTHER
        _, mother_rm = self.database.get_mother_from_child(profile_rm.get_id())
        _, mother_geni = self.database_geni.get_mother_from_child(profile_geni.get_id())
        #First case is a potential match between the profiles
        if (mother_rm and mother_rm):
            self._match_single_pair(mother_rm, mother_geni)
        #We can only have the father_rm
        elif mother_rm:
            self.non_matched_profiles_rm[mother_rm.get_id()] = MOTHER
            print_out("-    NO MATCH in profile " + str(mother_rm.nameLifespan()) + " Relation = " + MOTHER)
        elif mother_geni:
            self.non_matched_profiles_geni[mother_geni.get_id()] = MOTHER
            print_out("-    NO MATCH in profile " + str(mother_geni.nameLifespan()) + " Relation = " + MOTHER)
        #Notice that we do not consider teh case of no parents at all identified, no match needed.
        #PARTNERS
        partners_rm = self.database.get_partners_from_profile(profile_rm.get_id())
        partners_geni = self.database_geni.get_partners_from_profile(profile_geni.get_id())
        self._track_2_lists(partners_rm, partners_geni, PARTNER)
        #CHILDREN
        children_rm = self.database.get_all_children(profile_ID)
        children_geni = self.database_geni.get_all_children(url)
        self._track_2_lists(children_rm, children_geni, CHILD)
        return self.non_matched_profiles_rm, self.non_matched_profiles_geni, self.conflict_profiles, self.matched_profiles
    def _match_single_pair(self, profile_rm, profile_geni):
        '''
        Internal function to avoid duplication of code, the profiles to be introduced shall be a profile typenot the id
        '''
        score,factor = profile_rm.comparison_score(profile_geni, self.data_language, self.name_convention)
        if (score*factor > self.threshold):
            #We have a match, so we will create the link as a web link
            notes_to_add = MATCH_GENI + datetime.date.today().strftime("%d-%m-%Y")
            #Prior to add, we need to check is not today in the profile
            existing = False
            previous_match = False
            all_matches = [profile_geni.get_this_profile_url()]
            webs = profile_rm.get_all_webs()
            for web in webs:
                if web["url"] == profile_geni.get_this_profile_url(): existing = True
                elif (web["name"] ==  self.database_geni.get_db_kind()) and (web["url"] != profile_geni.get_this_profile_url()):
                    previous_match = True
                    all_matches.append(web["url"])
            #If it has not been created before, we create the new match in the profile
            if not existing:
                profile_rm.setWebReference(profile_geni.get_this_profile_url(), name=self.database_geni.get_db_kind(), notes=notes_to_add)
                self.matched_profiles[profile_rm.get_id()] = profile_geni.get_id()
                print_out("-    MATCHED :" + str(profile_rm.nameLifespan()) + " WITH " + str(profile_geni.nameLifespan()))
            #If there was a different previous match, we shall inform in the profile for checking    
            if previous_match:
                profile_rm.set_task(MATCH_REVIEW_TASK_BEGIN + self.database_geni.get_db_kind() + MATCH_REVIEW_TASK_END, 
                                    details=MATCH_REVIEW_DETAILS + str(all_matches))
        else:
            #This is a conflict, we should have a single match!!!
            self._conflict_storing(profile_rm, [profile_geni.get_id()])
    def _conflict_storing(self, profile_rm, conflicted_profiles_ids):
        '''
        Internal function to avoid duplicates. It stores a conflict of matches deviation
        profile_rm is a profile kind
        conflicted_profile_ids is a list of ids with conflict
        '''
        print_out("-    CONFLICT of profile " + str(profile_rm.nameLifespan()) + " WITH PROFILE(S) " + str(conflicted_profiles_ids))
        #This is a conflict, we should have a single match!!!
        self.conflict_profiles[profile_rm.get_id()] = conflicted_profiles_ids
        details_info = MATCH_CONFLICT_INFO
        for ids_geni in conflicted_profiles_ids:
            details_info += self.database_geni.get_profile_by_ID(ids_geni).get_this_profile_url() + "     "
        profile_rm.set_task(MATCH_CONFLICT_TASK, priority=1, details= details_info, task_type = 0)
    def _init_tracking_logs(self):
        '''
        Init to empty for each matching operations
        '''
        #It will be a dictionary of profiles not matched and their relationship "LEFT side"
        self.non_matched_profiles_rm = {}
        #It will be a dictionary of profiles not matched and their relationship "RIGTH side"
        self.non_matched_profiles_geni = {}
        #Each componenet will have a profile as key and a list as value with the conflicts found
        self.conflict_profiles = {}
        #Each matched profile will have a profile id as key and a single match of another profile as value.
        self.matched_profiles = {}
    def _track_2_lists(self, profiles_rm, profiles_geni, kind_of_match):
        '''
        Function used for both partners and children as is a common function
        '''
        #We store here the profiles that have been identified in profiles_geni
        profiles_not_identified = list(profiles_geni)
        for rm_id in profiles_rm:
            profile_rm = self.database.get_profile_by_ID(rm_id)
            geni_matches = []
            for geni_id in profiles_geni:
                profile_geni = self.database_geni.get_profile_by_ID(geni_id)
                score, factor = profile_rm.comparison_score(profile_geni, self.data_language, self.name_convention)
                if score*factor > self.threshold:
                    geni_matches.append(geni_id)
                    if geni_id in profiles_not_identified: profiles_not_identified.remove(geni_id)
            #If we have a single profile that is matched,
            if len(geni_matches) == 0:
                self.non_matched_profiles_rm[rm_id] = kind_of_match
                print_out("-    NO MATCH in profile " + str(profile_rm.nameLifespan()) + " Relation = " + kind_of_match)
            elif len(geni_matches) == 1:
                self._match_single_pair(profile_rm, self.database_geni.get_profile_by_ID(geni_matches[0]))
            #Or we have more than one match... that is a conflict
            else:
                self._conflict_storing(profile_rm, geni_matches)
        #Now, we are able to detect those children on the "RIGHT" side. Not linked to other
        if len(profiles_not_identified) > 0:
            for missing_prof in profiles_not_identified:
                self.non_matched_profiles_geni[missing_prof] = kind_of_match
                prof = self.database_geni.get_profile_by_ID(missing_prof)
                print_out("-    NO MATCH in profile " + str(prof.nameLifespan()) + " Relation = " + kind_of_match)
def print_out(message):
    '''
    Function to be used for printing the obtained results
    '''
    logging.info(message)