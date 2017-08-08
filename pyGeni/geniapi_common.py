'''
Created on 8 ago. 2017

@author: Val
'''


import pyGeni.geni_settings as s

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