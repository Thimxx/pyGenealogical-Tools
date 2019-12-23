'''
Created on 28 jul. 2019

@author: Val
'''
import logging, datetime
from messages.pygenanalyzer_messages import PROCESS_MATCH_NUMBER_OF_IMPACTS_BEGIN, PROCESS_MATCH_NUMBER_OF_IMPACTS_END
from messages.pygenanalyzer_messages import PROCESS_ADD_PROFILE_BEGIN, PROCESS_ADD_PROFILE_END, MATCH_ADDING_PROFILES, MATCH_POTENTIAL_DUPLICATE
from messages.pygenanalyzer_messages import PROCESS_TASK_NAME, PROCESS_TASK_DETAILS, PROCESS_NO_ACCESS
from analyzefamily.matcher_geni_profile import match_single_profile
from messages.pygenanalyzer_messages import MATCH_GENI
from messages import AND_STRING, TO_STRING
from pyGenealogy.generic_functions import get_research_log_id

MATCH = "_MATCH"
STATUS_MATCHED = "MATCHED="
STATUS_TO_CHECK = "CHECK "

class process_a_db(object):
    '''
    This class will take a database and will process it analyzing with the different databases
    already available in the code
    '''
    def __init__(self, db_input, db_check, data_language="en", name_convention="father_surname",
                 event_year_task = None):
        '''
        Constructor
        
        db_input = the database that will be matched
        db_check = the database that will be the source of match and reference in db_input
        
        '''
        self.db_input = db_input
        self.db_check = db_check
        self.data_language = data_language
        self.name_convention = name_convention
        self.event_year_task = event_year_task
    def process(self, profiles_2_analyze = "all", storage = False, threshold = 360, avoid_import_living_from = ["input", "check"]):
        '''
        Determines the full database and detects potential matches
        
        profiles_2_analyze = an array of profiles for the first database which shall be analyzed, in case of no
        input it will analyze all profiles.
        avoid_import_living_from will be a list with either input or check, it will not import the living from that database
        '''
        kind_match = self.db_check.get_db_kind()
        match_str = str(kind_match) + MATCH
        matcher_profiles = match_single_profile(self.db_input, self.db_check, data_language= self.data_language, name_convention= self.name_convention)
        linked_profiles = {}
        for prof in self.db_input.get_all_profiles():
            if prof.get_specific_web(kind_match): linked_profiles[prof.get_id()] = prof
        print_out(PROCESS_MATCH_NUMBER_OF_IMPACTS_BEGIN + str(kind_match) + PROCESS_MATCH_NUMBER_OF_IMPACTS_END + str(len(linked_profiles)))
        for prof_id in linked_profiles:
            if (profiles_2_analyze == "all") or (prof_id in profiles_2_analyze):
                prof_in_study = linked_profiles[prof_id]
                if continue_match(prof_in_study, match_str, threshold = threshold):
                    prof_linked_id = prof_in_study.get_specific_web(kind_match)["url"]
                    prof_linked = self.db_check.get_profile_by_ID(prof_linked_id)
                    #In order to get the marriage, first we get the family from the other database
                    _, family_profile = self.db_check.get_family_from_child(prof_linked.get_id())
                    _, family_input = self.db_input.get_family_from_child(prof_id)
                    #We will only analyze the profiles which have been introduced
                    loc_research = get_research_log_id(prof_in_study, storage = storage)
                    non_matched_profiles_input, non_matched_profiles_check, conflict_profiles, matched_profiles = matcher_profiles.match(prof_id)
                    #REMOVAL OF LIVING
                    #If the option is selected to not publish data that is restricted like living we remove teh matched characters
                    temp_data = {"input" :
                                    {"non_matches": non_matched_profiles_input,
                                     "database":self.db_input, "other_db": self.db_check,
                                     "family_is_child": family_input,
                                     "current_id_to_add": prof_linked_id,
                                     "current_id_matched": prof_id},
                                 "check" :
                                    {"non_matches": non_matched_profiles_check,
                                     "database":self.db_check, "other_db": self.db_input,
                                     "family_is_child": family_profile,
                                     "current_id_to_add": prof_id,
                                     "current_id_matched": prof_linked.get_id()}}
                    for kind_db in temp_data:
                        #We create a temporal copy to remove the data
                        temp_input = list(temp_data[kind_db]["non_matches"])
                        for prof in temp_input:
                            potential_profile = temp_data[kind_db]["database"].get_profile_by_ID(prof)
                            #REMOVAL OF LIVING
                            #If the option is selected to not publish data that is restricted like living we remove teh matched characters
                            if (kind_db in avoid_import_living_from) and potential_profile.getLiving():
                                del temp_data[kind_db]["non_matches"][prof]
                                print_out("-    AVOIDING INTRODUCTION OF LIVING "+ str(potential_profile.nameLifespan()) +
                                     " FROM THE DATABASE " + temp_data[kind_db]["database"].get_db_kind())
                    #Prior to starting the overall copy/match, we should check first if potential candidates exists in the input database
                    temp_checking = dict(non_matched_profiles_check)
                    for prof in temp_checking:
                        potential_profile = self.db_check.get_profile_by_ID(prof)
                        #MATCHING: we look if the profile also exists before
                        matches = self.db_input.get_potential_profile_match(potential_profile,
                                data_language = self.data_language, name_convention = self.name_convention)
                        if len(matches) > 0:
                            #In this case we have a certain potential match. We should not add and rather, leave for checking an human being
                            del non_matched_profiles_check[prof]
                            print_out("-    POTENTIAL DUPLICATE of profile " + str(potential_profile.nameLifespan()) +
                                " WITH PROFILE(S) ID(S) " + str(matches))
                            #This is a conflict, we should avoid duplicating job of checking and solving
                            conflict_profiles[prof] = matches
                            details_info = ("Potential existing duplicates for profile " + potential_profile.nameLifespan() +
                                            " with web " + potential_profile.get_this_profile_url() + " in the profiles:      ")
                            for ids_check in matches:
                                temp_prof = self.db_input.get_profile_by_ID(ids_check)
                                details_info += str(ids_check) + " : " + temp_prof.nameLifespan() + "        "
                            prof_in_study.set_task(MATCH_POTENTIAL_DUPLICATE, priority=1, details= details_info, task_type = 0)
                    ###################
                    #MATCH INTRODUCTION
                    ###################
                    for db_kind in temp_data:
                        #CASE MATCH: No parents at all and introducing both parents
                        non_match_now = temp_data[db_kind]["non_matches"]
                        db_now = temp_data[db_kind]["database"]
                        db_other = temp_data[db_kind]["other_db"]
                        family_is_child = temp_data[db_kind]["family_is_child"]
                        current_id_to_add = temp_data[db_kind]["current_id_to_add"]
                        if( ("father" in non_match_now.values()) and ("mother" in non_match_now.values())):
                            #We shall first obtain the id of the profiles from the check database (i.e. geni)
                            father_id = list(non_match_now.keys())[list(non_match_now.values()).index("father")]
                            mother_id = list(non_match_now.keys())[list(non_match_now.values()).index("mother")]
                            father_profile = db_now.get_profile_by_ID(father_id)
                            mother_profile = db_now.get_profile_by_ID(mother_id)
                            #We also add the link!
                            print_out(MATCH_ADDING_PROFILES + father_profile.nameLifespan() + AND_STRING +
                                    mother_profile.nameLifespan() + TO_STRING + db_other.get_db_kind() )
                            marriage_event = family_is_child.getMarriage()
                            #So.. we add the new profiles
                            new_father_id, new_mother_id, _ = db_other.add_parents(child_profile_id = current_id_to_add, father_profile = father_profile, 
                                                                            mother_profile= mother_profile, marriage_event= marriage_event)
                            if db_kind == "check":
                                self.add_match_to_prof(new_father_id, father_profile)
                                self.add_match_to_prof(new_mother_id, mother_profile)
                            #We remove the profiles, as will be added
                            del non_match_now[father_id]
                            del non_match_now[mother_id]
                    #################
                    # CONTINUE HERE
                    #################
                    #PARTNERS: Review of partners for inclusion
                    partners_input = self.db_input.get_partners_from_profile(prof_id)
                    matched_partners = {}
                    for partner_input in partners_input:
                        if partner_input in matched_profiles:
                            matched_partners[partner_input] = matched_profiles[partner_input]
                    for kind_db in temp_data:
                        #We create a temporal copy to remove the data
                        temp_2_use = list(temp_data[kind_db]["non_matches"])
                        for prof in temp_2_use:
                            if temp_data[kind_db]["non_matches"][prof] == "partner":
                                partner_profile = temp_data[kind_db]["database"].get_profile_by_ID(prof)
                                #Good, we will need now to add the new partner to the INPUT area
                                print_out(PROCESS_ADD_PROFILE_BEGIN + partner_profile.nameLifespan() + TO_STRING +
                                           temp_data[kind_db]["other_db"].get_db_kind() + PROCESS_ADD_PROFILE_END + temp_data[kind_db]["non_matches"][prof] )
                                family_check = temp_data[kind_db]["database"].get_family_from_partners(temp_data[kind_db]["current_id_matched"], 
                                                                                                       partner_profile.get_id())
                                marriage_event = temp_data[kind_db]["database"].get_family_by_ID(family_check).getMarriage()
                                id_partner, _ = temp_data[kind_db]["other_db"].add_partner(temp_data[kind_db]["current_id_to_add"], 
                                                                                           partner_profile, marriage = marriage_event)
                                if kind_db == "input":
                                    self.add_match_to_prof(prof, temp_data[kind_db]["other_db"].get_profile_by_ID(id_partner))
                                    matched_partners[prof] = id_partner
                                elif kind_db == "check":
                                    self.add_match_to_prof(id_partner, partner_profile)
                                    matched_partners[id_partner] = prof
                                del temp_data[kind_db]["non_matches"][partner_profile.get_id()]
                    #We go ahead looking first for each matched partner
                    for partner_input in matched_partners:
                        partner_check = matched_partners[partner_input]
                        #We need the family which will be the input for the children
                        family_part_input = self.db_input.get_family_from_partners(prof_id, partner_input)
                        family_part_check = self.db_check.get_family_from_partners(prof_linked.get_id(), partner_check)
                        family_part = {"input" : family_part_check, "check" : family_part_input}
                        family_current = {"input" : family_part_input, "check" : family_part_check}
                        #INTRODUCTION: CHILDREN in the family
                        for kind_db in temp_data:
                            temp = dict(temp_data[kind_db]["non_matches"])
                            for prof in temp.keys():
                                #We will only select those profiles which are children 
                                if (temp_data[kind_db]["non_matches"][prof] == "child") and (prof in temp_data[kind_db]["database"].get_children_from_family(family_current[kind_db])):
                                    child_profile = temp_data[kind_db]["database"].get_profile_by_ID(prof)
                                    #Ok, if the profile is accessible, we go ahead for creation
                                    if (child_profile.get_accessible()):
                                        print_out(PROCESS_ADD_PROFILE_BEGIN + child_profile.nameLifespan() + TO_STRING + temp_data[kind_db]["other_db"].get_db_kind() +
                                            PROCESS_ADD_PROFILE_END + temp_data[kind_db]["non_matches"][prof] )
                                        
                                        child_new_ids = temp_data[kind_db]["other_db"].add_child(family_part[kind_db], [child_profile] )
                                        if kind_db == "input":
                                            child_new_prof = self.db_check.get_profile_by_ID(child_new_ids[0])
                                            self.add_match_to_prof(prof, child_new_prof)
                                        elif kind_db == "check":
                                            self.add_match_to_prof(child_new_ids[0], child_profile)
                                    else:
                                        print_out(child_profile.nameLifespan() +PROCESS_NO_ACCESS)
                                    del temp_data[kind_db]["non_matches"][prof]
                    ################################################################
                    if len({**non_matched_profiles_input, **non_matched_profiles_check, **conflict_profiles}) == 0:
                        #In this case, we have achieved the full matching, we store the information
                        today = datetime.date.today().toordinal()
                        notes_toadd = STATUS_MATCHED + str(today)
                        record_research_log(prof_in_study, match_str, loc_research, prof_linked_id, notes_toadd)
                    else:
                        notes_toadd = (STATUS_TO_CHECK + " "*10 + "--Missing match input " + str(non_matched_profiles_input) + " "*10  +
                             "--Missing match check " + str(non_matched_profiles_check) + " "*10  + "--Pending conflicts " + str(conflict_profiles))
                        record_research_log(prof_in_study, match_str, loc_research, prof_linked_id, notes_toadd)
                else:
                    print_out("SKIPPING "+ prof_in_study.nameLifespan(), log_level = 15)
    def add_match_to_prof(self, prof_id, profile_to_match):
        '''
        It will add the match to the profile id
        prof_id shall be the profile in input database by ID
        profile_to_match shall be the profile of pyGenealogy.common_profile derived class
        '''
        notes_to_add = MATCH_GENI + datetime.date.today().strftime("%d-%m-%Y")
        profile = self.db_input.get_profile_by_ID(prof_id)
        profile.setWebReference(profile_to_match.get_this_profile_url(), name=self.db_check.get_db_kind(), notes=notes_to_add)
        #We also need to introduce the matching of tasks
        if self.event_year_task:
            #We only enter if the data has been introduced
            details = ""
            for event in profile.getEvents():
                if event.get_year() and (event.get_year() >= self.event_year_task):
                    details += PROCESS_TASK_DETAILS + str(event.get_event_type()) + "/n"
            if details != "":
                profile.set_task(PROCESS_TASK_NAME, priority=1, details=details)
def print_out(message, log_level = 20):
    '''
    Function to be used for printing the obtained results
    '''
    logging.log(log_level ,message)
def continue_match(profile, match_log, threshold = 360):
    ''''
    This function will confirm if match should or not continue
    '''
    items = profile.get_all_research_item()
    for item in items:
        if item.get("name", None) == match_log:
            identification_note = item.get("notes", "IDENTIFIED=0")
            if (STATUS_MATCHED in identification_note):
                current_date = int(identification_note.replace(STATUS_MATCHED, ""))
                if datetime.date.today().toordinal() - current_date < threshold: return False
    return True
def record_research_log(profile, match_str, log_id, source_prof, notes_2add):
    '''
    This function will introduce research logs information about the matching
    profile is a profile of pyGenealogy.common_profile type
    '''
    all_items = profile.get_all_research_item()
    all_urls = {}
    for item in all_items:
        all_urls[item["url"]] = item
    if (source_prof in all_urls.keys()):
        profile.update_research_item(log_id, source_prof , source = match_str , result = notes_2add)
    else:
        profile.set_research_item(log_id, repository = source_prof, source = match_str, result = notes_2add)