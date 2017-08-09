'''
Created on 8 ago. 2017

@author: Val
'''


import pyGeni.geni_settings as s
import requests
from messages.pygeni_messages import *
import logging

class geni_calls():
    '''
    This class introduces the common functions to be shared by several classes
    inside pyGeni
    '''


    def __init__(self, token):
        '''
        Just introducing the token, a common one between the different functions
        '''
        self.token = token
    def token_string(self):
        return s.GENI_TOKEN + self.token
    @classmethod
    def get_profile_url(cls, profile_id):
        '''
        Small function delivering back the profile url based on the profile_id
        '''
        return s.GENI_API + profile_id
    def check_valid_genikey(self):
        # Validate access token, connecting to Geni, this might take a while
        valid_token = requests.get(s.GENI_VALIDATE_TOKEN + self.token).json()

        tokenIsOk = False
        #The way the API informs of a wrong token is the following:
        #{'error': 'invalid_token', 'error_description': 'invalid token'}
        if ('error' in valid_token):
            #We got an error, we shall notify!
            logging.error(NO_VALID_TOKEN)
        elif ( str(valid_token['result']) == "OK"):
            tokenIsOk = True
        return tokenIsOk