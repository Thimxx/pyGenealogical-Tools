'''
Created on 1 nov. 2019

@author: Val
'''
from pyRegisters.pyCommonRegisters import BaseRegister
from html.parser import HTMLParser
from pyGenealogy.gen_utils import get_name_surname_from_complete_name
from datetime import datetime
from pyRegisters import sp_age_location_colector
from pyGenealogy.common_profile import gen_profile

BASE_VANGUARDIA = "https://enmemoria.lavanguardia.com/buscar?keywords="
END_VANGUARDIA = "&date_limit=custom&date=&type=all_memorial&_fstatus=search&order_by="

#First dead record in El Norte de Castilla
FIRST_YEAR = 2013

class vanguardia_reader(BaseRegister):
    '''
    This class analyzes and finds and matches profiles with death records in
    the obituary of the online database of LaVanguardia.es
    '''
    def __init__(self, language = "en", name_convention= "father_surname"):
        '''
        Constructor
        '''
        self.parser = VanguardiaParser()
        self.language = language
        self.name_convention = name_convention
        BaseRegister.__init__(self, "LAVANGUARDIA", first_year = FIRST_YEAR)
    def profile_is_matched(self, profile):
        '''
        This function will look in Esquelas website trying to match a profile
        Input shall be a profile of common profile values
        '''
        keywords = profile.getName().strip().replace(" ", "+") + "+" + profile.getSurname().strip().replace(" ", "+")
        keywords = keywords.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
        url = BASE_VANGUARDIA + keywords + END_VANGUARDIA
        return self.perform_match(profile,url)
class VanguardiaParser(HTMLParser):
    '''
    This function will parser an specific individual to extract specific data useful for comparison
    '''
    def __init__(self):
        '''
        As input we intoduce
        profile: a generic profile to be updated
        url: the specific url address
        '''
        HTMLParser.__init__(self)
        self.profiles = []
        self.initiate_data()
    def handle_starttag(self, tag, attrs):
        if tag == "a": 
            for attr in attrs:
                if attr[0] == "class" and attr[1] == "notice_name_link":
                    self.inside_profile = True
                elif attr[0] == "href":
                    self.web_link = "https://enmemoria.lavanguardia.com" + attr[1]
                elif attr[0] == "title":
                    name_data = attr[1].replace("Fallecimiento", "").replace(":","").strip()
                    name, surname, _ = get_name_surname_from_complete_name(name_data, convention="spanish_surname")
                    self.name = name
                    self.surname = surname
        elif tag == "p" and self.inside_profile: self.inside_data = True
        elif tag == "meta" and self.inside_profile: 
            itemprop = None
            content = None
            for attr in attrs:
                if attr[0] == "itemprop": itemprop = attr[1]
                elif attr[0] == "content": content = attr[1]
            if itemprop == "datePublished":
                self.death_date = datetime.strptime(content.strip(),"%Y-%m-%d" )
    def handle_data(self, data):
        if self.inside_data:
            self.location, self.age = sp_age_location_colector(data, detect_lan = True)
            self.inside_data = False
        if "Publicado en EnMemoria" in data: 
            #This means we are at the end of the profile.
            self.inside_profile = False
            prof_record = gen_profile(self.name, self.surname)
            prof_record.setWebReference(self.web_link)
            prof_record.setCheckedDate("death", self.death_date.year, self.death_date.month,self.death_date.day,"EXACT")
            if (self.age):
                prof_record.setCheckedDate("birth", self.death_date.year - self.age, accuracy="ABOUT")
            if (self.location):
                prof_record.setPlaces("death", self.location, language="es" )
            self.profiles.append(prof_record)
            self.initiate_data()
    def handle_endtag(self, tag):
        pass
    def initiate_data(self):
        self.inside_profile = False
        self.inside_data = False
        self.web_link = None
        self.name = None
        self.surname = None
        self.death_date = None
        self.location = None
        self.age = None