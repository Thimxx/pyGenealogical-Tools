'''
Created on 1 abr. 2018

@author: Val
'''
import requests, re
from datetime import datetime, date
from html.parser import HTMLParser
from pyGenealogy.common_profile import gen_profile
from pyGenealogy.gen_utils import get_name_surname_from_complete_name

BASE_NORTE = "http://esquelas.elnortedecastilla.es/buscar?keywords="
END_NORTE ="&location=&date_limit=&date=&type=all_memorial&_fstatus=search&location_id="
BASE_PERSON = "http://esquelas.elnortedecastilla.es"

#Maximum life span of a person
MAXIMUM_LIFESPAN = 123

class elnortedecastilla_reader(object):
    '''
    This class analyzes and finds and matches profiles with death records in
    the obituary of the newspaper El Norte de Castilla
    '''
    def __init__(self, language = "en", name_convention= "father_surname"):
        '''
        Constructor
        '''
        self.parser = NorteCastillaParser()
        self.language = language
        self.name_convention = name_convention
    def profile_is_matched(self, profile):
        '''
        This function will look in El Norte de Castilla trying to match a profile
        Input shall be a profile of common profile values
        '''
        keywords = profile.gen_data["name"].strip().replace(" ", "+") + "+" + profile.gen_data["surname"].strip().replace(" ", "+")
        url = BASE_NORTE + keywords + END_NORTE
        data = requests.get(url)
        self.parser.feed(data.text)
        final_profiles = []
        for deceased in self.parser.records:
            skip_profile = False
            if "birth_date" in profile.gen_data:
                if profile.gen_data["birth_date"].year - deceased.gen_data["death_date"].year > MAXIMUM_LIFESPAN:
                    skip_profile = True
            if not skip_profile:
                score, factor = deceased.comparison_score(profile, data_language=self.language, name_convention=self.name_convention)
                if (score*factor > 2.0):
                    final_profiles.append(deceased)
        return final_profiles
class NorteCastillaParser(HTMLParser):
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
                    self.weblink = BASE_PERSON + attr[1]
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
            result_M = re.search(' (.*) :', data)
            result_F = re.search(' (.*) :', data)
            if (result_M):
                self.sex = "M"
                self.name = result_M.group(1)
            else:
                self.sex = "F"
                self.name = result_F.group(1)
        if self.ending_citation and self.inside_citation:
            name, surname, _ = get_name_surname_from_complete_name(self.name, convention="spanish_surname")
            profile = gen_profile(name, surname)
            profile.setCheckedGender(self.sex)
            profile.setWebReference(self.weblink)
            profile.setComments(self.comment)
            profile.setCheckedDate("death_date", self.death_date, "EXACT")
            if (self.age_here):
                self.age_here = False
                #Just in case we have not extracted the right age of the person
                if (self.age.isdigit()):
                    birth = date(self.death_date.year - int(self.age),1,1)
                    profile.setCheckedDate("birth_date", birth, "ABOUT")
            if (self.location_here):
                self.location_here = False
                profile.setPlaces("death_place", self.location, language="es" )
            self.records.append(profile)
            #We just mark the end of the profile extraction
            self.ending_citation = False
            self.inside_citation = False
    def handle_endtag(self, tag):
        pass  