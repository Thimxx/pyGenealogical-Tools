__all__ = ["ancerstors_climb", "matcher_geni_profile", "process_for_matches", "quality_check", "sync_profile"]

import datetime, logging
from messages.pygenanalyzer_messages import MATCH_GENI
from messages.pygenanalyzer_messages import MATCH_REVIEW_TASK_BEGIN, MATCH_REVIEW_TASK_END, MATCH_REVIEW_DETAILS

FATHER = "father"
MOTHER = "mother"
CHILD = "child"
PARTNER = "partner"

saving_file = None


def include_task_no_duplicate(profile, task_details, priority, details):
    '''
    It will include a task in the profile avoiding to duplicate the already existing tasks
    '''
    new_task = {}
    new_task["task_details"] = task_details
    new_task["priority"] = priority
    new_task["details"] = details
    introduce_task = True
    for task in profile.get_all_tasks():
        if new_task == task: introduce_task = False
    if introduce_task: profile.set_task(task_details, priority=priority, details= details, task_type = 0)
def set_file(location):
    global saving_file
    saving_file = open(location, "w", encoding="utf-8")
def print_out(message, log_level = 20):
    '''
    Function to be used for printing the obtained results
    '''
    global saving_file
    logging.log(log_level ,message)
    if saving_file and log_level >= logging.getLogger().getEffectiveLevel():
        saving_file.write(message + "\n")
def include_match_profile(profile, profile_to_match, kind_db, db_match):
    '''
    This function will introduce a match of the profile with another database
    - profile: will be the profile where the link will be included
    - profile_to_match: will be the profile which will be linked.
    - kind_db: is the link to the kind of match.
    - db_match: is the db to match to check the current value
    '''
    url_link = profile_to_match.get_this_profile_url()
    #This will be information about the match profil
    notes_to_add = MATCH_GENI + datetime.date.today().strftime("%d-%m-%Y")
    #Prior to add, we need to check is not today in the profile
    existing = False
    previous_match = False
    all_matches = [url_link]
    webs = profile.get_all_webs()
    for web in webs:
        if web["url"] == url_link: existing = True
        elif (web["name"] ==  kind_db) and (web["url"] != url_link):
                #We need to check if we have the same profile, as the url might change during time!!!
                #First we get the profile that we have already in the link
                profile_already_matched = db_match.get_profile_by_ID(web["url"])
                #We compare the link existing with the new one
                if url_link == profile_already_matched.get_this_profile_url():
                    #In this case we need to update the existing link with the new data
                    profile.update_web_ref(url = url_link, name = kind_db)
                    #In this case this is existing... but we updat
                    existing = True
                else:
                    #In this case we have a previous match which is not the same profile
                    previous_match = True
                    all_matches.append(web["url"])
    #If it has not been created before, we create the new match in the profile
    if not existing:
        profile.setWebReference(url_link, name=kind_db, notes=notes_to_add)
        print_out("-    MATCHED :" + str(profile.nameLifespan()) + " WITH " + str(profile_to_match.nameLifespan()))
    #If there was a different previous match, we shall inform in the profile for checking
    if previous_match:
        #Ok, we have
        include_task_no_duplicate(profile, MATCH_REVIEW_TASK_BEGIN + kind_db + MATCH_REVIEW_TASK_END,
            1, details=MATCH_REVIEW_DETAILS + str(all_matches))
def continue_execution_step(profile, match_log, status_id, threshold = 360):
    ''''
    This method will confirm if the function shall continue or not depending if it has been
    previously executed and the given threshold
    prof is the profile with the match
    match_str is the matching string for comparing with the database
    status_id is the internal code used for executing the given function
    threshold is the number of days which once passed it shall be repeated
    '''
    item = profile.get_research_item_by_name(match_log)
    if item:
        identification_note = item.get("notes", "IDENTIFIED=0")
        if (status_id in identification_note):
            current_date = int(identification_note.replace(status_id, ""))
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