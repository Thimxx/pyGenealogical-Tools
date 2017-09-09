__all__ = ["profile", "data_models", "immediate_family", "geniapi_common"]

import requests, logging
from messages.pygeni_messages import ERROR_REQUESTS


#Several addresses of the Geni API
GENI_ADDRESS = "https://www.geni.com"
GENI_FAMILY = "/immediate-family"
GENI_INITIATE_PARAMETER = "?"
GENI_ADD_PARAMETER = "&"
GENI_TOKEN = "access_token="
GENI_SINGLE_TOKEN = GENI_INITIATE_PARAMETER + GENI_TOKEN
GENI_PARAM_TOKEN = GENI_ADD_PARAMETER + GENI_TOKEN
GENI_ADD_CHILD = "/add-child"
GENI_DELETE = "/delete"
GENI_ADD_PARTNER = "/add-partner"
GENI_UPDATE = "/update"
GENI_ADD_PARENT = "/add-parent"
#Parameters that depend on others
GENI_VALIDATE_TOKEN = GENI_ADDRESS + "/platform/oauth/validate_token" + GENI_SINGLE_TOKEN
GENI_API = GENI_ADDRESS + "/api/"
GENI_PEOPLE = GENI_ADDRESS + "/people/"
GENI_PROFILE =  GENI_API + "profile-"

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
    global GENI_SINGLE_TOKEN
    global GENI_PEOPLE
    #We update the variables
    GENI_ADDRESS = new_geni_address
    GENI_VALIDATE_TOKEN = GENI_ADDRESS + "/platform/oauth/validate_token" + GENI_SINGLE_TOKEN
    GENI_API = GENI_ADDRESS + "/api/"
    GENI_PEOPLE = GENI_ADDRESS + "/people/"
    GENI_PROFILE =  GENI_API + "profile-"
def geni_request_get(url):
    '''
    Function to perform get calls.
    '''
    global VERIFY_INPUT
    if (VERIFY_INPUT == "standard"):
        data = requests.get(url)
    else:
        data = requests.get(url, verify=VERIFY_INPUT)
    if "error" in data.json().keys():
        #Ok, now we know we have an error, we need to inform the user!
        print(data.json())
        logging.error(ERROR_REQUESTS + str(data.json()))
    return data 
    
def geni_request_post(url, data_input={}):
    '''
    Function to perform post calls.
    '''
    global VERIFY_INPUT
    if (VERIFY_INPUT == "standard"):
        data = requests.post(url, json=data_input)
    else:
        data = requests.post(url, verify=VERIFY_INPUT, json=data_input)
    if "error" in data.json().keys():
        #Ok, now we know we have an error, we need to inform the user!
        logging.error(ERROR_REQUESTS + str(data.json()))
    return data 
    