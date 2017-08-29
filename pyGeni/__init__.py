__all__ = ["profile", "data_models", "immediate_family", "geniapi_common"]

import requests

#Several addresses of the Geni API
GENI_ADDRESS = "https://www.geni.com"
GENI_VALIDATE_TOKEN = GENI_ADDRESS + "/platform/oauth/validate_token?access_token="
GENI_API = GENI_ADDRESS + "/api/"
GENI_PROFILE =  GENI_API + "profile-"
GENI_FAMILY = "/immediate-family"
GENI_TOKEN = "?access_token="

VERIFY_INPUT="standard"

def update_geni_address(new_geni_address):
    '''
    This function will update the values of geni variables to be able to use
    in testing mode
    '''
    global GENI_ADDRESS 
    global GENI_VALIDATE_TOKEN 
    global GENI_API 
    global GENI_PROFILE
    
    GENI_ADDRESS = new_geni_address
    GENI_VALIDATE_TOKEN = GENI_ADDRESS + "/platform/oauth/validate_token?access_token="
    GENI_API = GENI_ADDRESS + "/api/"
    GENI_PROFILE =  GENI_API + "profile-"
    
def geni_request_get(url):
    '''
    Function to activate/de-activate execution of the code. Just for being able
    to debug
    '''
    global VERIFY_INPUT
    if (VERIFY_INPUT == "standard"):
        return requests.get(url)
    else:
        return requests.get(url, verify=VERIFY_INPUT)
    