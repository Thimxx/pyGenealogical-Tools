'''
Created on 16 sept. 2017

@author: Val
'''
import requests
from html.parser import HTMLParser
from pyGenealogy.common_profile import gen_profile
from pyGenealogy.gen_utils import get_name_surname_from_complete_name
from datetime import date
import datetime

BASE_REMEMORY = "https://www.rememori.com"
SEARCH_LOCATION = BASE_REMEMORY + "/buscar/que:"
ADDING_CHAR = "%20"
#First dead record in rememory
FIRST_YEAR = 2008
#Maximum life span of a person
MAXIMUM_LIFESPAN = 123


class rememori_reader(object):
    '''
    This class analyzes and finds and matches profiles with death records in
    rememory
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.parser = RememoryParser()
    def profile_is_matched(self, profile):
        '''
        This function will look in rememory trying to match a profile
        Input shall be a profile of common profile values
        '''
        final_profiles = []
        #Before executing, if the profile is born before any logical date treated in rememory, we stop
        if (not ( (profile.get_earliest_event()) and (profile.get_earliest_event() < date(FIRST_YEAR-MAXIMUM_LIFESPAN,1,1)) )):
            
            url = SEARCH_LOCATION + profile.gen_data["name"] + ADDING_CHAR
            url += ADDING_CHAR.join(profile.gen_data["surname"].split(" "))
            data = requests.get(url)
            self.parser.feed(data.text)
            #This will remove all those matches that are very unlikely to be part
            for deceased in self.parser.records:
                score, factor = deceased.comparison_score(profile)
                if (score*factor > 2.0):
                    final_profiles.append(deceased)
        return final_profiles

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
                prof_record.setCheckedDate("death_date", self.death_date, "EXACT")
                prof_record.setComments(self.comments)
                self.records.append(prof_record)
        