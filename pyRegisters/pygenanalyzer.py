'''
Created on 28 mar. 2018

@author: Val
'''
from pyRegisters.pyrememori import rememori_reader
from pyRegisters.pyvocento import vocento_reader, BASE_PERSON
from pyRegisters.pyabc import abc_reader
from pyRegisters.pyesquelas import esquelas_reader
from pyRegisters.pycementry_valencia import valencia_reader
from pyRegisters.pylavanguardia import vanguardia_reader
from pyGenealogy.generic_functions import get_research_log_id
import logging, datetime
from messages.pygenanalyzer_messages import WEB_DETECTED

VOCENTO_PARSERS =  list(BASE_PERSON.keys())
ALL_PARSERS = ["REMEMORI",  "ABC", "ESQUELAS", "CEMENTRY VALENCIA", "LAVANGUARDIA" ] + VOCENTO_PARSERS

class gen_analyzer(object):
    '''
    This class will accept a given GEDCOM file for later on executing all pyRegister modules, final
    output will be a description of potential matches for helping in investigation.
    '''
    def __init__(self, language = "en", name_convention= "father_surname"):
        '''
        We shall introduce teh common database included in all areas
        '''
        self.language = language
        self.name_convention = name_convention
    def execute(self, database, output = None, storage = False, threshold = 360, id_profile = None):
        '''
        This will execute all checkings of data with other sources.
        Database shall be one instance of a database child of common_database
        Output is the optional argument to get the result
        Storage is to store the result in the database
        '''
        if id_profile:
            profiles = [database.get_profile_by_ID(id_profile)]
        else:
            profiles = database.get_all_profiles()
        self.file = None
        if output is not None: self.file = open(output, "w")
        print_out("Total number of profiles = " + str(len(profiles)), self.file)
        for person in profiles:
            #Firstly, we need to analyze if we need to add the research log, if does not exist, of course
            log_loc = get_research_log_id(person, storage = storage)
            #Check which analysis will be done
            checks_2_perform = {}
            overall_check = False
            for parser in ALL_PARSERS:
                checks_2_perform[parser] = continue_analysis(person, parser, threshold, log_loc, self.file)
                if checks_2_perform[parser]: overall_check = True
            skipping = ""
            log_level = 20
            if not overall_check:
                skipping = " -- SKIPPED"
                log_level = 15
            #We write in the screen the name of the person
            print_out(str(person.get_id()) + " = "  + person.nameLifespan() + skipping, self.file, log_level = log_level)
            #Variable for urls in tasks
            self.urls_task = ""
            #We accumulate all readers
            readers_2_use = {}
            readers_2_use["REMEMORI"] = rememori_reader(language=self.language, name_convention=self.name_convention)
            readers_2_use["ABC"] = abc_reader(language=self.language, name_convention=self.name_convention)
            readers_2_use["ESQUELAS"] = esquelas_reader(language=self.language, name_convention=self.name_convention)
            readers_2_use["CEMENTRY VALENCIA"] = valencia_reader(language=self.language, name_convention=self.name_convention)
            readers_2_use["LAVANGUARDIA"] = vanguardia_reader(language=self.language, name_convention=self.name_convention)
            for reader in VOCENTO_PARSERS:
                readers_2_use[reader] = vocento_reader(reader= reader, language=self.language, name_convention=self.name_convention)
            
            for parser in ALL_PARSERS:
                if checks_2_perform[parser]:
                    records = readers_2_use[parser].profile_is_matched(person)
                    self.result_analyzer(person, records, storage, parser, log_loc)
            #We add a single task for all URLs in the person
            if storage and self.urls_task != "": person.set_task("CHECK WEB REFERENCES ", details = self.urls_task)
        if self.file is not None: self.file.close()
    def result_analyzer(self, person, records, storage, web_site, log_id):
        '''
        Common function between all the functions executed above
        '''
        if records is not None:
            for obtained in records:
                is_stored = False
                if storage:
                    is_stored = store_url_task_in_db(person, list(obtained.get_all_urls().keys())[0], web_site, log_id)
                #We add all the identified urls for creating a single task later on
                if is_stored:
                    self.urls_task += list(obtained.get_all_urls().keys())[0] + "\n"
                    print_out("  -  " + obtained.nameLifespan() + "  " + list(obtained.get_all_urls().keys())[0], self.file)
            if len(records) == 0 and storage:
                if not person.getLiving():
                    #If the person is not living and does not appear in the site, there is no option that will appear anymore, we CLOSE
                    store_url_task_in_db(person, "Not found in " + web_site, web_site, log_id, notes_toadd="CLOSED")
                    print_out("  -  DISCARDED in " + web_site, self.file)
                else:
                    #If it is not found, then we keep a record for the future, for continuing reviewing.
                    store_url_task_in_db(person, "Not found in " + web_site, web_site, log_id)
def print_out(message, file, log_level = 20):
    '''
    Function to be used for printing
    '''
    logging.log(log_level ,message)
    if file is not None:
        file.write(message + "\n")
def store_url_task_in_db(profile, url, web_site, log_id, notes_toadd=None):
    '''
    This function will store the url as weblink, and the task to review
    '''
    all_items = profile.get_all_research_item()
    all_urls = {}
    for item in all_items:
        all_urls[item["url"]] = item
    today = datetime.date.today().toordinal()
    if not notes_toadd: notes_toadd = "IDENTIFIED=" + str(today)
    if (url in all_urls.keys()) and (all_urls[url]["notes"] != "CHECKED"):
        profile.update_research_item(log_id, url , result = notes_toadd)
        return True
    #We create a new entry either if does not exists before or is not already existing and appears as CHECKED
    elif (not (url in all_urls.keys())) or (all_urls[url]["notes"] != "CHECKED"):
        profile.set_research_item(log_id, repository = url, source = web_site, result = notes_toadd)
        return True
    return False
def continue_analysis(profile, web_site, threshold, log_loc, file):
    '''
    This function will say if the web site shall be analyzed or not, in principle
    it should not be analyzed if:
    - It has been confirmed before
    - It has been identified already and the timing threshold has not passed
    '''
    checked_found = False
    other_non_checked_found = False
    items = profile.get_all_research_item()
    date_last_analysis = 0
    for item in items:
        if item.get("name", None) == web_site:
            identification_note = item.get("notes", "IDENTIFIED=0")
            #It can be only CLOSED if it was dead and nothing was found, we stop reivew.
            #If it is CONFIRMED, that means that the profile has been confirmed linked to the website.
            if ("CONFIRMED" in identification_note):
                detected = False
                for web in profile.get_all_webs():
                    if web["name"] == web_site: detected = True
                if not detected:
                    profile.setWebReference(item["url"], name=item["name"], notes=WEB_DETECTED)
                #If the citation has not been created before, we create it now
                if not profile.get_citation_with_comments(item["url"]):
                    source_id = profile.get_source_id_ref(web_site)
                    if not source_id:
                        profile.set_source_id(web_site)
                        source_id = profile.get_source_id_ref(web_site)
                    #Now we know source_id, let's introduce the citation
                    profile.set_citation(source_id, details=item["url"])
                    print_out("Introducing citation from " + web_site + " and location = " + item["url"], file)
                return False
            #If closed, the analysis is not longer needed
            if ("CLOSED" in identification_note) and (not profile.getLiving()):
                return False
            #In this case, if closed, is a wrong data introduction. We change to CHECKED
            if ("CLOSED" in identification_note) and (profile.getLiving()):
                checked_found = True
                store_url_task_in_db(profile, item["url"], web_site, log_loc, notes_toadd="CHECKED")
            if ("IDENTIFIED" in identification_note):
                #In case there is somebody with "IDENTFIED" and "Not Found", it means it turned to be death, so we force analysis
                if ( ("Not found in " in item["url"]) and (not profile.getLiving())):
                    return True
                other_non_checked_found = True
                current_date = int(identification_note.replace("IDENTIFIED=", ""))
                if current_date > date_last_analysis: date_last_analysis=current_date
            #In this case, there was before an IDENTIFIED status that we converted to CHECKED.
            if ("CHECKED" in identification_note):
                checked_found = True
    #If we have only the checked status and no other
    if (checked_found and (not other_non_checked_found)):
        #We divide in 2 cases...
        #If the person lives, we need to create a "Not Found" status
        if profile.getLiving():
            store_url_task_in_db(profile, "Not found in " + web_site, web_site, log_loc)
            return False
        else:
            store_url_task_in_db(profile, "Not found in " + web_site, web_site, log_loc, notes_toadd="CLOSED")
            return False
    #If the last analysis is smaller that then threshold, we continue.
    if datetime.date.today().toordinal() - date_last_analysis < threshold: return False
    return True