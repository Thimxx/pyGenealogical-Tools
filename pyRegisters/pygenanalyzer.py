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
    def execute(self, database, output = None, storage = False, threshold = 360):
        '''
        This will execute all checkings of data with other sources.
        Database shall be one instance of a database child of common_database
        Output is the optional argument to get the result
        Storage is to store the result in the database
        '''
        profiles = database.get_all_profiles()
        self.file = None
        if not output == None: self.file = open(output, "w")
        print_out("Total number of profiles = " + str(len(profiles)), self.file)
        for person in profiles:
            #Variable for urls in tasks
            urls_task = ""
            #We write in the screen the name of the person
            print_out(str(person.get_id()) + " = "  + person.nameLifespan(), self.file)
            #REMEMORI
            if continue_analysis(person, "REMEMORI", threshold):
                reader = rememori_reader(language=self.language, name_convention=self.name_convention)
                records = reader.profile_is_matched(person)
                #Sometimes Rememori fails in a regular manner,a checking has been introduced.
                if records:
                    for obtained in records:
                        if storage: store_url_task_in_db(person, obtained.get_all_urls()[0], "REMEMORI")
                        urls_task += obtained.get_all_urls()[0] + "\n"
                        print_out("  -  " + obtained.nameLifespan() + "  " + obtained.get_all_urls()[0], self.file)
                    if len(records) == 0 and not person.getLiving() and storage:
                        person.setWebReference("Not found in REMEMORI", name="REMEMORI", notes="CLOSED")
            #EL NORTE DE CASTILLA
            if continue_analysis(person, "ELNORTEDECASTILLA", threshold):
                reader2 = elnortedecastilla_reader(language=self.language, name_convention=self.name_convention)
                records2 = reader2.profile_is_matched(person)
                for obtained in records2:
                    if storage: store_url_task_in_db(person, obtained.get_all_urls()[0], "ELNORTEDECASTILLA")
                    urls_task += obtained.get_all_urls()[0] + "\n"
                    print_out("  -  " + obtained.nameLifespan() + "  " + obtained.get_all_urls()[0], self.file)
                    if len(records2) == 0 and not person.getLiving() and storage:
                        person.setWebReference("Not found in ELNORTEDECASTILLA", name="ELNORTEDECASTILLA", notes="CLOSED")
            #ABC
            if continue_analysis(person, "ABC", threshold):
                reader3 = abc_reader(language=self.language, name_convention=self.name_convention)
                records3 = reader3.profile_is_matched(person)
                for obtained in records3:
                    if storage: store_url_task_in_db(person, obtained.get_all_urls()[0], "ABC")
                    urls_task += obtained.get_all_urls()[0] + "\n"
                    print_out("  -  " + obtained.nameLifespan() + "  " + obtained.get_all_urls()[0], self.file)
                    if len(records3) == 0 and not person.getLiving() and storage:
                        person.setWebReference("Not found in ABC", name="ABC", notes="CLOSED")
            #We add a single task for all URLs in the person
            if storage and urls_task != "": person.set_task("CHECK WEB REFERENCES ", details = urls_task)
        if not self.file == None: self.file.close()
def print_out(message, file):
    '''
    Function to be used for printing
    '''
    logging.info(message)
    if not file == None:
        file.write(message + "\n")
def store_url_task_in_db(profile, url, web_site):
    '''
    This function will store the url as weblink, and the task to review
    '''
    today = datetime.date.today().toordinal()
    notes_toadd = "IDENTIFIED=" + str(today)
    if url in profile.get_all_urls():
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
            date_last_analysis = int(identification_note.replace("IDENTIFIED=", ""))
    #If the last analysis is smaller that then threshold, we continue.
    if datetime.date.today().toordinal() - date_last_analysis < threshold: return False
    return True
        
    