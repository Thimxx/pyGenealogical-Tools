__all__ = ["common_profile", "gen_utils", "common_database", "common_event", "common_family", "generic_functions"]

VALUES_ACCURACY = ["EXACT", "BEFORE", "AFTER", "ABOUT", "BETWEEN"]

EVENT_TYPE = ["birth", "death", "baptism",  "burial", "marriage", "residence"]

ARRAY_EVENTS = ["marriage", "residence"]

NOT_KNOWN_VALUE = "N.N."

from os import environ, getenv

#The token data
MAPBOX_KEY = None


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
def set_mapbox_key_environmental():
    '''
    It will set-up the environmental variable using MAPBOX_API input
    '''
    set_mapbox_key(getenv("MAPBOX_API"))


if "MAPBOX_API" in environ : set_mapbox_key_environmental()