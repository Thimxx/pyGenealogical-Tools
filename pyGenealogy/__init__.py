__all__ = ["common_profile", "gen_utils"]

VALUES_ACCURACY = ["EXACT", "BEFORE", "AFTER", "ABOUT"]

NOT_KNOWN_VALUE = "N.N."

from os import environ, getenv

#The token data
GOOGLE_KEY = None

if "GOOGLE_API" in environ : GOOGLE_KEY = getenv("GOOGLE_API")

TOKEN = None

def get_google_key():
    '''
    Function to get the google key variable currently in use
    '''
    return GOOGLE_KEY

def set_google_key(key_value):
    '''
    Function to set-up the google key value
    '''
    global GOOGLE_KEY
    GOOGLE_KEY = key_value