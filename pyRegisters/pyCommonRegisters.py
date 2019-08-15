'''
Created on 15 ago. 2019

@author: Val
'''
from datetime import date

class BaseRegister(object):
    '''
    Base register for all different register parsers
    '''
    def __init__(self, first_year=None):
        '''
        Basic constructor for all registers
        '''
        self.maximum_lifespan = 123
        self.first_year = first_year
    def continue_death_register(self, profile):
        '''
        This is function to be used to continue or not with the base register
        '''
        continue_exec = True
        if (profile.getSurname() in [None, ""] or profile.getName() in [None, ""]):
            continue_exec = False
        if self.first_year and (profile.get_earliest_event()) and (profile.get_earliest_event() < date(self.first_year-self.maximum_lifespan,1,1)): 
            continue_exec = False
        event_death = profile.get_specific_event("death")
        if self.first_year and event_death and event_death.get_year() and event_death.get_year() < self.first_year:
            continue_exec = False
        return continue_exec