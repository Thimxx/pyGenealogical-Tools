__all__ = ["common_profile", "gen_utils"]

VALUES_ACCURACY = ["EXACT", "BEFORE", "AFTER", "ABOUT", "BETWEEN"]

EVENT_TYPE = ["birth", "death", "baptism",  "burial", "marriage", "residence"]

NOT_KNOWN_VALUE = "N.N."

from os import environ, getenv

#The token data
MAPBOX_KEY = None

if "MAPBOX_API" in environ : MAPBOX_KEY = getenv("MAPBOX_API")

TOKEN = None

def get_mapbox_key():
    '''
    Function to get the mabox key variable currently in use
    '''
    return MAPBOX_KEY
def set_mapbox_key(key_value):
    '''
    Function to set-up the google key value
    '''
    global MAPBOX_KEY
    MAPBOX_KEY = key_value