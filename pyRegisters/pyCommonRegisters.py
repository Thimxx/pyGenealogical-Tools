'''
Created on 15 ago. 2019

@author: Val
'''
import requests

class BaseRegister(object):
    '''
    Base register for all different register parsers
    '''
    def __init__(self,register, first_year=None):
        '''
        Basic constructor for all registers
        '''
        self.register = register
        self.maximum_lifespan = 123
        self.first_year = first_year
    def continue_death_register(self, profile):
        '''
        This is function to be used to continue or not with the base register
        '''
        continue_exec = True
        if (profile.getSurname() in [None, ""] or profile.getName() in [None, ""]):
            continue_exec = False
        event_earliest = profile.get_earliest_event_in_event_form()
        if self.first_year and (event_earliest) and (event_earliest.get_year()) and (profile.get_earliest_event_in_event_form().get_year() < self.first_year-self.maximum_lifespan):
            continue_exec = False
        event_death = profile.get_specific_event("death")
        if self.first_year and event_death and event_death.get_year() and event_death.get_year() < self.first_year:
            continue_exec = False
        return continue_exec
    def matching_profiles(self, profile, tentative_profiles):
        '''
        Common function to be used for checking potential common profiles
        '''
        final_profiles = []
        for selected_profile in tentative_profiles:
            score, factor = selected_profile.comparison_score(profile, data_language=self.language, name_convention=self.name_convention)
            if (score*factor > 2.0):
                final_profiles.append(selected_profile)
        return final_profiles
    def perform_match(self, profile, url):
        '''
        This function takes an url and will obtain the result, for afterwards obtain the
        matching of profiles
        '''
        final_profiles = []
        if self.continue_death_register(profile):
            data = requests.get(url)
            self.parser.feed(data.text)
            final_profiles = self.matching_profiles(profile, self.parser.profiles)
        return final_profiles