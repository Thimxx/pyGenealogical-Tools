'''
Created on 1 abr. 2018

@author: Val
'''
import requests, re
from datetime import datetime
from html.parser import HTMLParser
from pyGenealogy.common_profile import gen_profile
from pyGenealogy.gen_utils import get_name_surname_from_complete_name
from pyRegisters.pyCommonRegisters import BaseRegister

BASE_SEARCH = "/buscar?keywords="
END_SEARCH ="&location=&date_limit=&date=&type=all_memorial&_fstatus=search&location_id="
BASE_PERSON = { "ELNORTEDECASTILLA" : "http://esquelas.elnortedecastilla.es",
               "ELCORREO": "https://esquelas.elcorreo.com/",
                "ELDIARIOMONTAÑES" : "https://esquelas.eldiariomontanes.es/",
                "IDEAL" : "https://esquelas.ideal.es/",
                "LARIOJA" : "https://esquelas.larioja.com/"}

#First dead record in Vocento's readers
FIRST_YEAR = 2007

class vocento_reader(BaseRegister):
    '''
    This class analyzes and finds and matches profiles with death records in
    the obituary of the newspapers from Vocento
    '''
    def __init__(self, language = "en", name_convention= "father_surname", reader = "ELNORTEDECASTILLA"):
        '''
        Constructor
        '''
        self.parser = VocentoParser(reader)
        self.language = language
        self.name_convention = name_convention
        self.reader = reader
        BaseRegister.__init__(self, reader, first_year = FIRST_YEAR)
    def profile_is_matched(self, profile):
        '''
        This function will look in El Norte de Castilla trying to match a profile
        Input shall be a profile of common profile values
        '''
        keywords = profile.getName().strip().replace(" ", "+") + "+" + profile.getSurname().strip().replace(" ", "+")
        url = BASE_PERSON[self.reader] + BASE_SEARCH + keywords + END_SEARCH
        final_profiles = []
        if self.continue_death_register(profile):
            data = requests.get(url)
            self.parser.feed(data.text)
            for deceased in self.parser.records:
                skip_profile = False
                if "birth_date" in profile.gen_data:
                    if profile.gen_data["birth_date"].year - deceased.gen_data["death_date"].year > self.maximum_lifespan:
                        skip_profile = True
                if not skip_profile:
                    score, factor = deceased.comparison_score(profile, data_language=self.language, name_convention=self.name_convention)
                    if (score*factor > 2.0):
                        final_profiles.append(deceased)
        #If we do not execute, we also answer with not registers, we are not executing as not relevant.
        return final_profiles
class VocentoParser(HTMLParser):
    '''
    This function will parser an specific individual to extract specific data useful for comparison
    '''
    def __init__(self,reader):
        '''
        As input we intoduce
        reader: the specific vocento reader in place
        '''
        HTMLParser.__init__(self)
        self.reader = reader
        self.inside_profile = False
        self.inside_description = False
        self.inside_citation = False
        self.ending_citation = False
        self.age = None
        self.location = None
        self.name = None
        self.sex = None
        self.weblink = None
        self.comment = None
        self.death_date = None
        self.age_here = False
        self.location_here = False
        self.records = []
    def handle_starttag(self, tag, attrs):
        if (tag == "a"):
            for attr in attrs:
                if ("class" in attr) and ("notice_name_link" in attr):
                    self.inside_profile = True
                    self.inside_citation = True
                elif ("href" in attr) and self.inside_profile:
                    self.weblink = BASE_PERSON[self.reader] + attr[1]
        if (tag == "p"):
            for attr in attrs:
                if ("class" in attr) and ("shortText" in attr):
                    self.inside_description = True
        if (tag == "meta"):
            correct = False
            for attr in attrs:
                if ("itemprop" in attr) and ("datePublished" in attr):
                    correct = True
                    self.ending_citation = True
                if correct and ("content" in attr):
                    self.death_date = datetime.strptime(attr[1], '%Y-%m-%d').date()
    def handle_data(self, data):
        if self.inside_description:
            self.inside_description = False
            result_AGE = re.search('a los (.*) años', data.lower())
            result_LOC = re.search('fallecido en (.*) el día', data.lower())
            if result_AGE:
                self.age_here = True
                self.age = result_AGE.group(1)
            if result_LOC:
                self.location_here = True
                self.location = result_LOC.group(1)
            self.comment = data
        if self.inside_profile:
            self.inside_profile = False
            self.name = data.replace(" : Fallecimiento","").replace("Don ","").replace("Doña ","").replace("D. ","").replace("DON ","").replace("DOÑA ","")
        if self.ending_citation and self.inside_citation:
            name, surname, _ = get_name_surname_from_complete_name(self.name, convention="spanish_surname")
            profile = gen_profile(name, surname)
            profile.setCheckedGender(self.sex)
            profile.setWebReference(self.weblink)
            profile.setComments(self.comment)
            profile.setCheckedDateWithDates("death", self.death_date, "EXACT")
            if (self.age_here):
                self.age_here = False
                #Just in case we have not extracted the right age of the person
                if (self.age.isdigit()):
                    profile.setCheckedDate("birth", self.death_date.year - int(self.age), accuracy = "ABOUT")
            if (self.location_here):
                self.location_here = False
                profile.setPlaces("death", self.location, language="es" )
            self.records.append(profile)
            #We just mark the end of the profile extraction
            self.ending_citation = False
            self.inside_citation = False
    def handle_endtag(self, tag):
        pass  