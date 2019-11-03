'''
Created on 17 oct. 2019

@author: Val
'''

from pyRegisters.pyCommonRegisters import BaseRegister
from html.parser import HTMLParser
from datetime import datetime
from pyGenealogy.common_profile import gen_profile

FIRST_YEAR = 1849

DIRECT_LINK = "http://www.valencia.es/ayuntamiento/cementerios.nsf/"
INIT_ADDRESS = DIRECT_LINK + "fResultadoBusquedaCementerios?ReadForm=&lang=1&nivel=3&bdURL=ayuntamiento%2Fcementerios.nsf&pg=PXMLCE01&fc=FC0&pr=&wd=&idioma=C&apellido1="
LINK_SURNAME = "&apellido2="
LINK_NAME = "&nombre="
END_ADDRESS = "&anodef=&Buscar.x=28&Buscar.y=14&envio=0"

class valencia_reader(BaseRegister):
    '''
    This class analyzes and finds and matches profiles with death records in
    the database of the cementry of Valencia
    '''


    def __init__(self, language = "en", name_convention= "father_surname"):
        '''
        Constructor
        '''
        self.parser = CementryValenciaParser()
        self.language = language
        self.name_convention = name_convention
        BaseRegister.__init__(self, "CEMENTRY VALENCIA", first_year = FIRST_YEAR)
    def profile_is_matched(self, profile):
        '''
        This function will look in Valencia cementry website trying to match a profile
        Input shall be a profile of common profile values
        '''
        name = profile.getName().replace(" ","+")
        surname1 = profile.getSurname().split(" ")[0]
        surname2 = "+".join(profile.getSurname().split(" ")[1:])
        url = INIT_ADDRESS + surname1 + LINK_SURNAME + surname2 + LINK_NAME + name + END_ADDRESS
        return self.perform_match(profile,url)
class CementryValenciaParser(HTMLParser):
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
        #Data for the extraction
        self.initiate_person_data()
        self.profiles = []
    def handle_starttag(self, tag, attrs):
        if tag == "li":
            for attr in attrs:
                if (attr[0] == "class") and(attr[1] == "circulo"): self.inside_profile = True
        if tag == "span" and self.inside_profile: self.counter += 1
        if tag == "a" and self.counter == 1:
            for att in attrs:
                if att[0] == "href":
                    self.web_ref = DIRECT_LINK + att[1]
    def handle_data(self, data):
        if self.counter == 1:
            content = data.split(" ")
            self.surname1 = content[0]
            self.surname2 = content[1]
            self.name = (" ").join(content[2:])
        if self.counter == 2:
            value_date = data.strip().split(":")[1].strip()
            if len(value_date) > 6:
                self.death_date = datetime.strptime(value_date, "%d-%m-%Y")
    def handle_endtag(self, tag):
        if tag == "li" and self.inside_profile: self.inside_profile = False
        if self.counter == 3:
            profile = gen_profile(self.name.title().strip(), self.surname1.title().strip() + " " + self.surname2.title().strip())
            if self.web_ref: profile.setWebReference(self.web_ref)
            else: profile.setWebReference("Not available for : " + self.name+ " " + self.surname1 + " " + self.surname2)
            if self.death_date: profile.setCheckedDate("death", self.death_date.year, self.death_date.month, self.death_date.day, "EXACT")
            self.profiles.append(profile)
            self.initiate_person_data()
    def initiate_person_data(self):
        '''
        Function to initiate to None all data
        '''
        self.inside_profile = None
        self.counter = 0
        self.surname1 = None
        self.surname2 = None
        self.name = None
        self.web_ref = None
        self.death_date = None