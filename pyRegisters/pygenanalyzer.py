'''
Created on 28 mar. 2018

@author: Val
'''
from pyRegisters.pyrememori import rememori_reader
from pyRegisters.pyelnortedecastilla import elnortedecastilla_reader
from pyRegisters.pyabc import abc_reader
from pyRegisters.pyesquelas import esquelas_reader
import logging, datetime
from messages.pygenanalyzer_messages import RESEARCH_INFO, RESEARCH_LOG

ALL_PARSERS = ["REMEMORI", "ELNORTEDECASTILLA", "ABC", "ESQUELAS" ]

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
        if not output == None: self.file = open(output, "w")
        print_out("Total number of profiles = " + str(len(profiles)), self.file)
        for person in profiles:
            #Firstly, we need to analyze if we need to add the research log, if does not exist, of course
            log_loc = None
            if storage and (not person.get_specific_research_log(RESEARCH_LOG)):
                log_loc = person.set_task(RESEARCH_LOG, task_type=2, details=RESEARCH_INFO)
            else: log_loc = person.get_specific_research_log(RESEARCH_LOG)
            #Check which analysis will be done
            checks_2_perform = {}
            overall_check = False
            for parser in ALL_PARSERS:
                checks_2_perform[parser] = continue_analysis(person, parser, threshold, log_loc)
                if checks_2_perform[parser]: overall_check = True
            skipping = ""
            if not overall_check: skipping = " -- SKIPPED"
            #Variable for urls in tasks
            self.urls_task = ""
            #We write in the screen the name of the person
            print_out(str(person.get_id()) + " = "  + person.nameLifespan() + skipping, self.file)
            #We accumulate all readers
            readers_2_use = {}
            readers_2_use["REMEMORI"] = rememori_reader(language=self.language, name_convention=self.name_convention)
            readers_2_use["ELNORTEDECASTILLA"] = elnortedecastilla_reader(language=self.language, name_convention=self.name_convention)
            readers_2_use["ABC"] = abc_reader(language=self.language, name_convention=self.name_convention)
            readers_2_use["ESQUELAS"] = esquelas_reader(language=self.language, name_convention=self.name_convention)
            for parser in ALL_PARSERS:
                if checks_2_perform[parser]:
                    records = readers_2_use[parser].profile_is_matched(person)
                    self.result_analyzer(person, records, storage, parser, log_loc)
            #We add a single task for all URLs in the person
            if storage and self.urls_task != "": person.set_task("CHECK WEB REFERENCES ", details = self.urls_task)
        if not self.file == None: self.file.close()
    def result_analyzer(self, person, records, storage, web_site, log_id):
        '''
        Common function between all the functions executed above
        '''
        if records != None:
            for obtained in records:
                if storage: store_url_task_in_db(person, list(obtained.get_all_urls().keys())[0], web_site, log_id)
                self.urls_task += list(obtained.get_all_urls().keys())[0] + "\n"
                print_out("  -  " + obtained.nameLifespan() + "  " + list(obtained.get_all_urls().keys())[0], self.file)
            if len(records) == 0 and storage:
                if not person.getLiving():
                    store_url_task_in_db(person, "Not found in " + web_site, web_site, log_id, notes_toadd="CLOSED")
                    print_out("  -  DISCARDED in " + web_site, self.file)
                else:
                    store_url_task_in_db(person, "Not found in " + web_site, web_site, log_id)
def print_out(message, file):
    '''
    Function to be used for printing
    '''
    logging.info(message)
    if not file == None:
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
    else:
        profile.set_research_item(log_id, repository = url, source = web_site, result = notes_toadd)
def continue_analysis(profile, web_site, threshold, log_loc):
    '''
    This function will say if the web site shall be analyzed or not, in principle
    it should not be analyzed if:
    - It has been confirmed before
    - It has been identified already and the timing threshold has not passed
    '''
    items = profile.get_all_research_item()
    date_last_analysis = 0
    for item in items:
        if item.get("name", None) == web_site:
            identification_note = item.get("notes", "IDENTIFIED=0")
            if ("CONFIRMED" in identification_note) or ("CLOSED" in identification_note)  :
                return False
            if ("IDENTIFIED" in identification_note):
                current_date = int(identification_note.replace("IDENTIFIED=", ""))
                if current_date > date_last_analysis: date_last_analysis=current_date
    #If the last analysis is smaller that then threshold, we continue.
    if datetime.date.today().toordinal() - date_last_analysis < threshold: return False
    return True