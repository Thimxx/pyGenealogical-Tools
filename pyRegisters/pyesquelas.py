'''
Created on 15 oct. 2019

@author: Val
'''
import requests,  locale
from datetime import datetime
from pyGenealogy.common_profile import gen_profile
from pyGenealogy.gen_utils import get_name_surname_from_complete_name
from pyRegisters.pyCommonRegisters import BaseRegister
from html.parser import HTMLParser
from pyRegisters import sp_age_location_colector

BASE_ESQUELAS = "https://esquelas.es/search?busqueda="
#First dead record in El Norte de Castilla
FIRST_YEAR = 2010

class esquelas_reader(BaseRegister):
    '''
    This class analyzes and finds and matches profiles with death records in
    the obituary of the online database of Esquelas.es
    '''
    def __init__(self, language = "en", name_convention= "father_surname"):
        '''
        Constructor
        '''
        self.parser = EsquelasParser()
        self.language = language
        self.name_convention = name_convention
        BaseRegister.__init__(self, "ELNORTEDECASTILLA", first_year = FIRST_YEAR)
    def profile_is_matched(self, profile):
        '''
        This function will look in Esquelas website trying to match a profile
        Input shall be a profile of common profile values
        '''
        keywords = profile.getName().strip().replace(" ", "+") + "+" + profile.getSurname().strip().replace(" ", "+")
        keywords = keywords.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
        url = BASE_ESQUELAS + keywords
        final_profiles = []
        if self.continue_death_register(profile):
            data = requests.get(url)
            self.parser.feed(data.text)
            final_profiles = self.matching_profiles(profile, self.parser.profiles)
        return final_profiles
class EsquelasParser(HTMLParser):
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
        self.inside_profile = False
        self.inside_date = False
        self.inside_description = False
        self.profiles = []
        #Data for the extraction
        self.initiate_person_data()
    def handle_starttag(self, tag, attrs):
        if (tag == "h2"):
            self.inside_profile = True
        if (tag == "a") and self.inside_profile:
            for attr in attrs:
                if "href" in attr: self.weblink =  attr[1]
                if "title" in attr: self.name = attr[1]
        if (tag == "span") and self.inside_profile:
            if (attrs[0][1] == "text-info x-2 text-right text-nowrap-1"): self.inside_date = True
            if (attrs[0][1] == "text-muted text-nowrap-1"): self.inside_description = True
    def handle_data(self, data):
        if self.inside_date:
            locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
            self.death_date = datetime.strptime(data,"%d de %B de %Y" )
            self.inside_date = False
        if self.inside_description:
            self.location, self.age = sp_age_location_colector(data)
    def handle_endtag(self, tag):
        if self.inside_description:
            name, surname, _ = get_name_surname_from_complete_name(self.name, convention="spanish_surname")
            profile = gen_profile(name, surname)
            profile.setWebReference(self.weblink)
            profile.setCheckedDate("death", self.death_date.year, self.death_date.month, self.death_date.day, "EXACT")
            if (self.age):
                profile.setCheckedDate("birth", self.death_date.year - self.age, accuracy="ABOUT")
            if (self.location):
                profile.setPlaces("death_place", self.location, language="es" )
            self.inside_description = False
            self.initiate_person_data()
            self.profiles.append(profile)
    def initiate_person_data(self):
        '''
        Function to initiate to None all data
        '''
        self.name = None
        self.weblink = None
        self.death_date = None
        self.location = None
        self.age = None