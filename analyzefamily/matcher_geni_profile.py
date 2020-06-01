'''
Created on 22 oct. 2019

@author: Val
'''
import logging
from messages.pygenanalyzer_messages import MATCH_PROFILE_ERROR, MATCH_CONFLICT_TASK, MATCH_CONFLICT_INFO, MATCH_CONFLICT_URL_EXISTING, MATCH_CONFLICT_URL_MESSAGE
from analyzefamily import CHILD, FATHER, MOTHER, PARTNER
from analyzefamily import include_task_no_duplicate, include_match_profile, print_out

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
        self.current_match = None
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
        self.current_match = str(profile_ID) + ":" + profile_rm.nameLifespan()
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
        #We might have an address that has been updated, we double check for updating it in DB
        if url != profile_geni.get_this_profile_url():
            profile_rm.update_web_ref(url = profile_geni.get_this_profile_url(), name = self.database_geni.get_db_kind())
            print_out("UPDATING " + self.database_geni.get_db_kind() + " LINK to " + profile_geni.get_this_profile_url())
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
            print_out("-    NO MATCH of profile in " + self.database_geni.get_db_kind() + " " + str(father_rm.nameLifespan()) + " Relation = " + FATHER)
        elif father_geni:
            self.non_matched_profiles_geni[father_geni.get_id()] = FATHER
            print_out("-    NO MATCH of profile in " + self.database.get_db_kind() + " " + str(father_geni.nameLifespan()) + " Relation = " + FATHER)
        #Notice that we do not consider the case of no parents at all identified, no match needed.
        #MOTHER
        _, mother_rm = self.database.get_mother_from_child(profile_rm.get_id())
        _, mother_geni = self.database_geni.get_mother_from_child(profile_geni.get_id())
        #First case is a potential match between the profiles
        if (mother_rm and mother_geni):
            self._match_single_pair(mother_rm, mother_geni)
        #We can only have the father_rm
        elif mother_rm:
            self.non_matched_profiles_rm[mother_rm.get_id()] = MOTHER
            print_out("-    NO MATCH of profile in " + self.database_geni.get_db_kind() + " " + str(mother_rm.nameLifespan()) + " Relation = " + MOTHER)
        elif mother_geni:
            self.non_matched_profiles_geni[mother_geni.get_id()] = MOTHER
            print_out("-    NO MATCH of profile in " + self.database.get_db_kind() + " " + str(mother_geni.nameLifespan()) + " Relation = " + MOTHER)
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
            include_match_profile(profile_rm, profile_geni, self.database_geni.get_db_kind(), self.database_geni)
            #We always record the match obtained although was done before
            self.matched_profiles[profile_rm.get_id()] = profile_geni.get_id()
        else:
            #This is a conflict, we should have a single match!!!
            self._conflict_storing(profile_rm, [profile_geni.get_id()], self.database_geni)
    def _conflict_storing(self, profile_rm, conflicted_profiles_ids, db_conflict):
        '''
        Internal function to avoid duplicates. It stores a conflict of matches deviation
        profile_rm is a profile kind
        conflicted_profile_ids is a list of ids with conflict
        '''
        conflict_str = ""
        for prof_conf_id in conflicted_profiles_ids:
            prof_conf = db_conflict.get_profile_by_ID(prof_conf_id)
            conflict_str += str(prof_conf.nameLifespan()) + "  "
        print_out("-    CONFLICT of profile " + str(profile_rm.nameLifespan()) + " WITH PROFILE(S) " + conflict_str)
        #This is a conflict, we should have a single match!!!
        self.conflict_profiles[profile_rm.get_id()] = conflicted_profiles_ids
        details_info = MATCH_CONFLICT_INFO
        for ids_geni in conflicted_profiles_ids:
            details_info += self.database_geni.get_profile_by_ID(ids_geni).get_this_profile_url() + "     "
        include_task_no_duplicate(profile_rm, MATCH_CONFLICT_TASK, 1, details_info)
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
        conflict_potential_dictionary = {}
        for rm_id in profiles_rm:
            #We might be in a situation where very small similarities might create confusion of profiles, we store the previous score
            previous_score = 0
            conflict_match = False
            profile_rm = self.database.get_profile_by_ID(rm_id)
            url_rm_now = profile_rm.get_specific_web(self.database_geni.get_db_kind()).get("url", None)
            geni_matches = []
            for geni_id in list(profiles_not_identified):
                profile_geni = self.database_geni.get_profile_by_ID(geni_id)
                score, factor = profile_rm.comparison_score(profile_geni, self.data_language, self.name_convention)
                if score*factor > self.threshold:
                    #OPTIONS:
                    # 1.New profile is the right one
                    # 2.New profile is the first one
                    # 3.New profile is not the right one.but is the previous
                    # 4.New profile is as bad as the others.
                    #Option 1
                    if score*factor > 3*previous_score:
                        recover_profs = list(geni_matches)
                        geni_matches = [geni_id]
                        profiles_not_identified += recover_profs
                        previous_score = score*factor
                        if geni_id in profiles_not_identified: profiles_not_identified.remove(geni_id)
                    #Option 2
                    elif len(geni_matches) == 0:
                        geni_matches.append(geni_id)
                        previous_score = score*factor
                        if geni_id in profiles_not_identified: profiles_not_identified.remove(geni_id)
                    #Option 3
                    elif previous_score >= 3*score*factor:
                        #In this case we ignore... we keep the previous one
                        pass
                    #Option 4
                    else:
                        if score*factor > previous_score: previous_score = score*factor
                        if geni_id in profiles_not_identified: profiles_not_identified.remove(geni_id)
                elif score >= 3*self.threshold:
                    conflict_match = True
                    #This is a common case, where profiles have a minimum difference but still relevant, user to check
                    if rm_id in conflict_potential_dictionary:
                        conflict_potential_dictionary[rm_id].append(geni_id)
                    else:
                        conflict_potential_dictionary[rm_id] = [geni_id]
            #Options in place with the current match of url
            # No existing url => we ignore
            # Existing so...
            #  - The match is the same. => NO ACTION. Covered by code
            #  - The match is different => NO ACTION. Covered by code double match will be created with warning
            #  - There is no match => ACTION. Include a conflict warning
                
            #If there is a single match, whatever other conditions, we introduce as a match
            if len(geni_matches) == 1:
                self._match_single_pair(profile_rm, self.database_geni.get_profile_by_ID(geni_matches[0]))
                #In case there has been found also a conflict, the conflict is no longer needed, as we do have a match.
                if rm_id in conflict_potential_dictionary: del conflict_potential_dictionary[rm_id]
            else:
                #If there is no single match, we can have several options...
                if (len(geni_matches) == 0) and (not conflict_match):
                    if url_rm_now and (len(geni_matches) == 0):                        #This is the only option where we are going ot generate a conflict, as existing before!
                        print_out("-    CONFLICT of profile " + str(profile_rm.nameLifespan()) + " as has a previous match.")
                        details = MATCH_CONFLICT_URL_MESSAGE + self.current_match + " as " + kind_of_match
                        include_task_no_duplicate(profile_rm, MATCH_CONFLICT_URL_EXISTING, 1, details)
                        #We move the profile to conflicted ones
                        self.conflict_profiles[profile_rm.get_id()] = []
                    else:
                        self.non_matched_profiles_rm[rm_id] = kind_of_match
                        print_out("-    NO MATCH of profile in " + self.database_geni.get_db_kind() + " " +
                              str(profile_rm.nameLifespan()) + " Relation = " + kind_of_match)
                #Or we have more than one match... that is a conflict
                elif len(geni_matches) > 1:
                    self._conflict_storing(profile_rm, geni_matches, self.database_geni)
        #We perform another loop with those profiles which were conflicted as some of the might have been identified on the other side
        temp_conflicted = conflict_potential_dictionary.copy()
        for rm_id_conflicted in temp_conflicted.keys():
            #We might have some profiles that have been already identified but stored as potential conflicts. We shall remove them
            for geni_conflict_key in temp_conflicted[rm_id_conflicted]:
                if geni_conflict_key in self.matched_profiles.values(): conflict_potential_dictionary[rm_id_conflicted].remove(geni_conflict_key)
        #The profiles left, are either a match, or we have found again gaps of profiles not found
        for rm_id_final_confliced in conflict_potential_dictionary.keys():
            #If the list in the dictionary is empty, we do have a missing proifle
            profile_rm_new = self.database.get_profile_by_ID(rm_id_final_confliced)
            if conflict_potential_dictionary[rm_id_final_confliced] == []:
                #This profile was having a potential conflict that ended being actually an empty profile, it is a missing match
                self.non_matched_profiles_rm[rm_id_final_confliced] = kind_of_match
                print_out("-    NO MATCH of profile in " + self.database_geni.get_db_kind() + " " +
                              str(profile_rm_new.nameLifespan()) + " Relation = " + kind_of_match)
            else:
                #Ok, in this case we have a potential match with an actual conflict
                details_info = "-    CONFLICT POTENTIAL MATCH " + str(profile_rm_new.nameLifespan()) + " with the following: "
                address_list = []
                for profile_id in conflict_potential_dictionary[rm_id_final_confliced]:
                    #We remove conflicted profiles from the matching step
                    if profile_id in profiles_not_identified: profiles_not_identified.remove(profile_id)
                    profile = self.database_geni.get_profile_by_ID(profile_id)
                    address_list.append(profile.get_this_profile_url())
                    details_info += str(profile.nameLifespan()) + " Relation = " + kind_of_match
                include_task_no_duplicate(profile_rm_new, MATCH_CONFLICT_TASK, 1, details_info)
                print_out(details_info)
                self.conflict_profiles[rm_id_final_confliced] = address_list
        #Now, we are able to detect those children on the "RIGHT" side. Not linked to other
        if len(profiles_not_identified) > 0:
            for missing_prof in profiles_not_identified:
                self.non_matched_profiles_geni[missing_prof] = kind_of_match
                prof = self.database_geni.get_profile_by_ID(missing_prof)
                print_out("-    NO MATCH of profile in " + self.database.get_db_kind() + " " + str(prof.nameLifespan()) + " Relation = " + kind_of_match)