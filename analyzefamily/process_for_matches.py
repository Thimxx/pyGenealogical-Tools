'''
Created on 28 jul. 2019

@author: Val
'''
import datetime
from messages.pygenanalyzer_messages import PROCESS_MATCH_NUMBER_OF_IMPACTS_BEGIN, PROCESS_MATCH_NUMBER_OF_IMPACTS_END, MATCH_POTENTIAL_EXISTING, MATCH_POTENTIAL_INFO_EXISTING
from messages.pygenanalyzer_messages import PROCESS_ADD_PROFILE_BEGIN, PROCESS_ADD_PROFILE_END, MATCH_ADDING_PROFILES, MATCH_POTENTIAL_DUPLICATE
from messages.pygenanalyzer_messages import PROCESS_TASK_NAME, PROCESS_TASK_DETAILS, PROCESS_NO_ACCESS, MATCH_EXISTING_PROFILES, PROCESS_LINK_PROFILE_BEGIN
from analyzefamily.matcher_geni_profile import match_single_profile
from analyzefamily import CHILD, continue_execution_step, record_research_log
from messages import AND_STRING, TO_STRING
from pyGenealogy.generic_functions import get_research_log_id
from analyzefamily import include_task_no_duplicate, include_match_profile, print_out
from pyGenealogy import NOT_KNOWN_VALUE

MATCH = "_MATCH"
STATUS_MATCHED = "MATCHED="
STATUS_TO_CHECK = "CHECK "

FACTOR_DUPLICATE = 10.0

class process_a_db(object):
    '''
    This class will take a database and will process it analyzing with the different databases
    already available in the code
    '''
    def __init__(self, db_input, db_check, data_language="en", name_convention="father_surname",
                 event_year_task = None):
        '''
        Constructor
        .
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
                if continue_execution_step(prof_in_study, match_str, STATUS_MATCHED, threshold = threshold):
                    prof_linked_id = prof_in_study.get_specific_web(kind_match)["url"]
                    prof_linked = self.db_check.get_profile_by_ID(prof_linked_id)
                    #In order to get the marriage, first we get the family from the other database
                    _, family_profile = self.db_check.get_family_from_child(prof_linked.get_id())
                    _, family_input = self.db_input.get_family_from_child(prof_id)
                    #We will only analyze the profiles which have been introduced
                    loc_research = get_research_log_id(prof_in_study, storage = storage)
                    non_matched_profiles_input, non_matched_profiles_check, conflict_profiles, matched_profiles = matcher_profiles.match(prof_id)
                    #We create the following slots that will be used for the introduction of confirmed candidates inside the database
                    check_non_matches_existing_in_input = {}
                    input_non_matches_existing_in_check = {}
                    #REMOVAL OF LIVING
                    #If the option is selected to not publish data that is restricted like living we remove teh matched characters
                    temp_data = {"input" :
                                    {"non_matches": non_matched_profiles_input,
                                     "database":self.db_input, "other_db": self.db_check,
                                     "family_is_child": family_input,
                                     "current_id_to_add": prof_linked_id,
                                     "current_id_matched": prof_id,
                                     "existing_prof": input_non_matches_existing_in_check},
                                 "check" :
                                    {"non_matches": non_matched_profiles_check,
                                     "database":self.db_check, "other_db": self.db_input,
                                     "family_is_child": family_profile,
                                     "current_id_to_add": prof_id,
                                     "current_id_matched": prof_linked.get_id(),
                                     "existing_prof": check_non_matches_existing_in_input }}
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
                        #Profiles might have been matched before
                        Existing_found = False
                        duplicate_names =""
                        for candidate_prof in matches.keys():
                            existing_prof = self.db_input.get_profile_by_ID(candidate_prof)
                            if (existing_prof.getName() != NOT_KNOWN_VALUE) and (existing_prof.getSurname() != NOT_KNOWN_VALUE):
                                #We only continue looking for alternatives if there is no uncertain information int he profile
                                duplicate_names += existing_prof.nameLifespan() + " "
                                for web_data in existing_prof.get_all_webs():
                                    #We now know that the profiles are the same in this database, we can proceed to add this existing one
                                    if web_data["url"] == potential_profile.get_this_profile_url():
                                        #We store the link of a profile id in check to a profile existing in input (profile class)
                                        check_non_matches_existing_in_input[prof] = existing_prof
                                        Existing_found = True
                                if matches[candidate_prof]["score*factor"]>= FACTOR_DUPLICATE:
                                    check_non_matches_existing_in_input[prof] = existing_prof
                                    Existing_found = True
                        if (len(matches.keys()) > 0) and not Existing_found:
                            #In this case we have a certain potential match. We should not add and rather, leave for checking an human being
                            del non_matched_profiles_check[prof]
                            print_out("-    POTENTIAL DUPLICATE of profile " + str(potential_profile.nameLifespan()) +
                                " WITH PROFILE(S) ID(S) " + str(duplicate_names))
                            #This is a conflict, we should avoid duplicating job of checking and solving
                            conflict_profiles[prof] = matches
                            details_info = ("Potential existing duplicates for profile " + potential_profile.nameLifespan() +
                                            " with web " + potential_profile.get_this_profile_url() + " in the profiles:      ")
                            for ids_check in matches:
                                temp_prof = self.db_input.get_profile_by_ID(ids_check)
                                details_info += str(ids_check) + " : " + temp_prof.nameLifespan() + "        "
                            include_task_no_duplicate(prof_in_study, MATCH_POTENTIAL_DUPLICATE, 1, details_info)
                    ###################
                    #MATCH INTRODUCTION
                    ###################
                    for db_kind in temp_data:
                        #CASE MATCH: Missing a parents or several parents.
                        non_match_now = temp_data[db_kind]["non_matches"]
                        db_now = temp_data[db_kind]["database"]
                        db_other = temp_data[db_kind]["other_db"]
                        family_is_child = temp_data[db_kind]["family_is_child"]
                        current_id_to_add = temp_data[db_kind]["current_id_to_add"]
                        if( ("father" in non_match_now.values()) or ("mother" in non_match_now.values())):
                            father_id = None
                            mother_id = None
                            father_profile = None
                            mother_profile = None
                            #We shall first obtain the id of the profiles from the check database (i.e. geni)
                            if ("father" in non_match_now.values()):
                                father_id = list(non_match_now.keys())[list(non_match_now.values()).index("father")]
                                father_profile = db_now.get_profile_by_ID(father_id)
                            if ("mother" in non_match_now.values()):
                                mother_id = list(non_match_now.keys())[list(non_match_now.values()).index("mother")]
                                mother_profile = db_now.get_profile_by_ID(mother_id)
                            Intro_sentence = MATCH_ADDING_PROFILES
                            if (father_id in temp_data[kind_db]["existing_prof"]) or (mother_id in temp_data[kind_db]["existing_prof"]):
                                Intro_sentence = MATCH_EXISTING_PROFILES
                            #We also add the link!
                            if father_profile and mother_profile:
                                Intro_sentence += father_profile.nameLifespan() + AND_STRING + mother_profile.nameLifespan() + TO_STRING + db_other.get_db_kind()
                            elif father_profile:
                                Intro_sentence += father_profile.nameLifespan() + TO_STRING + db_other.get_db_kind()
                            elif mother_profile:
                                Intro_sentence += mother_profile.nameLifespan() + TO_STRING + db_other.get_db_kind()
                            #We inform of the inclusion of the new profiles
                            print_out(Intro_sentence )
                            marriage_event = family_is_child.getMarriage()
                            #If the parent was existing before, we avoid double introduction
                            father_to_add = temp_data[kind_db]["existing_prof"].get(father_id, father_profile)
                            mother_to_add = temp_data[kind_db]["existing_prof"].get(mother_id, mother_profile)
                            if father_to_add and mother_to_add:
                                #So.. we add the new profiles
                                new_father_id, new_mother_id, _ = db_other.add_parents(child_profile_id = current_id_to_add, father_profile = father_to_add,
                                            mother_profile= mother_to_add, marriage_event= marriage_event)
                            elif father_to_add:
                                #So.. we just add the father
                                new_father_id, new_mother_id, _ = db_other.add_parents(child_profile_id = current_id_to_add, father_profile = father_to_add,
                                            marriage_event= marriage_event)
                            elif mother_to_add:
                                #So.. we just add the father
                                new_father_id, new_mother_id, _ = db_other.add_parents(child_profile_id = current_id_to_add, mother_profile= mother_to_add,
                                            marriage_event= marriage_event)
                            if db_kind == "check":
                                if father_profile: self.add_match_to_prof(new_father_id, father_profile)
                                if mother_profile: self.add_match_to_prof(new_mother_id, mother_profile)
                            #We remove the profiles, as will be added
                            if father_id: del non_match_now[father_id]
                            if mother_id: del non_match_now[mother_id]
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
                            #We might delete some profiles (children) in the middle, that's why we check first if the profile is in the list
                            if (prof in temp_data[kind_db]["non_matches"]) and temp_data[kind_db]["non_matches"][prof] == "partner":
                                partner_profile = temp_data[kind_db]["database"].get_profile_by_ID(prof)
                                #Checking is already having a link to the database
                                existing_link = self.get_existing_before(partner_profile, self.db_check.get_db_kind(), prof_id)
                                #Now, if the partner is not accessible due to data restriction, we will skip this step
                                if partner_profile.get_accessible() and not existing_link:
                                    #Good, we will need now to add the new partner to the INPUT area
                                    Intro_sentence = PROCESS_ADD_PROFILE_BEGIN
                                    if prof in temp_data[kind_db]["existing_prof"]: Intro_sentence = PROCESS_LINK_PROFILE_BEGIN
                                    print_out(Intro_sentence + partner_profile.nameLifespan() + TO_STRING +
                                           temp_data[kind_db]["other_db"].get_db_kind() + PROCESS_ADD_PROFILE_END + temp_data[kind_db]["non_matches"][prof] )
                                    family_check = temp_data[kind_db]["database"].get_family_from_partners(temp_data[kind_db]["current_id_matched"],
                                                                                                       partner_profile.get_id())
                                    marriage_event = temp_data[kind_db]["database"].get_family_by_ID(family_check).getMarriage()
                                    #The profile might be existing before and we do not need to add it again, so we have a potential deviation
                                    #If we store it before, in this case, we will use the existing profile, if not, we continue we the one in the other database
                                    partner_to_introduce = temp_data[kind_db]["existing_prof"].get(prof, partner_profile)
                                    id_partner, _ = temp_data[kind_db]["other_db"].add_partner(temp_data[kind_db]["current_id_to_add"],
                                                                                           partner_to_introduce, marriage = marriage_event)
                                    if kind_db == "input":
                                        self.add_match_to_prof(prof, temp_data[kind_db]["other_db"].get_profile_by_ID(id_partner), adding = False)
                                        matched_partners[prof] = id_partner
                                    elif kind_db == "check":
                                        self.add_match_to_prof(id_partner, partner_profile)
                                        matched_partners[id_partner] = prof
                                elif not partner_profile.get_accessible():
                                    print_out("-    AVOIDING INTRODUCTION OF LIVING "+ str(partner_profile.nameLifespan()) +
                                              " FROM THE DATABASE " + temp_data[kind_db]["database"].get_db_kind())
                                    family_eliminate = temp_data[kind_db]["database"].get_family_from_partners(
                                        temp_data[kind_db]["current_id_matched"], partner_profile.get_id() )
                                    #As the partner is not known and we might have access issues,
                                    #we stop the review of those children in the non accesible partner
                                    for child in family_eliminate.getChildren():
                                        if child in temp_data[kind_db]["non_matches"]:
                                            del temp_data[kind_db]["non_matches"][child]
                                #We remove also from the non-matching pending those profiles that have been skipped due to privacy
                                if not existing_link: del temp_data[kind_db]["non_matches"][partner_profile.get_id()]
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
                                        Intro_sentence = PROCESS_ADD_PROFILE_BEGIN
                                        if prof in temp_data[kind_db]["existing_prof"]: Intro_sentence = PROCESS_LINK_PROFILE_BEGIN
                                        print_out(Intro_sentence + child_profile.nameLifespan() + TO_STRING +
                                             temp_data[kind_db]["other_db"].get_db_kind() + PROCESS_ADD_PROFILE_END +
                                             temp_data[kind_db]["non_matches"][prof])
                                        #If the child was existing before, we add it directly with the right profile, avoiding double introduction
                                        child_to_add = temp_data[kind_db]["existing_prof"].get(prof, child_profile)
                                        child_new_ids = temp_data[kind_db]["other_db"].add_child(family_part[kind_db], [child_to_add] )
                                        if kind_db == "input":
                                            child_new_prof = self.db_check.get_profile_by_ID(child_new_ids[0])
                                            self.add_match_to_prof(prof, child_new_prof, adding = False)
                                        elif kind_db == "check":
                                            self.add_match_to_prof(child_new_ids[0], child_profile)
                                    else:
                                        print_out(child_profile.nameLifespan() +PROCESS_NO_ACCESS)
                                    del temp_data[kind_db]["non_matches"][prof]
                    ################################################################
                    # Case of profiles missing one of the parents
                    ################################################################
                    for db_kind in temp_data:
                        #CASE MATCH: Missing a parents or several parents.
                        non_match_now = temp_data[db_kind]["non_matches"]
                        for missing_match in non_match_now:
                            #Firstly we define the different databases
                            db_origin = temp_data[db_kind]["database"]
                            db_destination = temp_data[db_kind]["other_db"]
                            #Now, we take the profile which is missing
                            prof_origin = db_origin.get_profile_by_ID(missing_match)
                            #This is going of check if the parent of the child is today included in the conflict list, and avoid including the children until is fixed
                            child_from_non_mathced_partner = any(x in conflict_profiles.keys() for x in db_origin.get_parents_from_child(missing_match)[0])
                            if (non_match_now[missing_match] == CHILD) and (not child_from_non_mathced_partner) :
                                #Parent that will receive the child
                                prof_parent = db_destination.get_profile_by_ID(temp_data[db_kind]["current_id_to_add"])
                                added_childs = db_destination.add_child_no_family(prof_parent, [prof_origin])
                                #Informing of the creation of hte profile
                                Intro_sentence = PROCESS_ADD_PROFILE_BEGIN
                                print_out(Intro_sentence + prof_origin.nameLifespan() + TO_STRING +
                                             temp_data[kind_db]["other_db"].get_db_kind() + PROCESS_ADD_PROFILE_END + CHILD)
                                if db_kind == "input":
                                    child_new_prof = self.db_check.get_profile_by_ID(added_childs[0])
                                    self.add_match_to_prof(missing_match, child_new_prof, adding = False)
                                elif db_kind  == "check":
                                    self.add_match_to_prof(added_childs[0], prof_origin)
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
    def add_match_to_prof(self, prof_id, profile_to_match, adding = True):
        '''
        It will add the match to the profile id and also a task to review depending on options, notice that
        we assume that only task will be included in "input" database
        prof_id shall be the profile in input database by ID
        profile_to_match shall be the profile of pyGenealogy.common_profile derived class
        '''
        profile = self.db_input.get_profile_by_ID(prof_id)
        include_match_profile(profile, profile_to_match, self.db_check.get_db_kind(), self.db_check)
        #We also need to introduce the matching of tasks
        if self.event_year_task and adding:
            #We only enter if the data has been introduced
            details = ""
            for event in profile.getEvents():
                #We will only look task, if there is a date, if the date greater than the threshold and if has an accurracy allowing the analysis
                if event.get_year() and (event.get_year() >= self.event_year_task) and (event.get_accuracy() not in ["AFTER", "BEFORE"]):
                    details += PROCESS_TASK_DETAILS + str(event.get_event_type()) + "/n"
            if details != "":
                include_task_no_duplicate(profile, PROCESS_TASK_NAME, 1, details)
    def get_existing_before(self, profile_to_check, link_string, prof_id):
        '''
        This function will detect if the profile has a link existing before
        it will create a task informing that profile should not be avoided
        '''
        #We first get all webs of the current profile
        current_webs = profile_to_check.get_all_webs()
        for web in current_webs:
            #This will mean that we have an existing match before
            if web["name"] == link_string:
                profile = self.db_input.get_profile_by_ID(prof_id)
                details = MATCH_POTENTIAL_INFO_EXISTING + profile_to_check.nameLifespan() + " " + str(profile_to_check.get_id())
                include_task_no_duplicate(profile, MATCH_POTENTIAL_EXISTING, 1, details)
                print_out("-    AVOIDING INTRODUCTION OF EXISTING LINK IN "+ str(profile_to_check.nameLifespan()) )
                return True
        return False
def continue_match(profile, match_log, threshold = 360):
    ''''
    This function will confirm if match should or not continue
    match_log is the matching string to be used
    threshold is the number of minimum days to repeat the check
    '''
    item = profile.get_research_item_by_name(match_log)
    if item:
        identification_note = item.get("notes", "IDENTIFIED=0")
        if (STATUS_MATCHED in identification_note):
            current_date = int(identification_note.replace(STATUS_MATCHED, ""))
            if datetime.date.today().toordinal() - current_date < threshold: return False
    return True