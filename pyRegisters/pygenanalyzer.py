'''
Created on 28 mar. 2018

@author: Val
'''
from pyRegisters.pyrememori import rememori_reader
from pyRegisters.pyelnortedecastilla import elnortedecastilla_reader
from pyRegisters.pyabc import abc_reader
import logging, datetime

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
            #Check which analysis will be done
            check_rememori = continue_analysis(person, "REMEMORI", threshold)
            check_norte = continue_analysis(person, "ELNORTEDECASTILLA", threshold)
            check_abc = continue_analysis(person, "ABC", threshold)
            skipping = ""
            if (not check_rememori) and (not check_norte) and (not check_abc): skipping = " -- SKIPPED"
            #Variable for urls in tasks
            self.urls_task = ""
            #We write in the screen the name of the person
            print_out(str(person.get_id()) + " = "  + person.nameLifespan() + skipping, self.file)
            #REMEMORI
            if check_rememori:
                reader = rememori_reader(language=self.language, name_convention=self.name_convention)
                records = reader.profile_is_matched(person)
                self.result_analyzer(person, records, storage, "REMEMORI")
            #EL NORTE DE CASTILLA
            if check_norte:
                reader2 = elnortedecastilla_reader(language=self.language, name_convention=self.name_convention)
                records2 = reader2.profile_is_matched(person)
                self.result_analyzer(person, records2, storage, "ELNORTEDECASTILLA")
            #ABC
            if check_abc:
                reader3 = abc_reader(language=self.language, name_convention=self.name_convention)
                records3 = reader3.profile_is_matched(person)
                self.result_analyzer(person, records3, storage, "ABC")
            #We add a single task for all URLs in the person
            if storage and self.urls_task != "": person.set_task("CHECK WEB REFERENCES ", details = self.urls_task)
        if not self.file == None: self.file.close()
    def result_analyzer(self, person, records, storage, web_site):
        '''
        Common function between all the functions executed above
        '''
        if records != None:
            for obtained in records:
                if storage: store_url_task_in_db(person, list(obtained.get_all_urls().keys())[0], web_site)
                self.urls_task += list(obtained.get_all_urls().keys())[0] + "\n"
                print_out("  -  " + obtained.nameLifespan() + "  " + list(obtained.get_all_urls().keys())[0], self.file)
            if len(records) == 0 and storage:
                if not person.getLiving():
                    store_url_task_in_db(person, "Not found in " + web_site, web_site, notes_toadd="CLOSED")
                    print_out("  -  DISCARDED in " + web_site, self.file)
                else:
                    store_url_task_in_db(person, "Not found in " + web_site, web_site)
def print_out(message, file):
    '''
    Function to be used for printing
    '''
    logging.info(message)
    if not file == None:
        file.write(message + "\n")
def store_url_task_in_db(profile, url, web_site, notes_toadd=None):
    '''
    This function will store the url as weblink, and the task to review
    '''
    all_urls = profile.get_all_urls()
    today = datetime.date.today().toordinal()
    if not notes_toadd: notes_toadd = "IDENTIFIED=" + str(today)
    if (url in all_urls.keys()) and (all_urls[url]["notes"] != "CHECKED"):
        profile.update_web_ref(url,  notes = notes_toadd)
    else:
        profile.setWebReference(url, name=web_site, notes=notes_toadd)
def continue_analysis(profile, web_site, threshold):
    '''
    This function will say if the web site shall be analyzed or not
    '''
    webs = profile.get_all_webs()
    date_last_analysis = 0
    for web in webs:
        if web.get("name", None) == web_site:
            identification_note = web.get("notes", "IDENTIFIED=0")
            if ("CONFIRMED" in identification_note) or ("CLOSED" in identification_note)  :
                return False
            if ("IDENTIFIED" in identification_note):
                date_last_analysis = int(identification_note.replace("IDENTIFIED=", ""))
    #If the last analysis is smaller that then threshold, we continue.
    if datetime.date.today().toordinal() - date_last_analysis < threshold: return False
    return True