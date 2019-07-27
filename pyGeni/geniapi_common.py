'''
Created on 8 ago. 2017

@author: Val
'''


import pyGeni as s
from messages.pygeni_messages import NO_VALID_TOKEN
import logging
from pyGenealogy.common_event import event_profile

class geni_calls():
    '''
    This class introduces the common functions to be shared by several classes
    inside pyGeni
    '''
    def __init__(self):
        '''
        Just introducing the token, a common one between the different functions
        '''
    @classmethod
    def token_string(self):
        return s.GENI_SINGLE_TOKEN + s.get_token()
    @classmethod
    def get_profile_url(cls, profile_id):
        '''
        Small function delivering back the profile url based on the profile_id
        '''
        return s.GENI_API + profile_id
    @classmethod
    def check_valid_genikey(self):
        # Validate access token, connecting to Geni, this might take a while
        valid_token = s.geni_request_get(s.GENI_VALIDATE_TOKEN + str(s.get_token())).json()

        tokenIsOk = False
        #The way the API informs of a wrong token is the following:
        #{'error': 'invalid_token', 'error_description': 'invalid token'}
        if ('error' in valid_token):
            #We got an error, we shall notify!
            logging.error(NO_VALID_TOKEN)
        elif ( str(valid_token['result']) == "OK"):
            tokenIsOk = True
        return tokenIsOk
    @classmethod
    def get_date(self, event_type, data_dict, previous_event = None):
        '''
        Get date from the Geni standard, used in unions and profiles
        '''
        if previous_event:
            my_event = previous_event
        else:
            my_event = event_profile(event_type)
        accuracy = None
        year = None
        month = None
        day = None
        year_end = None
        month_end = None
        day_end = None
        if (data_dict.get("year",None) != None):
            year = data_dict.get("year")
            month = data_dict.get("month", None)
            day = data_dict.get("day", None)
        #TODO: get and handle BETWEEN dates
        if (data_dict.get("circa", "false") == "true"): accuracy = "ABOUT"
        elif (data_dict.get("range", "") == "before"): accuracy = "BEFORE"
        elif (data_dict.get("range", "") == "after"): accuracy = "AFTER"
        elif (data_dict.get("range", "") == "between"):
            accuracy = "BETWEEN"
            year_end = data_dict.get("end_year", None)
            month_end = data_dict.get("end_month", None)
            day_end = data_dict.get("end_day", None)
        else: accuracy = "EXACT"
        #Now we transfer everything to the profile
        my_event.setDate(year, month, day, accuracy, year_end, month_end, day_end)
        return my_event