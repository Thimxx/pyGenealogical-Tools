__all__ = ["ancerstors_climb", "matcher_geni_profile", "process_for_matches"]

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
    saving_file = open(location, "w")
def print_out(message, log_level = 20):
    '''
    Function to be used for printing the obtained results
    '''
    global saving_file
    logging.log(log_level ,message)
    if saving_file and log_level >= logging.getLogger().getEffectiveLevel():
        saving_file.write(message + "\n")
def include_match_profile(profile, profile_to_match, kind_db):
    '''
    This function will introduce a match of the profile with another database
    '''
    url_link = profile_to_match.get_this_profile_url()
    #This will be inormation about the match profil
    notes_to_add = MATCH_GENI + datetime.date.today().strftime("%d-%m-%Y")
    #Prior to add, we need to check is not today in the profile
    existing = False
    previous_match = False
    all_matches = [url_link]
    webs = profile.get_all_webs()
    for web in webs:
        if web["url"] == url_link: existing = True
        elif (web["name"] ==  kind_db) and (web["url"] != url_link):
                previous_match = True
                all_matches.append(web["url"])
    #If it has not been created before, we create the new match in the profile
    if not existing:
        profile.setWebReference(url_link, name=kind_db, notes=notes_to_add)
        print_out("-    MATCHED :" + str(profile.nameLifespan()) + " WITH " + str(profile_to_match.nameLifespan()))
    #If there was a different previous match, we shall inform in the profile for checking
    if previous_match:
        include_task_no_duplicate(profile, MATCH_REVIEW_TASK_BEGIN + kind_db + MATCH_REVIEW_TASK_END,
            1, details=MATCH_REVIEW_DETAILS + str(all_matches))