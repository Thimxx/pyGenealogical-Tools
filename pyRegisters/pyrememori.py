'''
Created on 16 sept. 2017

@author: Val
'''
import requests, re
from html.parser import HTMLParser
from pyGenealogy.common_profile import gen_profile
from pyGenealogy.gen_utils import get_name_surname_from_complete_name
import datetime
from pyRegisters.pyCommonRegisters import BaseRegister

BASE_REMEMORY = "https://www.rememori.com"
SEARCH_LOCATION = BASE_REMEMORY + "/buscar/que:"
ADDING_CHAR = "%20"
#First dead record in rememory
FIRST_YEAR = 2008


class rememori_reader(BaseRegister):
    '''
    This class analyzes and finds and matches profiles with death records in
    rememory
    '''


    def __init__(self, language = "en", name_convention= "father_surname"):
        '''
        Constructor
        '''
        self.parser = RememoryParser()
        self.person_parser = RememoryPersonParser()
        self.language = language
        self.name_convention = name_convention
        BaseRegister.__init__(self, "REMEMORI", first_year = FIRST_YEAR)
    def profile_is_matched(self, profile):
        '''
        This function will look in rememory trying to match a profile
        Input shall be a profile of common profile values
        It will return an array of matches profiles, an empty array or None if the execution was wrong
        '''
        correct_execution = True
        intermediate_profiles = []
        final_profiles = []
        #Before executing, if the profile is born before any logical date treated in rememory, we stop
        if self.continue_death_register(profile):
            url = SEARCH_LOCATION + profile.getName() + ADDING_CHAR
            url += ADDING_CHAR.join(profile.getSurname().split(" "))
            data = requests.get(url)
            #We add a check in case the server is down, which happens quite oftenly
            if ("502 Server Error" in data.text) : correct_execution = False
            self.parser.feed(data.text)
            #This will remove all those matches that are very unlikely to be part
            for deceased in self.parser.records:
                score, factor = deceased.comparison_score(profile, data_language=self.language, name_convention=self.name_convention)
                if (score*factor > 2.0):
                    intermediate_profiles.append(deceased)
            #As takes a significant amount of time to obtain the profiles, in order to improve performance we get the details
            #only in those more suitable candidates, to reduce the number of html calls that will slow down the calculation
            for selected_profile in intermediate_profiles:
                data = requests.get(list(selected_profile.get_all_urls().keys())[0])
                self.person_parser.feed(data.text)
                if (self.person_parser.age):
                    #As the dates in rememory are exact we can freely do this
                    death = selected_profile.gen_data["death"].get_date()
                    selected_profile.setCheckedDate("birth", death.year - self.person_parser.age, accuracy="ABOUT")
                if (self.person_parser.location):
                    selected_profile.setPlaces("death_place", self.person_parser.location, language="es" )
                #As we have new data, we crosscheck the information to make sure we do not have profiles we should not have
                score, factor = selected_profile.comparison_score(profile, data_language=self.language, name_convention=self.name_convention)
                if (score*factor > 2.0):
                    final_profiles.append(selected_profile)
        if correct_execution : return final_profiles
        else: return None

class RememoryParser(HTMLParser):
    '''
    Parser of HTML that includes all the logic
    '''
    def __init__(self):
        HTMLParser.__init__(self)
        self.inside_results = False
        self.internal_div = 0
        self.records = []
        self.web_link = None
        self.name = None
        self.comments = None
        self.at_name_location = False
        self.at_data_location = False
        self.at_comments_location = False
    def handle_starttag(self, tag, attrs):
        if (tag == "div"):
            for attr in attrs:
                if ("id" in attr) and ("results" in attr):
                    self.inside_results = True
            if (self.inside_results):
                #If we are in and we foudn a new div, we add values
                self.internal_div += 1
        if self.inside_results:
            if (tag == "a"):
                for attr in attrs:
                    if "href" in attr:
                        self.web_link = BASE_REMEMORY + attr[1]
                        self.at_name_location = True
            elif (tag == "span"):
                self.at_data_location = True
            elif (tag == "div"):
                self.at_comments_location = True
    def handle_data(self, data):
        if self.at_name_location:
            self.name = data
            self.at_name_location = False
        elif self.at_data_location:
            if ("Ayer" in data): self.death_date = datetime.datetime.today().date() - datetime.timedelta(days=1)
            elif ("Hoy" in data): self.death_date = datetime.datetime.today().date()
            else:
                self.death_date = datetime.datetime.strptime(data, "%d/%m/%Y").date()
            self.at_data_location = False
        elif self.at_comments_location:
            self.comments = data
            self.at_comments_location = False
    def handle_endtag(self, tag):
        if tag == 'div' and self.inside_results:
            #We closed one of the tags
            if (self.internal_div > 0):
                self.internal_div -= 1
                if (self.internal_div == 0):
                    self.inside_results = False
        if self.inside_results:
            if (tag == "li"):
                name, surname, _ = get_name_surname_from_complete_name(self.name, convention="spanish_surname")
                prof_record = gen_profile(name, surname)
                prof_record.setWebReference(self.web_link)
                prof_record.setCheckedDate("death", self.death_date.year, self.death_date.month,self.death_date.day,"EXACT")
                prof_record.setComments(self.comments)
                self.records.append(prof_record)
class RememoryPersonParser(HTMLParser):
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
        self.location = None
        self.age = None
        self.located = False
    def handle_starttag(self, tag, attrs):
        if tag == "br":
            self.located = True
    def handle_data(self, data):
        if self.located:
            self.located = False
            if (("en" in data) and ("a los" in data)):
                result = re.search('en(.*)a los', data)
                if not (result == None):
                    self.location = result.group(1).strip()
                result = re.search('a los(.*)años', data)
                if not (result == None):
                    age = result.group(1).strip()
                    if age.isdigit(): self.age = int(result.group(1).strip())
            elif ("en" in data):
                self.location = data.split("en",1)[1].strip()
            elif  ("a los" in data) and ("años" in data):
                result = re.search('a los(.*)años', data)
                age = result.group(1).strip()
                if age.isdigit(): self.age = int(result.group(1).strip())
    def handle_endtag(self, tag):
        pass